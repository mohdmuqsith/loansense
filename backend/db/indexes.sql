-- ============================================================
--  LoanSenseAI — indexes.sql
--  Run AFTER schema.sql. Optimises common query patterns.
-- ============================================================

-- ─── applicants ──────────────────────────────────────────────
-- Filter applicants by area or employer category
CREATE INDEX idx_applicants_area_id     ON applicants(area_id);
CREATE INDEX idx_applicants_category_id ON applicants(category_id);

-- ─── employment ──────────────────────────────────────────────
-- Join employment back to applicant
CREATE INDEX idx_employment_applicant_id ON employment(applicant_id);

-- ─── financial_profile ───────────────────────────────────────
-- Join financial profile back to applicant
CREATE INDEX idx_financial_profile_applicant_id ON financial_profile(applicant_id);

-- ─── loan_applications ───────────────────────────────────────
-- Most common dashboard filters: by applicant, status, date
CREATE INDEX idx_loan_applications_applicant_id ON loan_applications(applicant_id);
CREATE INDEX idx_loan_applications_status       ON loan_applications(status);
CREATE INDEX idx_loan_applications_applied_at   ON loan_applications(applied_at DESC);
CREATE INDEX idx_loan_applications_purpose_id   ON loan_applications(purpose_id);

-- ─── ml_predictions ──────────────────────────────────────────
-- Look up prediction by application quickly
CREATE INDEX idx_ml_predictions_application_id ON ml_predictions(application_id);

-- ─── rag_explanations ────────────────────────────────────────
CREATE INDEX idx_rag_explanations_prediction_id ON rag_explanations(prediction_id);

-- ─── audit_log ───────────────────────────────────────────────
-- Filter audit log by application or manager
CREATE INDEX idx_audit_log_application_id ON audit_log(application_id);
CREATE INDEX idx_audit_log_manager_id     ON audit_log(manager_id);
CREATE INDEX idx_audit_log_changed_at     ON audit_log(changed_at DESC);
