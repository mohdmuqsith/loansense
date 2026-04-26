--SQL Queries can be done here. 
-- For example, to fetch all loan applications with their financial profiles, ML predictions, and RAG explanation.


SELECT
  la.application_id,
  fp.credit_score,
  fp.existing_loans,
  fp.dti_ratio,
  fp.savings,
  fp.collateral_value,
  mp.approved,
  mp.confidence,
  re.reasoning_text
FROM loan_applications la
LEFT JOIN applicants a ON a.applicant_id = la.applicant_id
LEFT JOIN financial_profile fp ON fp.applicant_id = a.applicant_id
LEFT JOIN ml_predictions mp ON mp.application_id = la.application_id
LEFT JOIN rag_explanations re ON re.prediction_id = mp.prediction_id
ORDER BY la.application_id DESC;

