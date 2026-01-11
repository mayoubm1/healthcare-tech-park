from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Patient, HealthcareProvider # Assuming users can be patients or providers
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role') # 'patient' or 'provider'

    if not username or not password or not role:
        return jsonify({'message': 'Missing username, password, or role'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    if role == 'patient':
        if Patient.query.filter_by(username=username).first():
            return jsonify({'message': 'Patient with this username already exists'}), 409
        new_user = Patient(username=username, first_name=username, last_name='N/A', password_hash=hashed_password, date_of_birth='2000-01-01', gender='Unknown', email=f'{username}@example.com', phone='N/A', address='N/A', city='N/A', country='N/A') # Placeholder for other fields
    elif role == 'provider':
        if HealthcareProvider.query.filter_by(username=username).first():
            return jsonify({'message': 'Provider with this username already exists'}), 409
        new_user = HealthcareProvider(username=username, first_name=username, last_name='N/A', password_hash=hashed_password, specialization='General', license_number=f'{username}-license', email=f'{username}@example.com') # Placeholder for other fields
    else:
        return jsonify({'message': 'Invalid role specified'}), 400

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f'{role.capitalize()} registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'message': 'Missing username, password, or role'}), 400

    user = None
    if role == 'patient':
        user = Patient.query.filter_by(username=username).first()
    elif role == 'provider':
        user = HealthcareProvider.query.filter_by(username=username).first()
    else:
        return jsonify({'message': 'Invalid role specified'}), 400

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'id': user.id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token}), 200

