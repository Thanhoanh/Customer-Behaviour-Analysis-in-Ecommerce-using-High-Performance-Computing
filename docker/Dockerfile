# Stage 1: Base image with Spark and essential tools
FROM bitnami/spark:3.3 AS spark-base

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl vim apt-transport-https ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=/opt/bitnami/spark \
    PYSPARK_PYTHON=python3 \
    PATH=$PATH:/opt/bitnami/spark/bin \
    JUPYTER_PORT=8889

WORKDIR $SPARK_HOME

COPY spark-defaults.conf $SPARK_HOME/conf/

# Stage 2: Install Python dependencies
FROM spark-base AS pyspark

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 3: Runtime pyspark
FROM pyspark AS pyspark-runner
CMD ["pyspark"]

# Stage 4: Jupyter support
FROM pyspark-runner AS pyspark-jupyter

ENV PYSPARK_DRIVER_PYTHON=jupyter \
    PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --ip=0.0.0.0 --port=$JUPYTER_PORT"

EXPOSE 8889

CMD ["jupyter", "notebook", "--no-browser", "--ip=0.0.0.0", "--port=8889"]
