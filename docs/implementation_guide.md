# Implementation Guide

## Overview

This guide provides technical details for developers working on the AI Hospital Resource Management System.

## Project Structure

```
ai-hospital-resource-management/
├── modules/          # Core AI algorithm implementations
├── agents/           # Intelligent agent with PEAS architecture
├── app/              # User interfaces (Streamlit, Flask)
├── data/             # Sample datasets
├── tests/            # Unit and integration tests
├── docs/             # Documentation
└── .github/workflows # CI/CD pipelines
```

## Module Details

### 1. bed_allocation.py (A* Search)

**Purpose:** Allocate optimal bed to incoming patient

**Key Functions:**
- `manhattan(a, b)` - Compute Manhattan distance
- `allocate_bed(patient, beds)` - Main allocation function

**Algorithm Complexity:**
- Time: O(n) where n = number of available beds
- Space: O(1)

**Extension Points:**
- Replace Manhattan with Euclidean distance
- Add more bed features (isolation, monitoring level)
- Implement full A* with priority queue

### 2. scheduling_csp.py (Constraint Satisfaction)

**Purpose:** Schedule surgeries and staff assignments

**Key Functions:**
- `schedule_surgeries(staff, surgeries, slots)` - CSP solver

**Algorithm Complexity:**
- Time: O(d^n) worst case, typically O(n log n) with pruning
- Space: O(n) for assignment tracking

**Constraints:**
1. Role matching: surgery.required_roles ⊆ staff.roles
2. Capacity: Σ(assigned_slots) ≤ staff.max_slots
3. Temporal: no overlapping assignments

**Extension Points:**
- Add OR-Tools for better performance
- Implement arc consistency (AC-3)
- Add soft constraints with preferences

### 3. expert_system.py (Rule-based Inference)

**Purpose:** Medical diagnosis from symptoms

**Key Classes:**
- `ExpertSystem` - Forward chaining inference engine

**Algorithm Complexity:**
- Time: O(R × F × I) where R=rules, F=facts, I=iterations
- Space: O(F) for fact storage

**Knowledge Representation:**
```python
{
    'if': ['symptom1', 'symptom2'],    # Antecedent
    'then': ['diagnosis']               # Consequent
}
```

**Extension Points:**
- Add backward chaining for goal-driven reasoning
- Implement certainty factors (CF model)
- Add explanation facility

### 4. fuzzy_triage.py (Fuzzy Logic)

**Purpose:** Compute patient priority from vital signs

**Key Functions:**
- `fuzz_temp(temp)` - Temperature fuzzy sets
- `fuzz_bp(sbp)` - Blood pressure fuzzy sets
- `fuzz_pain(pain)` - Pain level fuzzy sets
- `compute_priority(temp, sbp, pain)` - Mamdani inference

**Algorithm Complexity:**
- Time: O(R) for R rules
- Space: O(1)

**Fuzzy Sets:**
```
Temperature (°C):
  low:    [35, 37) with triangular membership
  normal: [36, 38] with trapezoidal membership
  high:   (37, 42] with triangular membership
```

**Extension Points:**
- Add more input variables (heart rate, O2 saturation)
- Use Sugeno inference for computational efficiency
- Implement adaptive fuzzy systems

### 5. genetic_optimizer.py (Genetic Algorithm)

**Purpose:** Optimize patient-to-bed assignments

**Key Functions:**
- `fitness(chrom, patients, beds)` - Evaluate chromosome
- `ga_optimize(patients, beds, pop_size, gens)` - GA main loop

**Algorithm Complexity:**
- Time: O(G × P × N) where G=generations, P=population, N=patients
- Space: O(P × N)

**Genetic Operators:**
1. **Selection:** Elitism - keep top 20%
2. **Crossover:** Single-point at random position
3. **Mutation:** 10% probability, random reassignment

**Fitness Function:**
```python
fitness = Σ(feature_matches) - 0.1 * Σ(distances)
```

**Extension Points:**
- Try tournament selection
- Implement multi-point or uniform crossover
- Add adaptive mutation rates
- Use multi-objective optimization (NSGA-II)

### 6. ml_predictor.py (Machine Learning)

**Purpose:** Predict patient admission likelihood

**Key Classes:**
- `AdmissionPredictor` - Wrapper for LogisticRegression

