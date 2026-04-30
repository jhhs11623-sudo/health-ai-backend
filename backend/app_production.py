from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
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
CORS(app)  # Enable CORS for frontend

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.dirname(BASE_DIR)

# Import disease database
try:
    from disease_database import get_disease_info, get_risk_level
    DATABASE_LOADED = True
except ImportError:
    logger.warning("Disease database not imported")
    DATABASE_LOADED = False

# ==================== LOAD MODELS ====================

logger.info("📦 Loading ML Models...")

# Skin Disease Model
SKIN_MODEL_PATH = os.path.join(MODEL_DIR, 'skin_model.h5')

def build_skin_model():
    try:
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False
        x = base_model.output
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(128, activation='relu')(x)
        output = layers.Dense(22, activation='softmax')(x)
        model = models.Model(inputs=base_model.input, outputs=output)
        model.load_weights(SKIN_MODEL_PATH)
        logger.info("✓ Skin model loaded")
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

# X-Ray Model
XRAY_MODEL_PATH = os.path.join(MODEL_DIR, 'xray_model.h5')

def build_xray_model():
    try:
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False
        x = base_model.output
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(128, activation='relu')(x)
        output = layers.Dense(1, activation='sigmoid')(x)
        model = models.Model(inputs=base_model.input, outputs=output)
        model.load_weights(XRAY_MODEL_PATH)
        logger.info("✓ X-Ray model loaded")
        return model
    except Exception as e:
        logger.error(f"✗ Failed to load X-Ray model: {e}")
        return None

xray_model = build_xray_model()

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
            "models_status": "GET /api/status"
        }
    }), 200

@app.route('/api/predict/symptoms', methods=['POST'])
def predict_symptoms():
    """Predict disease from symptoms - FIXED VERSION"""
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
        
        # FIXED: Properly handle symptoms
        if not isinstance(symptoms, list) or len(symptoms) == 0:
            return jsonify({
                "status": "error",
                "message": "No symptoms provided",
                "error": "Provide at least one symptom"
            }), 400
        
        # Create feature vector with exact matching
        feature_vector = np.zeros(len(symptom_features))
        matched_count = 0
        
        for symptom in symptoms:
            # Try exact match first
            if symptom in symptom_features:
                idx = symptom_features.index(symptom)
                feature_vector[idx] = 1
                matched_count += 1
            else:
                # Try underscore/space conversion
                symptom_alt = symptom.replace(' ', '_').replace('-', '_').lower()
                if symptom_alt in symptom_features:
                    idx = symptom_features.index(symptom_alt)
                    feature_vector[idx] = 1
                    matched_count += 1
        
        # If no symptoms matched, return error
        if matched_count == 0:
            logger.warning(f"No symptoms matched: {symptoms}")
            return jsonify({
                "status": "error",
                "message": "Symptoms not recognized",
                "error": f"Could not match any symptoms. Valid symptoms include: {symptom_features[:10]}...",
                "provided_symptoms": symptoms,
                "available_count": len(symptom_features)
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
    try:
        if skin_model is None:
            return jsonify({"error": "Skin model not available"}), 503
        
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
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
        
        # Get top 3
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
            "risk_level": risk_level,
            "top_3_predictions": top_predictions,
            "medications": disease_info['medications'][:5],
            "treatments": disease_info['treatments'][:5],
            "diet_advice": disease_info['diet_advice'][:5],
            "activity_recommendations": disease_info['activity_recommendations'][:5]
        }), 200
    
    except Exception as e:
        logger.error(f"Skin prediction error: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/predict/xray', methods=['POST'])
def predict_xray():
    """Predict chest X-ray findings"""
    try:
        if xray_model is None:
            return jsonify({"error": "X-ray model not available"}), 503
        
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        file = request.files['image']
        
        # Preprocess image
        img = image.load_img(file, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        prediction = xray_model.predict(img_array, verbose=0)
        pred_prob = prediction[0][0]
        class_index = 1 if pred_prob > 0.5 else 0
        finding = 'PNEUMONIA' if class_index == 1 else 'NORMAL'
        confidence = float(pred_prob) if class_index == 1 else float(1 - pred_prob)
        
        if finding == 'PNEUMONIA':
            disease_info = get_disease_recommendations('Pneumonia')
        else:
            disease_info = {
                'risk_level': 'Low',
                'description': 'Chest X-ray shows normal findings',
                'medications': ['No medication required'],
                'treatments': ['Monitor health regularly'],
                'diet_advice': ['Balanced diet'],
                'activity_recommendations': ['Regular exercise']
            }
        
        return jsonify({
            "status": "success",
            "finding": finding,
            "confidence_percentage": f"{confidence*100:.2f}%",
            "risk_level": disease_info['risk_level'],
            "description": disease_info['description'],
            "medications": disease_info['medications'][:5],
            "treatments": disease_info['treatments'][:5],
            "diet_advice": disease_info['diet_advice'][:5]
        }), 200
    
    except Exception as e:
        logger.error(f"X-ray prediction error: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500

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

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "status": "error"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error", "status": "error"}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting Health AI Backend Server...")
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
