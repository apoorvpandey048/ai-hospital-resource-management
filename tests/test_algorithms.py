"""Comprehensive functional tests for AI Hospital modules

Tests cover:
1. Basic functionality
2. Edge cases
3. Error handling
4. Integration scenarios
"""
import pytest
from modules import (
    bed_allocation,
    scheduling_csp,
    expert_system,
    fuzzy_triage,
    genetic_optimizer,
    nlp_chatbot
)


class TestBedAllocation:
    """Tests for A* bed allocation module"""
    
    def test_allocate_available_bed(self):
        patient = {'id': 'p1', 'needs_icu': True, 'needs_vent': False, 'location': (0, 0)}
        beds = [
            {'id': 'b1', 'is_occupied': False, 'icu': True, 'vent': False, 'location': (1, 0)}
        ]
        result = bed_allocation.allocate_bed(patient, beds)
        assert result is not None
        assert result['id'] == 'b1'
    
    def test_no_available_beds(self):
        patient = {'id': 'p1', 'needs_icu': True, 'location': (0, 0)}
        beds = [
            {'id': 'b1', 'is_occupied': True, 'icu': True, 'location': (1, 0)}
        ]
        result = bed_allocation.allocate_bed(patient, beds)
        assert result is None
    
    def test_feature_mismatch_penalty(self):
        patient = {'id': 'p1', 'needs_icu': True, 'location': (0, 0)}
        beds = [
            {'id': 'b1', 'is_occupied': False, 'icu': False, 'location': (1, 0)},  # close but wrong type
            {'id': 'b2', 'is_occupied': False, 'icu': True, 'location': (10, 10)},  # far but right type
        ]
        result = bed_allocation.allocate_bed(patient, beds)
        # Should prefer ICU bed despite distance
        assert result['icu'] == True


class TestSchedulingCSP:
    """Tests for CSP scheduling module"""
    
    def test_feasible_schedule(self):
        staff = [
            {'id': 's1', 'roles': ['surgeon'], 'max_slots': 4},
            {'id': 's2', 'roles': ['anesthetist'], 'max_slots': 4},
        ]
        surgeries = [
            {'id': 'op1', 'required_roles': ['surgeon', 'anesthetist'], 'duration_slots': 2}
        ]
        slots = ['08:00', '10:00', '12:00']
        result = scheduling_csp.schedule_surgeries(staff, surgeries, slots)
        assert result is not None
        assert 'op1' in result
    
    def test_infeasible_schedule(self):
        staff = [
            {'id': 's1', 'roles': ['surgeon'], 'max_slots': 1},
        ]
        surgeries = [
            {'id': 'op1', 'required_roles': ['surgeon', 'anesthetist'], 'duration_slots': 2}
        ]
        slots = ['08:00']
        result = scheduling_csp.schedule_surgeries(staff, surgeries, slots)
        # Should fail - missing anesthetist
        assert result is None


class TestExpertSystem:
    """Tests for rule-based expert system"""
    
    def test_forward_chaining(self):
        rules = [
            {'if': ['fever', 'cough'], 'then': ['possible_infection']},
            {'if': ['possible_infection', 'high_wbc'], 'then': ['bacterial_infection']},
        ]
        es = expert_system.ExpertSystem(rules)
        es.assert_fact('fever')
        es.assert_fact('cough')
        es.assert_fact('high_wbc')
        es.infer()
        
        assert 'possible_infection' in es.facts
        assert 'bacterial_infection' in es.facts
    
    def test_no_inference_without_facts(self):
        rules = [
            {'if': ['fever', 'cough'], 'then': ['possible_infection']},
        ]
        es = expert_system.ExpertSystem(rules)
        es.assert_fact('fever')  # Only one fact
        es.infer()
        
        assert 'possible_infection' not in es.facts
    
    def test_query(self):
        rules = [
            {'if': ['symptom_a'], 'then': ['diagnosis_x']},
        ]
        es = expert_system.ExpertSystem(rules)
        es.assert_fact('symptom_a')
        es.infer()
        
        assert es.query('diagnosis_x') == True
        assert es.query('diagnosis_y') == False


