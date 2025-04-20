import time
import google.generativeai as genai
from config import metrics

genai.configure(api_key=None)  # Set in app.py before calling

model = genai.GenerativeModel("gemini-1.5-flash")

def safe_llm_call(prompt, delay=1.5):
    try:
        time.sleep(delay)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        try:
            time.sleep(delay)
            response = model.generate_content(prompt)
            return response.text.strip()
        except:
            return "LLM could not generate a response."

def describe_plot(df, metric, player):
    values = df[[metric]].dropna().squeeze().tolist()[-15:]
    is_anomaly = df[df['anomaly_label'] == 'Anomaly']['match_num'].tolist()[-10:]
    prompt = f"""
    As a football Analyst, Describe the trend of the following metric for {player}:
    Metric: {metric.replace('_', ' ')}
    Values over matches: {values}
    Anomalies at matches: {is_anomaly}
    Write 2-3 sentences.
    """
    return safe_llm_call(prompt)

def compare_players(df1, df2, metric):
    prompt = f"""
    As a football Analyst, Compare {metric.replace('_', ' ')} trend for Emre Can vs James Milner.
    Emre Can values: {df1[metric].dropna().tolist()[-15:]}
    James Milner values: {df2[metric].dropna().tolist()[-15:]}
    Write 2-3 sentences summarizing who performed better or how they differed.
    """
    return safe_llm_call(prompt)
