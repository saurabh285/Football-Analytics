import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import metrics
from data_loader import load_data
from analysis import detect_anomalies

import google.generativeai as genai
st.set_page_config(page_title="Football Analytics", layout="wide")

# Configure API key first, before importing llm_utils
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("⚠️ GEMINI_API_KEY not found in Streamlit secrets. Please add it to your Streamlit secrets.")
    st.stop()

# Now import LLM utilities after API key is configured
from llm_utils import describe_plot, compare_players
df_can, df_milner = load_data()

fixture_df = pd.read_csv("match_fixtures.csv")
df_can = df_can.merge(fixture_df, on="match_num", how="left")
df_milner = df_milner.merge(fixture_df, on="match_num", how="left")

st.markdown("# FootBall Analytics - Trends & Comparison")
menu = st.radio(" ", [ "Emre Can", "James Milner", "Compare Players", "Matches"], horizontal=True)


if menu in ["Emre Can", "James Milner"]:
    player = "Emre Can" if menu == "Emre Can" else "James Milner"
    df = df_can.copy() if player == "Emre Can" else df_milner.copy()
    df = detect_anomalies(df)
    st.title(f"{player} - Stats + Anomalies")

    # Use selectbox instead of buttons to avoid state issues
    selected_metric = st.selectbox("Select a metric to analyze:", metrics, format_func=lambda x: x.replace('_', ' ').title())
    
    if selected_metric:
        # Fill NaN anomaly labels with 'Normal' for display
        if 'anomaly_label' not in df.columns:
            df['anomaly_label'] = 'Normal'
        df['anomaly_label'] = df['anomaly_label'].fillna('Normal')
        
        normal_df = df[df['anomaly_label'] != 'Anomaly']
        anomaly_df = df[df['anomaly_label'] == 'Anomaly']

        fig = go.Figure()

        if not normal_df.empty:
            fig.add_trace(go.Scatter(
                x=normal_df['match_num'],
                y=normal_df[selected_metric],
                mode='lines+markers',
                name='Normal',
                hovertext=normal_df.get('fixture', ''),
                marker=dict(color='green')
            ))

        if not anomaly_df.empty:
            fig.add_trace(go.Scatter(
                x=anomaly_df['match_num'],
                y=anomaly_df[selected_metric],
                mode='markers',
                name='Anomaly',
                hovertext=anomaly_df.get('fixture', ''),
                marker=dict(color='red', size=10)
            ))

        fig.update_layout(
            title=selected_metric.replace("_", " ").title(),
            xaxis_title="Match Number",
            yaxis_title=selected_metric.replace('_', ' ').title(),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show LLM description with loading indicator
        with st.spinner("Generating analysis..."):
            analysis = describe_plot(df, selected_metric, player)
            st.markdown(analysis)

elif menu == "Compare Players":
    st.title("Comparative Analysis: Emre Can vs James Milner")
    df1 = df_can.copy()
    df2 = df_milner.copy()
    df_compare = pd.concat([
        df1.assign(player="Emre Can"),
        df2.assign(player="James Milner")
    ])

    # Use selectbox instead of buttons
    selected_metric = st.selectbox("Select a metric to compare:", metrics, format_func=lambda x: x.replace('_', ' ').title(), key="compare_metric")
    
    if selected_metric:
        fig = px.line(
            df_compare,
            x="match_num",
            y=selected_metric,
            color="player",
            hover_data=["match_num", "fixture", "date", selected_metric],
            title=f"Comparison: {selected_metric.replace('_', ' ').title()}",
            markers=True
        )
        fig.update_layout(
            xaxis_title="Match Number",
            yaxis_title=selected_metric.replace('_', ' ').title(),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show LLM comparison with loading indicator
        with st.spinner("Generating comparison..."):
            comparison = compare_players(df_can, df_milner, selected_metric)
            st.markdown(comparison)
elif menu == "Matches":
    st.title("Match Files Available")
    matches = os.listdir("matches")
    matches = [m for m in matches if m.endswith(".csv")]
    for idx, match in enumerate(sorted(matches), 1):
        with open(os.path.join("matches", match), "rb") as file:
            fixture_label = fixture_df.loc[fixture_df.match_num == idx, 'fixture'].values[0] if idx <= len(fixture_df) else match
            st.download_button(label=f"Match {idx}: {fixture_label}", data=file, file_name=match)
