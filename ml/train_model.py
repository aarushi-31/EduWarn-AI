"""
Model Training & Comparison Script
Department of Computer Science & Engineering (AIML), JSS University, Noida

Compares Logistic Regression, Decision Tree, and Random Forest.
Selects best performing model, saves serialized pipeline artifact, and registers in database.
"""

import os
import sys
import joblib
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Ensure root directory is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.preprocessing import FEATURE_NAMES, create_preprocessing_pipeline
from app.db import get_session
from app.models import MLModel

def train_and_evaluate():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, 'dataset', 'student_academic_data.csv')
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    saved_model_path = os.path.join(models_dir, 'best_student_model.joblib')

    if not os.path.exists(data_path):
        from ml.dataset.generate_dataset import generate_academic_dataset
        df = generate_academic_dataset()
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)

    X = df[FEATURE_NAMES]
    y = df['risk_category']

    # 80-20 Train-Test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    candidate_classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    }

    results = []
    trained_pipelines = {}

    print("\n" + "="*70)
    print("MACHINE LEARNING MODEL COMPARISON & TRAINING")
    print("="*70)
    print(f"Dataset Size: {len(df)} samples | Features: {len(FEATURE_NAMES)}")
    print(f"Training Samples: {len(X_train)} | Test Samples: {len(X_test)}")
    print("-" * 70)
    print(f"{'Algorithm':<22} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 70)

    for name, clf in candidate_classifiers.items():
        pipe = Pipeline([
            ('preprocessor', create_preprocessing_pipeline()),
            ('classifier', clf)
        ])
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='macro', zero_division=0)
        rec = recall_score(y_test, y_pred, average='macro', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)

        results.append({
            'algorithm': name,
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'pipeline': pipe
        })
        trained_pipelines[name] = pipe

        print(f"{name:<22} | {acc*100:>8.2f}% | {prec*100:>8.2f}% | {rec*100:>8.2f}% | {f1*100:>8.2f}%")

    print("="*70)

    # Select best model by F1-score
    best = max(results, key=lambda x: x['f1_score'])
    print(f"\n[SELECTION] Best Performing Model: {best['algorithm']}")
    print(f"            Accuracy: {best['accuracy']*100:.2f}% | Macro F1: {best['f1_score']*100:.2f}%")

    # Serialize best pipeline artifact
    joblib.dump(best['pipeline'], saved_model_path)
    print(f"[SAVED] Persisted model artifact to: {saved_model_path}")

    # Register in SQLite database table ml_models
    try:
        session = get_session()
        # Create record
        model_version = "v1.0.0"
        ml_record = MLModel(
            algorithm=best['algorithm'],
            version=model_version,
            accuracy=round(float(best['accuracy']), 4),
            f1_score=round(float(best['f1_score']), 4),
            trained_on=datetime.utcnow()
        )
        session.add(ml_record)
        session.commit()
        print(f"[DATABASE] Registered model in 'ml_models' table (ID: {ml_record.model_id}, Version: {model_version})")
    except Exception as e:
        print(f"[WARNING] Could not log model metadata to database: {e}")

    return best

if __name__ == '__main__':
    train_and_evaluate()
