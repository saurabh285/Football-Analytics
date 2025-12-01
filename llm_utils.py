import time
import google.generativeai as genai
from config import metrics

# Lazy model initialization - created after API key is configured
_model = None
_failed_models = set()  # Track models that have failed

def get_model(reset=False):
    """Get or create the generative model. Should be called after API key is configured."""
    global _model, _failed_models
    if reset:
        _model = None
    
    if _model is None:
        # Try models in order of preference - don't include 'models/' prefix, 
        # GenerativeModel will add it automatically
        model_candidates = [
            "gemini-1.5-flash-002",  # Default model name
            "gemini-1.5-flash",      # Alternative
            "gemini-pro",            # Widely available fallback
            "gemini-1.5-pro",        # Pro version
        ]
        
        last_error = None
        for model_name in model_candidates:
            if model_name in _failed_models:
                continue
            try:
                _model = genai.GenerativeModel(model_name)
                # Test if model is actually accessible
                return _model
            except Exception as e:
                last_error = str(e)
                _failed_models.add(model_name)
                continue
        
        # If all models fail, try to list available models
        try:
            available_models = genai.list_models()
            for model in available_models:
                if hasattr(model, 'supported_generation_methods'):
                    if 'generateContent' in model.supported_generation_methods:
                        model_name = model.name.replace('models/', '')
                        try:
                            _model = genai.GenerativeModel(model_name)
                            return _model
                        except Exception:
                            continue
        except Exception:
            pass
        
        # If we still don't have a model, raise an error with helpful message
        raise Exception(
            f"Could not initialize any Gemini model. Tried: {', '.join(model_candidates)}. "
            f"Last error: {last_error}. "
            f"Please check your API key and available models."
        )
    
    return _model

def safe_llm_call(prompt, delay=1.5):
    """Safely call the LLM with retry logic and proper error handling."""
    try:
        model = get_model()
        time.sleep(delay)
        response = model.generate_content(prompt)
        
        # Check if response has text attribute
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            # Handle cases where response might have blocking or errors
            if hasattr(response, 'prompt_feedback'):
                return f"LLM response blocked or filtered: {response.prompt_feedback}"
            return "LLM returned an empty response."
            
    except Exception as e:
        error_msg = str(e)
        
        # Check if it's a model not found error - try a different model
        if "404" in error_msg or "not found" in error_msg.lower() or "not found for API version" in error_msg.lower():
            # Mark current model as failed and try again with a different model
            global _failed_models
            try:
                current_model_name = get_model()._model_name
                _failed_models.add(current_model_name.replace('models/', ''))
            except:
                pass
            
            # Try again with a different model
            try:
                model = get_model(reset=True)
                time.sleep(delay)
                response = model.generate_content(prompt)
                if hasattr(response, 'text') and response.text:
                    return response.text.strip()
            except Exception as retry_error:
                # If retry with different model fails, show available models
                try:
                    available = list(genai.list_models())
                    available_names = [m.name for m in available if hasattr(m, 'supported_generation_methods') and 'generateContent' in m.supported_generation_methods]
                    if available_names:
                        return f"Model not found. Available models that support generateContent: {', '.join(available_names[:5])}. Please update the model name in llm_utils.py. Original error: {error_msg}"
                except:
                    pass
        
        # First retry
        try:
            time.sleep(delay * 2)
            model = get_model()
            response = model.generate_content(prompt)
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            else:
                return f"LLM error after retry: {error_msg}"
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
