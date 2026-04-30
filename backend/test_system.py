#!/usr/bin/env python3
"""
Health AI System - Comprehensive Test Suite
Tests all models and API endpoints to ensure everything is working correctly
"""

import os
import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(backend_dir)
sys.path.insert(0, backend_dir)

# Styling
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def test_header(title):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}{Colors.ENDC}\n")

def test_pass(message):
    print(f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}: {message}")

def test_fail(message):
    print(f"{Colors.FAIL}✗ FAIL{Colors.ENDC}: {message}")

def test_warn(message):
    print(f"{Colors.WARNING}⚠️  WARN{Colors.ENDC}: {message}")

def test_info(message):
    print(f"{Colors.OKCYAN}ℹ️  INFO{Colors.ENDC}: {message}")

# Test 1: File Structure
def test_file_structure():
    test_header("TEST 1: FILE STRUCTURE VERIFICATION")
    
    required_files = {
        'Disease Database': os.path.join(backend_dir, 'disease_database.py'),
        'Enhanced App': os.path.join(backend_dir, 'app_enhanced.py'),
        'Training Script': os.path.join(backend_dir, 'train_symptoms_improved.py'),
        'Setup Script': os.path.join(backend_dir, 'setup_and_train.py'),
        'Data': os.path.join(root_dir, 'data', 'raw', 'Training.csv'),
        'Skin Model': os.path.join(root_dir, 'skin_model.h5'),
        'XRay Model': os.path.join(root_dir, 'xray_model.h5')
    }
    
    passed = 0
    failed = 0
    
    for name, path in required_files.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            if size > 1024 * 1024:  # > 1MB
                test_pass(f"{name} ({size/(1024*1024):.2f} MB)")
            else:
                test_pass(f"{name} ({size/1024:.2f} KB)")
            passed += 1
        else:
            test_fail(f"{name} - NOT FOUND at {path}")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0

# Test 2: Dependencies
def test_dependencies():
    test_header("TEST 2: DEPENDENCY VERIFICATION")
    
    dependencies = {
        'tensorflow': 'TensorFlow',
        'keras': 'Keras',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'flask': 'Flask',
        'joblib': 'Joblib',
        'PIL': 'Pillow'
    }
    
    passed = 0
    failed = 0
    
    for module, name in dependencies.items():
        try:
            lib = __import__(module)
            if hasattr(lib, '__version__'):
                test_pass(f"{name} ({lib.__version__})")
            else:
                test_pass(f"{name} (installed)")
            passed += 1
        except ImportError:
            test_fail(f"{name} - NOT INSTALLED")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0

# Test 3: Disease Database
def test_disease_database():
    test_header("TEST 3: DISEASE DATABASE VERIFICATION")
    
    try:
        from disease_database import (
            DISEASE_DATABASE, get_disease_info, get_risk_level,
            get_treatment_suggestions, get_medications, get_diet_advice,
            get_activity_recommendations
        )
        
        test_pass("Disease database imported successfully")
        test_info(f"Total diseases in database: {len(DISEASE_DATABASE)}")
        
        # Test some key diseases
        test_diseases = ['Diabetes', 'Pneumonia', 'Acne', 'Psoriasis', 'Heart attack']
        
        for disease in test_diseases:
            info = get_disease_info(disease)
            if info:
                risk = get_risk_level(disease)
                test_pass(f"{disease} - Risk Level: {risk}")
                
                # Verify all required fields
                required_fields = ['medications', 'treatments', 'diet_advice', 'activities']
                for field in required_fields:
                    if field in info:
                        test_pass(f"  └─ {field}: {len(info[field])} items")
                    else:
                        test_warn(f"  └─ {field}: MISSING")
            else:
                test_fail(f"{disease} - NOT FOUND in database")
        
        return True
    
    except Exception as e:
        test_fail(f"Disease database error: {str(e)}")
        return False

