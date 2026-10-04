# What I checked, and what the agent got wrong

## What the agent got wrong
During the initial review, the agent failed to identify the critical integer floor division bug (`//`) in `km_wachter.py`, which caused precision loss by rounding down vehicle wear percentages to 0% and hiding nearly-due maintenance tasks. Additionally, the agent incorrectly implemented the metric unit conversion math in `fleet_utils.py` by multiplying by `1.609` instead of dividing, which artificially inflated the distance logs sent to the UK partner garage. It also missed structural `KeyError` hazards in `fleet_report.py` when processing cars with incomplete service logs.

## What I checked before I accepted its work
I ran the automated unit test suite using `pytest` to confirm that the new and existing checks pass cleanly. I also thoroughly executed the `verify.py` acceptance engine locally to ensure that float wear values are computed properly without rounding down, cars missing baseline telemetry logs do not crash the integration workflow, and that the core 15,000 km and 80% business rules remain completely untouched.

## What the data actually said
The telemetry records from `fleet_history.csv` proved that common assumptions about total absolute mileage (`odometer_km`) and total vehicle age (`age_years`) are completely identical across both functioning and broken vehicles, showing no predictive gap. Instead, the factors that strongly predict operational breakdown risks are active metrics: the total distance accumulated since a car's last formal check (`km_since_service`), the average daily strain (`avg_daily_km`), and the structural load intensity (`load_factor`).
