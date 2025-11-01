"""Forward-chaining rule-based medical expert system (moved)

Small, educational expert system operating on propositional facts.
"""
from typing import List, Dict


class ExpertSystem:
    def __init__(self, rules: List[Dict]):
        self.rules = rules
        self.facts = set()

    def assert_fact(self, fact: str):
        self.facts.add(fact)

    def infer(self, max_iterations: int = 50) -> None:
        # Forward chaining until no new facts
        for _ in range(max_iterations):
            added = False
            for r in self.rules:
                if all(cond in self.facts for cond in r.get('if', [])):
                    for a in r.get('then', []):
                        if a not in self.facts:
                            self.facts.add(a)
                            added = True
            if not added:
                break

    def query(self, q: str) -> bool:
        return q in self.facts


if __name__ == '__main__':
    rules = [
        {'if': ['fever', 'cough'], 'then': ['possible_infection']},
        {'if': ['possible_infection', 'high_wbc'], 'then': ['bacterial_infection']},
    ]
    es = ExpertSystem(rules)
    es.assert_fact('fever')
    es.assert_fact('cough')
    es.assert_fact('high_wbc')
    es.infer()
    print('bacterial_infection' in es.facts)
