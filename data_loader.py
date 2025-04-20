import pandas as pd

def load_data():
    df_can = pd.read_csv("emre_can_match_stats.csv")
    df_milner = pd.read_csv("milner_match_stats.csv")
    df_can['match_num'] = range(1, len(df_can) + 1)
    df_milner['match_num'] = range(1, len(df_milner) + 1)
    return df_can, df_milner
