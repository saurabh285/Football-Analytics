import pandas as pd
from sklearn.ensemble import IsolationForest
from config import metrics

def detect_anomalies(df):
    """Detect anomalies in player statistics using Isolation Forest."""
    try:
        # Ensure we have the required columns
        if 'match_id' not in df.columns:
            # If match_id doesn't exist, try match_num or create one
            if 'match_num' in df.columns:
                df = df.copy()
                df['match_id'] = df['match_num']
            else:
                df['match_id'] = range(len(df))
        
        # Filter out rows with missing metric values
        available_metrics = [m for m in metrics if m in df.columns]
        if not available_metrics:
            # If no metrics available, return dataframe with 'Normal' labels
            df['anomaly_label'] = 'Normal'
            return df
        
        df_clean = df.dropna(subset=available_metrics).copy()
        
        if len(df_clean) < 2:
            # Not enough data for anomaly detection
            df['anomaly_label'] = 'Normal'
            return df
        
        # Fit isolation forest model
        model = IsolationForest(n_estimators=100, contamination=0.15, random_state=42)
        df_clean['anomaly'] = model.fit_predict(df_clean[available_metrics])
        df_clean['anomaly_label'] = df_clean['anomaly'].map({-1: 'Anomaly', 1: 'Normal'})
        
        # Merge back with original dataframe
        result = df.merge(df_clean[['match_id', 'anomaly_label']], on='match_id', how='left')
        result['anomaly_label'] = result['anomaly_label'].fillna('Normal')
        return result
        
    except Exception as e:
        # If anything goes wrong, return dataframe with 'Normal' labels
        df = df.copy()
        df['anomaly_label'] = 'Normal'
        return df
