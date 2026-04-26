from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base


class MLPrediction(Base):
    __tablename__ = "ml_predictions"

    prediction_id  = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.application_id", ondelete="CASCADE"), nullable=False)
    approved       = Column(Boolean, nullable=False)
    confidence     = Column(Numeric(5, 4), nullable=False)
    model_version  = Column(String(30), nullable=False, default="v1.0")
    predicted_at   = Column(TIMESTAMP(timezone=True), server_default=func.now())

    application  = relationship("LoanApplication", back_populates="predictions")
    explanations = relationship("RAGExplanation", back_populates="prediction")


class RAGExplanation(Base):
    __tablename__ = "rag_explanations"

    explanation_id    = Column(Integer, primary_key=True, index=True)
    prediction_id     = Column(Integer, ForeignKey("ml_predictions.prediction_id", ondelete="CASCADE"), nullable=False)
    reasoning_text    = Column(Text, nullable=False)
    retrieved_context = Column(Text)
    generated_at      = Column(TIMESTAMP(timezone=True), server_default=func.now())

    prediction = relationship("MLPrediction", back_populates="explanations")
