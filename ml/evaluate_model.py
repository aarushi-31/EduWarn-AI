"""
Model Evaluation and Confusion Matrix Generation
Department of Computer Science & Engineering (AIML), JSS University, Noida
"""

import os
import sys
import joblib
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Headless backend for server/command-line execution
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.preprocessing import FEATURE_NAMES

def evaluate_saved_model():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, 'dataset', 'student_academic_data.csv')
    model_path = os.path.join(base_dir, 'models', 'best_student_model.joblib')
    output_plot_path = os.path.join(base_dir, 'models', 'confusion_matrix.png')

    if not os.path.exists(model_path):
        print(f"[ERROR] Model artifact not found at {model_path}. Run train_model.py first.")
        return

    print(f"[INFO] Loading serialized ML pipeline from {model_path}...")
    pipeline = joblib.load(model_path)

    df = pd.read_csv(data_path)
    X = df[FEATURE_NAMES]
    y = df['risk_category']

    # Use the same stratified test split (20%, random_state=42)
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    y_pred = pipeline.predict(X_test)

    print("\n" + "="*60)
    print("CLASSIFICATION EVALUATION REPORT")
    print("="*60)
    report = classification_report(y_test, y_pred, target_names=['High', 'Low', 'Medium'], digits=4)
    print(report)

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, labels=['High', 'Medium', 'Low'])
    print("="*60)
    print("CONFUSION MATRIX:")
    header_label = "True \\ Pred"
    print(f"{header_label:<12} | {'High':<8} | {'Medium':<8} | {'Low':<8}")
    print("-" * 42)
    for i, label in enumerate(['High', 'Medium', 'Low']):
        print(f"{label:<12} | {cm[i][0]:<8} | {cm[i][1]:<8} | {cm[i][2]:<8}")
    print("="*60)

    # Plot Confusion Matrix
    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['High', 'Medium', 'Low'])
    disp.plot(cmap='Blues', ax=ax, values_format='d')
    plt.title("Confusion Matrix - Student Risk Prediction", fontsize=12, pad=12)
    plt.tight_layout()
    plt.savefig(output_plot_path, dpi=200)
    plt.close()
    print(f"[SUCCESS] Confusion matrix plot saved to: {output_plot_path}\n")

if __name__ == '__main__':
    evaluate_saved_model()
