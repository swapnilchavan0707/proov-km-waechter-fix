# Summary: Total odometer mileage and age do not correlate with breakdown trends.
# Fleet failure is strongly predicted by km_since_service, avg_daily_km, and load_factor.

import pandas as pd

# 1. Load telemetry history logs
df = pd.read_csv("fleet_history.csv")

# 2. Extract min/max scaling criteria from critical predictors
k_min, k_max = df['km_since_service'].min(), df['km_since_service'].max()
d_min, d_max = df['avg_daily_km'].min(), df['avg_daily_km'].max()
l_min, l_max = df['load_factor'].min(), df['load_factor'].max()

# 3. Calculate a normalized operational strain index (0 - 100)
df['risk_score'] = (
    0.40 * ((df['km_since_service'] - k_min) / (k_max - k_min)) +
    0.35 * ((df['avg_daily_km'] - d_min) / (d_max - d_min)) +
    0.25 * ((df['load_factor'] - l_min) / (l_max - l_min))
) * 100

# 4. Sort vehicles by critical maintenance exposure profile
ranked_fleet = df.sort_values(by='risk_score', ascending=False)

print("\n--- CRITICAL BREAKDOWN RISK RANKINGS ---")
for idx, car in ranked_fleet.head(15).iterrows():
    print(f"Car: {car['car_id']} | Risk Score: {car['risk_score']:.1f} | Dist Since Service: {car['km_since_service']}km")
