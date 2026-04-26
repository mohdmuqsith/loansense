-- ============================================================
--  LoanSenseAI — triggers.sql
--  Automatic audit logging on status changes.
-- ============================================================

-- ─── Trigger function: log status changes ────────────────────
CREATE OR REPLACE FUNCTION fn_audit_status_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Only fire when status column actually changes
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO audit_log (
            application_id,
            manager_id,
            old_status,
            new_status,
            changed_at,
            change_note
        ) VALUES (
            NEW.application_id,
            current_setting('app.current_manager_id', TRUE)::INT,  -- set by app layer
            OLD.status,
            NEW.status,
            NOW(),
            'Status updated via application'
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to loan_applications
DROP TRIGGER IF EXISTS trg_audit_status_change ON loan_applications;
CREATE TRIGGER trg_audit_status_change
    AFTER UPDATE OF status ON loan_applications
    FOR EACH ROW
    EXECUTE FUNCTION fn_audit_status_change();


-- ─── Trigger function: auto-set reviewed_at ──────────────────
-- Stamps reviewed_at when status moves out of Pending
CREATE OR REPLACE FUNCTION fn_set_reviewed_at()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status = 'Pending' AND NEW.status <> 'Pending' THEN
        NEW.reviewed_at := NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_set_reviewed_at ON loan_applications;
CREATE TRIGGER trg_set_reviewed_at
    BEFORE UPDATE OF status ON loan_applications
    FOR EACH ROW
    EXECUTE FUNCTION fn_set_reviewed_at();


-- ─── Trigger function: prevent deletion of reviewed apps ─────
-- Protects data integrity — approved/rejected apps must not be deleted
CREATE OR REPLACE FUNCTION fn_prevent_reviewed_delete()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IN ('Approved', 'Rejected') THEN
        RAISE EXCEPTION 'Cannot delete a reviewed application (status: %)', OLD.status;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_prevent_reviewed_delete ON loan_applications;
CREATE TRIGGER trg_prevent_reviewed_delete
    BEFORE DELETE ON loan_applications
    FOR EACH ROW
    EXECUTE FUNCTION fn_prevent_reviewed_delete();
