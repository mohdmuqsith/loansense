-- LoanSenseAI seed.sql
-- Sample data for dev/demo.
-- Run after schema, functions, procedures, triggers, views, indexes, and RBAC.

BEGIN;

TRUNCATE TABLE
    audit_log,
    rag_explanations,
    ml_predictions,
    loan_applications,
    financial_profile,
    employment,
    applicants,
    bank_managers,
    loan_purposes,
    property_areas,
    employer_categories
RESTART IDENTITY CASCADE;

INSERT INTO property_areas (area_type) VALUES
    ('Urban'),
    ('Semiurban'),
    ('Rural')
ON CONFLICT (area_type) DO NOTHING;

INSERT INTO employer_categories (category_name) VALUES
    ('Private'),
    ('Government'),
    ('MNC'),
    ('Business'),
    ('Unemployed')
ON CONFLICT (category_name) DO NOTHING;

INSERT INTO loan_purposes (purpose_name) VALUES
    ('Personal'),
    ('Car'),
    ('Home'),
    ('Business'),
    ('Education')
ON CONFLICT (purpose_name) DO NOTHING;

INSERT INTO bank_managers (username, password_hash, full_name, is_active) VALUES
    ('admin',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Admin User',    TRUE),
    ('manager1', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Sarah Ahmed',   TRUE),
    ('manager2', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Mashoor Gulati', TRUE)
ON CONFLICT (username) DO NOTHING;

INSERT INTO applicants (first_name, last_name, age, gender, marital_status, dependents, education_level, area_id, category_id) VALUES
    ('Priya',   'Sharma',   51, 'Female', 'Married',  0, 'Not Graduate', (SELECT area_id FROM property_areas WHERE area_type='Urban'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Raj',     'Mehta',    46, 'Male',   'Married',  3, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Semiurban'), (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Anita',   'Verma',    25, 'Female', 'Single',   2, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Urban'),     (SELECT category_id FROM employer_categories WHERE category_name='Government')),
    ('Deepa',   'Nair',     40, 'Female', 'Married',  2, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Rural'),     (SELECT category_id FROM employer_categories WHERE category_name='Government')),
    ('Arjun',   'Singh',    31, 'Male',   'Single',   2, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Urban'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Kiran',   'Das',      53, 'Male',   'Single',   1, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Semiurban'), (SELECT category_id FROM employer_categories WHERE category_name='Unemployed')),
    ('Vikram',  'Iyer',     58, 'Male',   'Married',  0, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Rural'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Meena',   'Pillai',   47, 'Female', 'Married',  2, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Rural'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Suresh',  'Kumar',    54, 'Male',   'Married',  1, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Semiurban'), (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Lakshmi', 'Rao',      35, 'Female', 'Single',   3, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Rural'),     (SELECT category_id FROM employer_categories WHERE category_name='Government')),
    ('Rohit',   'Gupta',    52, 'Male',   'Married',  2, 'Not Graduate', (SELECT area_id FROM property_areas WHERE area_type='Urban'),     (SELECT category_id FROM employer_categories WHERE category_name='MNC')),
    ('Sneha',   'Joshi',    41, 'Male',   'Married',  1, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Semiurban'), (SELECT category_id FROM employer_categories WHERE category_name='Government')),
    ('Ajay',    'Mishra',   25, 'Male',   'Married',  2, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Rural'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Pooja',   'Reddy',    26, 'Male',   'Single',   0, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Semiurban'), (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Anil',    'Desai',    58, 'Male',   'Single',   0, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Semiurban'), (SELECT category_id FROM employer_categories WHERE category_name='MNC')),
    ('Kavya',   'Menon',    42, 'Female', 'Married',  3, 'Not Graduate', (SELECT area_id FROM property_areas WHERE area_type='Urban'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Ravi',    'Tiwari',   38, 'Female', 'Married',  2, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Urban'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Sunita',  'Bajaj',    34, 'Male',   'Married',  1, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Urban'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Mohan',   'Saxena',   30, 'Female', 'Married',  3, 'Not Graduate', (SELECT area_id FROM property_areas WHERE area_type='Rural'),     (SELECT category_id FROM employer_categories WHERE category_name='Private')),
    ('Geeta',   'Pandey',   33, 'Male',   'Single',   2, 'Graduate',     (SELECT area_id FROM property_areas WHERE area_type='Urban'),     (SELECT category_id FROM employer_categories WHERE category_name='Private'));

INSERT INTO employment (applicant_id, employment_status, applicant_income, coapplicant_income) VALUES
    (1,  'Salaried',      17795.00, 1387.00),
    (2,  'Salaried',      2860.00,  2679.00),
    (3,  'Salaried',      7390.00,  2106.00),
    (4,  'Salaried',      13964.00, 8173.00),
    (5,  'Self-employed', 13284.00, 4223.00),
    (6,  'Salaried',      8265.00,  4831.00),
    (7,  'Salaried',      18850.00, 2768.00),
    (8,  'Salaried',      6426.00,  3186.00),
    (9,  'Salaried',      16423.00, 0.00),
    (10, 'Contract',      13363.00, 2599.00),
    (11, 'Salaried',      18023.00, 4033.00),
    (12, 'Self-employed', 10322.00, 8428.00),
    (13, 'Contract',      3685.00,  1304.00),
    (14, 'Self-employed', 2769.00,  7368.00),
    (15, 'Contract',      4433.00,  5877.00),
    (16, 'Salaried',      7311.00,  1301.00),
    (17, 'Unemployed',    7051.00,  2541.00),
    (18, 'Salaried',      8420.00,  2051.00),
    (19, 'Salaried',      19568.00, 6809.00),
    (20, 'Salaried',      8396.00,  8633.00);

INSERT INTO financial_profile (applicant_id, credit_score, existing_loans, dti_ratio, savings, collateral_value) VALUES
    (1,  637, 4, 0.53, 19403.00, 45638.00),
    (2,  621, 2, 0.30, 2580.00,  49272.00),
    (3,  674, 4, 0.20, 13844.00, 6908.00),
    (4,  579, 3, 0.31, 9553.00,  10844.00),
    (5,  721, 1, 0.29, 9386.00,  37629.00),
    (6,  602, 1, 0.56, 19522.00, 2911.00),
    (7,  687, 0, 0.48, 14635.00, 8991.00),
    (8,  636, 4, NULL, 671.00,   11572.00),
    (9,  729, 0, 0.59, 777.00,   43066.00),
    (10, 726, 1, NULL, 3022.00,  29693.00),
    (11, 688, 1, 0.13, 18244.00, 40004.00),
    (12, 743, 4, 0.23, NULL,     38333.00),
    (13, 735, 3, 0.32, 13817.00, 17493.00),
    (14, 767, 3, 0.18, 14260.00, 39697.00),
    (15, 713, 4, 0.57, 1074.00,  NULL),
    (16, 710, 4, 0.48, 9908.00,  24561.00),
    (17, 724, 0, 0.23, 9475.00,  18033.00),
    (18, 562, 4, 0.40, 12878.00, 7351.00),
    (19, 589, 3, 0.46, 15120.00, 25921.00),
    (20, 638, 0, 0.57, 1986.00, 19340.00);

INSERT INTO loan_applications (applicant_id, purpose_id, loan_amount, loan_term, status) VALUES
    (1,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Personal'),  16619.00, 84,   'Rejected'),
    (2,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Car'),       38687.00, NULL, 'Rejected'),
    (3,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Personal'),  27943.00, 72,   'Approved'),
    (4,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Business'),  27819.00, 60,   'Rejected'),
    (5,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Car'),       12741.00, 72,   'Approved'),
    (6,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Home'),      9798.00,  36,   'Rejected'),
    (7,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Home'),      26143.00, 24,   'Rejected'),
    (8,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Personal'),  33747.00, 84,   'Rejected'),
    (9,  (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Home'),      34651.00, 36,   'Rejected'),
    (10, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Personal'),  22182.00, 60,   'Approved'),
    (11, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Education'), 10415.00, 12,   'Approved'),
    (12, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Car'),       12085.00, 84,   'Approved'),
    (13, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Business'),  16008.00, 36,   'Rejected'),
    (14, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Personal'),  23102.00, 72,   'Rejected'),
    (15, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Personal'),  19452.00, 84,   'Rejected'),
    (16, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Personal'),  9120.00,  72,   'Pending'),
    (17, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Personal'),  8820.00,  48,   'Approved'),
    (18, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Home'),      19170.00, 48,   'Rejected'),
    (19, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Home'),      17259.00, 48,   'Rejected'),
    (20, (SELECT purpose_id FROM loan_purposes WHERE purpose_name='Car'),       23099.00, 84,   'Rejected');

INSERT INTO ml_predictions (application_id, approved, confidence, model_version) VALUES
    (1,  FALSE, 0.8321, 'v1.0'),
    (2,  FALSE, 0.7654, 'v1.0'),
    (3,  TRUE,  0.9102, 'v1.0'),
    (4,  FALSE, 0.8800, 'v1.0'),
    (5,  TRUE,  0.8754, 'v1.0'),
    (6,  FALSE, 0.7200, 'v1.0'),
    (7,  FALSE, 0.6901, 'v1.0'),
    (8,  FALSE, 0.7843, 'v1.0'),
    (9,  FALSE, 0.8123, 'v1.0'),
    (10, TRUE,  0.9231, 'v1.0');

INSERT INTO rag_explanations (prediction_id, reasoning_text, retrieved_context) VALUES
    (1, 'Application rejected due to high DTI ratio of 0.53 and 4 existing loans, indicating over-leveraged financial position.',
        'Policy: Applications with DTI > 0.50 require additional collateral review.'),
    (3, 'Application approved. Credit score of 674 meets minimum threshold. Income adequate relative to loan amount.',
        'Policy: Minimum credit score 620. Loan-to-income ratio within acceptable range.'),
    (5, 'Application approved. Strong credit score of 721, single existing loan, and good collateral value support approval.',
        'Policy: Credit score above 720 fast-tracked for approval with standard verification.');

INSERT INTO audit_log (application_id, manager_id, old_status, new_status, change_note) VALUES
    (1,  2, 'Pending', 'Rejected', 'High DTI and multiple existing loans'),
    (2,  2, 'Pending', 'Rejected', 'Missing loan term information'),
    (3,  3, 'Pending', 'Approved', 'Good credit profile and income'),
    (4,  2, 'Pending', 'Rejected', 'Low credit score 579'),
    (5,  3, 'Pending', 'Approved', 'Strong credit score and low risk'),
    (10, 3, 'Pending', 'Approved', 'Meets all criteria'),
    (11, 2, 'Pending', 'Approved', 'Excellent financial profile');

COMMIT;
