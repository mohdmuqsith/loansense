-- ============================================================
--  LoanSenseAI — cursors.sql
--  Cursor-based batch processing examples.
--  Run manually or call from a scheduled job / admin script.
-- ============================================================

-- ─── 1. Batch risk-flag pending applications ─────────────────
-- Loops over all Pending applications, computes risk score,
-- and flags high-risk ones as 'Under Review' automatically.
DO $$
DECLARE
    cur_pending CURSOR FOR
        SELECT la.application_id, la.applicant_id
        FROM   loan_applications la
        WHERE  la.status = 'Pending'
        ORDER  BY la.applied_at;

    rec          RECORD;
    v_risk_score INT;
BEGIN
    OPEN cur_pending;

    LOOP
        FETCH cur_pending INTO rec;
        EXIT WHEN NOT FOUND;

        v_risk_score := applicant_risk_score(rec.applicant_id);

        IF v_risk_score >= 70 THEN
            UPDATE loan_applications
            SET    status = 'Under Review'
            WHERE  application_id = rec.application_id;

            INSERT INTO audit_log (application_id, old_status, new_status, change_note)
            VALUES (rec.application_id, 'Pending', 'Under Review',
                    'Auto-flagged by batch risk scan (score: ' || v_risk_score || ')');
        END IF;
    END LOOP;

    CLOSE cur_pending;
END;
$$;


-- ─── 2. Batch export summary (cursor → temp table) ───────────
-- Useful for generating a nightly report of all decisions.
-- Creates a temp table you can SELECT from in the same session.
DO $$
DECLARE
    cur_decisions CURSOR FOR
        SELECT application_id, status, loan_amount, applied_at, reviewed_at
        FROM   loan_applications
        WHERE  status IN ('Approved', 'Rejected')
          AND  reviewed_at >= NOW() - INTERVAL '1 day'
        ORDER  BY reviewed_at DESC;

    rec RECORD;
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS nightly_decisions (
        application_id INT,
        status         VARCHAR(20),
        loan_amount    NUMERIC(12,2),
        applied_at     TIMESTAMPTZ,
        reviewed_at    TIMESTAMPTZ
    ) ON COMMIT DROP;

    OPEN cur_decisions;
    LOOP
        FETCH cur_decisions INTO rec;
        EXIT WHEN NOT FOUND;

        INSERT INTO nightly_decisions VALUES (
            rec.application_id,
            rec.status,
            rec.loan_amount,
            rec.applied_at,
            rec.reviewed_at
        );
    END LOOP;
    CLOSE cur_decisions;

    RAISE NOTICE 'Nightly decisions export complete. Rows inserted: %',
        (SELECT COUNT(*) FROM nightly_decisions);
END;
$$;
