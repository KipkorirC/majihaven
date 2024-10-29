from functions import load_and_process_data
from graph_agg import graph_agg
from sim_agg import sim_agg
from viz_sim import viz_sim
from viz_graph import viz_graph
#from optimizer.optimal import find_optimal_tank_capacity


import streamlit as st

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Rainwater Collection Simulator",
        page_icon="🌧",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar
    st.sidebar.title("Rainwater Collection Simulator")
    st.sidebar.markdown("Explore rainwater harvesting!")

    

    st.title("🌧Maji Haven Simulator")
    st.markdown('---')

    st.sidebar.header("Input Parameters")

    excel_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

    if excel_file:
        RAIN_DATA = load_and_process_data(excel_file)
        
        #option = st.selectbox(
        #    "Choose the method you would like to use",
        #    ('Simulation model', 'Graphing method'),
        #    index=None,
        #    format_func=lambda x: 'Select an option' if x == '' else x
        #)

        #if option == "Simulation model":
        st.sidebar.subheader("Simulation Parameters")
        RAINFALL_COEFFICIENT = st.sidebar.number_input("Runoff Coefficient", min_value=0.0)
        CONSUMPTION_RATE_IN_LITRES = st.sidebar.number_input("Consumption Rate (in Litres)", min_value=0.0)
        POPULATION_PER_HOUSEHOLD = st.sidebar.number_input("Population", min_value=0)
        EFFECTIVE_ROOF_AREA_M2 = st.sidebar.number_input("Effective Roof Area (m2)", min_value=0.0)
        TANK_CAPACITY_LITRES = st.sidebar.number_input("Tank Capacity (Litres)", min_value=0.0)
        #Money_spent = st.sidebar.number_input("Money (ksh)", min_value=0)


        if st.sidebar.button("Simulate"):
            sim_list = sim_agg(RAIN_DATA, RAINFALL_COEFFICIENT, CONSUMPTION_RATE_IN_LITRES, POPULATION_PER_HOUSEHOLD, EFFECTIVE_ROOF_AREA_M2, TANK_CAPACITY_LITRES)

            if sim_list:
                viz_sim(sim_list)
                #find_optimal_tank_capacity(sim_list,TANK_CAPACITY_LITRES)

        # elif option == "Graphing method":
        #     st.sidebar.subheader("Graphing Parameters")
        #     RAINFALL_COEFFICIENT = st.sidebar.number_input("Runoff Coefficient", min_value=0.0)
        #     CONSUMPTION_RATE_IN_LITRES = st.sidebar.number_input("Consumption Rate (in Litres)", min_value=0.0)
        #     POPULATION_PER_HOUSEHOLD = st.sidebar.number_input("Population", min_value=0)
        #     EFFECTIVE_ROOF_AREA_M2 = st.sidebar.number_input("Effective Roof Area (m2)", min_value=0.0)
            
        #     final = graph_agg(RAIN_DATA, RAINFALL_COEFFICIENT, CONSUMPTION_RATE_IN_LITRES, POPULATION_PER_HOUSEHOLD, EFFECTIVE_ROOF_AREA_M2)
            
        #     if final is not None:
        #         viz_graph(final)
        #     else:
        #         print("No data returned!!!!")
    # Copyright information
    footer=st.empty()
    footer.markdown(
    """
    <div style="position: fixed; bottom: 10px; width: 100%; text-align: center;">
        Copyright © 2023 Njuguna,Muthoni & Kipkorir. All rights reserved
              </div>
    """,
    unsafe_allow_html=True
        )       
if __name__ == "__main__":
    main()
