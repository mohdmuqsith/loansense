from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, loans, predictions, audit
from models import applicant, audit as audit_model, loan, manager, prediction  # register SQLAlchemy mappers

app = FastAPI(
    title="LoanSenseAI API",
    description="AI-powered loan approval system",
    version="1.0.0"
)

# Allow Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(predictions.router)
app.include_router(audit.router)


@app.get("/")
def root():
    return {"message": "LoanSenseAI API is running"}
