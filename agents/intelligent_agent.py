"""Intelligent Agent Implementation with PEAS Architecture

PEAS Model for Hospital Resource Management Agent:
- Performance: Maximize patient care, minimize wait times, optimize resource utilization
- Environment: Hospital with beds, staff, patients, equipment
- Actuators: Allocate beds, schedule surgeries, assign staff, triage patients
- Sensors: Patient data, bed availability, staff schedules, equipment status

This agent demonstrates:
1. Goal-based reasoning
2. Multi-objective optimization
3. Real-time decision making
4. Integration of multiple AI techniques
"""

from typing import Dict, List, Any
from modules import (
    bed_allocation,
    scheduling_csp,
    expert_system,
    fuzzy_triage,
    genetic_optimizer,
)


class HospitalAgent:
    """Intelligent agent for hospital resource management using PEAS architecture.
    
    This agent integrates multiple AI techniques to manage hospital resources:
    - A* search for bed allocation
    - CSP for staff scheduling
    - Rule-based expert system for medical diagnosis
    - Fuzzy logic for patient prioritization
    - Genetic algorithms for resource optimization
    """
    
    def __init__(self, beds: List[Dict], staff: List[Dict], rules: List[Dict]):
        """Initialize the hospital agent with environment state.
        
        Args:
            beds: List of bed resources with attributes (id, icu, vent, location, etc.)
            staff: List of staff with roles and availability
            rules: Medical knowledge base rules for expert system
        """
        self.beds = beds
        self.staff = staff
        self.expert_system = expert_system.ExpertSystem(rules)
        
        # Agent state
        self.patients_queue = []
        self.scheduled_surgeries = []
        self.allocated_beds = {}
        
    def perceive(self, patient_data: Dict) -> Dict[str, Any]:
        """Sensors: Gather information about incoming patient.
        
        Args:
            patient_data: Dictionary with patient vitals and requirements
            
        Returns:
            Processed perception with priority and medical assessment
        """
        # Use fuzzy logic to compute patient priority
        priority = fuzzy_triage.compute_priority(
            patient_data.get('temp', 37.0),
            patient_data.get('sbp', 120),
            patient_data.get('pain', 0)
        )
        
        # Use expert system for medical assessment
        for symptom in patient_data.get('symptoms', []):
            self.expert_system.assert_fact(symptom)
        self.expert_system.infer()
        
        diagnosis = list(self.expert_system.facts)
        
        return {
            'patient_id': patient_data.get('id'),
            'priority': priority,
            'diagnosis': diagnosis,
            'needs_icu': patient_data.get('needs_icu', False),
            'needs_vent': patient_data.get('needs_vent', False),
            'location': patient_data.get('location', (0, 0))
        }
    
    def decide(self, perception: Dict) -> Dict[str, Any]:
        """Goal-based reasoning: Decide on actions based on perception.
        
        Args:
            perception: Processed patient information
            
        Returns:
            Decision with bed allocation and scheduling recommendations
        """
        # Goal 1: Allocate appropriate bed using A* search
        bed = bed_allocation.allocate_bed(perception, self.beds)
        
        # Goal 2: Prioritize patient in queue
        self.patients_queue.append(perception)
        self.patients_queue.sort(key=lambda p: p['priority'], reverse=True)
        
        # Goal 3: Optimize resource allocation using GA if queue is large
        if len(self.patients_queue) > 5:
            optimal_allocation = genetic_optimizer.ga_optimize(
                self.patients_queue[:10], 
                self.beds,
                pop_size=30,
                gens=20
            )
        else:
            optimal_allocation = None
        
        return {
            'allocated_bed': bed,
            'queue_position': self.patients_queue.index(perception),
            'priority': perception['priority'],
            'diagnosis': perception['diagnosis'],
            'optimal_allocation': optimal_allocation
        }
    
    def act(self, decision: Dict) -> str:
        """Actuators: Execute the decision.
        
        Args:
            decision: Decision dictionary from decide()
            
        Returns:
            Action report string
        """
        bed = decision['allocated_bed']
        if bed:
            self.allocated_beds[decision.get('patient_id', 'unknown')] = bed
            bed['is_occupied'] = True
            action = f"Allocated bed {bed['id']} (Priority: {decision['priority']:.1f})"
        else:
            action = f"No bed available. Queue position: {decision['queue_position']}"
        
        if decision['diagnosis']:
            action += f" | Diagnosis: {', '.join(decision['diagnosis'])}"
        
        return action
    
    def schedule_surgery(self, surgeries: List[Dict], time_slots: List[str]) -> Dict:
        """Schedule surgeries using CSP solver.
        
        Args:
            surgeries: List of surgery requirements
            time_slots: Available time slots
            
        Returns:
            Surgery schedule or None if infeasible
        """
        schedule = scheduling_csp.schedule_surgeries(self.staff, surgeries, time_slots)
        if schedule:
            self.scheduled_surgeries.extend(surgeries)
        return schedule
    
    def get_status(self) -> Dict:
        """Get current agent state and performance metrics.
        
        Returns:
            Status dictionary with metrics
        """
        occupied_beds = sum(1 for b in self.beds if b.get('is_occupied', False))
        return {
            'total_beds': len(self.beds),
            'occupied_beds': occupied_beds,
            'available_beds': len(self.beds) - occupied_beds,
            'queue_length': len(self.patients_queue),
            'scheduled_surgeries': len(self.scheduled_surgeries),
            'avg_priority': sum(p['priority'] for p in self.patients_queue) / max(len(self.patients_queue), 1)
        }


