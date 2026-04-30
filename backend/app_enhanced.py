from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
import os
import pandas as pd
import secrets
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import logging
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import uuid

# Import disease database
try:
    from disease_database import (
        get_disease_info, get_risk_level, get_treatment_suggestions,
        get_medications, get_diet_advice, get_activity_recommendations
    )
    DATABASE_LOADED = True
except ImportError:
    logger_init = logging.getLogger(__name__)
    logger_init.warning("Disease database not imported - using fallback")
    DATABASE_LOADED = False

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.dirname(BASE_DIR)  # Root directory contains the ML model files

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/health_ai_db')

try:
    client = MongoClient(MONGODB_URI)
    db = client.health_ai_db
    # Test the connection
    client.admin.command('ping')
    logger.info("✓ Connected to MongoDB successfully!")
except Exception as e:
    logger.error(f"✗ Failed to connect to MongoDB: {e}")
    db = None

# Load ML models
logger.info("📦 Loading ML models...")

# Skin disease model
SKIN_MODEL_PATH = os.path.join(MODEL_DIR, 'skin_model.h5')

def build_skin_model():
    """Build and load skin disease model"""
    try:
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False
        x = base_model.output
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(128, activation='relu')(x)
        output = layers.Dense(22, activation='softmax')(x)
        model = models.Model(inputs=base_model.input, outputs=output)
        model.load_weights(SKIN_MODEL_PATH)
        logger.info("✓ Skin model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"✗ Failed to load skin model: {e}")
        return None

skin_model = build_skin_model()
skin_class_names = [
    'Acne', 'Actinic_Keratosis', 'Benign_tumors', 'Bullous', 'Candidiasis',
    'DrugEruption', 'Eczema', 'Infestations_Bites', 'Lichen', 'Lupus',
    'Moles', 'Psoriasis', 'Rosacea', 'Seborrh_Keratoses', 'SkinCancer',
    'Sun_Sunlight_Damage', 'Tinea', 'Unknown_Normal', 'Vascular_Tumors',
    'Vasculitis', 'Vitiligo', 'Warts'
]

# X-ray model
XRAY_MODEL_PATH = os.path.join(MODEL_DIR, 'xray_model.h5')

def build_xray_model():
    """Build and load X-ray model"""
    try:
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False
        x = base_model.output
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(128, activation='relu')(x)
        output = layers.Dense(1, activation='sigmoid')(x)
        model = models.Model(inputs=base_model.input, outputs=output)
        model.load_weights(XRAY_MODEL_PATH)
        logger.info("✓ X-ray model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"✗ Failed to load X-ray model: {e}")
        return None

xray_model = build_xray_model()
xray_class_names = ['NORMAL', 'PNEUMONIA']

# Symptom to disease model
SYMPTOM_MODEL_PATH = os.path.join(BASE_DIR, 'symptom_model.pkl')
SYMPTOM_ENCODER_PATH = os.path.join(BASE_DIR, 'symptom_encoder.pkl')
SYMPTOM_FEATURES_PATH = os.path.join(BASE_DIR, 'symptom_features.pkl')
SYMPTOM_SCALER_PATH = os.path.join(BASE_DIR, 'symptom_scaler.pkl')

symptom_model = None
symptom_encoder = None
symptom_features = []
symptom_scaler = None

if os.path.exists(SYMPTOM_MODEL_PATH):
    try:
        symptom_model = joblib.load(SYMPTOM_MODEL_PATH)
        symptom_encoder = joblib.load(SYMPTOM_ENCODER_PATH)
        symptom_features = joblib.load(SYMPTOM_FEATURES_PATH)
        
        # Load scaler if it exists
        if os.path.exists(SYMPTOM_SCALER_PATH):
            symptom_scaler = joblib.load(SYMPTOM_SCALER_PATH)
        
        logger.info(f"✓ Symptom model loaded successfully ({len(symptom_features)} features, {len(symptom_encoder.classes_)} diseases)")
    except Exception as e:
        logger.warning(f"⚠️  Failed to load symptom model: {e}")
        symptom_model = None
        symptom_encoder = None
        symptom_features = []
else:
    logger.warning("⚠️  Symptom model not found. Run: python backend/train_symptoms_improved.py")

logger.info("✓ All models loaded!")

# Risk level classification helper
def classify_risk_level(disease_name, confidence_score=1.0):
    """Classify disease risk level"""
    if DATABASE_LOADED:
        risk_level = get_risk_level(disease_name)
        if risk_level and risk_level in ['Low', 'Medium', 'High']:
            return risk_level
    
    # Fallback to confidence-based classification
    if confidence_score > 0.8:
        return 'High'
    elif confidence_score > 0.5:
        return 'Medium'
    else:
        return 'Low'

def get_disease_recommendations(disease_name):
    """Get comprehensive disease information and recommendations"""
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
    
    # Default fallback
    return {
        'risk_level': 'Medium',
        'description': f'Disease: {disease_name}',
        'medications': ['Consult with healthcare provider'],
        'treatments': ['Consult with healthcare provider'],
        'home_remedies': ['Rest and hydration'],
        'diet_advice': ['Balanced nutrition'],
        'activity_recommendations': ['Light exercise as tolerated'],
        'recovery_duration': 'Variable'
    }

# Risk probability calculation
def get_risk_probability(disease_name, confidence_score):
    """Calculate risk probability as percentage"""
    risk_level = classify_risk_level(disease_name, confidence_score)
    
    # Map confidence to risk probability
    risk_prob = int(confidence_score * 100)
    
    # Adjust based on risk level
    if risk_level == 'High':
        risk_prob = min(100, risk_prob + 20)
    elif risk_level == 'Low':
        risk_prob = max(0, risk_prob - 10)
    
    return risk_prob

# API key helpers
def generate_api_key():
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)

def get_api_key_from_request():
    """Extract API key from request"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header.split(' ', 1)[1].strip()
    api_key = request.headers.get('x-api-key') or request.args.get('api_key')
    if not api_key and request.is_json:
        payload = request.get_json(silent=True) or {}
        api_key = payload.get('api_key')
    return api_key

def authenticate_api_key():
    """Authenticate API key"""
    api_key = get_api_key_from_request()
    if not api_key or db is None:
        return None
    user = db.users.find_one({'api_key': api_key})
    return user

def require_api_key(f):
    """Decorator to require API key"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = authenticate_api_key()
        if not user:
            return jsonify({'error': 'API key missing or invalid'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated

# Database helper functions
def save_user_data(user_data):
    """Save user data to MongoDB"""
    if db is None:
        logger.error("Database not available")
        return None
    try:
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error saving user data: {e}")
        return None

def save_prediction_result(user_id, prediction_type, prediction_data):
    """Save prediction results to MongoDB"""
    if db is None:
        return None
    try:
        prediction_record = {
            'user_id': user_id,
            'prediction_type': prediction_type,
            'prediction_data': prediction_data,
            'created_at': datetime.utcnow()
        }
        result = db.predictions.insert_one(prediction_record)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error saving prediction: {e}")
        return None

# ==================== API ENDPOINTS ====================

@app.route('/')
def home():
    """Health AI API home endpoint"""
    return jsonify({
        "message": "🏥 Health AI Prediction System",
        "version": "2.0",
        "status": "running",
        "endpoints": {
            "skin_disease": "POST /predict/skin (with image file)",
            "xray_analysis": "POST /predict/xray (with image file)",
            "symptom_prediction": "POST /predict/symptoms (with symptoms array)",
            "disease_info": "GET /disease/<disease_name>",
            "cure_suggestions": "GET /cure/<disease_name>",
            "activity_recommendations": "GET /activities/<disease_name>"
        },
        "models_loaded": {
            "skin_model": skin_model is not None,
            "xray_model": xray_model is not None,
            "symptom_model": symptom_model is not None,
            "disease_database": DATABASE_LOADED
        }
    })

@app.route('/predict/skin', methods=['POST'])
def predict_skin():
    """Predict skin disease from image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        if skin_model is None:
            return jsonify({"error": "Skin model not available"}), 500
        
        file = request.files['image']
        
        # Preprocess image
        img = image.load_img(file, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        prediction = skin_model.predict(img_array, verbose=0)
        class_index = np.argmax(prediction[0])
        disease_name = skin_class_names[class_index]
        confidence = float(prediction[0][class_index])
        
        # Get top 3 predictions
        top_indices = np.argsort(prediction[0])[-3:][::-1]
        top_predictions = [
            {
                "disease": skin_class_names[idx],
                "confidence": float(prediction[0][idx]),
                "probability": f"{float(prediction[0][idx])*100:.2f}%"
            }
            for idx in top_indices
        ]
        
        # Get disease information
        disease_info = get_disease_recommendations(disease_name)
        
        # Calculate risk level and probability
        risk_level = classify_risk_level(disease_name, confidence)
        risk_probability = get_risk_probability(disease_name, confidence)
        
        prediction_data = {
            "status": "success",
            "predicted_disease": disease_name,
            "confidence_score": confidence,
            "confidence_percentage": f"{confidence*100:.2f}%",
            "risk_level": risk_level,
            "risk_probability": f"{risk_probability}%",
            "top_3_predictions": top_predictions,
            "disease_description": disease_info['description'],
            "risk_classification": risk_level,
            "medications": disease_info['medications'],
            "treatments": disease_info['treatments'],
            "home_remedies": disease_info['home_remedies'],
            "diet_advice": disease_info['diet_advice'],
            "activity_recommendations": disease_info['activity_recommendations'],
            "recovery_duration": disease_info['recovery_duration'],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(prediction_data), 200
    
    except Exception as e:
        logger.error(f"Skin prediction error: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/predict/xray', methods=['POST'])
def predict_xray():
    """Predict chest X-ray findings"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        if xray_model is None:
            return jsonify({"error": "X-ray model not available"}), 500
        
        file = request.files['image']
        
        # Preprocess image
        img = image.load_img(file, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        prediction = xray_model.predict(img_array, verbose=0)
        pred_prob = prediction[0][0]
        class_index = 1 if pred_prob > 0.5 else 0
        finding = xray_class_names[class_index]
        confidence = float(pred_prob) if class_index == 1 else float(1 - pred_prob)
        
        # Get disease information for pneumonia if detected
        if finding == 'PNEUMONIA':
            disease_info = get_disease_recommendations('Pneumonia')
        else:
            disease_info = {
                'risk_level': 'Low',
                'description': 'Chest X-ray shows normal findings',
                'medications': ['No medication required'],
                'treatments': ['Monitor health regularly'],
                'home_remedies': ['Maintain healthy lifestyle'],
                'diet_advice': ['Balanced nutritious diet'],
                'activity_recommendations': ['Regular exercise'],
                'duration': 'Normal - continue monitoring'
            }
        
        # Calculate risk
        risk_level = classify_risk_level(finding, confidence)
        risk_probability = get_risk_probability(finding, confidence)
        
        prediction_data = {
            "status": "success",
            "finding": finding,
            "confidence_score": confidence,
            "confidence_percentage": f"{confidence*100:.2f}%",
            "risk_level": risk_level,
            "risk_probability": f"{risk_probability}%",
            "normal_probability": f"{(1-confidence)*100:.2f}%",
            "pneumonia_probability": f"{confidence*100:.2f}%",
            "disease_description": disease_info['description'],
            "medications": disease_info['medications'],
            "treatments": disease_info['treatments'],
            "home_remedies": disease_info['home_remedies'],
            "diet_advice": disease_info['diet_advice'],
            "activity_recommendations": disease_info['activity_recommendations'],
            "clinical_notes": disease_info['duration'],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(prediction_data), 200
    
    except Exception as e:
        logger.error(f"X-ray prediction error: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/predict/symptoms', methods=['POST'])
def predict_symptoms():
    """Predict disease from symptoms"""
    try:
        if symptom_model is None:
            return jsonify({"error": "Symptom model not trained yet. Run training first."}), 503
        
        data = request.get_json()
        if not data or 'symptoms' not in data:
            return jsonify({"error": "Symptoms data required in JSON"}), 400
        
        symptoms = data.get('symptoms', [])
        if not isinstance(symptoms, list):
            return jsonify({"error": "Symptoms should be a list"}), 400
        
        # Create feature vector
        feature_vector = np.zeros(len(symptom_features))
        for symptom in symptoms:
            if symptom in symptom_features:
                feature_vector[symptom_features.index(symptom)] = 1
        
        # Scale if scaler exists
        if symptom_scaler:
            feature_vector = symptom_scaler.transform([feature_vector])[0]
        else:
            feature_vector = np.array([feature_vector])
        
        # Make prediction
        probabilities = symptom_model.predict_proba([feature_vector])[0]
        top_indices = np.argsort(probabilities)[-5:][::-1]
        
        predicted_class = np.argmax(probabilities)
        predicted_disease = symptom_encoder.classes_[predicted_class]
        confidence = float(probabilities[predicted_class])
        
        # Get top 5 predictions
        top_predictions = []
        for idx in top_indices:
            disease = symptom_encoder.classes_[idx]
            prob = float(probabilities[idx])
            risk = classify_risk_level(disease, prob)
            top_predictions.append({
                "disease": disease,
                "confidence": prob,
                "confidence_percentage": f"{prob*100:.2f}%",
                "risk_level": risk
            })
        
        # Get disease information
        disease_info = get_disease_recommendations(predicted_disease)
        
        # Calculate risk
        risk_level = disease_info['risk_level']
        risk_probability = get_risk_probability(predicted_disease, confidence)
        
        prediction_data = {
            "status": "success",
            "predicted_disease": predicted_disease,
            "confidence_score": confidence,
            "confidence_percentage": f"{confidence*100:.2f}%",
            "risk_level": risk_level,
            "risk_probability": f"{risk_probability}%",
            "top_5_predictions": top_predictions,
            "disease_description": disease_info['description'],
            "medications": disease_info['medications'],
            "treatments": disease_info['treatments'],
            "home_remedies": disease_info['home_remedies'],
            "diet_advice": disease_info['diet_advice'],
            "activity_recommendations": disease_info['activity_recommendations'],
            "recovery_duration": disease_info['recovery_duration'],
            "input_symptoms_count": len(symptoms),
            "matched_symptoms": [s for s in symptoms if s in symptom_features],
            "timestamp": datetime.utcnow().isoformat(),
            "disclaimer": "⚠️  This is an AI prediction. Always consult a healthcare professional for proper diagnosis."
        }
        
        return jsonify(prediction_data), 200
    
    except Exception as e:
        logger.error(f"Symptom prediction error: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/disease/<disease_name>', methods=['GET'])
def get_disease_details(disease_name):
    """Get detailed information about a disease"""
    try:
        # Handle underscores in URL
        disease_name = disease_name.replace('_', ' ')
        
        disease_info = get_disease_recommendations(disease_name)
        
        return jsonify({
            "status": "success",
            "disease": disease_name,
            "details": disease_info,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Disease info error: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/cure/<disease_name>', methods=['GET'])
def get_cure_recommendations(disease_name):
    """Get cure and treatment recommendations for a disease"""
    try:
        disease_name = disease_name.replace('_', ' ')
        disease_info = get_disease_recommendations(disease_name)
        
        cure_data = {
            "status": "success",
            "disease": disease_name,
            "risk_level": disease_info['risk_level'],
            "medications": disease_info['medications'],
            "treatments": disease_info['treatments'],
            "home_remedies": disease_info['home_remedies'],
            "diet_advice": disease_info['diet_advice'],
            "recovery_duration": disease_info['recovery_duration'],
            "timestamp": datetime.utcnow().isoformat(),
            "disclaimer": "⚠️  Medical advice should be obtained from licensed healthcare professionals."
        }
        
        return jsonify(cure_data), 200
    
    except Exception as e:
        logger.error(f"Cure recommendation error: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/activities/<disease_name>', methods=['GET'])
def get_activity_suggestions(disease_name):
    """Get activity recommendations for a disease"""
    try:
        disease_name = disease_name.replace('_', ' ')
        disease_info = get_disease_recommendations(disease_name)
        
        activity_data = {
            "status": "success",
            "disease": disease_name,
            "risk_level": disease_info['risk_level'],
            "recommended_activities": disease_info['activity_recommendations'],
            "dietary_recommendations": disease_info['diet_advice'],
            "recovery_duration": disease_info['recovery_duration'],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(activity_data), 200
    
    except Exception as e:
        logger.error(f"Activity recommendation error: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/models/status', methods=['GET'])
def model_status():
    """Get status of all loaded models"""
    return jsonify({
        "status": "success",
        "models": {
            "skin_disease_model": {
                "loaded": skin_model is not None,
                "classes": len(skin_class_names),
                "class_names": skin_class_names
            },
            "xray_model": {
                "loaded": xray_model is not None,
                "classes": len(xray_class_names),
                "class_names": xray_class_names
            },
            "symptom_model": {
                "loaded": symptom_model is not None,
                "features": len(symptom_features),
                "diseases": len(symptom_encoder.classes_) if symptom_encoder else 0,
                "diseases_list": list(symptom_encoder.classes_) if symptom_encoder else []
            },
            "disease_database": {
                "loaded": DATABASE_LOADED
            }
        },
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found", "status": "error"}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error", "status": "error"}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting Health AI Backend Server...")
    logger.info(f"📍 Flask Debug Mode: {os.getenv('FLASK_DEBUG', 'False')}")
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
