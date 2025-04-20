import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import metrics
from data_loader import load_data
from analysis import detect_anomalies
from llm_utils import describe_plot, compare_players, model
import google.generativeai as genai
st.set_page_config(page_title="Football Analytics", layout="wide")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

df_can, df_milner = load_data()

fixture_df = pd.read_csv("match_fixtures.csv")
df_can = df_can.merge(fixture_df, on="match_num", how="left")
df_milner = df_milner.merge(fixture_df, on="match_num", how="left")

st.markdown("# Navigation")
menu = st.radio(" ", [ "Player 1", "Player 2", "Compare Players", "Matches"], horizontal=True)


if menu in ["Player 1", "Player 2"]:
    player = "Emre Can" if menu == "Player 1" else "James Milner"
    df = df_can.copy() if player == "Emre Can" else df_milner.copy()
    df = detect_anomalies(df)
    st.title(f"{player} - Match Performance + Anomalies")

    for metric in metrics:
        if st.button(f"Show '{metric.replace('_', ' ').title()}'"):
            normal_df = df[df['anomaly_label'] != 'Anomaly']
            anomaly_df = df[df['anomaly_label'] == 'Anomaly']

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=normal_df['match_num'],
                y=normal_df[metric],
                mode='lines+markers',
                name='Normal',
                hovertext=normal_df['fixture'],
                marker=dict(color='green')
            ))

            fig.add_trace(go.Scatter(
                x=anomaly_df['match_num'],
                y=anomaly_df[metric],
                mode='markers',
                name='Anomaly',
                hovertext=anomaly_df['fixture'],
                marker=dict(color='red', size=10)
            ))

            fig.update_layout(
                title=metric.replace("_", " ").title(),
                xaxis_title="Match Number",
                yaxis_title=metric.replace('_', ' ').title(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(describe_plot(df, metric, player))

elif menu == "Compare Players":
    st.title("Comparative Analysis: Emre Can vs James Milner")
    df1 = df_can.copy()
    df2 = df_milner.copy()
    df_compare = pd.concat([
        df1.assign(player="Emre Can"),
        df2.assign(player="James Milner")
    ])

    for metric in metrics:
        if st.button(f"Compare '{metric.replace('_', ' ').title()}'"):
            fig = px.line(
                df_compare,
                x="match_num",
                y=metric,
                color="player",
                hover_data=["match_num", "fixture", "date", metric],
                title=f"Comparison: {metric.replace('_', ' ').title()}",
                markers=True
            )
            fig.update_layout(
                xaxis_title="Match Number",
                yaxis_title=metric.replace('_', ' ').title(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(compare_players(df_can, df_milner, metric))
elif menu == "Matches":
    st.title("Match Files Available")
    matches = os.listdir("matches")
    matches = [m for m in matches if m.endswith(".csv")]
    for idx, match in enumerate(sorted(matches), 1):
        with open(os.path.join("matches", match), "rb") as file:
            fixture_label = fixture_df.loc[fixture_df.match_num == idx, 'fixture'].values[0] if idx <= len(fixture_df) else match
            st.download_button(label=f"Match {idx}: {fixture_label}", data=file, file_name=match)
