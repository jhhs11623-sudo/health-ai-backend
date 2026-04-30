import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_selection import SelectKBest, chi2
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def train_advanced_symptom_model():
    print("🚀 Advanced Symptom Model Training with Multiple Algorithms...")

    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'Training.csv')
    df = pd.read_csv(data_path)

    print(f"📊 Data loaded. Shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    print(f"Sample columns: {list(df.columns[:10])}...")

    # Data cleaning and preprocessing
    print("\n🧹 Data Preprocessing...")

    # Drop unnamed columns and missing labels
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(subset=['prognosis'])

    # Check for missing values
    missing_values = df.isnull().sum()
    print(f"Missing values per column: {missing_values[missing_values > 0]}")

    # Fill missing values with 0 (symptoms not present)
    df = df.fillna(0)

    # Prepare features and labels
    X = df.drop('prognosis', axis=1)
    y = df['prognosis']

    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")

    # Encode labels
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    print(f"Unique diseases: {len(encoder.classes_)}")
    print("Disease distribution:")
    disease_counts = pd.Series(y).value_counts()
    print(disease_counts.head(10))

    # Feature selection
    print("\n🎯 Feature Selection...")
    selector = SelectKBest(chi2, k=min(100, X.shape[1]))  # Select top 100 features
    X_selected = selector.fit_transform(X, y_encoded)
    selected_features = X.columns[selector.get_support()].tolist()

    print(f"Selected {len(selected_features)} features out of {X.shape[1]}")
    print(f"Top 10 features: {selected_features[:10]}")

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    print(f"Train set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    # Define models to compare
    models = {
        'RandomForest': RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ),
        'GradientBoosting': GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=10,
            random_state=42
        ),
        'SVM': SVC(
            kernel='rbf',
            C=1.0,
            gamma='scale',
            probability=True,
            random_state=42
        )
    }

    # Train and evaluate models
    results = {}
    best_model = None
    best_accuracy = 0

    for name, model in models.items():
        print(f"\n🏃 Training {name}...")

        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        print(".4f")

        # Train on full training set
        model.fit(X_train, y_train)

        # Evaluate on test set
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(".4f")
        print(f"\n{name} Classification Report:")
        print(classification_report(y_test, y_pred, target_names=encoder.classes_))

        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_scores': cv_scores,
            'predictions': y_pred
        }

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_model_name = name

    # Plot results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Accuracy comparison
    plt.figure(figsize=(10, 6))
    model_names = list(results.keys())
    accuracies = [results[name]['accuracy'] for name in model_names]
    cv_means = [results[name]['cv_scores'].mean() for name in model_names]

    x = np.arange(len(model_names))
    width = 0.35

    plt.bar(x - width/2, accuracies, width, label='Test Accuracy', alpha=0.8)
    plt.bar(x + width/2, cv_means, width, label='CV Accuracy', alpha=0.8)

    plt.xlabel('Models')
    plt.ylabel('Accuracy')
    plt.title('Model Comparison - Symptom Prediction')
    plt.xticks(x, model_names)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f'symptom_model_comparison_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Confusion matrix for best model
    plt.figure(figsize=(12, 10))
    cm = confusion_matrix(y_test, results[best_model_name]['predictions'])
    # Create a simplified confusion matrix for visualization (too many classes)
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(f'{best_model_name} - Confusion Matrix (Simplified)')
    plt.colorbar()
    plt.savefig(f'symptom_confusion_matrix_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Feature importance (for tree-based models)
    if hasattr(best_model, 'feature_importances_'):
        plt.figure(figsize=(12, 8))
        feature_importance = best_model.feature_importances_
        top_features = np.argsort(feature_importance)[-20:]  # Top 20 features

        plt.barh(range(len(top_features)), feature_importance[top_features])
        plt.yticks(range(len(top_features)), [selected_features[i] for i in top_features])
        plt.xlabel('Feature Importance')
        plt.title(f'{best_model_name} - Top 20 Feature Importances')
        plt.tight_layout()
        plt.savefig(f'symptom_feature_importance_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()

    # Save the best model and preprocessing objects
    backend_dir = os.path.dirname(__file__)

    joblib.dump(best_model, os.path.join(backend_dir, 'symptom_model.pkl'))
    joblib.dump(encoder, os.path.join(backend_dir, 'symptom_encoder.pkl'))
    joblib.dump(selected_features, os.path.join(backend_dir, 'symptom_features.pkl'))
    joblib.dump(scaler, os.path.join(backend_dir, 'symptom_scaler.pkl'))
    joblib.dump(selector, os.path.join(backend_dir, 'symptom_selector.pkl'))

    # Save training results
    results_summary = {
        'best_model': best_model_name,
        'accuracy': best_accuracy,
        'cv_mean': results[best_model_name]['cv_scores'].mean(),
        'cv_std': results[best_model_name]['cv_scores'].std(),
        'all_results': {name: results[name]['accuracy'] for name in results.keys()},
        'timestamp': timestamp,
        'data_shape': df.shape,
        'n_features_selected': len(selected_features),
        'n_classes': len(encoder.classes_)
    }

    import json
    with open(os.path.join(backend_dir, 'symptom_training_results.json'), 'w') as f:
        json.dump(results_summary, f, indent=2, default=str)

    print("\n✅ Training completed!")
    print(f"🏆 Best Model: {best_model_name}")
    print(".4f")
    print(".4f")
    print(f"📁 Models saved in: {backend_dir}")
    print(f"📊 Results saved as: symptom_training_results.json")

    return best_model, encoder, selected_features, scaler

if __name__ == "__main__":
    train_advanced_symptom_model()

    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=encoder.classes_))

if __name__ == '__main__':
    train_symptom_model()