import streamlit as st
import pandas as pd
from roof_data_simulation import RoofDataSimulation as roof_data
from dateutil import relativedelta
from graph_agg import graph_agg

def sim_agg(RAIN_DATA,RAINFALL_COEFFICIENT,CONSUMPTION_RATE_IN_LITRES,POPULATION_PER_HOUSEHOLD,EFFECTIVE_ROOF_AREA_M2,TANK_CAPACITY_LITRES):
            # Create input widgets for Rainfall Coefficient, Consumption Rate, Effective Roof Area, and Tank Capacity
            #RAINFALL_COEFFICIENT = st.sidebar.number_input("Runoff Coefficient", min_value=0.0)
            #CONSUMPTION_RATE_IN_LITRES = st.sidebar.number_input("Consumption Rate (in Litres)", min_value=0.0)
            #POPULATION_PER_HOUSEHOLD = st.sidebar.number_input("Population",min_value=0)
            #EFFECTIVE_ROOF_AREA_M2 = st.sidebar.number_input("Effective Roof Area (m2)", min_value=0.0)
            #TANK_CAPACITY_LITRES = st.sidebar.number_input("Tank Capacity (Litres)", min_value=0.0)
        

    # Create a simulation button
            Roof = roof_data(RAIN_DATA,EFFECTIVE_ROOF_AREA_M2, POPULATION_PER_HOUSEHOLD, TANK_CAPACITY_LITRES,CONSUMPTION_RATE_IN_LITRES,RAINFALL_COEFFICIENT)
        #days_with_overflow,total_days = Roof.simulate()
            simulation_results = Roof.simulate()
        #st.write(simulation_results)
        #Results=[days_with_overflow,total_days,Demand_met,Demand_not_met]
            total_days = simulation_results[0]
            Total_days_Demand_met = simulation_results[1]
            Raw_data =simulation_results[2]
            Total_overflow = simulation_results[3]
            Total_volume_generated_from_roof = simulation_results[4]
            Total_rainfall = simulation_results[5]

        # Display simulation results in a dashboard
        # st.subheader("Simulation Results")


        #total volume_generated_m3- total overflow/total volume generated from roof)*100
            EFFICIENCY = ((Total_volume_generated_from_roof-Total_overflow)/Total_volume_generated_from_roof)*100
            RELIABILITY = (Total_days_Demand_met/total_days)*100
        #Displaying main efficiency
            

        ##grouping the data into years and months
            Raw_data['Date'] = pd.to_datetime(Raw_data['Date'], format="%Y-%m-%d")
            Raw_data['Month'] = Raw_data['Date'].dt.strftime('%B')
            Raw_data['Year'] = Raw_data['Date'].dt.year

        ##getting the number of years of the date
            first_date =(Raw_data["Date"][0])
            final_date =(Raw_data["Date"][total_days-1])
            difference = relativedelta.relativedelta(final_date,first_date)
            no_of_years = difference.years + difference.months / 12 + difference.days / 365.25


            #no_of_years = 
            
        ##calculating annual averages
            Average_annual_rainfall = Total_rainfall/no_of_years
            Average_rain_water_harvesting_potential = Total_volume_generated_from_roof/no_of_years
        ##grouping the data into years
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

            #Monthly_Rain_Analysis = Raw_data.groupby('Month')['Rainfall (mm)'].mean().reset_index()
            Monthly_Rain_sum = Raw_data.groupby(['Month', 'Date'])['Rainfall (mm)'].sum().reset_index()

# Group by 'Month' and calculate the sum of 'Rainfall (mm)' for each month
            Monthly_rain_mean = Monthly_Rain_sum.groupby('Month')['Rainfall (mm)'].sum().reindex(months).reset_index()
            Monthly_rain_mean['mean Rainfall(mm)'] = Monthly_rain_mean['Rainfall (mm)']/no_of_years
            Monthly_rain_mean.drop(columns='Rainfall (mm)',inplace=True)
            Yearly_Rain_analysis = Raw_data.groupby('Year')['Rainfall (mm)'].sum().reset_index()
            Yearly_Potential = Raw_data.groupby('Year')["Volume Generated (m3)"].sum().reset_index()
            daily_overflow = Raw_data.groupby("Date")["Overflow (m3)"].sum()
            daily_overflow = pd.DataFrame(daily_overflow.reset_index())
            daily_vstart = Raw_data.groupby("Date")["Volume in Tank (Start) (m3)"].sum()
            daily_vstart = pd.DataFrame(daily_vstart.reset_index())
            final = graph_agg(RAIN_DATA,RAINFALL_COEFFICIENT,CONSUMPTION_RATE_IN_LITRES,POPULATION_PER_HOUSEHOLD,EFFECTIVE_ROOF_AREA_M2)
            #return ("it Works")

            return [
            daily_overflow,
            daily_vstart,
            Monthly_rain_mean,
            Yearly_Rain_analysis,
            Yearly_Potential,
            Total_volume_generated_from_roof,
            no_of_years,
            Total_rainfall,
            Total_overflow,
            Total_days_Demand_met,
            total_days,
            EFFICIENCY,
            Average_annual_rainfall,
            Average_rain_water_harvesting_potential,
            Raw_data,
            RELIABILITY,
            final
]
