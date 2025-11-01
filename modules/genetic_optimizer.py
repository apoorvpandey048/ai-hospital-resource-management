"""Simple genetic algorithm for resource optimization (moved and renamed)

Chromosome: list of bed indices (or -1 for unassigned) per patient.
"""
import random
from typing import List, Dict


def fitness(chrom: List[int], patients: List[Dict], beds: List[Dict]) -> float:
    score = 0
    for i, b_idx in enumerate(chrom):
        if b_idx < 0 or b_idx >= len(beds):
            score -= 1
            continue
        bed = beds[b_idx]
        pat = patients[i]
        if pat.get('needs_icu') and bed.get('icu'):
            score += 2
        if pat.get('needs_vent') and bed.get('vent'):
            score += 2
        # distance penalty
        dist = abs(pat.get('location', (0,0))[0] - bed.get('location', (0,0))[0]) + abs(pat.get('location', (0,0))[1] - bed.get('location', (0,0))[1])
        score -= dist * 0.1
    return score


def ga_optimize(patients: List[Dict], beds: List[Dict], pop_size=50, gens=50) -> List[int]:
    n = len(patients)
    m = len(beds)
    # initialize population
    pop = [[random.randint(-1, m-1) for _ in range(n)] for _ in range(pop_size)]
    for g in range(gens):
        pop = sorted(pop, key=lambda c: -fitness(c, patients, beds))
        # keep top 10
        next_pop = pop[:10]
        # crossover
        while len(next_pop) < pop_size:
            a, b = random.sample(pop[:20], 2)
            cx = random.randint(1, n-1)
            child = a[:cx] + b[cx:]
            # mutation
            if random.random() < 0.1:
                idx = random.randrange(n)
                child[idx] = random.randint(-1, m-1)
            next_pop.append(child)
        pop = next_pop
    best = max(pop, key=lambda c: fitness(c, patients, beds))
    return best


if __name__ == '__main__':
    patients = [
        {'id': 'p1', 'needs_icu': True, 'needs_vent': False, 'location': (0,0)},
        {'id': 'p2', 'needs_icu': False, 'needs_vent': False, 'location': (5,5)},
    ]
    beds = [
        {'id': 'b1', 'icu': True, 'vent': False, 'location': (1,0)},
        {'id': 'b2', 'icu': False, 'vent': False, 'location': (6,6)},
    ]
    print(ga_optimize(patients, beds, pop_size=20, gens=10))
