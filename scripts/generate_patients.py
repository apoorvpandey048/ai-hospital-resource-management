#!/usr/bin/env python3
"""
scripts/generate_patients.py

Generates synthetic patient records (HIPAA-compliant synthetic data) with
realistic distributions and seasonal patterns.

Usage:
    python scripts/generate_patients.py --n 1000 --out data/patients_1000.csv --seed 42 --format csv

Outputs CSV or JSON. Reproducible via --seed.
"""
from __future__ import annotations
import argparse
import csv
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import random

import numpy as np
import pandas as pd
from faker import Faker

# --- Configuration / constants ---
ICD10_EXAMPLE = [
    "I10",  # Essential (primary) hypertension
    "E11.9",  # Type 2 diabetes mellitus without complications
    "J18.9",  # Pneumonia, unspecified
    "J45.9",  # Asthma, unspecified
    "I50.9",  # Heart failure
    "N39.0",  # Urinary tract infection
    "S72.001A",  # Fracture of femur
    "A41.9",  # Sepsis
    "K35.80",  # Acute appendicitis
    "G81.90",  # Hemiplegia, unspecified
    "J06.9",  # Acute upper respiratory infection
    "J10.1",  # Influenza with other respiratory manifestations
]

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
GENDERS = ["Male", "Female", "Other"]
ADMISSION_TYPES = ["ED", "Elective", "Transfer", "Urgent"]
INSURANCE_PROVIDERS = ["PrivateCare", "HealthNet", "GovHealth", "Medicare", "None"]
CHIEF_COMPLAINTS = [
    "Chest pain", "Shortness of breath", "Fever", "Cough",
    "Abdominal pain", "Headache", "Leg pain", "Weakness", "Fatigue",
]
ALLERGIES_POOL = ["None", "Penicillin", "Peanuts", "Latex", "Sulfa", "Aspirin"]
MEDICATIONS_POOL = [
    "Aspirin", "Metformin", "Lisinopril", "Atorvastatin", "Amoxicillin",
    "Albuterol", "Warfarin", "Prednisone"
]

# --- Helpers ---
def seasonality_multiplier(adm_dt: datetime, base_rate: float, condition: str) -> float:
    """
    Return multiplier for seasonal conditions (e.g., influenza spike in winter).
    For simplicity: winter months (Dec-Feb) have higher multiplier for respiratory codes.
    """
    month = adm_dt.month
    if condition == "respiratory":
        if month in (12, 1, 2):
            return 1.6  # winter spike
        elif month in (3, 11):
            return 1.2
    return base_rate

def clip(val, low, high):
    return max(low, min(high, val))