# Test 4: Symptom Model
def test_symptom_model():
    test_header("TEST 4: SYMPTOM MODEL VERIFICATION")
    
    try:
        import joblib
        
        model_path = os.path.join(backend_dir, 'symptom_model.pkl')
        encoder_path = os.path.join(backend_dir, 'symptom_encoder.pkl')
        features_path = os.path.join(backend_dir, 'symptom_features.pkl')
        scaler_path = os.path.join(backend_dir, 'symptom_scaler.pkl')
        
        # Load model
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            test_pass(f"Symptom model loaded")
        else:
            test_warn("Symptom model not found - needs training")
            return False
        
        # Load encoder
        encoder = joblib.load(encoder_path)
        test_pass(f"Symptom encoder loaded ({len(encoder.classes_)} diseases)")
        
        # Load features
        features = joblib.load(features_path)
        test_pass(f"Feature list loaded ({len(features)} features)")
        
        # Load scaler
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            test_pass("Feature scaler loaded")
        else:
            test_warn("Feature scaler not found - will use unscaled features")
        
        # Test prediction
        feature_vector = np.zeros(len(features))
        if len(features) > 0:
            feature_vector[0] = 1
        
        probabilities = model.predict_proba([feature_vector])[0]
        top_idx = np.argmax(probabilities)
        predicted_disease = encoder.classes_[top_idx]
        confidence = probabilities[top_idx]
        
        test_pass(f"Sample prediction: {predicted_disease} ({confidence:.2%} confidence)")
        
        # Show top 5 predictions
        top_indices = np.argsort(probabilities)[-5:][::-1]
        test_info("Top 5 predictions:")
        for i, idx in enumerate(top_indices, 1):
            print(f"  {i}. {encoder.classes_[idx]}: {probabilities[idx]:.4f}")
        
        return True
    
    except Exception as e:
        test_fail(f"Symptom model error: {str(e)}")
        return False

# Test 5: Image Models
def test_image_models():
    test_header("TEST 5: IMAGE MODEL VERIFICATION")
    
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        from tensorflow.keras.applications import MobileNetV2
        
        passed = 0
        failed = 0
        
        # Test Skin Model
        skin_path = os.path.join(root_dir, 'skin_model.h5')
        try:
            base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
            base_model.trainable = False
            x = base_model.output
            x = layers.GlobalAveragePooling2D()(x)
            x = layers.Dense(128, activation='relu')(x)
            output = layers.Dense(22, activation='softmax')(x)
            skin_model = models.Model(inputs=base_model.input, outputs=output)
            skin_model.load_weights(skin_path)
            test_pass("Skin model loaded successfully (22 classes)")
            passed += 1
        except Exception as e:
            test_fail(f"Skin model error: {str(e)}")
            failed += 1
        
        # Test XRay Model
        xray_path = os.path.join(root_dir, 'xray_model.h5')
        try:
            base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
            base_model.trainable = False
            x = base_model.output
            x = layers.GlobalAveragePooling2D()(x)
            x = layers.Dense(128, activation='relu')(x)
            output = layers.Dense(1, activation='sigmoid')(x)
            xray_model = models.Model(inputs=base_model.input, outputs=output)
            xray_model.load_weights(xray_path)
            test_pass("X-Ray model loaded successfully (Binary classification)")
            passed += 1
        except Exception as e:
            test_fail(f"X-Ray model error: {str(e)}")
            failed += 1
        
        print(f"\nResult: {passed} passed, {failed} failed")
        return failed == 0
    
    except Exception as e:
        test_fail(f"Image model verification error: {str(e)}")
        return False

