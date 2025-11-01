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
    print('='*60)
    print('AI Hospital Resource Management System - Complete Demo')
    print('='*60)
    
    print('\n--- 1. Bed Allocation (A* Search) ---')
    patient = {'id': 'p1', 'needs_icu': True, 'needs_vent': False, 'location': (2,2)}
    beds = [
        {'id': 'b1', 'is_occupied': False, 'icu': True, 'vent': False, 'location': (3,2)},
        {'id': 'b2', 'is_occupied': False, 'icu': False, 'vent': False, 'location': (10,10)},
    ]
    result = bed_allocation.allocate_bed(patient, beds)
    print(f'Patient {patient["id"]} allocated to bed: {result}')

    print('\n--- 2. Patient Triage (Fuzzy Logic) ---')
    priority = fuzzy_triage.compute_priority(39.0, 130, 8)
    print(f'Patient vitals: Temp=39.0°C, BP=130, Pain=8/10')
    print(f'Computed priority score: {priority:.1f}/100 (higher = more urgent)')
    
    print('\n--- 3. Staff & Surgery Scheduling (CSP Solver) ---')
    staff = [
        {'id': 's1', 'roles': ['surgeon'], 'max_slots': 4},
        {'id': 's2', 'roles': ['anesthetist'], 'max_slots': 4},
    ]
    surgeries = [
        {'id': 'op1', 'required_roles': ['surgeon', 'anesthetist'], 'duration_slots': 2},
    ]
    slots = ['08:00', '09:00', '10:00', '11:00']
    schedule = scheduling_csp.schedule_surgeries(staff, surgeries, slots)
    print(f'Surgery schedule: {schedule}')

    print('\n--- 4. Medical Expert System (Rule-based Inference) ---')
    rules = [
        {'if': ['fever', 'cough'], 'then': ['possible_infection']},
        {'if': ['possible_infection', 'high_wbc'], 'then': ['bacterial_infection']},
    ]
    es = expert_system.ExpertSystem(rules)
    es.assert_fact('fever')
    es.assert_fact('cough')
    es.assert_fact('high_wbc')
    es.infer()
    print(f'Input symptoms: fever, cough, high_wbc')
    print(f'Expert system inferred: {es.facts}')

    print('\n--- 5. Resource Optimization (Genetic Algorithm) ---')
    patients = [
        {'id': 'p1', 'needs_icu': True, 'needs_vent': False, 'location': (0,0)},
        {'id': 'p2', 'needs_icu': False, 'needs_vent': False, 'location': (5,5)},
    ]
    beds = [
        {'id': 'b1', 'icu': True, 'vent': False, 'location': (1,0)},
        {'id': 'b2', 'icu': False, 'vent': False, 'location': (6,6)},
    ]
    allocation = genetic_optimizer.ga_optimize(patients, beds, pop_size=20, gens=10)
    print(f'Optimal bed allocation: {allocation}')
    print(f'(chromosome: [bed_index for each patient, -1=unassigned])')

    print('\n--- 6. Patient Admission Prediction (Machine Learning) ---')
    X, y = ml_predictor.make_sample_dataset()
    ap = ml_predictor.AdmissionPredictor()
    acc = ap.train(X, y)
    print(f'Logistic Regression model trained on 200 samples')
    print(f'Test accuracy: {acc:.2%}')
    pred = ap.predict([30, 39.0, 115, 9])
    print(f'Sample prediction (age=30, temp=39, sbp=115, pain=9): {"Admit" if pred else "Discharge"}')

    print('\n--- 7. Disease Classification (Neural Network) ---')
    Xn, yn = nn_classifier.make_sample_data()
    nn = nn_classifier.NNClassifier()
    nn_acc = nn.train(Xn, yn)
    print(f'MLP Neural Network trained on 200 samples')
    print(f'Test accuracy: {nn_acc:.2%}')

    print('\n--- 8. Patient Query Chatbot (NLP) ---')
    queries = ['Hi there', 'I have a fever', 'I need an appointment']
    for q in queries:
        response = nlp_chatbot.respond(q)
        print(f'Q: {q}')
        print(f'A: {response}')
    
    print('\n' + '='*60)
    print('Demo complete! All 8 AI modules demonstrated.')
    print('='*60)

if __name__ == '__main__':
    demo()