# --- Core generator ---
def generate_one(fake: Faker, seed_for_record: Optional[int] = None) -> Dict[str, Any]:
    if seed_for_record is not None:
        random.seed(seed_for_record)
        np.random.seed(seed_for_record)

    # Demographics
    first_name = fake.first_name()
    last_name = fake.last_name()
    patient_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{seed_for_record}"))
    gender = random.choice(GENDERS)
    blood_type = random.choice(BLOOD_TYPES)

    # Age distribution: Normal(mean=45, std=20), clipped to [0, 100]
    age = int(clip(int(np.random.normal(45, 20)), 0, 100))
    # DOB from age +/- 364 days
    dob = (datetime.now() - timedelta(days=age * 365 + random.randint(0, 364))).date().isoformat()

    # Admission datetime with seasonality (over past 3 years)
    start = datetime.now() - timedelta(days=365*3)
    end = datetime.now()
    total_seconds = int((end - start).total_seconds())
    adm_dt = start + timedelta(seconds=random.randint(0, total_seconds))

    # Admission type and triage
    admission_type = np.random.choice(ADMISSION_TYPES, p=[0.5, 0.2, 0.1, 0.2])
    triage_level = int(clip(int(np.random.choice([1,2,3,4,5], p=[0.05,0.10,0.35,0.35,0.15])), 1, 5))

    # Vitals with age-appropriate distributions
    # Temperature: Normal(37.0, 0.5) but create fever cases (~5-8%)
    base_temp = np.random.normal(37.0, 0.5)
    if random.random() < 0.07:
        temp = round(base_temp + np.random.uniform(1.0, 3.5), 1)  # fever
    else:
        temp = round(base_temp, 1)
    # Heart rate: Normal(75, 12) but slightly higher for younger/fever
    hr = int(clip(int(np.random.normal(75 + (100-age)/100*3 + (temp>38)*10, 12)), 30, 200))
    # Respiratory rate: Normal(16, 3)
    rr = int(clip(int(np.random.normal(16, 3)), 8, 40))
    # SpO2: Normal(97,1.5) but lower if respiratory issue
    spo2 = round(clip(np.random.normal(97, 1.5), 70, 100), 1)
    # Weight/Height/BMI
    height_cm = int(clip(int(np.random.normal(168, 10)), 120, 210))
    weight_kg = round(clip(np.random.normal(70 + (age-45)*0.1, 15), 30, 200), 1)
    bmi = round(weight_kg / ((height_cm/100)**2), 1)

    # BP correlated with age and hypertension prevalence
    # Baseline systolic around 110-120, increases with age and with some chance of hypertension
    htn_prob = clip(0.05 + 0.01 * max(age - 40, 0), 0, 0.6)  # increases after 40
    has_htn = random.random() < htn_prob
    bp_systolic = int(clip(int(np.random.normal(115 + 0.6*age + (has_htn*10), 15)), 80, 240))
    bp_diastolic = int(clip(int(np.random.normal(75 + 0.2*age + (has_htn*5), 10)), 40, 140))

    # Pain level 0-10 (higher for traumatic/admissions)
    pain_level = int(clip(int(np.random.normal(3 + (triage_level<=2)*3, 2)), 0, 10))

    # Allergies, medications, medical history
    allergies = random.choice(ALLERGIES_POOL)
    meds = random.sample(MEDICATIONS_POOL, k=random.choice([0,1,1,2]))
    medical_history = []
    # Add some chronic conditions probabilistically
    if random.random() < 0.25:
        medical_history.append("Hypertension")
    if random.random() < 0.20:
        medical_history.append("Diabetes")
    if random.random() < 0.10:
        medical_history.append("COPD")
    if random.random() < 0.08:
        medical_history.append("Coronary artery disease")
    medical_history_text = ";".join(medical_history) if medical_history else "None"

    # Chief complaint & diagnosis: include seasonal spike for respiratory/flu codes
    # Create probability for respiratory cases higher in winter months
    resp_multiplier = seasonality_multiplier(adm_dt, 1.0, "respiratory")
    if random.random() < 0.12 * resp_multiplier:
        # respiratory complaint & ICD10
        chief = random.choice(["Cough", "Shortness of breath", "Fever", "Sore throat"])
        diagnosis_icd10 = random.choice(["J10.1", "J18.9", "J06.9", "J45.9"])
    else:
        chief = random.choice(CHIEF_COMPLAINTS)
        diagnosis_icd10 = random.choice(ICD10_EXAMPLE)

    # Admission and discharge timestamps: length of stay 0-30 days skewed toward short stays
    los_days = int(clip(int(np.random.exponential(2.5)), 0, 30))
    discharge_dt = adm_dt + timedelta(days=los_days, seconds=random.randint(0, 86400))

    # Location/demographics
    city = fake.city()
    zip_code = fake.postcode()
    insurance_provider = random.choice(INSURANCE_PROVIDERS)
    emergency_contact = fake.phone_number()
    location = random.choice(["Ward A", "Ward B", "ICU", "ER", "Clinic"])

    record = {
        "patient_id": patient_id,
        "first_name": first_name,
        "last_name": last_name,
        "dob": dob,
        "age": age,
        "gender": gender,
        "blood_type": blood_type,
        "admission_datetime": adm_dt.isoformat(timespec='seconds'),
        "discharge_datetime": discharge_dt.isoformat(timespec='seconds'),
        "chief_complaint": chief,
        "triage_level": triage_level,
        "temperature": temp,
        "heart_rate": hr,
        "bp_systolic": bp_systolic,
        "bp_diastolic": bp_diastolic,
        "respiratory_rate": rr,
        "spo2": spo2,
        "pain_level": pain_level,
        "weight_kg": weight_kg,
        "height_cm": height_cm,
        "bmi": bmi,
        "allergies": allergies,
        "medications": ";".join(meds) if meds else "None",
        "medical_history": medical_history_text,
        "insurance_provider": insurance_provider,
        "emergency_contact": emergency_contact,
        "diagnosis_icd10": diagnosis_icd10,
        "admission_type": admission_type,
        "location": location,
        "city": city,
        "zip_code": zip_code,
        # Add a short free-text note (synthetic)
        "notes": fake.sentence(nb_words=10),
    }

    return record

def generate_n(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)
    np.random.seed(seed)

    rows: List[Dict[str, Any]] = []
    for i in range(n):
        # For reproducibility and variety, derive a per-record seed
        rec_seed = seed + i
        rows.append(generate_one(fake, seed_for_record=rec_seed))

    df = pd.DataFrame(rows)

    # Make sure required fields exist and drop duplicates if any (shouldn't)
    df = df.drop_duplicates(subset=["patient_id"])
    return df

def save(df: pd.DataFrame, out_path: str, fmt: str = "csv"):
    if fmt == "csv":
        df.to_csv(out_path, index=False)
    elif fmt == "json":
        df.to_json(out_path, orient="records", date_format="iso", indent=2)
    else:
        raise ValueError("Unsupported format: " + fmt)

def cli_main():
    parser = argparse.ArgumentParser(description="Generate synthetic patient dataset")
    parser.add_argument("--n", type=int, default=1000, help="Number of records to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--out", type=str, default="data/patients_1000.csv", help="Output path")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Output file format")
    args = parser.parse_args()

    df = generate_n(n=args.n, seed=args.seed)
    save(df, args.out, fmt=args.format)
    print(f"Wrote {len(df)} records to {args.out}")

if __name__ == "__main__":
    cli_main()