def demo_agent():
    """Demonstrate the intelligent agent in action."""
    print("=== Intelligent Hospital Agent Demo (PEAS Architecture) ===\n")
    
    # Initialize environment
    beds = [
        {'id': 'ICU-1', 'is_occupied': False, 'icu': True, 'vent': True, 'location': (0, 0)},
        {'id': 'ICU-2', 'is_occupied': False, 'icu': True, 'vent': False, 'location': (0, 1)},
        {'id': 'Ward-1', 'is_occupied': False, 'icu': False, 'vent': False, 'location': (5, 5)},
        {'id': 'Ward-2', 'is_occupied': False, 'icu': False, 'vent': False, 'location': (5, 6)},
    ]
    
    staff = [
        {'id': 'Dr. Smith', 'roles': ['surgeon'], 'max_slots': 4},
        {'id': 'Dr. Jones', 'roles': ['anesthetist'], 'max_slots': 4},
        {'id': 'Nurse Kelly', 'roles': ['nurse'], 'max_slots': 8},
    ]
    
    rules = [
        {'if': ['fever', 'cough'], 'then': ['possible_infection']},
        {'if': ['possible_infection', 'high_wbc'], 'then': ['bacterial_infection']},
        {'if': ['chest_pain', 'shortness_of_breath'], 'then': ['cardiac_event']},
    ]
    
    agent = HospitalAgent(beds, staff, rules)
    
    # Simulate incoming patients
    patients = [
        {
            'id': 'P001',
            'temp': 39.5,
            'sbp': 145,
            'pain': 8,
            'symptoms': ['fever', 'cough', 'high_wbc'],
            'needs_icu': True,
            'needs_vent': False,
            'location': (1, 1)
        },
        {
            'id': 'P002',
            'temp': 37.0,
            'sbp': 120,
            'pain': 3,
            'symptoms': [],
            'needs_icu': False,
            'needs_vent': False,
            'location': (6, 5)
        },
        {
            'id': 'P003',
            'temp': 38.2,
            'sbp': 160,
            'pain': 9,
            'symptoms': ['chest_pain', 'shortness_of_breath'],
            'needs_icu': True,
            'needs_vent': True,
            'location': (0, 2)
        }
    ]
    
    print("Processing patients through PEAS cycle:\n")
    for patient in patients:
        print(f"Patient {patient['id']}:")
        
        # PEAS Cycle
        perception = agent.perceive(patient)
        print(f"  Sensors → Priority: {perception['priority']:.1f}, Diagnosis: {perception['diagnosis']}")
        
        decision = agent.decide(perception)
        print(f"  Reasoning → {decision}")
        
        action = agent.act(decision)
        print(f"  Actuators → {action}\n")
    
    # Schedule surgeries
    print("\n--- Surgery Scheduling (CSP) ---")
    surgeries = [
        {'id': 'Surgery-1', 'required_roles': ['surgeon', 'anesthetist'], 'duration_slots': 2}
    ]
    schedule = agent.schedule_surgery(surgeries, ['08:00', '10:00', '12:00', '14:00'])
    print(f"Schedule: {schedule}\n")
    
    # Agent status
    print("--- Agent Status ---")
    status = agent.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")


if __name__ == '__main__':
    demo_agent()
