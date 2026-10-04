# fleet_report.py
"""Prints the nightly fleet-health summary for Vossberg Mobility."""

from km_wachter import wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car: dict) -> float:
    """Calculates car wear safely even if missing service milestones."""
    last: int = car.get("last_service_km", 0)
    return wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list) -> dict:
    """Compiles exact average wear figures and maintenance flags."""
    if not fleet:
        return {"count": 0, "due": 0, "average_wear": 0.0}

    total_wear: float = 0.0
    due_count: int = 0

    for car in fleet:
        total_wear += car_wear(car)
        if needs_service(car):
            due_count += 1

    average_wear: float = total_wear / len(fleet)
    return {"count": len(fleet), "due": due_count, "average_wear": average_wear}


def print_report(fleet: list) -> None:
    settings: dict = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    
    s: dict = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.2f}%")
    
    total_km: int = sum(car["odometer"] for car in fleet)
    miles: float = fleet_utils.km_to_miles(total_km)
    
    print(f"Fleet distance: {fleet_utils.format_number(miles)} miles")
    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
