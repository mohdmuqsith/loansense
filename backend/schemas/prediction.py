from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PredictionOut(BaseModel):
    prediction_id:  int
    application_id: int
    approved:       bool
    confidence:     float
    model_version:  str
    predicted_at:   datetime
    reasoning_text: Optional[str] = None

    class Config:
        from_attributes = True
