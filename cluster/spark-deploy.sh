#!/bin/bash

# Submit Spark job to the cluster
MASTER_CONTAINER=$(docker ps --filter name=spark-master --format "{{.ID}}")

# Copy job file to master
docker cp spark_jobs/cluster_analysis.py $MASTER_CONTAINER:/tmp/

# Execute job
docker exec $MASTER_CONTAINER \
  spark-submit --master spark://spark-master:7077 \
  --executor-memory 2G \
  --total-executor-cores 4 \
  /tmp/cluster_analysis.py
