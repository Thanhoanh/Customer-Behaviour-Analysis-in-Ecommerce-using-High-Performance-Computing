# anomaly_detection.py
from utils import load_data, compute_rfm, preprocess_features, create_spark_session
from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd

def detect_anomalies_with_isolation_forest(df_scaled):
    df_pd = df_scaled.select("Customer ID", "features").toPandas()
    feature_array = np.array(df_pd["features"].tolist())

    iforest = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    df_pd["anomaly"] = iforest.fit_predict(feature_array)
    df_pd["anomaly_score"] = iforest.decision_function(feature_array)

    return df_pd  # Trả về Pandas DataFrame

def full_pipeline(file_path):
    spark = create_spark_session("AnomalyDetection")
    df = load_data(file_path, spark)
    rfm_df = compute_rfm(df)
    scaled_df = preprocess_features(rfm_df)
    
    anomaly_df_pd = detect_anomalies_with_isolation_forest(scaled_df)

    # Chuyển đổi lại về Spark DataFrame nếu cần
    print(anomaly_df_pd[["Customer ID", "anomaly", "anomaly_score"]].head(10))
    anomaly_df_pd.to_csv("anomaly_result.csv", index=False)

    spark.stop()

# Chạy
if __name__ == "__main__":
    full_pipeline(r"C:\Users\ASUS\Downloads\df_cleaned.csv")
