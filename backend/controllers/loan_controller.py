from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from schemas.loan import LoanApplicationCreate, LoanStatusUpdate
from models.loan import LoanApplication
from models.prediction import MLPrediction, RAGExplanation


def submit_loan(data: LoanApplicationCreate, db: Session):
    """Calls the stored procedure submit_application(), then runs ML prediction."""
    try:
        db.execute(text("""
            CALL submit_application(
                CAST(:first_name AS VARCHAR),
                CAST(:last_name AS VARCHAR),
                CAST(:age AS SMALLINT),
                CAST(:gender AS VARCHAR),
                CAST(:marital_status AS VARCHAR),
                CAST(:dependents AS SMALLINT),
                CAST(:education_level AS VARCHAR),
                CAST(:area_type AS VARCHAR),
                CAST(:employer_category AS VARCHAR),
                CAST(:employment_status AS VARCHAR),
                CAST(:applicant_income AS NUMERIC),
                CAST(:coapplicant_income AS NUMERIC),
                CAST(:credit_score AS SMALLINT),
                CAST(:existing_loans AS SMALLINT),
                CAST(:dti_ratio AS NUMERIC),
                CAST(:savings AS NUMERIC),
                CAST(:collateral_value AS NUMERIC),
                CAST(:loan_purpose AS VARCHAR),
                CAST(:loan_amount AS NUMERIC),
                CAST(:loan_term AS SMALLINT),
                CAST(NULL AS INTEGER)
            )
        """), data.model_dump())
        db.commit()

        # Fetch the latest application just created
        app = db.query(LoanApplication).order_by(
            LoanApplication.application_id.desc()
        ).first()

        # Run ML prediction
        try:
            from ml.predict import predict
            input_data = {
                "Applicant_Income":    data.applicant_income,
                "Coapplicant_Income":  data.coapplicant_income,
                "Employment_Status":   data.employment_status,
                "Age":                 data.age,
                "Marital_Status":      data.marital_status,
                "Dependents":          data.dependents,
                "Credit_Score":        data.credit_score,
                "Existing_Loans":      data.existing_loans,
                "DTI_Ratio":           data.dti_ratio or 0,
                "Savings":             data.savings or 0,
                "Collateral_Value":    data.collateral_value or 0,
                "Loan_Amount":         data.loan_amount,
                "Loan_Term":           data.loan_term or 60,
                "Loan_Purpose":        data.loan_purpose or "Personal",
                "Property_Area":       data.area_type or "Urban",
                "Education_Level":     data.education_level or "Graduate",
                "Gender":              data.gender or "Male",
                "Employer_Category":   data.employer_category or "Private",
            }
            result = predict(input_data)

            # Save prediction to DB
            prediction = MLPrediction(
                application_id=app.application_id,
                approved=result["approved"],
                confidence=result["confidence"],
                model_version=result["model_version"]
            )
            db.add(prediction)
            db.commit()

            # Generate and save RAG explanation for the result page
            try:
                from rag.explainer import generate_explanation
                rag_result = generate_explanation(
                    input_data,
                    result["approved"],
                    result["confidence"]
                )
                explanation = RAGExplanation(
                    prediction_id=prediction.prediction_id,
                    reasoning_text=rag_result["reasoning_text"],
                    retrieved_context=rag_result["retrieved_context"]
                )
                db.add(explanation)
                db.commit()
            except Exception as rag_error:
                # RAG failure should not block the application submission
                print(f"RAG explanation failed: {rag_error}")

        except Exception as ml_error:
            # ML failure should not block the application submission
            print(f"ML prediction failed: {ml_error}")

        return {
            "application_id": app.application_id,
            "applicant_id": app.applicant_id,
            "loan_amount": float(app.loan_amount),
            "loan_term": app.loan_term,
            "status": app.status,
            "applied_at": app.applied_at,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def get_all_applications(db: Session, status: str = None):
    result = db.execute(text("""
        SELECT * FROM loan_summary_view
        ORDER BY applied_at DESC
    """ if not status else """
        SELECT * FROM loan_summary_view
        WHERE status = :status
        ORDER BY applied_at DESC
    """), {"status": status} if status else {})
    return [dict(row._mapping) for row in result]


def get_application(application_id: int, db: Session):
    result = db.execute(text("""
        SELECT * FROM loan_summary_view WHERE application_id = :id
    """), {"id": application_id}).first()
    if not result:
        raise HTTPException(status_code=404, detail="Application not found")
    return dict(result._mapping)


def update_status(application_id: int, data: LoanStatusUpdate, db: Session):
    try:
        db.execute(text("""
            CALL review_application(:app_id, :manager_id, :status, :note)
        """), {
            "app_id":     application_id,
            "manager_id": data.manager_id,
            "status":     data.status,
            "note":       data.note
        })
        db.commit()
        return {"message": f"Application {application_id} updated to {data.status}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
