# Stage 1: Base Spark
FROM bitnami/spark:3.3 AS spark-base

# Install system tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV SPARK_HOME="/opt/bitnami/spark"
ENV PYSPARK_PYTHON=python3
ENV PATH="$PATH:$SPARK_HOME/bin"

# Copy Spark config
COPY spark-defaults.conf "$SPARK_HOME/conf/"

# Stage 2: Python dependencies
FROM spark-base AS pyspark
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Entrypoint setup
FROM pyspark AS pyspark-runner
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Stage 4: Jupyter (optional)
FROM pyspark-runner AS pyspark-jupyter
RUN pip install --no-cache-dir notebook && \
    useradd -m jupyter-user && \
    chown -R jupyter-user:jupyter-user /home/jupyter-user

USER jupyter-user
WORKDIR /home/jupyter-user

ENV JUPYTER_PORT=8889
ENV PYSPARK_DRIVER_PYTHON="jupyter"
ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --ip=0.0.0.0 --port=${JUPYTER_PORT}"

ENTRYPOINT ["/entrypoint.sh"]
