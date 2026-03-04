import streamlit as st
from data_loader import load_data
from charts.chart import chart_q1, chart_q2, chart_q4_scatter, chart_q4_table
from PIL import Image

st.set_page_config(page_title="Analysis of Weather Patterns in Seattle:", layout="wide")

st.title("Looking at Soccer teams performance between two recent seasons")
st.write("This website is made to satisfy the criteria for Homework 4 of DATA 22700, using visualizations and data used from Homework 3.\n")

st.info("Datasets: `PL-season-2324.csv`, `PL-season-2425.csv`")

df, team_summary, melted = load_data() 

st.header("Team Performance Across Seasons") 
st.caption("First, comparing how teams performed across the two seasons is important to see if a team improved or got worse over time.")
st.altair_chart(chart_q1(team_summary), use_container_width=True) 
st.caption("Excluding the teams who only played for one of the two seasons, the improvement here varies. Teams like Nott'm Forest, Brentford, and Brighton saw massive improvement over previous seasons while teams such as Arsenal and Man City saw massive loss in the total points they earned in their most recent season.")

st.header("Q2: Rolling Attacking Metrics") 
st.altair_chart(chart_q2(melted), use_container_width=True) 
st.write("Q2 melted shape:", melted.shape)
st.write("Q2 chart object:", chart_q2(melted))

st.header("Q4: Extreme Match Outcomes") 
col1, col2 = st.columns([2, 1]) 
with col1: 
    st.altair_chart(chart_q4_scatter(df), use_container_width=True) 
with col2: 
    st.altair_chart(chart_q4_table(df), use_container_width=True)
