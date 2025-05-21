# clustering_analysis.py
import numpy as np
import matplotlib.pyplot as plt
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
from pyspark.sql.functions import mean
from pyspark.sql import functions as F
from pyspark.sql.functions import mean, count
from pyspark.sql import SparkSession
# Import các hàm từ utils.py
from utils import create_spark_session, load_data, compute_rfm, preprocess_features, get_preprocessing_stages

def find_best_k(scaled_df, k_range=range(2, 11)):
    wssse_list = []

    for k in k_range:
        kmeans = KMeans().setK(k).setSeed(42).setFeaturesCol("features")
        model = kmeans.fit(scaled_df)
        wssse = model.summary.trainingCost
        wssse_list.append((k, wssse))

    # Tính điểm gãy (Elbow method)
    ks, costs = zip(*wssse_list)
    ks, costs = np.array(ks), np.array(costs)

    point1, point2 = np.array([ks[0], costs[0]]), np.array([ks[-1], costs[-1]])

    def perp_dist(point):
        return np.abs(np.cross(point2 - point1, point1 - point)) / np.linalg.norm(point2 - point1)

    distances = [perp_dist(np.array([ks[i], costs[i]])) for i in range(len(ks))]
    best_k = int(ks[np.argmax(distances)])

    print(f"Best k by Elbow Method = {best_k}")
    return best_k

def main():
    spark = create_spark_session("ClusterAnalysis")

    # Load data và tính RFM
    df = load_data(r"C:\Users\ASUS\Downloads\df_cleaned.csv", spark)
    rfm_df = compute_rfm(df)
    scaled_df = preprocess_features(rfm_df)
    best_k = find_best_k(scaled_df)

    # Lấy lại assembler và scaler stages
    preprocessing_stages = get_preprocessing_stages()
    kmeans = KMeans(featuresCol="features", predictionCol="cluster", k=best_k, seed=42)
    pipeline = Pipeline(stages=preprocessing_stages + [kmeans])

    model = pipeline.fit(rfm_df)
    clustered_df = model.transform(rfm_df)

    clustered_df.groupBy("cluster").agg(
        mean("Recency").alias("Avg_Recency"),
        mean("Frequency").alias("Avg_Frequency"),
        mean("Monetary").alias("Avg_Monetary"),
        count("*").alias("Cluster_Size")
    ).orderBy("cluster").show()

    spark.stop()

if __name__ == "__main__":
    main()
