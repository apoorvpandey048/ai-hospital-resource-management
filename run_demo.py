"""Runner script demonstrating the modules quickly.
Run: python run_demo.py
"""
from modules import (
    bed_allocation,
    scheduling_csp,
    expert_system,
    fuzzy_triage,
    genetic_optimizer,
    ml_predictor,
    nn_classifier,
    nlp_chatbot,
)


def demo():
    print('--- Bed allocation demo ---')
    patient = {'id': 'p1', 'needs_icu': True, 'needs_vent': False, 'location': (2,2)}
    beds = [
        {'id': 'b1', 'is_occupied': False, 'icu': True, 'vent': False, 'location': (3,2)},
        {'id': 'b2', 'is_occupied': False, 'icu': False, 'vent': False, 'location': (10,10)},
    ]
    print(bed_allocation.allocate_bed(patient, beds))

    print('\n--- Fuzzy priority demo ---')
    print('priority =', fuzzy_triage.compute_priority(39.0, 130, 8))

    print('\n--- Expert system demo ---')
    rules = [
        {'if': ['fever', 'cough'], 'then': ['possible_infection']},
    ]
    es = expert_system.ExpertSystem(rules)
    es.assert_fact('fever')
    es.assert_fact('cough')
    es.infer()
    print('facts=', es.facts)

    print('\n--- GA optimization demo ---')
    patients = [
        {'id': 'p1', 'needs_icu': True, 'needs_vent': False, 'location': (0,0)},
        {'id': 'p2', 'needs_icu': False, 'needs_vent': False, 'location': (5,5)},
    ]
    beds = [
        {'id': 'b1', 'icu': True, 'vent': False, 'location': (1,0)},
        {'id': 'b2', 'icu': False, 'vent': False, 'location': (6,6)},
    ]
    print(genetic_optimizer.ga_optimize(patients, beds, pop_size=20, gens=10))

    print('\n--- ML prediction demo ---')
    X, y = ml_predictor.make_sample_dataset()
    ap = ml_predictor.AdmissionPredictor()
    print('train acc', ap.train(X, y))

    print('\n--- NN classifier demo ---')
    Xn, yn = nn_classifier.make_sample_data()
    nn = nn_classifier.NNClassifier()
    print('nn acc', nn.train(Xn, yn))

    print('\n--- Chatbot demo ---')
    print(nlp_chatbot.respond('I have a fever'))

if __name__ == '__main__':
    demo()
