import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
def viz_graph(final):
    df2 = final
    df2["Cumulative Harvested water (m3)"] = df2["Water Harvested (m3)"].cumsum()
    df2["Cumulative Demand (m3)"] = df2["Water demand (m3)"].cumsum()
    df2["Storage Requirement (m3)"] = df2["Cumulative Harvested water (m3)"]-df2["Cumulative Demand (m3)"]
    #st.write(df2)
    #latest_df = pd.concat([Monthly_rain_mean,df2])
    #st.write(latest_df)
    #st.write(RAIN_DATA.iloc[0:,2])
    #st.write(Roof.Generate_demand(no_of_days,no_of_years))
    st.subheader("Optimum storage requirement in litres")
    st.markdown(max(df2["Storage Requirement (m3)"])*1000)
    fig_monthly_rain_dist=px.bar(
    df2,
        x='Months',
        y="Storage Requirement (m3)",
        orientation="v",
        title="<b>Cumulative water supply and estimation of storage requirement</b>",
        color_discrete_sequence=["#0083B8"]*len(df2),
        template="plotly_white"
    )
    #st.plotly_chart(fig_monthly_rain_dist)