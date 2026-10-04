# fleet_utils.py
"""Shared math helpers and distance utilities for fleet metrics."""

# 1 Mile = 1.609 Kilometers. To convert Kilometers to Miles, divide by 1.609.
MILES_PER_KM: float = 1.609


def km_to_miles(km: float) -> float:
    """Converts metric distances over to British miles standard."""
    return km / MILES_PER_KM


def format_number(value: float) -> str:
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    return f"{int(value)}%"


def mean(values: list) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)
