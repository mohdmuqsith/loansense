from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from models.prediction import MLPrediction, RAGExplanation
from rag.explainer import generate_explanation


def get_prediction(application_id: int, db: Session):
    pred = db.query(MLPrediction).filter(
        MLPrediction.application_id == application_id
    ).order_by(MLPrediction.predicted_at.desc()).first()

    if not pred:
        raise HTTPException(status_code=404, detail="No prediction found for this application")

    app_row = db.execute(text("""
        SELECT *
        FROM loan_summary_view
        WHERE application_id = :id
    """), {"id": application_id}).mappings().first()

    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")

    explanation = db.query(RAGExplanation).filter(
        RAGExplanation.prediction_id == pred.prediction_id
    ).first()

    rag_result = generate_explanation(dict(app_row), pred.approved, float(pred.confidence))

    if explanation:
        explanation.reasoning_text = rag_result["reasoning_text"]
        explanation.retrieved_context = rag_result["retrieved_context"]
    else:
        explanation = RAGExplanation(
            prediction_id=pred.prediction_id,
            reasoning_text=rag_result["reasoning_text"],
            retrieved_context=rag_result["retrieved_context"]
        )
        db.add(explanation)
    db.commit()

    return {
        "prediction_id":  pred.prediction_id,
        "application_id": pred.application_id,
        "approved":       pred.approved,
        "confidence":     float(pred.confidence),
        "model_version":  pred.model_version,
        "predicted_at":   pred.predicted_at,
        "reasoning_text": explanation.reasoning_text if explanation else None,
    }


def get_stats(db: Session):
    result = db.execute(text("SELECT * FROM approval_stats_view"))
    return [dict(row._mapping) for row in result]
