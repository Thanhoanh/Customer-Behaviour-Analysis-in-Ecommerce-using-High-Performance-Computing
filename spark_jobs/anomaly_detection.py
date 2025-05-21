# anomaly_detection.py
from utils import create_spark_session, load_data, compute_rfm, preprocess_features
from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd

def detect_anomalies_with_isolation_forest(scaled_df):
    df_pd = scaled_df.select("Customer ID", "features").toPandas()
    feature_array = np.array(df_pd["features"].tolist())

    model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    df_pd["anomaly"] = model.fit_predict(feature_array)
    df_pd["anomaly_score"] = model.decision_function(feature_array)

    return df_pd

def main():
    spark = create_spark_session("AnomalyDetection")

    # 1. Load và xử lý dữ liệu
    df = load_data(r"C:\Users\ASUS\Downloads\df_cleaned.csv", spark)
    rfm_df = compute_rfm(df)
    scaled_df = preprocess_features(rfm_df)

    # 2. Detect anomaly
    anomaly_df = detect_anomalies_with_isolation_forest(scaled_df)

    # 3. Hiển thị kết quả
    print("\nTop 10 khách hàng nghi ngờ là bất thường:")
    print(anomaly_df[["Customer ID", "anomaly", "anomaly_score"]].head(10))

    spark.stop()

if __name__ == "__main__":
    main()
