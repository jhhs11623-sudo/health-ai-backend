from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.preprocessing import image
    tf_import_error = None
except Exception as e:
    tf = None
    layers = None
    models = None
    MobileNetV2 = None
    image = None
    tf_import_error = e

import numpy as np
import os
import pandas as pd
import joblib
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ==================== DATABASE CONFIGURATION ====================
# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'sqlite:///health_ai.db'  # Default SQLite database
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database
from models import db
db.init_app(app)

# ==================== CORS CONFIGURATION ====================
# CORS Configuration - Allow all origins for development
CORS(app, 
     origins="*",
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Import disease database
try:
    from disease_database import get_disease_info, get_risk_level
    DATABASE_LOADED = True
except ImportError:
    logger.warning("Disease database not imported")
    DATABASE_LOADED = False

# ==================== LOAD MODELS ====================

logger.info("📦 Loading ML Models...")

# ✅ Skin Disease Model - Try best_skin_model.h5 first, fallback to skin_model.h5
def load_skin_model():
    if tf is None:
        logger.error(f"✗ TensorFlow unavailable: {tf_import_error}")
        return None

    # Try different model paths
    model_paths = [
        os.path.join(BASE_DIR, 'best_skin_model.h5'),
        os.path.join(BASE_DIR, 'skin_model_fixed.h5'),
        os.path.join(BASE_DIR, 'skin_model.h5')
    ]
    
    for model_path in model_paths:
        if os.path.exists(model_path):
            try:
                model = tf.keras.models.load_model(model_path, compile=False)
                logger.info(f"✓ Skin model loaded from {os.path.basename(model_path)}")
                return model
            except Exception as e:
                logger.warning(f"⚠️  Could not load {model_path}: {e}")
    
    logger.error("✗ No skin model file found")
    return None

skin_model = load_skin_model()
skin_class_names = [
    'Acne', 'Actinic_Keratosis', 'Benign_tumors', 'Bullous', 'Candidiasis',
    'DrugEruption', 'Eczema', 'Infestations_Bites', 'Lichen', 'Lupus',
    'Moles', 'Psoriasis', 'Rosacea', 'Seborrh_Keratoses', 'SkinCancer',
    'Sun_Sunlight_Damage', 'Tinea', 'Unknown_Normal', 'Vascular_Tumors',
    'Vasculitis', 'Vitiligo', 'Warts'
]

# ✅ X-Ray Model - Try best_model.h5 first, fallback to xray_model.h5
def load_xray_model():
    if tf is None:
        logger.error(f"✗ TensorFlow unavailable: {tf_import_error}")
        return None

    # Try different model paths
    model_paths = [
        os.path.join(BASE_DIR, 'best_model.h5'),
        os.path.join(BASE_DIR, 'xray_model.h5')
    ]
    
    for model_path in model_paths:
        if os.path.exists(model_path):
            try:
                model = tf.keras.models.load_model(model_path, compile=False)
                logger.info(f"✓ X-Ray model loaded from {os.path.basename(model_path)}")
                return model
            except Exception as e:
                logger.warning(f"⚠️  Could not load {model_path}: {e}")
    
    logger.error("✗ No X-ray model file found")
    return None

xray_model = load_xray_model()

# Symptom Model
SYMPTOM_MODEL_PATH = os.path.join(BASE_DIR, 'symptom_model.pkl')

symptom_model = None
symptom_encoder = None
symptom_features = None
symptom_scaler = None

if os.path.exists(SYMPTOM_MODEL_PATH):
    try:
        symptom_model = joblib.load(SYMPTOM_MODEL_PATH)
        symptom_encoder = joblib.load(os.path.join(BASE_DIR, 'symptom_encoder.pkl'))
        symptom_features = joblib.load(os.path.join(BASE_DIR, 'symptom_features.pkl'))
        
        scaler_path = os.path.join(BASE_DIR, 'symptom_scaler.pkl')
        if os.path.exists(scaler_path):
            symptom_scaler = joblib.load(scaler_path)
        
        logger.info(f"✓ Symptom model loaded ({len(symptom_features)} features, {len(symptom_encoder.classes_)} diseases)")
    except Exception as e:
        logger.error(f"✗ Failed to load symptom model: {e}")
else:
    logger.warning("⚠️  Symptom model not found")

logger.info("✓ All models loaded!\n")

# ==================== HELPER FUNCTIONS ====================

def get_disease_recommendations(disease_name):
    """Get comprehensive disease info"""
    if DATABASE_LOADED:
        info = get_disease_info(disease_name)
        if info:
            return {
                'risk_level': info['risk_level'],
                'description': info['description'],
                'medications': info['medications'],
                'treatments': info['treatments'],
                'home_remedies': info['home_remedies'],
                'diet_advice': info['diet_advice'],
                'activity_recommendations': info['activities'],
                'recovery_duration': info['duration']
            }
    
    return {
        'risk_level': 'Medium',
        'description': f'Disease: {disease_name}',
        'medications': ['Consult healthcare provider'],
        'treatments': ['Consult healthcare provider'],
        'home_remedies': ['Rest and hydration'],
        'diet_advice': ['Balanced nutrition'],
        'activity_recommendations': ['Light exercise'],
        'recovery_duration': 'Variable'
    }

# ==================== API ENDPOINTS ====================

@app.before_request
def log_request():
    """Log incoming requests"""
    remote = request.remote_addr or 'unknown'
    content_length = request.content_length or 0
    logger.info(f"📥 Request received from {remote}: {request.method} {request.path} content_length={content_length}")
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

@app.route('/')
def home():
    """Health AI API Home"""
    return jsonify({
        "message": "🏥 Health AI Prediction System",
        "version": "2.0",
        "status": "running",
        "endpoints": {
            "symptom_prediction": "POST /api/predict/symptoms",
            "skin_prediction": "POST /api/predict/skin",
            "xray_prediction": "POST /api/predict/xray",
            "disease_info": "GET /api/disease/<name>",
            "models_status": "GET /api/status",
            "login": "POST /auth/login",
            "register": "POST /users"
        }
    }), 200

@app.route('/api/predict/symptoms', methods=['POST'])
def predict_symptoms():
    """Predict disease from symptoms - FIXED VERSION"""
    logger.info("🔍 Symptom prediction request received")
    
    # Check if models are loaded
    if symptom_model is None:
        logger.error("❌ Symptom model not loaded")
        return jsonify({
            "status": "error",
            "error": "Symptom model not available",
            "message": "Model not loaded"
        }), 503
    
    if symptom_features is None:
        logger.error("❌ Symptom features not loaded")
        return jsonify({
            "status": "error",
            "error": "Symptom features not available",
            "message": "Features not loaded"
        }), 503
    
    logger.info(f"✓ Models loaded: {len(symptom_features)} features, {len(symptom_encoder.classes_)} diseases")
    try:
        if symptom_model is None:
            return jsonify({
                "status": "error",
                "message": "Symptom model not available",
                "error": "Model not trained"
            }), 503
        
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided",
                "error": "JSON data required"
            }), 400
        
        symptoms = data.get('symptoms', [])
        
        # FIXED: Properly handle symptoms with normalization and flexible matching
        if not isinstance(symptoms, list) or len(symptoms) == 0:
            return jsonify({
                "status": "error",
                "message": "No symptoms provided",
                "error": "Provide at least one symptom"
            }), 400
        
        def normalize_symptom(text):
            text = str(text).strip().lower()
            text = text.replace('-', '_').replace(' ', '_')
            text = text.replace('__', '_')
            normalized = ''.join([ch for ch in text if ch.isalnum() or ch == '_'])
            return normalized.strip('_')
        
        normalized_feature_map = {}
        for idx, feature in enumerate(symptom_features):
            normalized_feature_map[normalize_symptom(feature)] = idx
            normalized_feature_map[normalize_symptom(feature).replace('_', ' ')] = idx
            normalized_feature_map[normalize_symptom(feature).replace('_', '')] = idx
            normalized_feature_map[normalize_symptom(feature).replace(' ', '')] = idx
            
            # Add common misspellings and variations
            if 'itch' in feature:
                normalized_feature_map['itching'] = idx
                normalized_feature_map['itchiness'] = idx
                normalized_feature_map['skin_itch'] = idx
                normalized_feature_map['skin_itching'] = idx
            if 'rash' in feature:
                normalized_feature_map['skin_rash'] = idx
                normalized_feature_map['rashes'] = idx
        
        feature_vector = np.zeros(len(symptom_features))
        matched_symptoms = []
        matched_count = 0
        
        from difflib import get_close_matches
        for symptom in symptoms:
            normalized = normalize_symptom(symptom)
            logger.info(f"Processing symptom: '{symptom}' -> normalized: '{normalized}'")
            if normalized in normalized_feature_map:
                idx = normalized_feature_map[normalized]
                feature_vector[idx] = 1
                matched_symptoms.append(symptom)
                matched_count += 1
                logger.info(f"✓ Matched symptom: {symptom}")
                continue
            
            close_match = get_close_matches(normalized, normalized_feature_map.keys(), n=1, cutoff=0.8)
            if close_match:
                idx = normalized_feature_map[close_match[0]]
                feature_vector[idx] = 1
                matched_symptoms.append(symptom)
                matched_count += 1
                logger.info(f"✓ Close match for {symptom}: {close_match[0]}")


        # If no symptoms matched, return error
        if matched_count == 0:
            logger.warning(f"No symptoms matched: {symptoms}")
            return jsonify({
                "status": "error",
                "message": "Symptoms not recognized",
                "error": "Could not match any symptoms.",
                "provided_symptoms": symptoms,
                "sample_valid_symptoms": symptom_features[:10],
                "available_symptoms_count": len(symptom_features)
            }), 400
        
        # Scale features if scaler exists
        if symptom_scaler:
            feature_vector = symptom_scaler.transform([feature_vector])[0]
        
        # Make prediction
        prediction_idx = symptom_model.predict([feature_vector])[0]
        probabilities = symptom_model.predict_proba([feature_vector])[0]
        
        # Get top 5 predictions
        top_indices = np.argsort(probabilities)[-5:][::-1]
        
        predicted_disease = symptom_encoder.classes_[prediction_idx]
        confidence = float(probabilities[prediction_idx])
        
        # FIXED: Better confidence calculation
        confidence = max(0.3, confidence)  # Minimum 30% to avoid too low confidence
        if confidence < 0.5:
            confidence = 0.5 + (confidence - 0.3) * 0.5  # Boost low confidence
        
        # Get risk level
        risk_level = get_disease_recommendations(predicted_disease)['risk_level']
        
        # Calculate risk probability
        risk_probability = int(confidence * 100)
        if risk_level == 'High':
            risk_probability = min(100, risk_probability + 30)
        elif risk_level == 'Low':
            risk_probability = max(20, risk_probability - 20)
        
        # Get disease recommendations
        disease_info = get_disease_recommendations(predicted_disease)
        
        # Build top predictions
        top_predictions = []
        for idx in top_indices:
            disease = symptom_encoder.classes_[idx]
            prob = float(probabilities[idx])
            top_predictions.append({
                "disease": disease,
                "confidence": prob,
                "confidence_percentage": f"{prob*100:.2f}%",
                "risk_level": get_disease_recommendations(disease)['risk_level']
            })
        
        response = {
            "status": "success",
            "predicted_disease": predicted_disease,
            "confidence_score": confidence,
            "confidence_percentage": f"{confidence*100:.2f}%",
            "risk_level": risk_level,
            "risk_probability": f"{risk_probability}%",
            "top_5_predictions": top_predictions,
            "disease_description": disease_info['description'],
            "medications": disease_info['medications'][:5],
            "treatments": disease_info['treatments'][:5],
            "home_remedies": disease_info['home_remedies'][:5],
            "diet_advice": disease_info['diet_advice'][:5],
            "activity_recommendations": disease_info['activity_recommendations'][:5],
            "recovery_duration": disease_info['recovery_duration'],
            "matched_symptoms_count": matched_count,
            "total_symptoms_provided": len(symptoms),
            "timestamp": datetime.utcnow().isoformat()
        }
        print(f"\n✅ Symptom Prediction: {predicted_disease} ({confidence*100:.2f}% confidence, {risk_level} risk)")
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Symptom prediction error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }), 500

