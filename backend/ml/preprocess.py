import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import pickle
import os

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")

CATEGORICAL_OHE_COLS = [
    "Employment_Status", "Marital_Status", "Loan_Purpose",
    "Property_Area", "Gender", "Employer_Category"
]
LABEL_ENCODE_COLS = ["Education_Level"]
DROP_COLS         = ["Applicant_ID", "Loan_Approved"]
FEATURE_COLS      = None  # Set after fitting


def preprocess_training_data(df: pd.DataFrame):
    """
    Full preprocessing pipeline for training.
    Matches the notebook exactly:
    - Impute missing values
    - Label encode Education_Level
    - OHE categorical columns
    - Feature engineering (squared terms)
    - Drop raw Credit_Score and DTI_Ratio
    - Scale with StandardScaler
    Returns X_scaled, y, scaler, ohe, le, feature_columns
    """
    df = df.copy()

    # Drop ID
    if "Applicant_ID" in df.columns:
        df.drop("Applicant_ID", axis=1, inplace=True)

    # Impute
    num_cols = df.select_dtypes(include=["number"]).columns
    cat_cols = df.select_dtypes(include=["object"]).columns

    num_imp = SimpleImputer(strategy="mean")
    cat_imp = SimpleImputer(strategy="most_frequent")

    df[num_cols] = num_imp.fit_transform(df[num_cols])
    df[cat_cols] = cat_imp.fit_transform(df[cat_cols])

    # Label encode target + education
    le = LabelEncoder()
    df["Education_Level"] = le.fit_transform(df["Education_Level"])
    df["Loan_Approved"]   = le.fit_transform(df["Loan_Approved"])

    # OHE
    ohe = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
    encoded        = ohe.fit_transform(df[CATEGORICAL_OHE_COLS])
    encoded_df     = pd.DataFrame(encoded, columns=ohe.get_feature_names_out(CATEGORICAL_OHE_COLS), index=df.index)
    df             = pd.concat([df.drop(columns=CATEGORICAL_OHE_COLS), encoded_df], axis=1)

    # Feature engineering — squared terms
    df["DTI_Ratio_sq"]    = df["DTI_Ratio"] ** 2
    df["Credit_Score_sq"] = df["Credit_Score"] ** 2

    # Split X, y — drop raw Credit_Score and DTI_Ratio
    X = df.drop(columns=["Loan_Approved", "Credit_Score", "DTI_Ratio"])
    y = df["Loan_Approved"]

    feature_columns = list(X.columns)

    # Scale
    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, ohe, le, feature_columns


def preprocess_single(input_data: dict, scaler, ohe, feature_columns: list) -> np.ndarray:
    """
    Preprocess a single applicant dict for inference.
    input_data keys must match the original CSV column names.
    """
    df = pd.DataFrame([input_data])

    # Impute missing
    num_cols = df.select_dtypes(include=["number"]).columns
    cat_cols = df.select_dtypes(include=["object"]).columns

    for col in num_cols:
        df[col] = df[col].fillna(df[col].mean() if not df[col].isnull().all() else 0)
    for col in cat_cols:
        df[col] = df[col].fillna("Unknown")

    # Label encode Education_Level
    edu_map = {"Graduate": 1, "Not Graduate": 0}
    df["Education_Level"] = df["Education_Level"].map(edu_map).fillna(0)

    # OHE
    encoded    = ohe.transform(df[CATEGORICAL_OHE_COLS])
    encoded_df = pd.DataFrame(encoded, columns=ohe.get_feature_names_out(CATEGORICAL_OHE_COLS))
    df         = pd.concat([df.drop(columns=CATEGORICAL_OHE_COLS).reset_index(drop=True), encoded_df], axis=1)

    # Feature engineering
    df["DTI_Ratio_sq"]    = df["DTI_Ratio"] ** 2
    df["Credit_Score_sq"] = df["Credit_Score"] ** 2

    # Drop raw
    df = df.drop(columns=["Credit_Score", "DTI_Ratio"], errors="ignore")

    # Align columns
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_columns]

    return scaler.transform(df)
