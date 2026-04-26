import pickle
import os
import numpy as np
from ml.preprocess import preprocess_single

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")

# Load artifacts once at module level
def _load(filename):
    path = os.path.join(ARTIFACTS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Artifact not found: {path}. Run ml/train.py first.")
    with open(path, "rb") as f:
        return pickle.load(f)

model           = _load("loan_model.pkl")
scaler          = _load("scaler.pkl")
ohe             = _load("ohe.pkl")
feature_columns = _load("feature_columns.pkl")


def predict(applicant_data: dict) -> dict:
    """
    Takes a dict of applicant features (matching CSV column names),
    returns prediction result with approval decision and confidence.

    Returns:
        {
            "approved": bool,
            "confidence": float,       # probability of predicted class
            "approval_probability": float,  # P(approved=Yes)
            "model_version": str
        }
    """
    X = preprocess_single(applicant_data, scaler, ohe, feature_columns)

    probs      = model.predict_proba(X)[0]   # [P(No), P(Yes)]
    prediction = model.predict(X)[0]         # 0 or 1

    approved             = bool(prediction == 1)
    approval_probability = float(probs[1])
    confidence           = float(np.max(probs))

    return {
        "approved":             approved,
        "confidence":           round(confidence, 4),
        "approval_probability": round(approval_probability, 4),
        "model_version":        "v1.0"
    }
