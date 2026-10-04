# km_wachter.py
"""KM-Waechter decides when a Vossberg Mobility car needs a service."""

SERVICE_INTERVAL_KM: int = 15000
WARN_AT_PERCENT: int = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Calculates precision wear percentage instead of flooring numbers."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Flags if a car has used up 80% or more of its service window."""
    if "last_service_km" not in car:
        return False

    last_service: int = car["last_service_km"]
    km_since: int = car["odometer"] - last_service
    pct: float = wear_percent(km_since, SERVICE_INTERVAL_KM)

    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list) -> list:
    """Scans active fleet records for immediate maintenance needs."""
    flagged: list = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
