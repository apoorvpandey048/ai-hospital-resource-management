"""Fuzzy logic patient prioritization (Mamdani-style) — moved and renamed

Inputs: temperature (C), systolic_bp, pain_level (0-10)
Output: priority score 0-100 (higher = higher priority)
"""
from typing import Dict


def fuzz_temp(temp: float) -> Dict[str, float]:
    # low, normal, high
    return {
        'low': max(0.0, min(1.0, (37.0 - temp) / 2.0)),
        'normal': max(0.0, min(1.0, 1 - abs(temp - 37.0) / 1.5)),
        'high': max(0.0, min(1.0, (temp - 37.0) / 3.0)),
    }


def fuzz_bp(sbp: float) -> Dict[str, float]:
    # low, normal, high
    return {
        'low': max(0.0, min(1.0, (120 - sbp) / 40.0)),
        'normal': max(0.0, min(1.0, 1 - abs(sbp - 120) / 20.0)),
        'high': max(0.0, min(1.0, (sbp - 120) / 40.0)),
    }


def fuzz_pain(pain: float) -> Dict[str, float]:
    # mild, moderate, severe
    return {
        'mild': max(0.0, min(1.0, (5 - pain) / 5.0)),
        'moderate': max(0.0, min(1.0, 1 - abs(pain - 5) / 3.0)),
        'severe': max(0.0, min(1.0, (pain - 5) / 5.0)),
    }


def compute_priority(temp: float, sbp: float, pain: float) -> float:
    t = fuzz_temp(temp)
    b = fuzz_bp(sbp)
    p = fuzz_pain(pain)

    # Rules (small set):
    # If temp is high OR pain is severe OR bp is high -> high priority
    # If temp is normal and pain moderate and bp normal -> medium
    # If temp low and pain mild -> low

    high_strength = max(t['high'], p['severe'], b['high'])
    medium_strength = min(t['normal'], p['moderate'], b['normal'])
    low_strength = max(t['low'], p['mild'])

    # Defuzzify using weighted average of representative scores
    numerator = high_strength * 90 + medium_strength * 50 + low_strength * 10
    denom = high_strength + medium_strength + low_strength
    if denom == 0:
        return 0.0
    return float(numerator / denom)


if __name__ == '__main__':
    print(compute_priority(39.0, 130, 8))
    print(compute_priority(36.5, 115, 2))
