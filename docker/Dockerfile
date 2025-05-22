# Stage 1: Base image with Spark and essential tools
FROM bitnami/spark:3.3 AS spark-base

# Switch to root user for package installation
USER root

# Install system tools and security packages
RUN mkdir -p /var/lib/apt/lists/partial && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        vim \
        apt-transport-https \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV SPARK_HOME="/opt/bitnami/spark" \
    PYSPARK_PYTHON=python3 \
    PATH="$PATH:$SPARK_HOME/bin" \
    JUPYTER_PORT=8889

# Copy Spark config
COPY spark-defaults.conf "$SPARK_HOME/conf/"

# Stage 2: Install Python dependencies
FROM spark-base AS pyspark

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip==23.1.2 && \
    pip install --no-cache-dir -r requirements.txt

# Stage 3: Runtime environment with entrypoint
FROM pyspark AS pyspark-runner

# Copy and set permissions FIRST
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create a non-root user for safety
RUN useradd -m sparkuser
USER sparkuser
WORKDIR /home/sparkuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["pyspark"]

# Stage 4: Optional Jupyter support
FROM pyspark-runner AS pyspark-jupyter

# Install Jupyter as root
USER root
RUN pip install --no-cache-dir notebook
USER sparkuser  # Switch back

# Jupyter configuration
ENV PYSPARK_DRIVER_PYTHON="jupyter" \
    PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --ip=0.0.0.0 --port=${JUPYTER_PORT}"

EXPOSE 8889
CMD ["jupyter", "notebook",
