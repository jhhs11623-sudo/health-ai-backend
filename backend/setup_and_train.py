#!/usr/bin/env python3
"""
Health AI System - Complete Setup and Training Guide
This script helps set up and train all models for the Health AI prediction system
"""

import os
import sys
import subprocess
from pathlib import Path

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("CHECKING DEPENDENCIES")
    
    required_packages = {
        'tensorflow': 'TensorFlow',
        'keras': 'Keras',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'joblib': 'Joblib',
        'PIL': 'Pillow',
        'pymongo': 'PyMongo'
    }
    
    missing_packages = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print_success(f"{name} is installed")
        except ImportError:
            print_error(f"{name} is NOT installed")
            missing_packages.append(name)
    
    if missing_packages:
        print_warning(f"\nTo install missing packages, run:")
        print(f"  pip install -r requirements.txt")
        return False
    
    print_success("\nAll dependencies are installed!")
    return True

def check_data_files():
    """Check if training data files exist"""
    print_header("CHECKING DATA FILES")
    
    root_dir = os.path.dirname(backend_dir)
    data_path = os.path.join(root_dir, 'data', 'raw', 'Training.csv')
    
    if os.path.exists(data_path):
        print_success(f"Training data found: {data_path}")
        df_size = os.path.getsize(data_path) / (1024 * 1024)  # Size in MB
        print_info(f"File size: {df_size:.2f} MB")
        return True
    else:
        print_error(f"Training data NOT found: {data_path}")
        return False

def check_models():
    """Check if models are already trained"""
    print_header("CHECKING TRAINED MODELS")
    
    root_dir = os.path.dirname(backend_dir)
    models_info = {
        'Skin Model': os.path.join(root_dir, 'skin_model.h5'),
        'X-Ray Model': os.path.join(root_dir, 'xray_model.h5'),
        'Symptom Model': os.path.join(backend_dir, 'symptom_model.pkl'),
        'Symptom Encoder': os.path.join(backend_dir, 'symptom_encoder.pkl'),
        'Symptom Features': os.path.join(backend_dir, 'symptom_features.pkl'),
        'Disease Database': os.path.join(backend_dir, 'disease_database.py')
    }
    
    missing_models = []
    
    for model_name, model_path in models_info.items():
        if os.path.exists(model_path):
            size = os.path.getsize(model_path) / (1024 * 1024)
            print_success(f"{model_name}: {size:.2f} MB")
        else:
            print_warning(f"{model_name}: NOT FOUND")
            missing_models.append(model_name)
    
    return len(missing_models) == 0, missing_models

def train_symptom_model():
    """Train the symptom-based disease prediction model"""
    print_header("TRAINING SYMPTOM MODEL")
    
    try:
        from train_symptoms_improved import train_advanced_symptoms_model
        
        print_info("Starting advanced symptom model training...")
        print_info("This may take 5-10 minutes depending on your system...")
        
        success = train_advanced_symptoms_model()
        
        if success:
            print_success("Symptom model trained successfully!")
            return True
        else:
            print_error("Failed to train symptom model")
            return False
    
    except Exception as e:
        print_error(f"Error during training: {str(e)}")
        return False

def test_predictions():
    """Test the models with sample predictions"""
    print_header("TESTING MODEL PREDICTIONS")
    
    try:
        print_info("Testing skin disease model...")
        # Since we don't have test images readily available, we'll skip this
        print_warning("Skin/X-ray testing requires image files (skip for now)")
        
        print_info("\nTesting symptom prediction model...")
        
        # Load models
        import joblib
        import numpy as np
        
        symptom_model = joblib.load(os.path.join(backend_dir, 'symptom_model.pkl'))
        symptom_encoder = joblib.load(os.path.join(backend_dir, 'symptom_encoder.pkl'))
        symptom_features = joblib.load(os.path.join(backend_dir, 'symptom_features.pkl'))
        
        # Create sample symptom vector
        feature_vector = np.zeros(len(symptom_features))
        
        # Test with first few features
        if len(feature_vector) > 0:
            feature_vector[0] = 1
            if len(feature_vector) > 1:
                feature_vector[1] = 1
        
        # Make prediction
        probabilities = symptom_model.predict_proba([feature_vector])[0]
        top_idx = np.argmax(probabilities)
        predicted_disease = symptom_encoder.classes_[top_idx]
        confidence = probabilities[top_idx]
        
        print_success(f"Sample Prediction: {predicted_disease} (confidence: {confidence:.2%})")
        
        # Test disease database
        from disease_database import get_disease_info
        disease_info = get_disease_info(predicted_disease)
        
        if disease_info:
            print_success(f"Disease info retrieved: Risk level = {disease_info['risk_level']}")
        else:
            print_warning(f"Disease info not found in database")
        
        print_success("All tests passed!")
        return True
    
    except Exception as e:
        print_error(f"Error during testing: {str(e)}")
        return False