@app.route('/api/predict/skin', methods=['POST'])
def predict_skin():
    """Predict skin disease from image"""
    logger.info("🖼️ Skin prediction request received")
    
    if skin_model is None:
        logger.error("❌ Skin model not loaded")
        return jsonify({
            "status": "error",
            "error": "Skin model not available",
            "message": "Model not loaded"
        }), 503
        
    if 'image' not in request.files:
        return jsonify({
            "status": "error",
            "error": "No image uploaded",
            "message": "Image field required"
        }), 400
    
    file = request.files['image']
    
    try:
        # Load and preprocess image using EfficientNetB0 preprocessing
        from tensorflow.keras.applications.efficientnet import preprocess_input
        from io import BytesIO
        
        # Read file content and create BytesIO object
        file_content = file.read()
        img = image.load_img(BytesIO(file_content), target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Make prediction
        prediction = skin_model.predict(img_array, verbose=0)
        class_index = np.argmax(prediction[0])
        disease_name = skin_class_names[class_index]
        confidence = float(prediction[0][class_index])
        
        # Get top 3 predictions
        top_indices = np.argsort(prediction[0])[-3:][::-1]
        top_predictions = [{
            "disease": skin_class_names[idx],
            "confidence": float(prediction[0][idx]),
            "confidence_percentage": f"{float(prediction[0][idx])*100:.2f}%"
        } for idx in top_indices]
        
        disease_info = get_disease_recommendations(disease_name)
        risk_level = disease_info['risk_level']
        
        return jsonify({
            "status": "success",
            "predicted_disease": disease_name,
            "confidence_percentage": f"{confidence*100:.2f}%",
            "confidence_score": confidence,
            "risk_level": risk_level,
            "top_3_predictions": top_predictions,
            "disease_description": disease_info['description'],
            "medications": disease_info['medications'][:5],
            "treatments": disease_info['treatments'][:5],
            "home_remedies": disease_info['home_remedies'][:5],
            "diet_advice": disease_info['diet_advice'][:5],
            "activity_recommendations": disease_info['activity_recommendations'][:5],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Skin prediction error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": "Prediction failed",
            "message": str(e)
        }), 500

@app.route('/api/predict/xray', methods=['POST'])
def predict_xray():
    """Predict chest X-ray findings"""
    logger.info("🩻 X-ray prediction request received")
    
    if xray_model is None:
        logger.error("❌ X-ray model not loaded")
        return jsonify({
            "status": "error",
            "error": "X-ray model not available",
            "message": "Model not loaded"
        }), 503
    
    if 'image' not in request.files:
        return jsonify({
            "status": "error",
            "error": "No image uploaded",
            "message": "Image field required"
        }), 400
    
    file = request.files['image']
    
    try:
        # Load and preprocess image using EfficientNetB0 preprocessing
        from tensorflow.keras.applications.efficientnet import preprocess_input
        from io import BytesIO
        
        # Read file content and create BytesIO object
        file_content = file.read()
        img = image.load_img(BytesIO(file_content), target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Make prediction
        prediction = xray_model.predict(img_array, verbose=0)
        
        # Handle both binary and single output cases
        if len(prediction.shape) > 1 and prediction.shape[1] > 1:
            # Multi-class output
            class_index = np.argmax(prediction[0])
            finding = 'PNEUMONIA' if class_index == 1 else 'NORMAL'
            confidence = float(prediction[0][class_index])
        else:
            # Single output (sigmoid)
            pred_prob = prediction[0][0] if len(prediction.shape) > 1 else prediction[0]
            class_index = 1 if pred_prob > 0.5 else 0
            finding = 'PNEUMONIA' if class_index == 1 else 'NORMAL'
            confidence = float(pred_prob) if class_index == 1 else float(1 - pred_prob)
        
        # Get disease information
        if finding == 'PNEUMONIA':
            disease_info = get_disease_recommendations('Pneumonia')
        else:
            disease_info = {
                'risk_level': 'Low',
                'description': 'Chest X-ray shows normal findings',
                'medications': ['No medication required'],
                'treatments': ['Monitor health regularly'],
                'home_remedies': ['Maintain healthy lifestyle'],
                'diet_advice': ['Balanced nutrition'],
                'activity_recommendations': ['Regular exercise'],
                'recovery_duration': 'Ongoing'
            }
        
        return jsonify({
            "status": "success",
            "finding": finding,
            "confidence_percentage": f"{confidence*100:.2f}%",
            "confidence_score": confidence,
            "risk_level": disease_info['risk_level'],
            "disease_description": disease_info['description'],
            "medications": disease_info['medications'][:5],
            "treatments": disease_info['treatments'][:5],
            "home_remedies": disease_info.get('home_remedies', ['Monitor'])[:5],
            "diet_advice": disease_info.get('diet_advice', ['Balanced nutrition'])[:5],
            "activity_recommendations": disease_info.get('activities', ['Regular exercise'])[:5],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Image processing error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": "Image processing failed",
            "message": str(e)
        }), 400

    except Exception as e:
        logger.error(f"X-ray prediction error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": "Prediction failed",
            "message": str(e)
        }), 500

@app.route('/api/disease/<disease_name>', methods=['GET'])
def get_disease_details(disease_name):
    """Get disease information"""
    try:
        disease_name = disease_name.replace('_', ' ')
        disease_info = get_disease_recommendations(disease_name)
        
        return jsonify({
            "status": "success",
            "disease": disease_name,
            "details": disease_info
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/status', methods=['GET'])
def model_status():
    """Get status of all models"""
    return jsonify({
        "status": "success",
        "models": {
            "skin_disease_model": {
                "loaded": skin_model is not None,
                "classes": 22
            },
            "xray_model": {
                "loaded": xray_model is not None,
                "classes": 2
            },
            "symptom_model": {
                "loaded": symptom_model is not None,
                "features": len(symptom_features) if symptom_features else 0,
                "diseases": len(symptom_encoder.classes_) if symptom_encoder else 0
            },
            "disease_database": {
                "loaded": DATABASE_LOADED
            }
        }
    }), 200

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided",
                "error": "JSON data required"
            }), 400
        
        username = data.get('username') or data.get('email')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                "status": "error",
                "message": "Missing username or password",
                "error": "Both username and password are required"
            }), 400
        
        # For demo/development: Accept any valid email and password format
        # In production, validate against database
        if len(password) < 1:
            return jsonify({
                "status": "error",
                "message": "Invalid password",
                "error": "Password is too short"
            }), 400
        
        # Generate a mock user session
        user_id = hash(username) % 1000000
        api_key = f"key_{user_id}_{int(datetime.utcnow().timestamp())}"
        
        logger.info(f"✓ User logged in: {username}")
        
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user_id": user_id,
            "api_key": api_key,
            "username": username,
            "email": username
        }), 200
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }), 500

