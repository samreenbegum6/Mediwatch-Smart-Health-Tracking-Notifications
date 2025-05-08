
import pandas as pd

def detect_anomalies(df):
    anomalies = df[
        (df['HeartRate'] < 60) | (df['HeartRate'] > 100) |
        (df['BP_Systolic'] < 90) | (df['BP_Systolic'] > 140) |
        (df['BP_Diastolic'] < 60) | (df['BP_Diastolic'] > 90) |
        (df['SpO2'] < 95)
    ]
    return anomalies
