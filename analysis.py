import pandas as pd
from sklearn.ensemble import IsolationForest
from config import metrics

def detect_anomalies(df):
    df_clean = df.dropna(subset=metrics).copy()
    model = IsolationForest(n_estimators=100, contamination=0.15, random_state=42)
    df_clean['anomaly'] = model.fit_predict(df_clean[metrics])
    df_clean['anomaly_label'] = df_clean['anomaly'].map({-1: 'Anomaly', 1: 'Normal'})
    return df.merge(df_clean[['match_id', 'anomaly_label']], on='match_id', how='left')
