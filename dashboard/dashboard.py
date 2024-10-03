import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

# Load the dataset
data_cleaned = pd.read_csv("dataset/PRSA_Data_Shunyi_20130301-20170228.csv").fillna(method='ffill')

# Creating a new date column
data_cleaned["date"] = pd.to_datetime(data_cleaned[["year", "month", "day", "hour"]])

# Preparing the data for PM2.5 trend
pm25_trend = data_cleaned.groupby(data_cleaned["date"].dt.year)["PM2.5"].mean().reset_index()

# Streamlit dashboard layout
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")  # Set page title and layout

# Header
st.title("🌍 Air Quality Dashboard - Shunyi Station")
st.markdown("This dashboard provides insights into air quality levels, particularly PM2.5, "
            "and its correlation with temperature (TEMP) over the years.")

# Trend Variable Selection
trend_variable = st.selectbox("Select a variable to view its trend:", 
                                options=['PM2.5', 'TEMP', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])

# Preparing the data for selected trend variable
trend_data = data_cleaned.groupby(data_cleaned["date"].dt.year)[trend_variable].mean().reset_index()

# Trend Chart
st.subheader(f"📈 Trend of {trend_variable} Levels Over the Years")
fig_trend = px.line(trend_data, x='date', y=trend_variable, 
                     title=f'Average {trend_variable} Level by Year',
                     labels={'date': 'Year', trend_variable: f'Average {trend_variable} Level'},
                     template='plotly_white')
st.plotly_chart(fig_trend, use_container_width=True)

# Correlation Heatmap between TEMP and PM2.5
st.subheader("🌡️ Correlation Heatmap between TEMP and PM2.5")

# Create the heatmap using Plotly
correlation_matrix = data_cleaned[['TEMP', 'PM2.5']].corr()

# Create heatmap figure
fig_corr = ff.create_annotated_heatmap(z=correlation_matrix.values,
                                        x=correlation_matrix.columns.tolist(),
                                        y=correlation_matrix.columns.tolist(),
                                        colorscale='RdBu',
                                        showscale=True)

# Update layout for the heatmap
fig_corr.update_layout(title='',
                       xaxis=dict(title='Variables'),
                       yaxis=dict(title='Variables'),
                       title_x=0.5,  # Center the title
                       margin=dict(t=50),  # Add margin above the title
                       width=600, height=500)  # Set dimensions for better visibility

st.plotly_chart(fig_corr, use_container_width=True)

# Correlation Variable Selection
st.subheader("🔍 Select Two Different Variables to View Correlation")
correlation_variable_options = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']

var1 = st.selectbox("Select the first variable:", options=correlation_variable_options)
var2 = st.selectbox("Select the second variable:", options=[var for var in correlation_variable_options if var != var1])

# Calculate the correlation matrix for the selected variables
correlation_matrix_selected = data_cleaned[[var1, var2]].corr()

# Create heatmap for selected variables
fig_corr_selected = ff.create_annotated_heatmap(z=correlation_matrix_selected.values,
                                                 x=correlation_matrix_selected.columns.tolist(),
                                                 y=correlation_matrix_selected.columns.tolist(),
                                                 colorscale='RdBu',
                                                 showscale=True)

# Update layout for the heatmap
fig_corr_selected.update_layout(title=f'Correlation Heatmap between {var1} and {var2}',
                                 xaxis=dict(title='Variables'),
                                 yaxis=dict(title='Variables'),
                                 title_x=0.37,  # Center the title
                                 margin=dict(t=150, b=50),  # Add margin above the title
                                 width=600, height=500)  # Set dimensions for better visibility

st.plotly_chart(fig_corr_selected, use_container_width=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)  # Add spacing
st.markdown("© 2024 Air Quality Monitoring Team | Data Source: Shunyi Station")
