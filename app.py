import streamlit as st
from PIL import Image

st.set_page_config(page_title="Analysis of Weather Patterns in Seattle:", layout="wide")

st.title("Looking at Soccer teams performance between two recent seasons")
st.write("This website is made to satisfy the criteria for Homework 4 of DATA 22700, using visualizations and data used from Homework 3.\n")
st.write(
    "To see the narrative data story, navigate through the pages in the sidebar:\n"
    "- **Story**: The central narrative\n"
    "- **Explore**: For a closer reader-driven exploration of the data.\n"
    "- **Methods**: Key details about our data and limitations to our analysis.\n"
)
st.info("Datasets: `PL-season-2324.csv`, `PL-season-2425.csv`")

df, team_summary, melted = load_data() st.header("Q1: Team Performance Across Seasons") st.altair_chart(chart_q1(team_summary), use_container_width=True) st.header("Q2: Rolling Attacking Metrics") st.altair_chart(chart_q2(melted), use_container_width=True) st.header("Q4: Extreme Match Outcomes") col1, col2 = st.columns([2, 1]) with col1: st.altair_chart(chart_q4_scatter(df), use_container_width=True) with col2: st.altair_chart(chart_q4_table(df), use_container_width=True)
