# utils.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import max, datediff, countDistinct, col, sum as Fsum
from pyspark.ml.feature import VectorAssembler, MinMaxScaler
import pyspark.sql.functions as F

def create_spark_session(app_name="RFM_Pipeline"):
    return SparkSession.builder.appName(app_name).getOrCreate()

def load_data(file_path, spark):
    return spark.read.csv(file_path, header=True, inferSchema=True)

def compute_rfm(df):
    snapshot_date = df.agg(max("InvoiceDate")).collect()[0][0]
    rfm = df.groupBy("Customer ID").agg(
        datediff(F.lit(snapshot_date), max("InvoiceDate")).alias("Recency"),
        countDistinct("Invoice").alias("Frequency"),
        Fsum(col("Quantity") * col("Price")).alias("Monetary")
    )
    return rfm.dropna()

def get_preprocessing_stages():
    assembler = VectorAssembler(inputCols=["Recency", "Frequency", "Monetary"], outputCol="features_raw")
    scaler = MinMaxScaler(inputCol="features_raw", outputCol="features")
    return [assembler, scaler]

def preprocess_features(rfm_df):
    stages = get_preprocessing_stages()
    from pyspark.ml import Pipeline
    pipeline = Pipeline(stages=stages)
    model = pipeline.fit(rfm_df)
    return model.transform(rfm_df)
