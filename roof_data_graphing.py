class RoofDataGraphing:
    def __init__(self,RAIN_DATA,RAINFALL_COEFFICIENT,CONSUMPTION_RATE_IN_LITRES,POPULATION_PER_HOUSEHOLD,EFFECTIVE_ROOF_AREA_M2):
        self.POPULATION_PER_HOUSEHOLD = POPULATION_PER_HOUSEHOLD
        self.RAIN_DATA = RAIN_DATA
        self.EFFECTIVE_ROOF_AREA_M2 = EFFECTIVE_ROOF_AREA_M2
        self.CONSUMPTION_RATE_IN_LITRES = CONSUMPTION_RATE_IN_LITRES
        self.RAINFALL_COEFFICIENT = RAINFALL_COEFFICIENT
        
    #method to calculate the volume generated by the attributes specified above.
    def Generate_Volume(self,number,rain):
        #reading the specific row that contains the rain in milimeters from the rain data
        RAIN_IN_MM = self.RAIN_DATA.iloc[0:,2] 
        Rain = []
        Rain1=[]
        data = []
       #rain = []
        data1 = []
        Month = []
        Month1 =[]
        Tester = True
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        #s_d=[]
        average_in_m3 = RAIN_IN_MM.mean()/1000
       # demand2 = number
        ##RR = ERA*RAINx*RCOEFF
        for i in range(len(RAIN_IN_MM)):
            Volume_Generated_m3 = self.EFFECTIVE_ROOF_AREA_M2*(RAIN_IN_MM[i]/1000)*self.RAINFALL_COEFFICIENT
            data.append(Volume_Generated_m3)
            demand2 = (average_in_m3)*self.EFFECTIVE_ROOF_AREA_M2*self.RAINFALL_COEFFICIENT
            Rain.append(RAIN_IN_MM[i])
            #if number>Volume_Generated_m3:
                #number = Volume_Generated_m3
            #demand2 = (average_in_m3)*self.EFFECTIVE_ROOF_AREA_M2*self.RAINFALL_COEFFICIENT
                #demand.append(demand2)
            #else:
                #demand.append(number)
                #s_d.append(Volume_Generated_m3-number)
            
            ##########################################
            ###  How to log the months             ###
            ##########################################
            demand2 = (average_in_m3)*self.EFFECTIVE_ROOF_AREA_M2*self.RAINFALL_COEFFICIENT
            #if Tester:

            #    if demand2<=Volume_Generated_m3:
            #        data.append(Volume_Generated_m3)
            #        Month.append(months[i])
            #        Rain.append(rain[i])
            #        Tester=False

            #    else:
            #        data1.append(Volume_Generated_m3)
            #        Month1.append(months[i])
            #        Rain1.append(rain[i])
            #else:
            #    data.append(Volume_Generated_m3)
            #    Month.append(months[i])
            #    Rain.append(rain[i])
        #data=data+data1
        #Month = Month+Month1
        #Rain = Rain+Rain1
        #st.write(rain)
            
        

        #Monthly_rain_mean.iloc[0:,2]
        


        return {"Months":months,
                "Rainfal (m3)":Rain,
            "Water Harvested (m3)":data,
                "Water demand (m3)":demand2,
                }
    
    #def Monthly_rainfall(rain):
    #           Monthly_Rain_sum = df2.groupby(['Month', 'Date'])['Rain in mm'].sum().reset_index()
    #            Monthly_rain_mean = Monthly_Rain_sum.groupby('Month')['Rain in mm'].sum().reindex(months).reset_index()
    #            Monthly_rain_mean['mean Rainfall(mm)'] = Monthly_rain_mean['Rain in mm']/no_of_years

    def Generate_demand(self,days,no_of_years):
        demand = self.CONSUMPTION_RATE_IN_LITRES*self.POPULATION_PER_HOUSEHOLD
        demand =  demand*days
        demand = demand/no_of_years
        demand = demand/12
        demand = demand/1000
        

        return demand