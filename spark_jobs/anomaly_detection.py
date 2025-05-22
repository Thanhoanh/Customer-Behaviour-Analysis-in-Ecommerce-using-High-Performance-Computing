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

    # 3. Tính toán ngưỡng anomaly_score (min score của nhóm anomaly)
    anomaly_threshold = anomaly_df.loc[anomaly_df["anomaly"] == -1, "anomaly_score"].min()

    # 4. Tính số lượng và tỷ lệ khách hàng bất thường
    num_anomalies = (anomaly_df["anomaly"] == -1).sum()
    total_customers = len(anomaly_df)
    anomaly_ratio = num_anomalies / total_customers # % tính cho dễ đọc

    # 5. Nối anomaly_df với rfm_df để có đủ thông tin cho thống kê
    rfm_pd = rfm_df.toPandas()
    anomaly_full = anomaly_df.merge(rfm_pd, on="Customer ID", how="left")

    # 6. Hiển thị kết quả
    print(f"\nNgưỡng anomaly_score để bị coi là bất thường: {anomaly_threshold:.5f}")
    print(f"Số lượng khách hàng bất thường: {num_anomalies}")
    print(f"Tổng số khách hàng: {total_customers}")
    print(f"Tỷ lệ khách hàng bất thường: {anomaly_ratio:.2f}%")

    print("\nTop 10 khách hàng nghi ngờ là bất thường:")
    print(anomaly_full[anomaly_full["anomaly"] == -1][["Customer ID", "Recency", "Frequency", "Monetary", "anomaly_score"]]
          .sort_values("anomaly_score").head(10))

    # 7. Thống kê mô tả cho nhóm khách hàng bất thường
    print("\nThống kê mô tả cho khách hàng bất thường:")
    print(anomaly_full[anomaly_full["anomaly"] == -1][["Recency", "Frequency", "Monetary", "anomaly_score"]].describe())

    spark.stop()

if __name__ == "__main__":
    main()
