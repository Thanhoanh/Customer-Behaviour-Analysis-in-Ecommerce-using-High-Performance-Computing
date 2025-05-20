# Dockerfile
FROM bitnami/spark:3.3

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install pandas numpy scikit-learn

# Set working directory
WORKDIR /app

# Copy Spark jobs and configs
COPY spark_jobs/ /app/spark_jobs/
COPY config/ /app/config/

# Set environment variables
ENV PYTHONPATH /app
ENV SPARK_HOME /opt/bitnami/spark
ENV PATH $PATH:$SPARK_HOME/bin

# Set entrypoint
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
