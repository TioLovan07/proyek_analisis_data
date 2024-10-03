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

# Calculate the correlation matrix for TEMP and PM2.5
correlation_matrix = data_cleaned[['TEMP', 'PM2.5']].corr()

# Streamlit dashboard layout
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")  # Set page title and layout

# Header
st.title("🌍 Air Quality Dashboard - Shunyi Station")
st.markdown("This dashboard provides insights into air quality levels, particularly PM2.5, "
            "and its correlation with temperature (TEMP) over the years.")

# PM2.5 Trend Chart
st.subheader("📈 Trend of PM2.5 Levels Over the Years")
fig_pm25 = px.line(pm25_trend, x='date', y='PM2.5', title='Average PM2.5 Level by Year',
                    labels={'date': 'Year', 'PM2.5': 'Average PM2.5 Level'},
                    template='plotly_white')
st.plotly_chart(fig_pm25, use_container_width=True)

# Correlation Heatmap between TEMP and PM2.5
st.subheader("🌡️ Correlation Heatmap between TEMP and PM2.5")

# Create the heatmap using Plotly
fig_corr = ff.create_annotated_heatmap(z=correlation_matrix.values,
                                        x=correlation_matrix.columns.tolist(),
                                        y=correlation_matrix.columns.tolist(),
                                        colorscale='RdBu',
                                        showscale=True)

# Update layout for the heatmap
fig_corr.update_layout(title='Correlation Heatmap between TEMP and PM2.5',
                       xaxis=dict(title='Variables'),
                       yaxis=dict(title='Variables'),
                       title_x=0.5,  # Center the title
                       width=600, height=500)  # Set dimensions for better visibility

st.plotly_chart(fig_corr, use_container_width=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)  # Add spacing
st.markdown("© 2024 Air Quality Monitoring Team | Data Source: Shunyi Station")
