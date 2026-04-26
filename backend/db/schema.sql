-- ============================================================
--  LoanSenseAI — schema.sql
--  Run this FIRST. Creates all tables in dependency order.
-- ============================================================

-- Drop tables if re-running (safe for dev)
DROP TABLE IF EXISTS audit_log          CASCADE;
DROP TABLE IF EXISTS rag_explanations   CASCADE;
DROP TABLE IF EXISTS ml_predictions     CASCADE;
DROP TABLE IF EXISTS loan_applications  CASCADE;
DROP TABLE IF EXISTS financial_profile  CASCADE;
DROP TABLE IF EXISTS employment         CASCADE;
DROP TABLE IF EXISTS applicants         CASCADE;
DROP TABLE IF EXISTS bank_managers      CASCADE;
DROP TABLE IF EXISTS loan_purposes      CASCADE;
DROP TABLE IF EXISTS property_areas     CASCADE;
DROP TABLE IF EXISTS employer_categories CASCADE;

-- ─── Lookup / reference tables ───────────────────────────────

CREATE TABLE property_areas (
    area_id     SERIAL      PRIMARY KEY,
    area_type   VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE employer_categories (
    category_id   SERIAL      PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE loan_purposes (
    purpose_id   SERIAL      PRIMARY KEY,
    purpose_name VARCHAR(50) NOT NULL UNIQUE
);

-- ─── Core entity tables ───────────────────────────────────────

CREATE TABLE applicants (
    applicant_id    SERIAL          PRIMARY KEY,
    first_name      VARCHAR(50)     NOT NULL,
    last_name       VARCHAR(50)     NOT NULL,
    age             SMALLINT        NOT NULL,
    gender          VARCHAR(10),
    marital_status  VARCHAR(20),
    dependents      SMALLINT        NOT NULL DEFAULT 0,
    education_level VARCHAR(20),
    area_id         INT             REFERENCES property_areas(area_id),
    category_id     INT             REFERENCES employer_categories(category_id),
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE TABLE employment (
    employment_id       SERIAL      PRIMARY KEY,
    applicant_id        INT         NOT NULL REFERENCES applicants(applicant_id) ON DELETE CASCADE,
    employment_status   VARCHAR(20) NOT NULL,
    applicant_income    NUMERIC(12,2) NOT NULL DEFAULT 0,
    coapplicant_income  NUMERIC(12,2) NOT NULL DEFAULT 0
);

CREATE TABLE financial_profile (
    profile_id        SERIAL        PRIMARY KEY,
    applicant_id      INT           NOT NULL REFERENCES applicants(applicant_id) ON DELETE CASCADE,
    credit_score      SMALLINT      NOT NULL,
    existing_loans    SMALLINT      NOT NULL DEFAULT 0,
    dti_ratio         NUMERIC(5,2),
    savings           NUMERIC(12,2),
    collateral_value  NUMERIC(12,2)
);

-- ─── Loan tables ──────────────────────────────────────────────

CREATE TABLE loan_applications (
    application_id  SERIAL        PRIMARY KEY,
    applicant_id    INT           NOT NULL REFERENCES applicants(applicant_id) ON DELETE CASCADE,
    purpose_id      INT           REFERENCES loan_purposes(purpose_id),
    loan_amount     NUMERIC(12,2) NOT NULL,
    loan_term       SMALLINT,                          -- in months
    status          VARCHAR(20)   NOT NULL DEFAULT 'Pending',
    applied_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    reviewed_at     TIMESTAMPTZ
);

-- ─── ML & RAG tables ─────────────────────────────────────────

CREATE TABLE ml_predictions (
    prediction_id   SERIAL        PRIMARY KEY,
    application_id  INT           NOT NULL REFERENCES loan_applications(application_id) ON DELETE CASCADE,
    approved        BOOLEAN       NOT NULL,
    confidence      NUMERIC(5,4)  NOT NULL,            -- e.g. 0.8712
    model_version   VARCHAR(30)   NOT NULL DEFAULT 'v1.0',
    predicted_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE TABLE rag_explanations (
    explanation_id    SERIAL      PRIMARY KEY,
    prediction_id     INT         NOT NULL REFERENCES ml_predictions(prediction_id) ON DELETE CASCADE,
    reasoning_text    TEXT        NOT NULL,
    retrieved_context TEXT,
    generated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─── Bank manager & audit tables ─────────────────────────────

CREATE TABLE bank_managers (
    manager_id      SERIAL        PRIMARY KEY,
    username        VARCHAR(50)   NOT NULL UNIQUE,
    password_hash   TEXT          NOT NULL,
    full_name       VARCHAR(100)  NOT NULL,
    is_active       BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE TABLE audit_log (
    log_id          SERIAL        PRIMARY KEY,
    application_id  INT           NOT NULL REFERENCES loan_applications(application_id) ON DELETE CASCADE,
    manager_id      INT           REFERENCES bank_managers(manager_id),
    old_status      VARCHAR(20),
    new_status      VARCHAR(20)   NOT NULL,
    changed_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    change_note     TEXT
);