class TestFuzzyTriage:
    """Tests for fuzzy logic triage system"""
    
    def test_high_priority(self):
        # High fever, high BP, severe pain
        priority = fuzzy_triage.compute_priority(40.0, 160, 9)
        assert priority > 70  # Should be high priority
    
    def test_low_priority(self):
        # Normal vitals
        priority = fuzzy_triage.compute_priority(37.0, 120, 2)
        assert priority < 40  # Should be low priority
    
    def test_medium_priority(self):
        # Moderate vitals
        priority = fuzzy_triage.compute_priority(38.0, 130, 5)
        assert 40 <= priority <= 70  # Should be medium
    
    def test_edge_case_zero_denom(self):
        # Test handling of edge case
        priority = fuzzy_triage.compute_priority(37.0, 120, 0)
        assert priority >= 0  # Should not crash


class TestGeneticOptimizer:
    """Tests for genetic algorithm"""
    
    def test_optimization_converges(self):
        patients = [
            {'id': 'p1', 'needs_icu': True, 'location': (0, 0)},
            {'id': 'p2', 'needs_icu': False, 'location': (5, 5)},
        ]
        beds = [
            {'id': 'b1', 'icu': True, 'location': (1, 0)},
            {'id': 'b2', 'icu': False, 'location': (6, 6)},
        ]
        result = genetic_optimizer.ga_optimize(patients, beds, pop_size=10, gens=5)
        
        assert len(result) == len(patients)
        assert all(-1 <= x < len(beds) for x in result)
    
    def test_fitness_function(self):
        chrom = [0, 1]
        patients = [
            {'id': 'p1', 'needs_icu': True, 'location': (0, 0)},
            {'id': 'p2', 'needs_icu': False, 'location': (5, 5)},
        ]
        beds = [
            {'id': 'b1', 'icu': True, 'location': (1, 0)},
            {'id': 'b2', 'icu': False, 'location': (6, 6)},
        ]
        fitness = genetic_optimizer.fitness(chrom, patients, beds)
        assert isinstance(fitness, (int, float))
        assert fitness > 0  # Good allocation should have positive fitness


class TestNLPChatbot:
    """Tests for chatbot"""
    
    def test_greeting_response(self):
        response = nlp_chatbot.respond('Hello')
        assert 'Hello' in response or 'help' in response.lower()
    
    def test_appointment_query(self):
        response = nlp_chatbot.respond('I need an appointment')
        assert 'appointment' in response.lower()
    
    def test_fever_query(self):
        response = nlp_chatbot.respond('I have a fever')
        assert 'fever' in response.lower() or 'temperature' in response.lower()
    
    def test_unknown_query_fallback(self):
        response = nlp_chatbot.respond('Random gibberish xyz123')
        assert 'help' in response.lower() or 'ask' in response.lower()


class TestIntegration:
    """Integration tests combining multiple modules"""
    
    def test_full_patient_workflow(self):
        # Test a complete patient admission workflow
        
        # 1. Triage
        priority = fuzzy_triage.compute_priority(39.0, 140, 7)
        assert priority > 50  # Patient is high priority
        
        # 2. Diagnosis
        rules = [{'if': ['fever'], 'then': ['needs_monitoring']}]
        es = expert_system.ExpertSystem(rules)
        es.assert_fact('fever')
        es.infer()
        assert 'needs_monitoring' in es.facts
        
        # 3. Bed allocation
        patient = {'id': 'p1', 'needs_icu': True, 'location': (0, 0)}
        beds = [{'id': 'b1', 'is_occupied': False, 'icu': True, 'location': (1, 0)}]
        bed = bed_allocation.allocate_bed(patient, beds)
        assert bed is not None
        
        # Workflow complete
        assert True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
