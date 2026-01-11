"""
Healthcare Provider Routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models import HealthcareProvider
from datetime import datetime

bp = Blueprint('providers', __name__)


@bp.route('', methods=['GET'])
def get_providers():
    """Get all providers with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    specialization = request.args.get('specialization', '')
    search = request.args.get('search', '')
    verified_only = request.args.get('verified', 'false').lower() == 'true'
    
    query = HealthcareProvider.query.filter_by(is_active=True)
    
    if specialization:
        query = query.filter(HealthcareProvider.specialization.ilike(f'%{specialization}%'))
    
    if search:
        query = query.filter(
            db.or_(
                HealthcareProvider.first_name.ilike(f'%{search}%'),
                HealthcareProvider.last_name.ilike(f'%{search}%'),
                HealthcareProvider.email.ilike(f'%{search}%')
            )
        )
    
    if verified_only:
        query = query.filter_by(is_verified=True)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'providers': [provider.to_dict() for provider in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@bp.route('/<provider_id>', methods=['GET'])
def get_provider(provider_id):
    """Get a specific provider by ID"""
    provider = HealthcareProvider.query.get_or_404(provider_id)
    return jsonify(provider.to_dict()), 200


@bp.route('', methods=['POST'])
def create_provider():
    """Create a new healthcare provider"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'specialization', 'license_number', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        provider = HealthcareProvider(
            first_name=data['first_name'],
            last_name=data['last_name'],
            title=data.get('title', 'Dr.'),
            specialization=data['specialization'],
            license_number=data['license_number'],
            years_of_experience=data.get('years_of_experience'),
            qualifications=data.get('qualifications', []),
            certifications=data.get('certifications', []),
            email=data['email'],
            phone=data.get('phone'),
            office_address=data.get('office_address'),
            working_hours=data.get('working_hours', {}),
            consultation_fee=data.get('consultation_fee'),
            accepts_insurance=data.get('accepts_insurance', True)
        )
        
        db.session.add(provider)
        db.session.commit()
        
        return jsonify({
            'message': 'Provider created successfully',
            'provider': provider.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<provider_id>', methods=['PUT'])
def update_provider(provider_id):
    """Update an existing provider"""
    provider = HealthcareProvider.query.get_or_404(provider_id)
    data = request.get_json()
    
    try:
        # Update fields
        updateable_fields = [
            'first_name', 'last_name', 'title', 'specialization', 'license_number',
            'years_of_experience', 'qualifications', 'certifications', 'email', 'phone',
            'office_address', 'working_hours', 'consultation_fee', 'accepts_insurance'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(provider, field, data[field])
        
        provider.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Provider updated successfully',
            'provider': provider.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<provider_id>/verify', methods=['POST'])
def verify_provider(provider_id):
    """Verify a healthcare provider"""
    provider = HealthcareProvider.query.get_or_404(provider_id)
    
    try:
        provider.is_verified = True
        provider.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Provider verified successfully',
            'provider': provider.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<provider_id>/availability', methods=['GET'])
def get_provider_availability(provider_id):
    """Get provider's availability schedule"""
    provider = HealthcareProvider.query.get_or_404(provider_id)
    
    return jsonify({
        'provider_id': provider_id,
        'working_hours': provider.working_hours,
        'consultation_fee': float(provider.consultation_fee) if provider.consultation_fee else None,
        'accepts_insurance': provider.accepts_insurance
    }), 200


@bp.route('/<provider_id>/appointments', methods=['GET'])
def get_provider_appointments(provider_id):
    """Get all appointments for a provider"""
    provider = HealthcareProvider.query.get_or_404(provider_id)
    appointments = provider.appointments.order_by('appointment_date desc').all()
    
    return jsonify({
        'provider_id': provider_id,
        'appointments': [apt.to_dict() for apt in appointments]
    }), 200

