from flask import Blueprint, request, jsonify
from models import db, User, MedicalHistory
from auth import generate_token, token_required, get_user_from_token
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ==================== AUTHENTICATION ENDPOINTS ====================

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields: username, email, password'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            age=data.get('age'),
            gender=data.get('gender')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = generate_token(user.id)
        
        logger.info(f"✓ User registered: {user.username}")
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"✗ Registration error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password'}), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == data['username']) | (User.email == data['username'])
        ).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 403
        
        # Generate token
        token = generate_token(user.id)
        
        logger.info(f"✓ User logged in: {user.username}")
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        logger.error(f"✗ Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(user):
    """Logout user"""
    try:
        logger.info(f"✓ User logged out: {user.username}")
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        logger.error(f"✗ Logout error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(user):
    """Get user profile"""
    try:
        return jsonify(user.to_dict()), 200
    except Exception as e:
        logger.error(f"✗ Get profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(user):
    """Update user profile"""
    try:
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'age' in data:
            user.age = data['age']
        if 'gender' in data:
            user.gender = data['gender']
        
        db.session.commit()
        
        logger.info(f"✓ User profile updated: {user.username}")
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"✗ Update profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(user):
    """Change user password"""
    try:
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({'error': 'Missing old_password or new_password'}), 400
        
        # Verify old password
        if not user.check_password(data['old_password']):
            return jsonify({'error': 'Incorrect old password'}), 401
        
        # Set new password
        user.set_password(data['new_password'])
        db.session.commit()
        
        logger.info(f"✓ Password changed for user: {user.username}")
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"✗ Change password error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/delete-account', methods=['DELETE'])
@token_required
def delete_account(user):
    """Delete user account"""
    try:
        data = request.get_json()
        
        # Require password confirmation
        if not data or not data.get('password'):
            return jsonify({'error': 'Password confirmation required'}), 400
        
        if not user.check_password(data['password']):
            return jsonify({'error': 'Incorrect password'}), 401
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        logger.info(f"✓ Account deleted: {username}")
        return jsonify({'message': 'Account deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"✗ Delete account error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== MEDICAL HISTORY ENDPOINTS ====================

@auth_bp.route('/medical-history', methods=['GET'])
@token_required
def get_medical_history(user):
    """Get user's medical history records"""
    try:
        records = MedicalHistory.query.filter_by(user_id=user.id).order_by(
            MedicalHistory.created_at.desc()
        ).all()
        
        return jsonify({
            'records': [record.to_dict() for record in records],
            'total': len(records)
        }), 200
        
    except Exception as e:
        logger.error(f"✗ Get medical history error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/medical-history', methods=['POST'])
@token_required
def add_medical_history(user):
    """Add a new medical history record"""
    try:
        data = request.get_json()
        
        record = MedicalHistory(
            user_id=user.id,
            symptoms=data.get('symptoms'),
            symptom_predictions=data.get('symptom_predictions'),
            image_type=data.get('image_type'),
            image_predictions=data.get('image_predictions'),
            risk_assessment=data.get('risk_assessment'),
            blood_type=data.get('blood_type'),
            allergies=data.get('allergies'),
            medications=data.get('medications'),
            medical_conditions=data.get('medical_conditions'),
            blood_pressure=data.get('blood_pressure'),
            heart_rate=data.get('heart_rate'),
            temperature=data.get('temperature'),
            weight=data.get('weight'),
            height=data.get('height'),
            record_type=data.get('record_type', 'general'),
            consultation_notes=data.get('consultation_notes'),
            doctor_name=data.get('doctor_name')
        )
        
        db.session.add(record)
        db.session.commit()
        
        logger.info(f"✓ Medical history record added for user: {user.username}")
        return jsonify({
            'message': 'Medical history record added successfully',
            'record': record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"✗ Add medical history error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/medical-history/<int:record_id>', methods=['GET'])
@token_required
def get_medical_record(user, record_id):
    """Get specific medical history record"""
    try:
        record = MedicalHistory.query.filter_by(id=record_id, user_id=user.id).first()
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        return jsonify(record.to_dict()), 200
        
    except Exception as e:
        logger.error(f"✗ Get medical record error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/medical-history/<int:record_id>', methods=['PUT'])
@token_required
def update_medical_record(user, record_id):
    """Update medical history record"""
    try:
        record = MedicalHistory.query.filter_by(id=record_id, user_id=user.id).first()
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'consultation_notes' in data:
            record.consultation_notes = data['consultation_notes']
        if 'doctor_name' in data:
            record.doctor_name = data['doctor_name']
        if 'blood_pressure' in data:
            record.blood_pressure = data['blood_pressure']
        if 'heart_rate' in data:
            record.heart_rate = data['heart_rate']
        if 'temperature' in data:
            record.temperature = data['temperature']
        if 'weight' in data:
            record.weight = data['weight']
        if 'height' in data:
            record.height = data['height']
        
        db.session.commit()
        
        logger.info(f"✓ Medical record updated for user: {user.username}")
        return jsonify({
            'message': 'Medical record updated successfully',
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"✗ Update medical record error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/medical-history/<int:record_id>', methods=['DELETE'])
@token_required
def delete_medical_record(user, record_id):
    """Delete medical history record"""
    try:
        record = MedicalHistory.query.filter_by(id=record_id, user_id=user.id).first()
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        db.session.delete(record)
        db.session.commit()
        
        logger.info(f"✓ Medical record deleted for user: {user.username}")
        return jsonify({'message': 'Medical record deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"✗ Delete medical record error: {str(e)}")
        return jsonify({'error': str(e)}), 500
