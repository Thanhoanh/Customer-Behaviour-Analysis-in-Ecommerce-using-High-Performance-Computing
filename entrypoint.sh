#!/bin/bash

# entrypoint.sh

# Start Spark master or worker based on environment variable
if [ "$SPARK_MODE" = "master" ]; then
    /opt/bitnami/spark/sbin/start-master.sh
elif [ "$SPARK_MODE" = "worker" ]; then
    /opt/bitnami/spark/sbin/start-worker.sh $SPARK_MASTER_URL
fi

# Keep the container running
tail -f /dev/null
