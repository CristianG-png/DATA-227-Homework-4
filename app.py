import streamlit as st
from PIL import Image
import pandas as pd
from charts import chart_q1

st.set_page_config(page_title="Analysis of Weather Patterns in Seattle:", layout="wide")

st.title("Looking at Soccer teams performance between two recent seasons")
st.write("This t.\n")
st.write(
    "To explore this visual data story, please navigate it through the pages in the sidebar:\n"
    "- **Story**: The central narrative, beginning with taking into account daily weather patterns over time.\n"
    "- **Explore**: For a closer reader-driven exploration of the data, we provide a few interactive designs.\n"
    "- **Methods**: We lay down some key details about our data and limitations to our analysis.\n"
)
st.info("Dataset: `vega_datasets.data.seattle_weather()`")

df = pd.read_csv("data/yourfile.csv")
team_summary = df.groupby(["Season", "Team"], as_index=False).agg({
    "Points": "sum",
    "GoalsFor": "sum",
    "GoalsAgainst": "sum",
    "GD": "sum"
})

# call the chart function
st.altair_chart(chart_q1(team_summary), use_container_width=True)
