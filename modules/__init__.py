"""modules package re-exporting core AI hospital functionality.

This package provides a stable import path `modules.<module>` for the
project. It re-exports the main functions / classes from individual
module files.
"""

from . import bed_allocation as bed_allocation
from . import scheduling_csp as scheduling_csp
from . import expert_system as expert_system
from . import fuzzy_triage as fuzzy_triage
from . import genetic_optimizer as genetic_optimizer
from . import ml_predictor as ml_predictor
from . import nn_classifier as nn_classifier
from . import nlp_chatbot as nlp_chatbot

__all__ = [
    'bed_allocation',
    'scheduling_csp',
    'expert_system',
    'fuzzy_triage',
    'genetic_optimizer',
    'ml_predictor',
    'nn_classifier',
    'nlp_chatbot',
]
