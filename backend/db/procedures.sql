-- ============================================================
--  LoanSenseAI — procedures.sql
--  Stored procedures for multi-step transactional operations.
-- ============================================================
 
-- ─── 1. submit_application ───────────────────────────────────
-- Submits a complete loan application in one atomic transaction.
-- Creates applicant + employment + financial_profile + loan_application
CREATE OR REPLACE PROCEDURE submit_application(
    -- Applicant fields
    p_first_name        VARCHAR,
    p_last_name         VARCHAR,
    p_age               SMALLINT,
    p_gender            VARCHAR,
    p_marital_status    VARCHAR,
    p_dependents        SMALLINT,
    p_education_level   VARCHAR,
    p_area_type         VARCHAR,
    p_employer_category VARCHAR,
    -- Employment fields
    p_employment_status VARCHAR,
    p_applicant_income  NUMERIC,
    p_coapplicant_income NUMERIC,
    -- Financial fields
    p_credit_score      SMALLINT,
    p_existing_loans    SMALLINT,
    p_dti_ratio         NUMERIC,
    p_savings           NUMERIC,
    p_collateral_value  NUMERIC,
    -- Loan fields
    p_loan_purpose      VARCHAR,
    p_loan_amount       NUMERIC,
    p_loan_term         SMALLINT,
    -- OUT: newly created application_id
    OUT p_application_id INT
)
LANGUAGE plpgsql AS $$
DECLARE
    v_applicant_id  INT;
    v_area_id       INT;
    v_category_id   INT;
    v_purpose_id    INT;
BEGIN
    -- Resolve FK lookups
    SELECT area_id     INTO v_area_id     FROM property_areas       WHERE area_type     = p_area_type;
    SELECT category_id INTO v_category_id FROM employer_categories  WHERE category_name = p_employer_category;
    SELECT purpose_id  INTO v_purpose_id  FROM loan_purposes         WHERE purpose_name  = p_loan_purpose;
 
    -- Insert applicant
    INSERT INTO applicants (
        first_name, last_name, age, gender, marital_status,
        dependents, education_level, area_id, category_id
    ) VALUES (
        p_first_name, p_last_name, p_age, p_gender, p_marital_status,
        p_dependents, p_education_level, v_area_id, v_category_id
    ) RETURNING applicant_id INTO v_applicant_id;
 
    -- Insert employment
    INSERT INTO employment (applicant_id, employment_status, applicant_income, coapplicant_income)
    VALUES (v_applicant_id, p_employment_status, p_applicant_income, p_coapplicant_income);
 
    -- Insert financial profile
    INSERT INTO financial_profile (
        applicant_id, credit_score, existing_loans,
        dti_ratio, savings, collateral_value
    ) VALUES (
        v_applicant_id, p_credit_score, p_existing_loans,
        p_dti_ratio, p_savings, p_collateral_value
    );
 
    -- Insert loan application
    INSERT INTO loan_applications (applicant_id, purpose_id, loan_amount, loan_term, status)
    VALUES (v_applicant_id, v_purpose_id, p_loan_amount, p_loan_term, 'Pending')
    RETURNING application_id INTO p_application_id;
 
    -- First audit log entry
    INSERT INTO audit_log (application_id, old_status, new_status, change_note)
    VALUES (p_application_id, NULL, 'Pending', 'Application submitted');
 
EXCEPTION WHEN OTHERS THEN
    RAISE;   -- re-raise so the caller sees the error; transaction rolls back automatically
END;
$$;
 
 
-- ─── 2. review_application ───────────────────────────────────
-- Manager approves or rejects an application with an optional note
CREATE OR REPLACE PROCEDURE review_application(
    p_application_id INT,
    p_manager_id     INT,
    p_new_status     VARCHAR,   -- 'Approved' or 'Rejected'
    p_note           TEXT DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_new_status NOT IN ('Approved', 'Rejected', 'Under Review') THEN
        RAISE EXCEPTION 'Invalid status: %. Must be Approved, Rejected, or Under Review.', p_new_status;
    END IF;
 
    -- Set app context so the audit trigger can capture manager_id
    PERFORM set_config('app.current_manager_id', p_manager_id::TEXT, TRUE);
 
    UPDATE loan_applications
    SET status = p_new_status
    WHERE application_id = p_application_id;
 
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Application % not found.', p_application_id;
    END IF;
 
    -- Update note in the audit log row just inserted by trigger
    UPDATE audit_log
    SET change_note = COALESCE(p_note, 'Reviewed by manager')
    WHERE log_id = (
        SELECT log_id FROM audit_log
        WHERE application_id = p_application_id
          AND manager_id = p_manager_id
        ORDER BY changed_at DESC
        LIMIT 1
    );
END;
$$;
