import pandas as pd
import numpy as np

class RoofDataSimulation:
    def __init__(self, RAIN_DATA, EFFECTIVE_ROOF_AREA_M2, POPULATION_PER_HOUSEHOLD, TANK_CAPACITY_LITRES, CONSUMPTION_RATE_IN_LITRES, RAINFALL_COEFFICIENT):
        self.POPULATION_PER_HOUSEHOLD = POPULATION_PER_HOUSEHOLD
        self.RAIN_DATA = RAIN_DATA
        self.EFFECTIVE_ROOF_AREA_M2 = EFFECTIVE_ROOF_AREA_M2
        self.TANK_CAPACITY_LITRES = TANK_CAPACITY_LITRES
        self.CONSUMPTION_RATE_IN_LITRES = CONSUMPTION_RATE_IN_LITRES
        self.RAINFALL_COEFFICIENT = RAINFALL_COEFFICIENT
        self.current_date = 0

        # Calculate constant values outside the loop
        self.CONSUMPTION_PER_DAY = self.POPULATION_PER_HOUSEHOLD * self.CONSUMPTION_RATE_IN_LITRES / 1000
        self.TANK_CAPACITY_M3 = self.TANK_CAPACITY_LITRES / 1000

        # Initialize variables outside the loop
        self.volume_at_the_end_m3 = 0

    def generate_daily_volume(self):
        rain_in_mm = self.RAIN_DATA.iloc[self.current_date, 1]
        date = self.RAIN_DATA.iloc[self.current_date, 0]

        volume_generated_m3 = self.EFFECTIVE_ROOF_AREA_M2 * (rain_in_mm / 1000) * self.RAINFALL_COEFFICIENT

        volume_at_the_start_m3 = 0 if self.current_date == 0 else self.volume_at_the_end_m3

        volume_consumed_m3 = min(volume_at_the_start_m3, self.CONSUMPTION_PER_DAY)

        volume_at_the_end_m3 = max(0, volume_at_the_start_m3 + volume_generated_m3 - volume_consumed_m3, self.TANK_CAPACITY_M3)

        overflow = max(0, volume_at_the_start_m3 + volume_generated_m3 - volume_consumed_m3 - self.TANK_CAPACITY_M3)

        demand_met = 1 if volume_at_the_start_m3 >= self.CONSUMPTION_PER_DAY else 0

        self.volume_at_the_end_m3 = volume_at_the_end_m3

        return {
            "Date": date,
            "Rainfall (mm)": rain_in_mm,
            "Effective Roof Area": self.EFFECTIVE_ROOF_AREA_M2,
            "Tank Capacity (litres)": self.TANK_CAPACITY_LITRES,
            "Volume Generated (m3)": volume_generated_m3,
            "Volume in Tank (Start) (m3)": volume_at_the_start_m3,
            "Demand per Day (m3)": self.CONSUMPTION_PER_DAY,
            "Volume Consumed (m3)": volume_consumed_m3,
            "Volume in Tank (End) (m3)": volume_at_the_end_m3,
            "Overflow (m3)": overflow,
            "Demand Met": demand_met,
        }

    def simulate(self):
        daily_data = []  # empty array
        total_days = 0  # Variable to count total days
        total_days_demand_met = 0
        total_volume_generated_from_roof = 0
        total_overflow = 0
        total_rainfall = 0

        for _ in range(len(self.RAIN_DATA)):
            day_data = self.generate_daily_volume()
            daily_data.append(day_data)
            self.current_date += 1
            total_days += 1
            total_volume_generated_from_roof += day_data["Volume Generated (m3)"]
            total_rainfall += day_data["Rainfall (mm)"]
            total_overflow += day_data["Overflow (m3)"]

            if day_data["Demand Met"] != 0:
                total_days_demand_met += 1

        raw_data = pd.DataFrame(daily_data)

        results = [total_days, total_days_demand_met, raw_data, total_overflow, total_volume_generated_from_roof, total_rainfall]
        return results
