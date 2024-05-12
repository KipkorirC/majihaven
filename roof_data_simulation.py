import pandas as pd
class RoofDataSimulation:
    def __init__(self,RAIN_DATA,EFFECTIVE_ROOF_AREA_M2,POPULATION_PER_HOUSEHOLD,TANK_CAPACITY_LITRES,CONSUMPTION_RATE_IN_LITRES,RAINFALL_COEFFICIENT):
        ## variables that are used within this class
        self.POPULATION_PER_HOUSEHOLD = POPULATION_PER_HOUSEHOLD
        self.RAIN_DATA = RAIN_DATA
        self.EFFECTIVE_ROOF_AREA_M2 = EFFECTIVE_ROOF_AREA_M2
        self.TANK_CAPACITY_LITRES = TANK_CAPACITY_LITRES
        self.CONSUMPTION_RATE_IN_LITRES = CONSUMPTION_RATE_IN_LITRES
        self.RAINFALL_COEFFICIENT = RAINFALL_COEFFICIENT
        #for iteration through the data
        self.current_date= 0
    

    def Generate_Daily_Volume(self):
        RAIN_IN_MM = self.RAIN_DATA.iloc[self.current_date,:][1]
        Date=self.RAIN_DATA.iloc[self.current_date,:][0]

        ##calculating the volume of water generated from the roof
        ##RR = ERA*RAINx*RCOEFF
        Volume_Generated_m3 = self.EFFECTIVE_ROOF_AREA_M2*(RAIN_IN_MM/1000)*self.RAINFALL_COEFFICIENT

        ##calculating the volume at the start of the day
        if self.current_date==0: 
            Volume_at_the_start_m3 = 0
        else:
            Volume_at_the_start_m3 = self.volume_at_the_end_m3# previous day
        
        ##calculating the volume of water consumed per day(demand)
        demand_per_day = self.POPULATION_PER_HOUSEHOLD * self.CONSUMPTION_RATE_IN_LITRES/1000

        #logic of water is only consumed if the demand is met
        if Volume_at_the_start_m3 >= demand_per_day:
            Volume_consumed_m3 = demand_per_day
        else:
            Volume_consumed_m3 = 0
       



        ##calculating the volume in the tank at the end of the day

        volume_at_the_end_m3 = (Volume_at_the_start_m3 +Volume_Generated_m3)-Volume_consumed_m3

        ##logic to ensure that volume at the end does not exceed the tank capacity
        if volume_at_the_end_m3>(self.TANK_CAPACITY_LITRES/1000):
            volume_at_the_end_m3=(self.TANK_CAPACITY_LITRES/1000)
            

        self.volume_at_the_end_m3 = volume_at_the_end_m3



        ##calculating overflow
        ##OFx= VT x-1+ RROx – MCx-TC
        overflow = max(0,Volume_at_the_start_m3 + Volume_Generated_m3 - Volume_consumed_m3 - (self.TANK_CAPACITY_LITRES/1000))

        #calculating if demand was met(1) if it was not met(0)
        if Volume_at_the_start_m3 >= demand_per_day:
            demand_met = 1
        else:
            demand_met = 0

        #returning the data as a dictionary
        return {
            "Date":Date,
            "Rainfall (mm)": RAIN_IN_MM,
            "effective roof area":self.EFFECTIVE_ROOF_AREA_M2,
            "Tank capacity (litres)":self.TANK_CAPACITY_LITRES,
            "Volume Generated (m3)": Volume_Generated_m3,
            "Volume in Tank (Start) (m3)": Volume_at_the_start_m3,
            "Demand per Day (m3)": demand_per_day,
            "Volume Consumed (m3)": Volume_consumed_m3,
            "Volume in Tank (End) (m3)": volume_at_the_end_m3,
            "Overflow (m3)": overflow,
            "Demand Met": demand_met,
        }
    

    def simulate(self):
        Daily_data=[]#empty array
        total_days =0 # Variable to count total days
        Total_days_Demand_met = 0
        Total_volume_generated_from_roof = 0
        Total_overflow =0
        Total_rainfall = 0
        for _ in range(len(self.RAIN_DATA)):#15000
            day_data = self.Generate_Daily_Volume()
            Daily_data.append(day_data)
            self.current_date += 1
            total_days += 1
            Total_volume_generated_from_roof += day_data["Volume Generated (m3)"]
            Total_rainfall += day_data["Rainfall (mm)"]
            
            # update count of overflow
            Total_overflow +=day_data["Overflow (m3)"] 
           

            if day_data["Demand Met"]!=0:
                Total_days_Demand_met+=1
        
        #filename =(f"AREA_{self.EFFECTIVE_ROOF_AREA_M2}_POP_{self.POPULATION_PER_HOUSEHOLD}_TANK_{self.TANK_CAPACITY_LITRES}.csv")
        Raw_data = pd.DataFrame(Daily_data)
        #Raw_data.to_csv(filename)
        
        Results=[total_days,Total_days_Demand_met,Raw_data,Total_overflow,Total_volume_generated_from_roof,Total_rainfall]
        return Results