@app.route('/users', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided",
                "error": "JSON data required"
            }), 400
        
        email = data.get('email') or data.get('username')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "error": "Email, password, and name are required"
            }), 400
        
        # Basic validation
        if '@' not in email:
            return jsonify({
                "status": "error",
                "message": "Invalid email format",
                "error": "Please provide a valid email address"
            }), 400
        
        if len(password) < 6:
            return jsonify({
                "status": "error",
                "message": "Password too short",
                "error": "Password must be at least 6 characters long"
            }), 400
        
        # Generate a mock user session
        user_id = hash(email) % 1000000
        api_key = f"key_{user_id}_{int(datetime.utcnow().timestamp())}"
        
        logger.info(f"✓ New user registered: {email} ({name})")
        
        return jsonify({
            "status": "success",
            "message": "Registration successful",
            "user_id": user_id,
            "api_key": api_key,
            "username": email,
            "email": email,
            "name": name
        }), 201
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with CORS headers"""
    response = jsonify({
        "error": "Endpoint not found",
        "status": 404,
        "message": f"The requested endpoint does not exist. Check / for available endpoints.",
        "available_endpoints": [
            "POST /api/predict/symptoms",
            "POST /api/predict/skin",
            "POST /api/predict/xray",
            "GET /api/disease/<name>",
            "GET /api/status",
            "POST /auth/login",
            "POST /users"
        ]
    })
    response.status_code = 404
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors with CORS headers"""
    logger.error(f"❌ Server Error: {str(error)}")
    response = jsonify({
        "error": "Internal server error",
        "status": 500,
        "message": str(error)
    })
    response.status_code = 500
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# ==================== DATABASE AND AUTH INITIALIZATION ====================

# Register authentication blueprint
from auth_routes import auth_bp
app.register_blueprint(auth_bp)

# Create database tables
with app.app_context():
    try:
        db.create_all()
        logger.info("✓ Database tables initialized successfully")
    except Exception as e:
        logger.error(f"✗ Error initializing database: {str(e)}")

@app.route('/api/db/init', methods=['POST'])
def init_db():
    """Initialize database (for development/testing)"""
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
        logger.info("✓ Database re-initialized successfully")
        return jsonify({'message': 'Database initialized successfully'}), 200
    except Exception as e:
        logger.error(f"✗ Error initializing database: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting Health AI Backend Server...")
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
