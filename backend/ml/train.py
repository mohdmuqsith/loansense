import pandas as pd
#import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from xgboost import XGBClassifier
from ml.preprocess import preprocess_training_data

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
DATA_PATH     = os.path.join(os.path.dirname(__file__), "../../data/loan_data.csv")


def train():
    print("📂 Loading data...")
    df = pd.read_csv(DATA_PATH)
    print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")

    print("⚙️  Preprocessing...")
    X_scaled, y, scaler, ohe, le, feature_columns = preprocess_training_data(df)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    print("🚀 Training XGBoost model...")
    model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("\n📊 Model Evaluation:")
    print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"   Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"   Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"   F1 Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"   Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

    # Save artifacts
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    with open(os.path.join(ARTIFACTS_DIR, "loan_model.pkl"), "wb") as f:
        pickle.dump(model, f)

    with open(os.path.join(ARTIFACTS_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    with open(os.path.join(ARTIFACTS_DIR, "ohe.pkl"), "wb") as f:
        pickle.dump(ohe, f)

    with open(os.path.join(ARTIFACTS_DIR, "feature_columns.pkl"), "wb") as f:
        pickle.dump(feature_columns, f)

    print(f"\n✅ Artifacts saved to {ARTIFACTS_DIR}")
    return model, scaler, ohe, feature_columns


if __name__ == "__main__":
    train()