**Algorithm Complexity:**
- Training: O(n × d × i) where n=samples, d=features, i=iterations
- Prediction: O(d)

**Features:**
1. Age (years)
2. Temperature (°C)
3. Systolic BP (mmHg)
4. Pain level (0-10)

**Extension Points:**
- Try ensemble methods (Random Forest, XGBoost)
- Add feature engineering (interactions, polynomials)
- Implement cross-validation
- Add hyperparameter tuning (GridSearchCV)

### 7. nn_classifier.py (Neural Network)

**Purpose:** Classify disease from symptoms

**Key Classes:**
- `NNClassifier` - Wrapper for MLPClassifier

**Architecture:**
```
Input (3) → Hidden (10, ReLU) → Output (1, Sigmoid)
```

**Algorithm Complexity:**
- Training: O(n × h × e) where n=samples, h=hidden neurons, e=epochs
- Prediction: O(h)

**Extension Points:**
- Add more hidden layers (deep learning)
- Try different activations (Leaky ReLU, ELU)
- Implement dropout for regularization
- Use early stopping

### 8. nlp_chatbot.py (Natural Language Processing)

**Purpose:** Answer patient queries

**Key Functions:**
- `respond(message)` - Pattern matching and response generation

**Algorithm Complexity:**
- Time: O(P) where P = number of patterns
- Space: O(P)

**Pattern Format:**
```python
(re.compile(pattern, re.I), response_string)
```

**Extension Points:**
- Use spaCy for entity recognition
- Implement intent classification (sklearn)
- Add context/dialog management
- Use transformers (BERT, GPT) for better understanding

### 9. intelligent_agent.py (PEAS Agent)

**Purpose:** Integrate all modules into intelligent agent

**Key Classes:**
- `HospitalAgent` - Main agent class

**PEAS Cycle:**
```
1. perceive(patient_data) → sensors gather information
2. decide(perception)     → reasoning and planning
3. act(decision)          → actuators execute actions
```

**Extension Points:**
- Add learning capability (Q-learning, policy gradient)
- Implement multi-agent coordination
- Add planning (STRIPS, HTN)

## Testing

### Unit Tests

Location: `tests/test_modules.py`

**Current Coverage:**
- Import tests: ✅
- Functional tests: ⚠️ Needs expansion

**Adding Tests:**
```python
def test_bed_allocation():
    patient = {'id': 'p1', 'needs_icu': True, 'location': (0,0)}
    beds = [{'id': 'b1', 'icu': True, 'location': (1,0)}]
    result = bed_allocation.allocate_bed(patient, beds)
    assert result is not None
    assert result['icu'] == True
```

### Integration Tests

Run full demo: `python run_demo.py`

Expected output: All 8 modules execute without errors

## Performance Optimization

### Profiling

```powershell
python -m cProfile -o output.prof run_demo.py
python -m pstats output.prof
```

### Bottlenecks

1. **GA optimizer**: Most time-consuming (100-200ms)
   - Solution: Reduce population size or generations
   
2. **ML training**: 180ms for 200 samples
   - Solution: Use incremental learning or caching

3. **NN training**: 1.8s for 200 samples
   - Solution: Reduce epochs or use GPU

## Deployment

### Local Development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_demo.py
```

### Web Dashboard

```powershell
streamlit run app/dashboard_streamlit.py
```

### REST API

```powershell
flask run --app app.api_flask
```

### Production Considerations

1. **Database**: Add PostgreSQL for persistence
2. **Caching**: Use Redis for model caching
3. **Monitoring**: Add Prometheus metrics
4. **Logging**: Structured logging with ELK stack
5. **Security**: Add authentication, rate limiting

## Coding Style

- **Format**: PEP 8
- **Docstrings**: Google style
- **Type Hints**: Use typing module
- **Comments**: Explain why, not what

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'sklearn'`

**Solution:**
```powershell
pip install scikit-learn
```

### CI Failures

**Problem:** Tests fail on GitHub Actions

**Solution:** Check `.github/workflows/ci.yml` Python version format (use quotes)

### Performance Issues

**Problem:** Demo takes too long

**Solution:** Reduce GA parameters in `run_demo.py`:
```python
genetic_optimizer.ga_optimize(patients, beds, pop_size=10, gens=5)
```

---

**Last Updated:** November 2025  
**Maintainer:** AI Hospital Team
