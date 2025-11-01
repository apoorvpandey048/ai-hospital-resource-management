"""Bed allocation using A*-style scoring (moved to modules/)

This file implements a simplified A*-like scoring function to select a
bed that best matches patient needs and proximity.
"""
from typing import List, Dict, Tuple, Optional


def manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def allocate_bed(patient: Dict, beds: List[Dict]) -> Optional[Dict]:
    """Allocate a best-fit bed for the patient using an A*-style scoring.

    patient: dict with keys 'id', 'needs_icu' (bool), 'needs_vent' (bool), 'location' (x,y)
    beds: list of dicts with keys 'id', 'is_occupied', 'icu', 'vent', 'location'

    Returns the selected bed dict or None if no match.
    """
    open_beds = [b for b in beds if not b.get("is_occupied")]
    if not open_beds:
        return None

    best = None
    best_score = float("inf")
    for bed in open_beds:
        # Heuristic: distance + heavy penalty for missing required features
        dist = manhattan(tuple(patient.get("location", (0, 0))), tuple(bed.get("location", (0, 0))))
        penalty = 0
        if patient.get("needs_icu") and not bed.get("icu"):
            penalty += 100
        if patient.get("needs_vent") and not bed.get("vent"):
            penalty += 100
        score = dist + penalty
        if score < best_score:
            best_score = score
            best = bed
    return best


if __name__ == "__main__":
    # quick demo
    patients = [{"id": "p1", "needs_icu": True, "needs_vent": False, "location": (2, 2)}]
    beds = [
        {"id": "b1", "is_occupied": False, "icu": True, "vent": False, "location": (3, 2)},
        {"id": "b2", "is_occupied": False, "icu": False, "vent": False, "location": (10, 10)},
    ]
    print(allocate_bed(patients[0], beds))
