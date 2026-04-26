from typing import Any

from rag.retriever import retrieve


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _str(value: Any) -> str:
    return str(value or "").strip()


def _fmt_money(value: float) -> str:
    return f"{value:,.2f}"


def _build_facts(applicant_data: dict) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    credit_score = _num(applicant_data.get("credit_score"))
    dti_ratio = _num(applicant_data.get("dti_ratio"))
    existing_loans = int(_num(applicant_data.get("existing_loans")))
    applicant_income = _num(applicant_data.get("applicant_income"))
    coapplicant_income = _num(applicant_data.get("coapplicant_income"))
    loan_amount = _num(applicant_data.get("loan_amount"))
    loan_term = int(_num(applicant_data.get("loan_term")))
    loan_purpose = _str(applicant_data.get("loan_purpose"))
    employment_status = _str(applicant_data.get("employment_status"))
    education_level = _str(applicant_data.get("education_level"))
    employer_category = _str(applicant_data.get("employer_category"))
    collateral_value = _num(applicant_data.get("collateral_value"))
    dependents = int(_num(applicant_data.get("dependents")))
    age = int(_num(applicant_data.get("age")))

    combined_income = applicant_income + coapplicant_income
    annual_income = combined_income * 12
    age_at_maturity = age + (loan_term / 12 if loan_term else 0)

    hard_reasons: list[tuple[str, str]] = []
    positive_reasons: list[tuple[str, str]] = []

    # Critical rules
    if credit_score < 580:
        hard_reasons.append(("Credit Score", f"Credit score {credit_score:.0f} is below 580, which triggers rejection."))
    elif credit_score < 620:
        hard_reasons.append(("Credit Score", f"Credit score {credit_score:.0f} is below the minimum approval threshold of 620."))
    elif credit_score < 670:
        positive_reasons.append(("Credit Score", f"Credit score {credit_score:.0f} is in the high-risk band and normally needs collateral support."))
    elif credit_score < 740:
        positive_reasons.append(("Credit Score", f"Credit score {credit_score:.0f} is in the standard approval band."))
    else:
        positive_reasons.append(("Credit Score", f"Credit score {credit_score:.0f} is in the fast-track approval band."))

    if dti_ratio > 0.50 and collateral_value < (2 * loan_amount):
        hard_reasons.append(("DTI", f"DTI ratio {dti_ratio:.2f} is above 0.50 and collateral is below 2x the loan amount."))
    elif dti_ratio > 0.35:
        positive_reasons.append(("DTI", f"DTI ratio {dti_ratio:.2f} is in the moderate-risk band and needs a strong credit profile."))
    else:
        positive_reasons.append(("DTI", f"DTI ratio {dti_ratio:.2f} is within the low-risk band."))

    if combined_income < 3000:
        hard_reasons.append(("Income", f"Combined monthly income {_fmt_money(combined_income)} is below the 3,000 minimum."))
    else:
        positive_reasons.append(("Income", f"Combined monthly income {_fmt_money(combined_income)} meets the minimum income policy."))

    if existing_loans >= 4 and dti_ratio >= 0.30:
        hard_reasons.append(("Existing Loans", f"{existing_loans} existing loans with DTI {dti_ratio:.2f} triggers rejection under the loan-count policy."))
    elif existing_loans > 0:
        positive_reasons.append(("Existing Loans", f"{existing_loans} existing loan(s) reduce the maximum eligible amount by {existing_loans * 10}%."))

    if loan_amount < 1000:
        hard_reasons.append(("Loan Amount", f"Requested loan amount {_fmt_money(loan_amount)} is below the minimum of 1,000."))
    elif loan_amount > 500000:
        hard_reasons.append(("Loan Amount", f"Requested loan amount {_fmt_money(loan_amount)} exceeds the maximum of 500,000."))
    elif annual_income > 0 and loan_amount > (5 * annual_income):
        hard_reasons.append(("Loan Amount", f"Requested loan amount {_fmt_money(loan_amount)} exceeds 5x annual income ({_fmt_money(5 * annual_income)})."))
    else:
        positive_reasons.append(("Loan Amount", f"Requested loan amount {_fmt_money(loan_amount)} stays within the 5x annual income limit."))

    if loan_purpose == "Home" and collateral_value > 0 and loan_amount > 0.8 * collateral_value:
        hard_reasons.append(("Home Loan", f"Home loan amount exceeds 80% of collateral value."))

    if loan_purpose == "Personal" and loan_term > 84:
        hard_reasons.append(("Loan Term", "Personal loan term exceeds the 84-month limit."))
    elif loan_purpose == "Car" and loan_term > 84:
        hard_reasons.append(("Loan Term", "Car loan term exceeds the 84-month limit."))
    elif loan_purpose == "Home" and loan_term > 360:
        hard_reasons.append(("Loan Term", "Home loan term exceeds the 360-month limit."))
    elif loan_purpose == "Education" and loan_term > 120:
        hard_reasons.append(("Loan Term", "Education loan term exceeds the 120-month limit."))
    elif loan_purpose == "Business" and loan_term > 120:
        hard_reasons.append(("Loan Term", "Business loan term exceeds the 120-month limit."))
    else:
        positive_reasons.append(("Loan Term", f"Loan term of {loan_term} months is within the policy limit for this product."))

    if education_level == "Not Graduate" and credit_score < 680 and collateral_value < loan_amount:
        hard_reasons.append(("Education", "Non-graduate rule requires credit score 680+ or collateral above the loan amount."))

    if employment_status == "Unemployed" and coapplicant_income < 3000:
        hard_reasons.append(("Employment", "Unemployed applicants need sufficient co-applicant income."))

    if age < 18:
        hard_reasons.append(("Age", "Applicant age is below the minimum of 18."))
    elif age_at_maturity > 70:
        hard_reasons.append(("Age", f"Loan matures after age 70 (age at maturity: {age_at_maturity:.1f})."))
    else:
        positive_reasons.append(("Age", f"Age and loan term keep maturity within the age-70 policy limit."))

    if employer_category in {"Government", "MNC"}:
        positive_reasons.append(("Employer", f"{employer_category} employment is treated as low risk."))

    if collateral_value >= loan_amount and collateral_value > 0:
        positive_reasons.append(("Collateral", "Collateral value covers the requested loan amount."))

    if dependents >= 4:
        positive_reasons.append(("Dependents", f"{dependents} dependents increases risk and may require stronger income support."))
    elif dependents >= 2:
        positive_reasons.append(("Dependents", f"{dependents} dependents adds a small risk adjustment."))

    return hard_reasons, positive_reasons


