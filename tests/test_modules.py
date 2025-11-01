import importlib

modules = [
    'modules.bed_allocation',
    'modules.scheduling_csp',
    'modules.expert_system',
    'modules.fuzzy_triage',
    'modules.genetic_optimizer',
    'modules.ml_predictor',
    'modules.nn_classifier',
    'modules.nlp_chatbot',
]


def test_imports():
    for m in modules:
        mod = importlib.import_module(m)
        assert mod is not None
