-- ============================================================
--  LoanSenseAI — views.sql
--  Pre-joined views used by the frontend dashboard.
-- ============================================================

-- ─── 1. loan_summary_view ────────────────────────────────────
-- Flat view for the dashboard table — one row per application
CREATE OR REPLACE VIEW loan_summary_view AS
SELECT
    la.application_id,
    la.applied_at,
    la.reviewed_at,
    la.status,
    la.loan_amount,
    la.loan_term,

    -- Applicant info
    a.applicant_id,
    a.first_name || ' ' || a.last_name   AS full_name,
    a.age,
    a.gender,
    a.marital_status,
    a.dependents,
    a.education_level,

    -- Area & category
    pa.area_type,
    ec.category_name                     AS employer_category,

    -- Employment
    e.employment_status,
    e.applicant_income,
    e.coapplicant_income,
    (e.applicant_income + e.coapplicant_income) AS total_income,

    -- Financial profile
    fp.credit_score,
    fp.existing_loans,
    fp.dti_ratio,
    fp.savings,
    fp.collateral_value,

    -- Loan purpose
    lp.purpose_name                      AS loan_purpose,

    -- Latest ML prediction
    mp.approved                          AS ml_approved,
    mp.confidence                        AS ml_confidence,
    mp.model_version

FROM loan_applications la
JOIN applicants          a   ON a.applicant_id  = la.applicant_id
LEFT JOIN property_areas pa  ON pa.area_id      = a.area_id
LEFT JOIN employer_categories ec ON ec.category_id = a.category_id
LEFT JOIN employment     e   ON e.applicant_id  = a.applicant_id
LEFT JOIN financial_profile fp ON fp.applicant_id = a.applicant_id
LEFT JOIN loan_purposes  lp  ON lp.purpose_id   = la.purpose_id
LEFT JOIN LATERAL (
    SELECT approved, confidence, model_version
    FROM ml_predictions
    WHERE application_id = la.application_id
    ORDER BY predicted_at DESC
    LIMIT 1
) mp ON TRUE;


-- ─── 2. approval_stats_view ──────────────────────────────────
-- Aggregated stats per status for charts
CREATE OR REPLACE VIEW approval_stats_view AS
SELECT
    status,
    COUNT(*)                                     AS total,
    ROUND(AVG(loan_amount), 2)                   AS avg_loan_amount,
    ROUND(AVG(fp.credit_score), 2)               AS avg_credit_score,
    ROUND(AVG(fp.dti_ratio), 4)                  AS avg_dti_ratio
FROM loan_applications la
JOIN applicants a              ON a.applicant_id  = la.applicant_id
LEFT JOIN financial_profile fp ON fp.applicant_id = a.applicant_id
GROUP BY status;


-- ─── 3. manager_activity_view ────────────────────────────────
-- Shows how many reviews each manager has performed
CREATE OR REPLACE VIEW manager_activity_view AS
SELECT
    bm.manager_id,
    bm.full_name,
    bm.username,
    COUNT(al.log_id)                    AS total_reviews,
    MAX(al.changed_at)                  AS last_activity
FROM bank_managers bm
LEFT JOIN audit_log al ON al.manager_id = bm.manager_id
GROUP BY bm.manager_id, bm.full_name, bm.username;
