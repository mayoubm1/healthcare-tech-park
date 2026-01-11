"""
Patient Routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models import Patient
from datetime import datetime

bp = Blueprint('patients', __name__)


@bp.route('', methods=['GET'])
def get_patients():
    """Get all patients with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = Patient.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            db.or_(
                Patient.first_name.ilike(f'%{search}%'),
                Patient.last_name.ilike(f'%{search}%'),
                Patient.email.ilike(f'%{search}%')
            )
        )
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'patients': [patient.to_dict() for patient in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@bp.route('/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a specific patient by ID"""
    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict()), 200


@bp.route('', methods=['POST'])
def create_patient():
    """Create a new patient"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'date_of_birth']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # Parse date of birth
        dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=dob,
            gender=data.get('gender'),
            blood_type=data.get('blood_type'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            country=data.get('country'),
            allergies=data.get('allergies', []),
            chronic_conditions=data.get('chronic_conditions', []),
            current_medications=data.get('current_medications', []),
            emergency_contact=data.get('emergency_contact'),
            insurance_provider=data.get('insurance_provider'),
            insurance_policy_number=data.get('insurance_policy_number')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({
            'message': 'Patient created successfully',
            'patient': patient.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update an existing patient"""
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()
    
    try:
        # Update fields
        if 'first_name' in data:
            patient.first_name = data['first_name']
        if 'last_name' in data:
            patient.last_name = data['last_name']
        if 'date_of_birth' in data:
            patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        if 'gender' in data:
            patient.gender = data['gender']
        if 'blood_type' in data:
            patient.blood_type = data['blood_type']
        if 'email' in data:
            patient.email = data['email']
        if 'phone' in data:
            patient.phone = data['phone']
        if 'address' in data:
            patient.address = data['address']
        if 'city' in data:
            patient.city = data['city']
        if 'country' in data:
            patient.country = data['country']
        if 'allergies' in data:
            patient.allergies = data['allergies']
        if 'chronic_conditions' in data:
            patient.chronic_conditions = data['chronic_conditions']
        if 'current_medications' in data:
            patient.current_medications = data['current_medications']
        if 'emergency_contact' in data:
            patient.emergency_contact = data['emergency_contact']
        if 'insurance_provider' in data:
            patient.insurance_provider = data['insurance_provider']
        if 'insurance_policy_number' in data:
            patient.insurance_policy_number = data['insurance_policy_number']
        
        patient.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Patient updated successfully',
            'patient': patient.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Soft delete a patient"""
    patient = Patient.query.get_or_404(patient_id)
    
    try:
        patient.is_active = False
        patient.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Patient deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<patient_id>/appointments', methods=['GET'])
def get_patient_appointments(patient_id):
    """Get all appointments for a patient"""
    patient = Patient.query.get_or_404(patient_id)
    appointments = patient.appointments.order_by('appointment_date desc').all()
    
    return jsonify({
        'patient_id': patient_id,
        'appointments': [apt.to_dict() for apt in appointments]
    }), 200


@bp.route('/<patient_id>/medical-records', methods=['GET'])
def get_patient_medical_records(patient_id):
    """Get all medical records for a patient"""
    patient = Patient.query.get_or_404(patient_id)
    records = patient.medical_records.order_by('record_date desc').all()
    
    return jsonify({
        'patient_id': patient_id,
        'medical_records': [record.to_dict() for record in records]
    }), 200

