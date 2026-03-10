"""
AI Stylist Package
"""

__version__ = "1.0.0"

# Make key classes available at package level
from ai_stylist.schemas import (
    UserQuery, UserContext, Product, CategorySpec,
    Occasion, Style, Color, Gender, Season
)
from ai_stylist.orchestrator import Orchestrator

__all__ = [
    'UserQuery', 'UserContext', 'Product', 'CategorySpec',
    'Occasion', 'Style', 'Color', 'Gender', 'Season',
    'Orchestrator'
]