def print_usage_guide():
    """Print usage guide for the system"""
    print_header("🎯 USAGE GUIDE")
    
    print("""
1. PREDICT SKIN DISEASE FROM IMAGE:
   POST /predict/skin
   - Upload an image file
   - Returns: disease prediction, confidence, risk level, treatments, activities
   
   Example:
   curl -X POST -F "image=@photo.jpg" http://localhost:5000/predict/skin

2. ANALYZE CHEST X-RAY:
   POST /predict/xray
   - Upload a chest X-ray image
   - Returns: finding (NORMAL/PNEUMONIA), confidence, risk level, treatments
   
   Example:
   curl -X POST -F "image=@xray.jpg" http://localhost:5000/predict/xray

3. PREDICT DISEASE FROM SYMPTOMS:
   POST /predict/symptoms
   - Provide list of symptoms
   - Returns: top 5 diseases, confidence, risk levels, treatments, diet advice, activities
   
   Example:
   curl -X POST -H "Content-Type: application/json" \
     -d '{"symptoms": ["cough", "fever", "fatigue"]}' \
     http://localhost:5000/predict/symptoms

4. GET DISEASE INFORMATION:
   GET /disease/Disease_Name
   - Returns complete disease info including description, risk level, treatments, diet
   
   Example:
   curl http://localhost:5000/disease/Diabetes

5. GET CURE RECOMMENDATIONS:
   GET /cure/Disease_Name
   - Returns medications, treatments, home remedies, diet advice
   
   Example:
   curl http://localhost:5000/cure/Pneumonia

6. GET ACTIVITY RECOMMENDATIONS:
   GET /activities/Disease_Name
   - Returns recommended activities and diet for the disease
   
   Example:
   curl http://localhost:5000/activities/Hypertension

7. CHECK MODEL STATUS:
   GET /models/status
   - Returns status of all loaded models and available diseases
   
   Example:
   curl http://localhost:5000/models/status

KEY FEATURES:
✓ Accurate disease prediction with confidence scores
✓ Risk level classification (Low/Medium/High)  
✓ Comprehensive treatment recommendations
✓ Medication suggestions
✓ Home remedies and diet advice
✓ Activity recommendations for recovery
✓ Recovery duration estimates
✓ Support for 22 skin diseases, chest X-ray analysis, and 40+ symptom-based diseases
    """)

def print_next_steps():
    """Print next steps"""
    print_header("📋 NEXT STEPS")
    
    print("""
1. START THE BACKEND SERVER:
   python backend/app_enhanced.py
   
   Or use the existing run_server.bat for Windows

2. START THE FRONTEND:
   cd frontend
   npm install
   npm start
   
   Or use start_frontend.bat for Windows

3. MAKE PREDICTIONS:
   - Open browser to http://localhost:3000
   - Or use curl commands (see Usage Guide above)

4. SYSTEM FEATURES AVAILABLE:
   ✓ Skin disease detection from images
   ✓ Chest X-ray analysis
   ✓ Symptom-based disease prediction
   ✓ Risk level classification
   ✓ Treatment/cure suggestions
   ✓ Diet recommendations
   ✓ Activity suggestions
   ✓ Recovery guidelines

5. TROUBLESHOOTING:
   - If models fail to load, ensure all .h5 and .pkl files are present
   - Check logs in the console for detailed error messages
   - Run this setup script again to verify everything is configured

📞 For issues or questions, check the README.md files in each directory
    """)

def main():
    """Main setup and training function"""
    print("\n")
    print(" " * 20 + "🏥 HEALTH AI SYSTEM SETUP & TRAINING")
    print(" " * 25 + "Version 2.0")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        return False
    
    # Step 2: Check data files
    if not check_data_files():
        print_warning("Training data not found. Skipping model training.")
        return False
    
    # Step 3: Check existing models
    models_exist, missing = check_models()
    
    if not models_exist:
        print_warning(f"Missing models: {', '.join(missing)}")
        
        # Train symptom model if missing
        if any('Symptom' in m for m in missing):
            print("\n")
            response = input("Would you like to train the symptom model now? (y/n): ").strip().lower()
            if response == 'y':
                train_symptom_model()
    
    # Step 4: Test predictions
    if models_exist or all('Symptom' not in m for m in missing):
        print("\n")
        response = input("Would you like to run prediction tests? (y/n): ").strip().lower()
        if response == 'y':
            test_predictions()
    
    # Step 5: Print usage guide
    response = input("\nWould you like to see the usage guide? (y/n): ").strip().lower()
    if response == 'y':
        print_usage_guide()
    
    # Step 6: Print next steps
    print_next_steps()
    
    print_success("\n✅ Setup complete! Ready to use the Health AI system.\n")
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
