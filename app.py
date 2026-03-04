import streamlit as st
from data_loader import load_data
from charts.chart import chart_q1, chart_q2_single_season, chart_q4_scatter, chart_q4_table
from PIL import Image

st.set_page_config(page_title="Analysis of Weather Patterns in Seattle:", layout="wide")

st.title("Looking at Soccer teams performance between two recent seasons")
st.write("This website is made to satisfy the criteria for Homework 4 of DATA 22700, using visualizations and data used from Homework 3 to create a visual narrative.\n")

st.info("Datasets: `PL-season-2324.csv`, `PL-season-2425.csv`")

df, team_summary, melted = load_data() 

st.header("Team Performance Across Seasons") 
st.caption("First, comparing how teams performed across the two seasons is important to see if a team improved or got worse over time. You can hover the points to see which season each point is for, but it's worth noting that Triangle shaped points are for the 2024-25 season and Circles are for the 2023-24 season.")
st.altair_chart(chart_q1(team_summary), use_container_width=True) 
st.caption("Excluding the teams who only played for one of the two seasons, the improvement here varies. Teams like Nott'm Forest, Brentford, and Brighton saw massive improvement over previous seasons while teams such as Arsenal and Man City saw massive loss in the total points they earned in their most recent season.")

st.header("Rolling Attacking Metrics")
st.caption("Instead of looking at point totals for teams, looking at the rolling averages for each team's scores would be a better indicator of a team's consistency in performance. Hover over the lines according to team color to see how consistent or inconsistent their performance was over the course of a season.")
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(chart_q2_single_season(melted, "2023-24"), use_container_width=True)
with col2:
    st.altair_chart(chart_q2_single_season(melted, "2024-25"), use_container_width=True)
st.caption("We can see some interesting stats here but I'll just focus on Arsenal's performance. We see that they had fluctuating performance the 2023-24 season, but still ended with them earning the most points in the 2023-24 season. In contrast, in 2024-25, they performed well early in the year but did much worse later, leading to them seeing a massive point loss")

st.header("Extreme Match Outcomes")
st.caption("
col1, col2 = st.columns(2) 
with col1: 
    st.altair_chart(chart_q4_scatter(df), use_container_width=True) 
with col2: 
    st.altair_chart(chart_q4_table(df), use_container_width=True)