def generate_explanation(applicant_data: dict, approved: bool, confidence: float) -> dict:
    """
    Deterministic policy explanation.
    The policy knowledge base is used as retrieval context, but the final wording
    is generated from explicit rules so it stays factual and repeatable.
    """
    context = retrieve(
        f"credit score {applicant_data.get('credit_score')}; "
        f"dti {applicant_data.get('dti_ratio')}; "
        f"existing loans {applicant_data.get('existing_loans')}; "
        f"income {applicant_data.get('applicant_income')}; "
        f"loan amount {applicant_data.get('loan_amount')}; "
        f"purpose {applicant_data.get('loan_purpose')}; "
        f"term {applicant_data.get('loan_term')}."
    )

    hard_reasons, positive_reasons = _build_facts(applicant_data)
    decision_word = "APPROVED" if approved else "REJECTED"
    confidence_pct = confidence * 100
    borderline = confidence < 0.60

    def _compose(reasons: list[tuple[str, str]]) -> str:
        cleaned = [reason.rstrip(".") for _, reason in reasons if reason]
        if not cleaned:
            return ""
        if len(cleaned) == 1:
            return cleaned[0]
        if len(cleaned) == 2:
            return f"{cleaned[0]} and {cleaned[1]}"
        return f"{cleaned[0]}, {cleaned[1]}, and {cleaned[2]}"

    if approved:
        reasons = positive_reasons[:3] if positive_reasons else [("Policy", "No major policy violations were detected in the supplied data")]
        body = _compose(reasons)
        if borderline:
            reasoning = (
                f"The model leans toward APPROVAL with only {confidence_pct:.1f}% confidence, so the application should be manually reviewed by a bank manager. "
                f"{body}."
            )
        else:
            reasoning = (
                f"The loan was APPROVED with {confidence_pct:.1f}% model confidence because the applicant meets the main policy checks. "
                f"{body}."
            )
    else:
        if hard_reasons:
            reasons = hard_reasons[:3]
            body = _compose(reasons)
        else:
            reasons = positive_reasons[:2]
            body = _compose(reasons) if reasons else "The supplied data does not show a single hard policy violation, so the model likely rejected it on learned scoring"
        if borderline:
            reasoning = (
                f"The model leans toward REJECTION with only {confidence_pct:.1f}% confidence, so the application should be manually reviewed by a bank manager before a final decision. "
                f"{body}."
            )
        else:
            reasoning = f"The loan was REJECTED with {confidence_pct:.1f}% model confidence because the strongest policy checks point to higher risk. {body}."

    return {
        "reasoning_text": reasoning,
        "retrieved_context": context,
    }
