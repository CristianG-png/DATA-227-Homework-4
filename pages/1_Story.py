import streamlit as st
from data_loader import load_data
from charts.chart import chart_q1, chart_q2, chart_q4_scatter, chart_q4_table

df, team_summary, melted = load_data()

st.altair_chart(chart_q1(team_summary))
st.altair_chart(chart_q2(melted))
st.altair_chart(chart_q4_scatter(df))
st.altair_chart(chart_q4_table(df))
