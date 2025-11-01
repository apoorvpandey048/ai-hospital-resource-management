"""Simple CSP solver for staff and surgery scheduling (moved and renamed)

This is a backtracking CSP with light constraint propagation (forward checking).
It is intended as a clear, educational example.
"""
from typing import List, Dict, Optional


def schedule_surgeries(staff: List[Dict], surgeries: List[Dict], slots: List[str]) -> Optional[Dict]:
    """Assign staff to surgeries into time slots.

    staff: list of {'id', 'roles': ['surgeon','anesthetist',...], 'max_slots'}
    surgeries: list of {'id', 'required_roles': ['surgeon','anesthetist'], 'duration_slots'}
    slots: list of slot identifiers (e.g., '08:00-09:00')

    Returns assignment mapping or None.
    """
    # Preprocess: map role -> available staff ids
    role_staff = {}
    for s in staff:
        for r in s.get("roles", []):
            role_staff.setdefault(r, []).append(s["id"])

    # Simple domains: for each surgery, possible starting slot indices
    max_start = len(slots)
    domains = {sur['id']: list(range(0, max_start)) for sur in surgeries}

    assignment = {}
    staff_load = {s['id']: 0 for s in staff}

    def consistent(sur_id, start_idx, sur):
        # check if enough consecutive slots
        if start_idx + sur.get('duration_slots', 1) > len(slots):
            return False
        # check staff availability for required roles
        for role in sur['required_roles']:
            available = role_staff.get(role, [])
            if not available:
                return False
        return True

    def backtrack(i=0):
        if i >= len(surgeries):
            return True
        sur = surgeries[i]
        for start in domains[sur['id']]:
            if not consistent(sur['id'], start, sur):
                continue
            # naive: pick first staff for each role that still under max load
            chosen = {}
            ok = True
            for role in sur['required_roles']:
                for sid in role_staff.get(role, []):
                    if staff_load[sid] + sur.get('duration_slots', 1) <= next(s['max_slots'] for s in staff if s['id'] == sid):
                        chosen[role] = sid
                        break
                else:
                    ok = False
                    break
            if not ok:
                continue
            # assign
            assignment[sur['id']] = {'start': start, 'roles': chosen}
            for sid in chosen.values():
                staff_load[sid] += sur.get('duration_slots', 1)
            if backtrack(i+1):
                return True
            # undo
            del assignment[sur['id']]
            for sid in chosen.values():
                staff_load[sid] -= sur.get('duration_slots', 1)
        return False

    if backtrack():
        return assignment
    return None


if __name__ == '__main__':
    staff = [
        {'id': 's1', 'roles': ['surgeon'], 'max_slots': 4},
        {'id': 's2', 'roles': ['anesthetist'], 'max_slots': 4},
    ]
    surgeries = [
        {'id': 'op1', 'required_roles': ['surgeon', 'anesthetist'], 'duration_slots': 2},
    ]
    slots = ['08:00', '09:00', '10:00', '11:00']
    print(schedule_surgeries(staff, surgeries, slots))
