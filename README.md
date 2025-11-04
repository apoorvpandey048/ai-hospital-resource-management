# 🏥 AI-Driven Hospital Resource Management System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI Tests](https://github.com/apoorvpandey048/ai-hospital-resource-management/workflows/CI/badge.svg)](https://github.com/apoorvpandey048/ai-hospital-resource-management/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive AI-powered hospital resource management system demonstrating **9 distinct AI algorithms** including search algorithms, constraint satisfaction, expert systems, fuzzy logic, genetic algorithms, machine learning, neural networks, and natural language processing.

## 📋 Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [AI Modules](#-ai-modules)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Technologies](#-technologies)
- [Academic Context](#-academic-context)

## ✨ Features

### Core AI Algorithms
1. **A\* Search Algorithm** - Optimal bed allocation with heuristic search
2. **CSP Solver** - Staff and surgery scheduling with constraint propagation
3. **Rule-Based Expert System** - Forward chaining inference for medical diagnosis
4. **Fuzzy Logic System** - Patient triage priority using Mamdani inference
5. **Genetic Algorithm** - Resource optimization with elitism and crossover
6. **Machine Learning** - Admission prediction using Logistic Regression
7. **Neural Network** - Disease classification using Multi-Layer Perceptron
8. **NLP Chatbot** - Patient query handling with regex-based intent recognition
9. **Intelligent Agent** - PEAS architecture integrating all modules

### Web Interfaces
- **Streamlit Dashboard** - Interactive web UI for triage, allocation, and chatbot
- **Flask REST API** - RESTful endpoints for system integration
- **Comprehensive Testing** - 19 functional tests covering all algorithms

## 📁 Project Structure

```
ai-hospital-resource-management/
├── modules/                      # Core AI algorithm implementations
│   ├── bed_allocation.py        # A* search for bed allocation
│   ├── scheduling_csp.py        # CSP solver for scheduling
│   ├── expert_system.py         # Rule-based inference engine
│   ├── fuzzy_triage.py          # Fuzzy logic patient priority
│   ├── genetic_optimizer.py     # Genetic algorithm optimizer
│   ├── ml_predictor.py          # ML admission predictor
│   ├── nn_classifier.py         # Neural network classifier
│   └── nlp_chatbot.py           # NLP chatbot
├── agents/                       # Intelligent agent integration
│   └── intelligent_agent.py     # PEAS architecture agent (250+ lines)
├── app/                          # Web interfaces
│   ├── dashboard_streamlit.py   # Streamlit dashboard
│   └── api_flask.py             # Flask REST API
├── data/                         # Sample datasets
│   ├── patients.csv             # Patient records
│   ├── beds.csv                 # Hospital bed inventory
│   ├── staff.csv                # Staff availability
│   └── medical_rules.json       # Expert system rules
├── tests/                        # Test suite
│   └── test_algorithms.py       # 19 functional tests
├── docs/                         # Comprehensive documentation
│   ├── project_report.md        # Academic report (350+ lines)
│   └── implementation_guide.md  # Technical guide (450+ lines)
├── .github/workflows/           # CI/CD pipeline
│   └── ci.yml                   # GitHub Actions workflow
├── run_demo.py                  # Complete system demonstration
├── requirements.txt             # Python dependencies
├── EVALUATION_SUMMARY.md        # Project evaluation checklist
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```powershell
git clone https://github.com/apoorvpandey048/ai-hospital-resource-management.git
cd ai-hospital-resource-management
```

2. **Create virtual environment (recommended)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

### Running the System

#### Complete Demo (All 8 AI Modules)
```powershell
python run_demo.py
```

#### Intelligent Agent (PEAS Architecture)
```powershell
$env:PYTHONPATH="$PWD"
python agents/intelligent_agent.py
```

#### Web Dashboard (Streamlit)
```powershell
streamlit run app/dashboard_streamlit.py
```

#### REST API (Flask)
```powershell
python app/api_flask.py
```

#### Run Tests
```powershell
pytest tests/test_algorithms.py -v
```

## 🤖 AI Modules

### 1. Bed Allocation (A\* Search)
- **Algorithm**: A\* pathfinding with Manhattan distance heuristic
- **Features**: ICU/ventilator matching, location-based optimization
- **Complexity**: O(b^d) where b=branching factor, d=depth
- **Use Case**: Optimal bed assignment considering patient requirements

```python
from modules.bed_allocation import allocate_bed

patient = {'id': 'P001', 'icu': True, 'vent': False, 'location': (0, 0)}
beds = [{'id': 'B1', 'is_occupied': False, 'icu': True, 'location': (3, 2)}]
assigned_bed = allocate_bed(patient, beds)
```

### 2. Staff Scheduling (CSP Solver)
- **Algorithm**: Backtracking with forward checking
- **Features**: Multi-role scheduling, time slot constraints
- **Complexity**: O(d^n) where d=domain size, n=variables
- **Use Case**: Surgery and staff schedule optimization

```python
from modules.scheduling_csp import schedule_surgeries

staff = [{'id': 'S1', 'roles': ['surgeon'], 'available': [0, 1]}]
surgeries = [{'id': 'OP1', 'duration': 2, 'roles': ['surgeon']}]
schedule = schedule_surgeries(surgeries, staff, time_slots=10)
```

### 3. Expert System (Forward Chaining)
- **Algorithm**: Rule-based inference with forward chaining
- **Features**: Medical diagnosis, symptom analysis
- **Complexity**: O(r × f) where r=rules, f=facts
- **Use Case**: Automated diagnosis based on symptoms

```python
from modules.expert_system import ExpertSystem

es = ExpertSystem()
es.add_rule({"fever", "cough"}, "possible_infection")
es.assert_fact("fever")
es.assert_fact("cough")
conclusions = es.infer()  # Returns: {'possible_infection'}
```

### 4. Fuzzy Logic Triage
- **Algorithm**: Mamdani-style fuzzy inference
- **Features**: Vital signs analysis (temp, BP, pain)
- **Complexity**: O(n × m) where n=inputs, m=rules
- **Use Case**: Patient priority scoring for triage

```python
from modules.fuzzy_triage import compute_priority

priority = compute_priority(temp=39.0, bp=130, pain=8)
# Returns: 90.0 (scale 0-100)
```

### 5. Genetic Algorithm Optimizer
- **Algorithm**: GA with elitism, tournament selection
- **Features**: Crossover, mutation, multi-generation evolution
- **Complexity**: O(g × p × n) where g=generations, p=population, n=chromosome length
- **Use Case**: Optimal resource allocation across patients

```python
from modules.genetic_optimizer import ga_optimize

patients = [{'id': 'P1', 'priority': 80}]
beds = [{'id': 'B1', 'capacity': 100}]
solution = ga_optimize(patients, beds, pop_size=50, generations=100)
```

### 6. ML Admission Predictor
- **Algorithm**: Logistic Regression (scikit-learn)
- **Features**: Patient history-based admission prediction
- **Complexity**: O(n × d) training, O(d) prediction
- **Use Case**: Predict admission likelihood from vitals

```python
from modules.ml_predictor import AdmissionPredictor

predictor = AdmissionPredictor()
X, y = predictor.make_sample_dataset(n_samples=200)
accuracy = predictor.train(X, y)
prediction = predictor.predict([[30, 39, 115, 9]])  # Returns: 1 (admit)
```

### 7. Neural Network Classifier
- **Algorithm**: Multi-Layer Perceptron (100 hidden units)
- **Features**: Disease classification from symptoms
- **Complexity**: O(n × h × c) where n=features, h=hidden units, c=classes
- **Use Case**: Multi-class disease diagnosis

```python
from modules.nn_classifier import NNClassifier

clf = NNClassifier()
X, y = clf.make_sample_data(n_samples=200)
accuracy = clf.train(X, y)
prediction = clf.predict([[1, 0, 1, 0]])  # Returns disease class
```

### 8. NLP Chatbot
- **Algorithm**: Regex-based pattern matching
- **Features**: Intent recognition for common queries
- **Complexity**: O(n × p) where n=patterns, p=input length
- **Use Case**: Patient query handling

```python
from modules.nlp_chatbot import respond

response = respond("I have a fever")
# Returns: "If you have fever, please measure your temperature..."
```

### 9. Intelligent Agent (PEAS Architecture)
- **Architecture**: Performance, Environment, Actuators, Sensors
- **Integration**: All 8 modules working together
- **Features**: Perceive → Decide → Act cycle
- **Use Case**: Autonomous hospital resource management

```python
from agents.intelligent_agent import HospitalAgent

agent = HospitalAgent()
state = agent.perceive(patients, beds, staff)
decisions = agent.decide(state)
results = agent.act(decisions, state)
```

## 📊 Usage Examples

### REST API Endpoints

```powershell
# Start Flask server
python app/api_flask.py
```

**Allocate Bed**
```bash
curl -X POST http://localhost:5000/allocate ^
  -H "Content-Type: application/json" ^
  -d "{\"patient\": {\"id\": \"P1\", \"icu\": true}, \"beds\": []}"
```

**Compute Priority**
```bash
curl -X POST http://localhost:5000/priority ^
  -H "Content-Type: application/json" ^
  -d "{\"temp\": 39, \"bp\": 130, \"pain\": 8}"
```

**Chatbot Query**
```bash
curl -X POST http://localhost:5000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"I have a fever\"}"
```

## 🧪 Testing

### Run All Tests
```powershell
pytest tests/test_algorithms.py -v
```

### Test Coverage
- **19 functional tests** covering all 8 AI modules
- **100% pass rate** (19/19 passing)
- **Integration test** validating full patient workflow
- **Edge cases** tested (infeasible schedules, no beds, zero denominators)

### Test Results
```
tests/test_algorithms.py::TestBedAllocation::test_allocate_available_bed PASSED
tests/test_algorithms.py::TestBedAllocation::test_no_available_beds PASSED
tests/test_algorithms.py::TestBedAllocation::test_feature_mismatch_penalty PASSED
tests/test_algorithms.py::TestSchedulingCSP::test_feasible_schedule PASSED
tests/test_algorithms.py::TestSchedulingCSP::test_infeasible_schedule PASSED
tests/test_algorithms.py::TestExpertSystem::test_forward_chaining PASSED
... (19 total tests passing)
```

## 📖 Documentation

### Comprehensive Guides
1. **[Project Report](docs/project_report.md)** (350+ lines)
   - Problem statement and PEAS model
   - Algorithm descriptions with complexity analysis
   - Experimental results and performance metrics
   - Academic context and conclusions

2. **[Implementation Guide](docs/implementation_guide.md)** (450+ lines)
   - Module architecture and APIs
   - Extension points and customization
   - Testing strategies and deployment guide
   - Best practices and troubleshooting

3. **[Evaluation Summary](EVALUATION_SUMMARY.md)** (255 lines)
   - Comprehensive feature checklist
   - Performance metrics and test results
   - Syllabus coverage mapping
   - Quality assurance validation

## 🔧 Technologies

### Core Technologies
- **Python 3.10+** - Primary language
- **NumPy** - Numerical computing
- **scikit-learn** - Machine learning (LogisticRegression, MLPClassifier)
- **Flask** - REST API framework
- **Streamlit** - Interactive dashboard
- **pytest** - Testing framework

### AI/ML Techniques
- **Search Algorithms**: A\* with heuristics
- **Constraint Satisfaction**: Backtracking with forward checking
- **Knowledge Representation**: Rule-based systems
- **Fuzzy Logic**: Mamdani inference
- **Evolutionary Computing**: Genetic algorithms
- **Supervised Learning**: Classification and regression
- **Natural Language Processing**: Pattern matching and intent recognition
- **Agent Architecture**: PEAS model

### Development Tools
- **GitHub Actions** - CI/CD pipeline
- **Virtual Environment** - Dependency isolation
- **Git** - Version control
- **VS Code** - Development environment

## 🎓 Academic Context

This project demonstrates comprehensive coverage of AI/ML concepts for academic evaluation:

### Syllabus Coverage
- ✅ **Search Algorithms** (A\* search)
- ✅ **Constraint Satisfaction Problems** (CSP solver)
- ✅ **Knowledge Representation** (Expert systems)
- ✅ **Fuzzy Logic** (Triage system)
- ✅ **Optimization** (Genetic algorithms)
- ✅ **Machine Learning** (Classification, regression)
- ✅ **Neural Networks** (MLP classifier)
- ✅ **Natural Language Processing** (Chatbot)
- ✅ **Intelligent Agents** (PEAS architecture)

### Key Metrics
- **Total Lines of Code**: 2,500+
- **Documentation**: 1,000+ lines
- **Test Coverage**: 19 functional tests
- **Modules**: 9 distinct AI algorithms
- **Complexity Analysis**: Provided for all algorithms
- **Performance**: All tests passing, demo functional

## 🤝 Contributing

This is an academic project for evaluation purposes. For questions or suggestions:

1. **Issues**: Submit GitHub issues for bugs or feature requests
2. **Documentation**: Refer to [Implementation Guide](docs/implementation_guide.md)
3. **Testing**: All PRs must pass CI checks (19/19 tests)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Apoorv Pandey**
- GitHub: [@apoorvpandey048](https://github.com/apoorvpandey048)
- Repository: [ai-hospital-resource-management](https://github.com/apoorvpandey048/ai-hospital-resource-management)

## 🙏 Acknowledgments

- Python community for excellent AI/ML libraries
- Academic institution for project requirements and guidance
- Open-source contributors for inspiration and best practices

---

**Project Status**: ✅ Complete and ready for academic evaluation

**Last Updated**: 2025
**Version**: 1.0.0
