FROM bitnami/spark:3.3

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl vim apt-transport-https ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME="/opt/bitnami/spark" \
    PYSPARK_PYTHON=python3 \
    PATH="$PATH:$SPARK_HOME/bin" \
    JUPYTER_PORT=8889

WORKDIR ${SPARK_HOME}

COPY spark-defaults.conf "$SPARK_HOME/conf/"

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip==23.1.2 && \
    pip install --no-cache-dir -r requirements.txt

# Để user root vì docker-compose dùng user: root rồi

CMD ["pyspark"]
