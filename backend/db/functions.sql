-- ============================================================
--  LoanSenseAI — functions.sql
--  Reusable SQL functions called by the app or procedures.
-- ============================================================

-- ─── 1. calculate_dti ────────────────────────────────────────
-- Debt-to-Income ratio = monthly loan payment / total monthly income
-- monthly_payment uses simple amortisation formula
CREATE OR REPLACE FUNCTION calculate_dti(
    p_applicant_income   NUMERIC,
    p_coapplicant_income NUMERIC,
    p_loan_amount        NUMERIC,
    p_loan_term_months   INT
)
RETURNS NUMERIC AS $$
DECLARE
    v_total_income   NUMERIC;
    v_monthly_payment NUMERIC;
BEGIN
    v_total_income := COALESCE(p_applicant_income, 0) + COALESCE(p_coapplicant_income, 0);

    IF v_total_income = 0 OR p_loan_term_months IS NULL OR p_loan_term_months = 0 THEN
        RETURN NULL;
    END IF;

    v_monthly_payment := p_loan_amount / p_loan_term_months;

    RETURN ROUND(v_monthly_payment / v_total_income, 4);
END;
$$ LANGUAGE plpgsql IMMUTABLE;


-- ─── 2. get_approval_rate ────────────────────────────────────
-- Returns approval % for a given property area type
CREATE OR REPLACE FUNCTION get_approval_rate(p_area_type VARCHAR)
RETURNS NUMERIC AS $$
DECLARE
    v_total    INT;
    v_approved INT;
BEGIN
    SELECT COUNT(*)
    INTO v_total
    FROM loan_applications la
    JOIN applicants a       ON a.applicant_id = la.applicant_id
    JOIN property_areas pa  ON pa.area_id     = a.area_id
    WHERE pa.area_type = p_area_type;

    IF v_total = 0 THEN RETURN 0; END IF;

    SELECT COUNT(*)
    INTO v_approved
    FROM loan_applications la
    JOIN applicants a       ON a.applicant_id = la.applicant_id
    JOIN property_areas pa  ON pa.area_id     = a.area_id
    WHERE pa.area_type = p_area_type
      AND la.status = 'Approved';

    RETURN ROUND((v_approved::NUMERIC / v_total) * 100, 2);
END;
$$ LANGUAGE plpgsql STABLE;


-- ─── 3. applicant_risk_score ─────────────────────────────────
-- Returns a simple integer risk score (0 = low risk, 100 = high risk)
-- Used as a quick heuristic before ML model runs
CREATE OR REPLACE FUNCTION applicant_risk_score(p_applicant_id INT)
RETURNS INT AS $$
DECLARE
    v_credit_score    SMALLINT;
    v_dti_ratio       NUMERIC;
    v_existing_loans  SMALLINT;
    v_risk            INT := 0;
BEGIN
    SELECT fp.credit_score, fp.dti_ratio, fp.existing_loans
    INTO v_credit_score, v_dti_ratio, v_existing_loans
    FROM financial_profile fp
    WHERE fp.applicant_id = p_applicant_id;

    IF NOT FOUND THEN RETURN NULL; END IF;

    -- Credit score contribution (lower score → higher risk)
    IF v_credit_score < 580 THEN v_risk := v_risk + 40;
    ELSIF v_credit_score < 670 THEN v_risk := v_risk + 20;
    ELSIF v_credit_score < 740 THEN v_risk := v_risk + 10;
    END IF;

    -- DTI contribution
    IF v_dti_ratio > 0.50 THEN v_risk := v_risk + 30;
    ELSIF v_dti_ratio > 0.35 THEN v_risk := v_risk + 15;
    END IF;

    -- Existing loans contribution
    IF v_existing_loans >= 4 THEN v_risk := v_risk + 30;
    ELSIF v_existing_loans >= 2 THEN v_risk := v_risk + 15;
    END IF;

    RETURN LEAST(v_risk, 100);
END;
$$ LANGUAGE plpgsql STABLE;


-- ─── 4. pending_applications_count ──────────────────────────
-- Returns how many applications are still Pending
CREATE OR REPLACE FUNCTION pending_applications_count()
RETURNS INT AS $$
    SELECT COUNT(*)::INT FROM loan_applications WHERE status = 'Pending';
$$ LANGUAGE sql STABLE;
