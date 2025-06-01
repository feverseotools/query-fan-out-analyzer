"""
QFAP Core Module
Core functionality for query analysis and fan-out prediction
"""

from .fanout_engine import ProfessionalFanOutEngine, SubQueryPrediction, QueryAnalysis

__all__ = ['ProfessionalFanOutEngine', 'SubQueryPrediction', 'QueryAnalysis']
