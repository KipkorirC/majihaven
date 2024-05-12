import streamlit as st
import pandas as pd
from roof_data_graphing import RoofDataGraphing as Roof_data2
from dateutil import relativedelta
from functools import reduce
from datetime import datetime
def graph_agg(RAIN_DATA,RAINFALL_COEFFICIENT,CONSUMPTION_RATE_IN_LITRES,POPULATION_PER_HOUSEHOLD,EFFECTIVE_ROOF_AREA_M2):
    df = RAIN_DATA
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Year'] = df['Date'].dt.year
    df2 =pd.DataFrame(df)
    #st.write(df2)

    #RAINFALL_COEFFICIENT = st.sidebar.number_input("Runoff Coefficient", min_value=0.0)
    #CONSUMPTION_RATE_IN_LITRES = st.sidebar.number_input("Consumption Rate (in Litres)", min_value=0.0)
    #POPULATION_PER_HOUSEHOLD = st.sidebar.number_input("Population",min_value=0)
    #EFFECTIVE_ROOF_AREA_M2 = st.sidebar.number_input("Effective Roof Area (m2)", min_value=0.0)


        ##getting the number of years of the date
    first_date = df2["Date"].iloc[0]
    final_date = df2["Date"].iloc[-1]
    no_of_years = relativedelta.relativedelta(final_date,first_date).years
    def numOfDays(date1, date2):
        return reduce(lambda x, y: (y-x).days, [date1, date2])
    
    no_of_days = numOfDays(first_date,final_date)

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    Monthly_Rain_sum = df2.groupby(['Month', 'Date'])['Rain in mm'].mean().reset_index()
    Monthly_rain_mean = Monthly_Rain_sum.groupby('Month')['Rain in mm'].sum().reindex(months).reset_index()
    Monthly_rain_mean['mean Rainfall(mm)'] = Monthly_rain_mean['Rain in mm']/no_of_years
    #Monthly_rain_mean.drop(columns="Rain in mm",inplace=True)
    Monthly_rain_mean.set_index("Month",drop=False)
    RAIN_DATA = Monthly_rain_mean
    Test = RAIN_DATA["mean Rainfall(mm)"].tolist()
    #st.write(len(RAIN_DATA["mean Rainfall(mm)"]))
    #Tester = True
    #if Tester:
    Roof = Roof_data2(RAIN_DATA,RAINFALL_COEFFICIENT,CONSUMPTION_RATE_IN_LITRES,POPULATION_PER_HOUSEHOLD,EFFECTIVE_ROOF_AREA_M2)
    
    demand = ((Roof.Generate_demand(no_of_days,no_of_years)))
    data = Roof.Generate_Volume(demand,Test)
    df = {}
    df2 = pd.DataFrame(data)
    def sorting(df2):
        positive = df2[df2["s-d"]>0]
        min_positive_index = min(positive["s-d"])
        for i ,val in enumerate(df2["s-d"]):
            if min_positive_index==val:
                return i
        #return min_positive_index
    df2["s-d"] = df2[ "Water demand (m3)"]-df2["Water Harvested (m3)"]
    df6 = df2
    i=sorting(df6)
    test2 = df2.iloc[i:]
    test = df2.iloc[0:i]
    final = pd.concat([test2, test])
    final.reset_index(drop=True, inplace=True)
    return final