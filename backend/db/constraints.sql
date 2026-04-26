-- ============================================================
--  LoanSenseAI — constraints.sql
--  Run AFTER schema.sql. Adds CHECK, UNIQUE constraints.
-- ============================================================

-- ─── applicants ──────────────────────────────────────────────
ALTER TABLE applicants
    ADD CONSTRAINT chk_age
        CHECK (age BETWEEN 18 AND 75),
    ADD CONSTRAINT chk_gender
        CHECK (gender IN ('Male', 'Female', 'Other')),
    ADD CONSTRAINT chk_marital_status
        CHECK (marital_status IN ('Married', 'Single', 'Divorced', 'Widowed')),
    ADD CONSTRAINT chk_dependents
        CHECK (dependents >= 0),
    ADD CONSTRAINT chk_education
        CHECK (education_level IN ('Graduate', 'Not Graduate'));

-- ─── employment ──────────────────────────────────────────────
ALTER TABLE employment
    ADD CONSTRAINT chk_employment_status
        CHECK (employment_status IN ('Salaried', 'Self-employed', 'Contract', 'Unemployed')),
    ADD CONSTRAINT chk_applicant_income
        CHECK (applicant_income >= 0),
    ADD CONSTRAINT chk_coapplicant_income
        CHECK (coapplicant_income >= 0);

-- ─── financial_profile ───────────────────────────────────────
ALTER TABLE financial_profile
    ADD CONSTRAINT chk_credit_score
        CHECK (credit_score BETWEEN 300 AND 900),
    ADD CONSTRAINT chk_existing_loans
        CHECK (existing_loans >= 0),
    ADD CONSTRAINT chk_dti_ratio
        CHECK (dti_ratio IS NULL OR dti_ratio BETWEEN 0 AND 5),
    ADD CONSTRAINT chk_savings
        CHECK (savings IS NULL OR savings >= 0),
    ADD CONSTRAINT chk_collateral_value
        CHECK (collateral_value IS NULL OR collateral_value >= 0);

-- ─── loan_applications ───────────────────────────────────────
ALTER TABLE loan_applications
    ADD CONSTRAINT chk_loan_amount
        CHECK (loan_amount > 0),
    ADD CONSTRAINT chk_loan_term
        CHECK (loan_term IS NULL OR loan_term IN (12, 24, 36, 48, 60, 72, 84, 120, 180, 240, 360)),
    ADD CONSTRAINT chk_loan_status
        CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Under Review'));

-- ─── ml_predictions ──────────────────────────────────────────
ALTER TABLE ml_predictions
    ADD CONSTRAINT chk_confidence
        CHECK (confidence BETWEEN 0 AND 1);

-- ─── loan_purposes (no duplicate purpose names) ──────────────
ALTER TABLE loan_purposes
    ADD CONSTRAINT uq_purpose_name UNIQUE (purpose_name);

-- ─── property_areas (no duplicate area types) ────────────────
ALTER TABLE property_areas
    ADD CONSTRAINT uq_area_type UNIQUE (area_type);

-- ─── employer_categories (no duplicate category names) ───────
ALTER TABLE employer_categories
    ADD CONSTRAINT uq_category_name UNIQUE (category_name);
