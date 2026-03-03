import streamlit as st
import pandas as pd
from charts import chart_q1

# load your data
df = pd.read_csv("data/yourfile.csv")
team_summary = df.groupby(["Season", "Team"], as_index=False).agg({
    "Points": "sum",
    "GoalsFor": "sum",
    "GoalsAgainst": "sum",
    "GD": "sum"
})

st.altair_chart(chart_q1(team_summary), use_container_width=True)
