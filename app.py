import streamlit as st
import os
import matplotlib.pyplot as plt
import seaborn as sns
from config import metrics
from data_loader import load_data
from analysis import detect_anomalies
from llm_utils import describe_plot, compare_players, model
import google.generativeai as genai

# Set your API key securely
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load data
df_can, df_milner = load_data()

menu = st.sidebar.radio("Navigation", ["Matches", "Player 1", "Player 2", "Compare Players"])

if menu == "Matches":
    st.title("Match Files Available")
    matches = os.listdir("matches")
    matches = [m for m in matches if m.endswith(".csv")]
    for idx, match in enumerate(sorted(matches), 1):
        with open(os.path.join("matches", match), "rb") as file:
            st.download_button(label=f"Match {idx}: Download {match}", data=file, file_name=match)

elif menu in ["Player 1", "Player 2"]:
    player = "Emre Can" if menu == "Player 1" else "James Milner"
    df = df_can.copy() if player == "Emre Can" else df_milner.copy()
    df = detect_anomalies(df)
    st.title(f"{player} - Match Performance + Anomalies")

    for metric in metrics:
        if st.button(f"Show '{metric.replace('_', ' ').title()}'"):
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=df[df['anomaly_label'] != 'Anomaly'], x='match_num', y=metric, label='Normal', ax=ax)
            sns.scatterplot(data=df[df['anomaly_label'] == 'Anomaly'], x='match_num', y=metric, color='red', s=80, label='Anomaly', ax=ax)
            ax.set_title(metric.replace('_', ' ').title())
            ax.set_xlabel("Match Number")
            ax.set_ylabel(metric.replace('_', ' ').title())
            ax.grid(True)
            st.pyplot(fig)
            st.markdown(describe_plot(df, metric, player))

elif menu == "Compare Players":
    st.title("Comparative Analysis: Emre Can vs James Milner")
    for metric in metrics:
        if st.button(f"Compare '{metric.replace('_', ' ').title()}'"):
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=df_can, x='match_num', y=metric, label='Emre Can', ax=ax)
            sns.lineplot(data=df_milner, x='match_num', y=metric, label='James Milner', ax=ax)
            ax.set_title(metric.replace('_', ' ').title())
            ax.set_xlabel("Match Number")
            ax.set_ylabel(metric.replace('_', ' ').title())
            ax.grid(True)
            st.pyplot(fig)
            st.markdown(compare_players(df_can, df_milner, metric))
