import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def train_advanced_symptoms_model():
    print("=" * 80)
    print("🚀 ADVANCED SYMPTOM-BASED DISEASE PREDICTION MODEL TRAINING")
    print("=" * 80)
    
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'Training.csv')
    print(f"\n📂 Loading dataset from: {data_path}")
    
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("❌ ERROR: Training.csv not found!")
        print(f"Expected location: {data_path}")
        return False
    
    print(f"✓ Dataset loaded successfully")
    print(f"  Shape: {df.shape} (rows: {df.shape[0]}, columns: {df.shape[1]})")
    
    # Data cleaning and preprocessing
    print("\n" + "=" * 80)
    print("🧹 DATA PREPROCESSING")
    print("=" * 80)
    
    # Drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Drop missing labels
    initial_rows = len(df)
    df = df.dropna(subset=['prognosis'])
    dropped_rows = initial_rows - len(df)
    
    if dropped_rows > 0:
        print(f"⚠️  Dropped {dropped_rows} rows with missing prognosis")
    
    # Check for missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        print(f"⚠️  Found {missing_count} missing values - filling with 0")
        df = df.fillna(0)
    else:
        print(f"✓ No missing values found")
    
    # Prepare features and labels
    X = df.drop('prognosis', axis=1)
    y = df['prognosis']
    
    print(f"\n✓ Dataset prepared:")
    print(f"  Features: {X.shape[1]}")
    print(f"  Samples: {X.shape[0]}")
    print(f"  Target column: 'prognosis'")
    
    # Encode labels
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    print(f"\n✓ Label encoding completed:")
    print(f"  Unique diseases: {len(encoder.classes_)}")
    print(f"\nDisease distribution (top 15):")
    disease_counts = pd.Series(y).value_counts()
    for disease, count in disease_counts.head(15).items():
        print(f"    - {disease}: {count} samples")
    
    # Feature selection with multiple methods
    print("\n" + "=" * 80)
    print("🎯 ADVANCED FEATURE SELECTION")
    print("=" * 80)
    
    # Try multiple feature selection methods
    print("\n1️⃣  Chi-squared feature selection...")
    chi2_selector = SelectKBest(chi2, k=min(50, X.shape[1]))
    chi2_features = chi2_selector.fit_transform(X, y_encoded)
    chi2_feature_names = X.columns[chi2_selector.get_support()].tolist()
    
    print(f"   Selected {len(chi2_feature_names)} features:")
    for i, feat in enumerate(chi2_feature_names[:10], 1):
        print(f"     {i}. {feat}")
    if len(chi2_feature_names) > 10:
        print(f"     ... and {len(chi2_feature_names) - 10} more")
    
    print("\n2️⃣  Mutual information feature selection...")
    mi_selector = SelectKBest(mutual_info_classif, k=min(50, X.shape[1]))
    mi_features = mi_selector.fit_transform(X, y_encoded)
    mi_feature_names = X.columns[mi_selector.get_support()].tolist()
    
    # Combine both approaches - take union of top features
    combined_features = list(set(chi2_feature_names + mi_feature_names))
    print(f"   Combined selection: {len(combined_features)} unique features")
    
    # Use combined features for final preprocessing
    X_selected = X[chi2_feature_names]  # Use chi2 as primary
    selected_features = chi2_feature_names
    
    print(f"\n✓ Final feature set: {len(selected_features)} features")
    
    # Scale features
    print("\n" + "=" * 80)
    print("⚖️  FEATURE SCALING")
    print("=" * 80)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)
    print("✓ Features standardized using StandardScaler")
    
    # Split data
    print("\n" + "=" * 80)
    print("✂️  TRAIN-TEST SPLIT")
    print("=" * 80)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"✓ Data split completed:")
    print(f"  Training set: {X_train.shape[0]} samples ({100*X_train.shape[0]/(X_train.shape[0]+X_test.shape[0]):.1f}%)")
    print(f"  Testing set:  {X_test.shape[0]} samples ({100*X_test.shape[0]/(X_train.shape[0]+X_test.shape[0]):.1f}%)")
    
    # Define and train models
    print("\n" + "=" * 80)
    print("🤖 MODEL TRAINING AND HYPERPARAMETER TUNING")
    print("=" * 80)
    
    models = {
        'RandomForest': {
            'model': RandomForestClassifier(random_state=42, n_jobs=-1),
            'params': {
                'n_estimators': [100, 150, 200],
                'max_depth': [15, 20, 25],
                'min_samples_split': [5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        },
        'GradientBoosting': {
            'model': GradientBoostingClassifier(random_state=42),
            'params': {
                'n_estimators': [100, 150, 200],
                'learning_rate': [0.05, 0.1, 0.15],
                'max_depth': [5, 7, 10],
                'min_samples_split': [5, 10]
            }
        }
    }
    
    best_models = {}
    results = {}
    
    for model_name, config in models.items():
        print(f"\n{'▶️  ' + model_name.upper()}")
        print("-" * 80)
        
        # Grid search for best hyperparameters
        print(f"⏳ Performing grid search...")
        grid_search = GridSearchCV(
            config['model'],
            config['params'],
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            verbose=0
        )
        
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        best_models[model_name] = best_model
        
        print(f"✓ Best parameters found:")
        for param, value in grid_search.best_params_.items():
            print(f"    - {param}: {value}")
        print(f"  Best CV Score: {grid_search.best_score_:.4f}")
        
        # Evaluate on test set
        train_pred = best_model.predict(X_train)
        test_pred = best_model.predict(X_test)
        
        train_accuracy = accuracy_score(y_train, train_pred)
        test_accuracy = accuracy_score(y_test, test_pred)
        test_f1 = f1_score(y_test, test_pred, average='weighted')
        
        results[model_name] = {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'f1_score': test_f1,
            'model': best_model
        }
        
        print(f"\n📊 Performance:")
        print(f"  Training Accuracy: {train_accuracy:.4f} ({100*train_accuracy:.2f}%)")
        print(f"  Testing Accuracy:  {test_accuracy:.4f} ({100*test_accuracy:.2f}%)")
        print(f"  Weighted F1-Score: {test_f1:.4f}")
        
        # Cross-validation score
        cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='accuracy')
        print(f"  CV Scores: {[f'{s:.4f}' for s in cv_scores]}")
        print(f"  Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Select best model
    print("\n" + "=" * 80)
    print("🏆 MODEL SELECTION")
    print("=" * 80)
    
    best_model_name = max(results, key=lambda x: results[x]['test_accuracy'])
    best_model = best_models[best_model_name]
    best_accuracy = results[best_model_name]['test_accuracy']
    
    print(f"\n✓ Best Model: {best_model_name}")
    print(f"  Test Accuracy: {best_accuracy:.4f} ({100*best_accuracy:.2f}%)")
    print(f"  F1-Score: {results[best_model_name]['f1_score']:.4f}")
    
    # Detailed classification report
    test_pred = best_model.predict(X_test)
    print(f"\nDetailed Classification Report:")
    print(classification_report(y_test, test_pred, target_names=encoder.classes_, digits=4))
    
    # Save models
    print("\n" + "=" * 80)
    print("💾 SAVING MODELS")
    print("=" * 80)
    
    base_dir = os.path.dirname(__file__)
    
    model_path = os.path.join(base_dir, 'symptom_model.pkl')
    encoder_path = os.path.join(base_dir, 'symptom_encoder.pkl')
    features_path = os.path.join(base_dir, 'symptom_features.pkl')
    scaler_path = os.path.join(base_dir, 'symptom_scaler.pkl')
    
    joblib.dump(best_model, model_path)
    joblib.dump(encoder, encoder_path)
    joblib.dump(selected_features, features_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"✓ Model saved: {model_path}")
    print(f"✓ Encoder saved: {encoder_path}")
    print(f"✓ Features saved: {features_path}")
    print(f"✓ Scaler saved: {scaler_path}")
    
    print("\n" + "=" * 80)
    print("✅ TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\n📈 Summary:")
    print(f"  - Model: {best_model_name}")
    print(f"  - Training Samples: {X_train.shape[0]}")
    print(f"  - Features Used: {len(selected_features)}")
    print(f"  - Diseases Classified: {len(encoder.classes_)}")
    print(f"  - Test Accuracy: {100*best_accuracy:.2f}%")
    print(f"  - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

def test_model_prediction(symptoms_dict):
    """Test the trained model with sample symptoms"""
    print("\n" + "=" * 80)
    print("🧪 TESTING MODEL PREDICTION")
    print("=" * 80)
    
    try:
        base_dir = os.path.dirname(__file__)
        model = joblib.load(os.path.join(base_dir, 'symptom_model.pkl'))
        encoder = joblib.load(os.path.join(base_dir, 'symptom_encoder.pkl'))
        features = joblib.load(os.path.join(base_dir, 'symptom_features.pkl'))
        scaler = joblib.load(os.path.join(base_dir, 'symptom_scaler.pkl'))
        
        # Create feature vector
        feature_vector = np.array([[symptoms_dict.get(f, 0) for f in features]])
        
        # Scale
        feature_vector_scaled = scaler.transform(feature_vector)
        
        # Predict
        prediction = model.predict(feature_vector_scaled)[0]
        probabilities = model.predict_proba(feature_vector_scaled)[0]
        
        # Get top 5 predictions
        top_indices = np.argsort(probabilities)[-5:][::-1]
        
        print("✓ Prediction successful!")
        print(f"\nTop 5 predictions:")
        for i, idx in enumerate(top_indices, 1):
            disease = encoder.classes_[idx]
            confidence = probabilities[idx]
            print(f"  {i}. {disease}: {100*confidence:.2f}%")
        
        return encoder.classes_[prediction]
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return None

if __name__ == '__main__':
    # Train the model
    success = train_advanced_symptoms_model()
    
    if success:
        print("\n" + "=" * 80)
        print("Testing with sample data...")
        print("=" * 80)
        
        # Load data for testing
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'Training.csv')
        df = pd.read_csv(data_path)
        
        # Test with first few samples
        print("\nTesting with actual training data samples:")
        X = df.drop('prognosis', axis=1)
        
        for i in range(min(3, len(X))):
            sample = X.iloc[i].to_dict()
            actual_disease = df.iloc[i]['prognosis']
            print(f"\n📋 Sample {i+1}:")
            print(f"  Actual disease: {actual_disease}")
            predicted = test_model_prediction(sample)
            if predicted:
                print(f"  Predicted: {predicted}")
                print(f"  Match: {'✓ YES' if predicted == actual_disease else '✗ NO'}")
