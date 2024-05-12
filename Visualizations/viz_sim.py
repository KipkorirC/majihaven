#importing libraries
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from aggregation.sim_agg import sim_agg
from Visualizations.viz_graph import viz_graph

def viz_sim(visualization_variables):
    fig_daily_overflow = go.Figure()

    # Add a scatter plot with mode='lines'
    fig_daily_overflow.add_trace(go.Scatter(x=visualization_variables[0]["Date"],y=visualization_variables[0]["Overflow (m3)"], mode='lines', name='Curve'))

    # Update layout for labels and title
    fig_daily_overflow.update_layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Overflow(m3)'),
        
    )
    fig_daily_vstart = go.Figure()

    # Add a scatter plot with mode='lines'
    fig_daily_vstart.add_trace(go.Scatter(x=visualization_variables[1]["Date"],y=visualization_variables[1]["Volume in Tank (Start) (m3)"], mode='lines', name='Curve'))

    # Update layout for labels and title
    fig_daily_vstart.update_layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='volume at the start of the day',range=[0,15]),
        
    )

    fig_monthly_rain_dist=px.bar(
        visualization_variables[2],
        x='Month',
        y='mean Rainfall(mm)',
        orientation="v",
        title="<b>Monthly Rainfall Distribution</b>",
        color_discrete_sequence=["#0083B8"]*len(visualization_variables[2]),
        template="plotly_white"
    )

        
    fig_year_rain_dist=px.bar(
        visualization_variables[3],
        x="Year",
        y="Rainfall (mm)",
        orientation="v",
        title="<b>Yearly Rainfall Distribution</b>",
        color_discrete_sequence=["#0083B8"]*len(visualization_variables[3]),
        template="plotly_white"
    )

    fig_harvesting_potential=px.bar(
        visualization_variables[4],
        x="Year",
        y="Volume Generated (m3)",
        orientation="v",
        title="<b>Yearly harvesting potential Distribution</b>",
        color_discrete_sequence=["#0083B8"]*len(visualization_variables[4]),
        template="plotly_white"
    )

    ## actual visualization

    # Define a custom style for better visibility
    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        # Define CSS style for the value
        value_style = "font-size: 19px; color: #0000cc; font-weight: bold;"

        # Volume Generated (m³)/year
        st.subheader("Volume Generated (m³)/year:")
        st.markdown(
            "<p style='{}'>{:.2f}</p>".format(value_style, visualization_variables[5] / visualization_variables[6]),
            unsafe_allow_html=True
        )

    with middle_column:
        st.subheader("Rainfall (mm)/year:")
        st.markdown("<p style='font-size: 19px; color: #3366cc; font-weight: bold;'>{}</p>".format(visualization_variables[7]/visualization_variables[6]),
                    unsafe_allow_html=True)

    with right_column:
        st.subheader("Overflow (m³)/year: ")
        st.markdown("<p style='font-size: 19px; color: #3366cc; font-weight: bold;'>{}</p>".format(visualization_variables[8]/visualization_variables[6]),
                    unsafe_allow_html=True)

    left, middle = st.columns(2)

    with left:
        st.subheader("Total Days where demand was met")
        st.markdown("<p style='font-size: 19px; color: #3366cc; font-weight: bold;'>{}</p>".format(visualization_variables[9]/visualization_variables[6]),
                    unsafe_allow_html=True)

    with middle:
        st.subheader("Total Days where demand was not met")
        st.markdown("<p style='font-size: 19px; color: #3366cc; font-weight: bold;'>{}</p>".format((visualization_variables[10] - visualization_variables[9])/visualization_variables[6]),
                    unsafe_allow_html=True)

                


    # Define your data for the first pie chart
    pie_chart_data = {
        "Labels": ["Efficiency", "Losses"],
        "Values": [visualization_variables[11], 100-visualization_variables[11]]

    }

    # Define your data for the second pie chart
    pie_chart_data2 = {
        "Labels": ["Days where demand was met", "Days where demand was not met"],
        "Values": [visualization_variables[9], visualization_variables[10]-visualization_variables[9]]
    }

    # Create DataFrames
    pie_chart_df = pd.DataFrame(pie_chart_data)
    pie_chart_df2 = pd.DataFrame(pie_chart_data2)

    fig2 = px.pie(
        pie_chart_df2,
        names="Labels",
        values="Values",
        title="Reliablity",
        color="Labels",
        color_discrete_map=({"Days where demand was met":"blue",
                            "Days where demand was not met":"red"})
    )
    fig2.update_layout(width=400, height=400) 
    fig2.update_traces(
     textfont=dict(size=20, color='white', family='Arial'),  # Adjust font size, color, and family
)
    fig = px.pie(
        pie_chart_df,
        names="Labels",
        values="Values",
        title="Efficiency",
        color="Labels",
        color_discrete_map=({"Efficiency":"blue",
                            "Losses":"red"})
                            
        )
    fig.update_layout(width=400, height=400) 
    fig.update_traces(
     textfont=dict(size=20, color='white', family='Arial'),  # Adjust font size, color, and family
)
    #st.write(visualization_variables[16])

    # Display the pie charts in Streamlit
    col1, col2 = st.columns(2)

    # Display the first chart in the first column
    col1.plotly_chart(fig, use_container_width=False)

    # Display the second chart in the second column
    col2.plotly_chart(fig2, use_container_width=False)
    viz_graph(visualization_variables[16])

    #displaying charts and averages between them
    st.plotly_chart(fig_year_rain_dist)
    st.subheader("Average annual Rainfall(mm)")
    st.text(visualization_variables[12])
    st.plotly_chart(fig_harvesting_potential)
    st.subheader("Average annual Rainwater harvesting potential (m3)")
    st.text(visualization_variables[13])
    st.plotly_chart(fig_monthly_rain_dist)
    st.subheader("Overflow distribution")
    st.plotly_chart(fig_daily_overflow)
    st.subheader("Daily volume at the start of the day")
    st.plotly_chart(fig_daily_vstart)


    #display data
    #st.write(visualization_variables[6])
    st.write(visualization_variables[14])