# Test 6: API Endpoints Structure
def test_api_endpoints():
    test_header("TEST 6: API ENDPOINTS VERIFICATION")
    
    try:
        from app_enhanced import app
        
        # Get all registered routes
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                    'path': str(rule)
                })
        
        test_pass(f"Flask app loaded with {len(routes)} endpoints")
        
        # Check critical endpoints
        critical_endpoints = [
            ('/', 'GET'),
            ('/predict/skin', 'POST'),
            ('/predict/xray', 'POST'),
            ('/predict/symptoms', 'POST'),
            ('/disease/<disease_name>', 'GET'),
            ('/cure/<disease_name>', 'GET'),
            ('/activities/<disease_name>', 'GET'),
            ('/models/status', 'GET')
        ]
        
        for path, method in critical_endpoints:
            matching = [r for r in routes if r['path'] == path and method in r['methods']]
            if matching:
                test_pass(f"{method:6} {path}")
            else:
                test_warn(f"{method:6} {path} - NOT FOUND")
        
        return True
    
    except Exception as e:
        test_fail(f"API endpoint verification error: {str(e)}")
        return False

# Test 7: Data Integrity
def test_data_integrity():
    test_header("TEST 7: DATA INTEGRITY CHECK")
    
    try:
        import pandas as pd
        
        # Load training data
        data_path = os.path.join(root_dir, 'data', 'raw', 'Training.csv')
        df = pd.read_csv(data_path)
        
        test_pass(f"Training data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Check for missing values
        missing = df.isnull().sum().sum()
        if missing == 0:
            test_pass("No missing values found")
        else:
            test_warn(f"{missing} missing values found")
        
        # Check for required columns
        if 'prognosis' in df.columns:
            test_pass(f"'prognosis' column found with {df['prognosis'].nunique()} unique diseases")
        else:
            test_fail("'prognosis' column NOT FOUND")
        
        # Check data balance
        disease_counts = df['prognosis'].value_counts()
        test_info(f"Disease distribution (top 5):")
        for disease, count in disease_counts.head().items():
            print(f"  {disease:30}: {count:3} samples")
        
        return True
    
    except Exception as e:
        test_fail(f"Data integrity check error: {str(e)}")
        return False

# Summary Test
def test_summary():
    test_header("TEST EXECUTION SUMMARY")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Dependencies", test_dependencies),
        ("Disease Database", test_disease_database),
        ("Symptom Model", test_symptom_model),
        ("Image Models", test_image_models),
        ("API Endpoints", test_api_endpoints),
        ("Data Integrity", test_data_integrity)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            test_fail(f"Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    test_header("FINAL RESULTS")
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for test_name, result in results:
        status = f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}" if result else f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"
        print(f"{status}: {test_name}")
    
    print(f"\n{Colors.BOLD}Overall: {passed}/{len(results)} tests passed{Colors.ENDC}\n")
    
    if failed == 0:
        print(f"{Colors.OKGREEN}{Colors.BOLD}✓ ALL TESTS PASSED - SYSTEM READY FOR USE!{Colors.ENDC}\n")
        return True
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}⚠️  {failed} tests failed - Check above for details{Colors.ENDC}\n")
        return False

# Main execution
def main():
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("=" * 80)
    print("  HEALTH AI SYSTEM - COMPREHENSIVE TEST SUITE v2.0")
    print("=" * 80)
    print(f"{Colors.ENDC}\n")
    
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Location: {backend_dir}\n")
    
    success = test_summary()
    
    print("=" * 80)
    if success:
        print(f"{Colors.OKGREEN}System is ready for production use!{Colors.ENDC}")
        print("\nNext steps:")
        print("1. Start the backend: python app_enhanced.py")
        print("2. Start the frontend: cd frontend && npm start")
        print("3. Access API at: http://localhost:5000")
        print("4. Access UI at: http://localhost:3000")
    else:
        print(f"{Colors.FAIL}Please resolve the errors above before using the system{Colors.ENDC}")
        print("\nHint: Run 'python train_symptoms_improved.py' to train missing models")
    print("=" * 80 + "\n")
    
    return 0 if success else 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Tests interrupted by user{Colors.ENDC}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {str(e)}{Colors.ENDC}\n")
        sys.exit(1)
