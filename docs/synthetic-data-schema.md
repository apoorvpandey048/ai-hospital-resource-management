# Synthetic Patient Data - Generation methodology

This dataset is synthetic and intended for training/testing only. It does NOT contain any real patient data.

## Fields generated
patient_id, first_name, last_name, dob, age, gender, blood_type,
admission_datetime, discharge_datetime, chief_complaint, triage_level, temperature,
heart_rate, bp_systolic, bp_diastolic, respiratory_rate, spo2,
pain_level, weight_kg, height_cm, bmi, allergies, medications,
medical_history, insurance_provider, emergency_contact,
diagnosis_icd10, admission_type, location, city, zip_code, notes

## Statistical choices
- Age ~ Normal(mean=45, std=20), clipped to 0–100.
- Blood pressure increases with age; hypertension probability increases after age 40.
- Temperature ~ Normal(37.0, 0.5) with ~7% simulated fever cases.
- Respiratory/flu incidence has a seasonal spike during winter months (Dec–Feb).
- LOS (length of stay) follows a skewed (exponential) distribution (mean short stay).

## Reproducibility
Run with `--seed <int>`; per-record seed is derived as `seed + index` to provide both repeatability and variety.

## HIPAA & Privacy
All values are synthetically generated (Faker + random/noise). This dataset must not be combined with real PHI without appropriate safeguards.
