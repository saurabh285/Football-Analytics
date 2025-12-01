import time
import google.generativeai as genai
from config import metrics

# Lazy model initialization - created after API key is configured
_model = None

def get_model():
    """Get or create the generative model. Should be called after API key is configured."""
    global _model
    if _model is None:
        _model = genai.GenerativeModel("gemini-1.5-flash")
    return _model

def safe_llm_call(prompt, delay=1.5):
    """Safely call the LLM with retry logic and proper error handling."""
    try:
        time.sleep(delay)
        response = get_model().generate_content(prompt)
        
        # Check if response has text attribute
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            # Handle cases where response might have blocking or errors
            if hasattr(response, 'prompt_feedback'):
                return f"LLM response blocked or filtered: {response.prompt_feedback}"
            return "LLM returned an empty response."
            
    except Exception as e:
        # First retry
        try:
            time.sleep(delay * 2)
            response = get_model().generate_content(prompt)
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            else:
                return f"LLM error after retry: {str(e)}"
        except Exception as e2:
            return f"LLM could not generate a response. Error: {str(e2)}"

def describe_plot(df, metric, player):
    """Generate a description of the plot trend using LLM."""
    try:
        # Get the last 15 non-null values
        values = df[metric].dropna().tolist()[-15:] if metric in df.columns else []
        
        # Get anomaly match numbers if anomaly_label exists
        is_anomaly = []
        if 'anomaly_label' in df.columns:
            anomaly_df = df[df['anomaly_label'] == 'Anomaly']
            if 'match_num' in anomaly_df.columns:
                is_anomaly = anomaly_df['match_num'].tolist()[-10:]
        
        if not values:
            return f"No data available for {metric.replace('_', ' ')} for {player}."
        
        prompt = f"""As a professional football analyst, analyze and describe the performance trend of {player} for the metric "{metric.replace('_', ' ')}".

Metric: {metric.replace('_', ' ')}
Player: {player}
Recent values across matches (last 15 matches): {values}
Match numbers with anomalies: {is_anomaly if is_anomaly else "None"}

Please provide a brief 2-3 sentence analysis of the trend, performance consistency, and any notable patterns. Focus on actionable insights."""
        
        return safe_llm_call(prompt)
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

def compare_players(df1, df2, metric):
    """Compare two players' performance for a given metric using LLM."""
    try:
        # Get the last 15 non-null values for each player
        can_values = df1[metric].dropna().tolist()[-15:] if metric in df1.columns else []
        milner_values = df2[metric].dropna().tolist()[-15:] if metric in df2.columns else []
        
        if not can_values or not milner_values:
            return f"Insufficient data to compare {metric.replace('_', ' ')} between players."
        
        prompt = f"""As a professional football analyst, compare the performance of two players for the metric "{metric.replace('_', ' ')}".

Metric: {metric.replace('_', ' ')}
Emre Can's recent values (last 15 matches): {can_values}
James Milner's recent values (last 15 matches): {milner_values}

Please provide a 2-3 sentence comparison analyzing:
1. Which player shows better performance or consistency
2. Key differences in their playing styles or contributions
3. Notable patterns or trends in the data

Be specific and provide actionable insights."""
        
        return safe_llm_call(prompt)
    except Exception as e:
        return f"Error generating comparison: {str(e)}"
