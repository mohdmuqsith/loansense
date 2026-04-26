-- ============================================================
--  LoanSenseAI — rbac.sql
--  Role-Based Access Control.
--  Run AFTER schema.sql. Adjust role passwords before production.
-- ============================================================

-- ─── Create roles (ignore error if they already exist) ───────
DO $$ BEGIN
    CREATE ROLE bank_manager_role;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE ROLE ml_service_role;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE ROLE readonly_analyst_role;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;


-- ─── bank_manager_role ───────────────────────────────────────
-- Can view all data, update loan statuses, insert audit logs.
-- Cannot delete reviewed applications (enforced by trigger too).
GRANT SELECT, INSERT, UPDATE ON
    applicants,
    employment,
    financial_profile,
    loan_applications,
    loan_purposes,
    property_areas,
    employer_categories,
    audit_log,
    bank_managers
TO bank_manager_role;

GRANT SELECT ON
    ml_predictions,
    rag_explanations
TO bank_manager_role;

-- Access to views
GRANT SELECT ON
    loan_summary_view,
    approval_stats_view,
    manager_activity_view
TO bank_manager_role;

-- Access to sequences (needed for INSERT)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO bank_manager_role;


-- ─── ml_service_role ─────────────────────────────────────────
-- The Python ML service only needs to insert predictions and RAG explanations.
GRANT SELECT ON loan_applications, applicants, employment, financial_profile TO ml_service_role;
GRANT INSERT ON ml_predictions, rag_explanations TO ml_service_role;
GRANT USAGE, SELECT ON SEQUENCE ml_predictions_prediction_id_seq  TO ml_service_role;
GRANT USAGE, SELECT ON SEQUENCE rag_explanations_explanation_id_seq TO ml_service_role;


-- ─── readonly_analyst_role ───────────────────────────────────
-- Read-only access to views only (for BI / reporting tools).
GRANT SELECT ON
    loan_summary_view,
    approval_stats_view,
    manager_activity_view
TO readonly_analyst_role;


-- ─── Create login users and assign roles ─────────────────────
-- Change passwords before deploying!

DO $$ BEGIN
    CREATE USER app_manager WITH PASSWORD 'change_me_manager';
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
GRANT bank_manager_role TO app_manager;

DO $$ BEGIN
    CREATE USER app_ml WITH PASSWORD 'change_me_ml';
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
GRANT ml_service_role TO app_ml;

DO $$ BEGIN
    CREATE USER app_analyst WITH PASSWORD 'change_me_analyst';
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
GRANT readonly_analyst_role TO app_analyst;
