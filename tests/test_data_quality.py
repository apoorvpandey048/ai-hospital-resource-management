import os
import pandas as pd
import numpy as np
from scripts.generate_patients import generate_n, save
import tempfile

def test_generate_count_and_unique_ids():
    df = generate_n(n=1200, seed=123)
    assert len(df) == 1200
    assert df['patient_id'].nunique() == 1200

def test_no_nulls_for_required_fields():
    df = generate_n(n=100, seed=7)
    required = [
        "patient_id","first_name","last_name","dob","age","gender",
        "admission_datetime","diagnosis_icd10","bp_systolic","bp_diastolic"
    ]
    for col in required:
        assert col in df.columns
        # ensure no nulls
        assert df[col].isnull().sum() == 0

def test_age_distribution_stats():
    df = generate_n(n=5000, seed=11)
    # check mean near 45 (allowable tolerance because sampling)
    mean_age = df['age'].mean()
    assert 35 <= mean_age <= 55, f"Mean age out of expected range: {mean_age}"

def test_bp_age_correlation():
    df = generate_n(n=2000, seed=42)
    corr = df['age'].corr(df['bp_systolic'])
    # expectation: positive correlation (should be > 0.1)
    assert corr > 0.05, f"Unexpected low age-BP correlation: {corr}"

def test_write_and_read_csv(tmp_path):
    df = generate_n(n=50, seed=99)
    out = tmp_path / "test_out.csv"
    save(df, str(out), fmt="csv")
    df2 = pd.read_csv(out)
    assert len(df2) == 50

def test_reproducibility():
    d1 = generate_n(n=200, seed=500)
    d2 = generate_n(n=200, seed=500)
    pd.testing.assert_frame_equal(d1.reset_index(drop=True), d2.reset_index(drop=True))
