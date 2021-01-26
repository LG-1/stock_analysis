#!/bin/bash

export AIRFLOW_HOME=/mnt/f/08_Stock_Analysis/stock_analysis/airflow_jobs
cd airflow_jobs

PIDFILE=$AIRFLOW_HOME/airflow-webserver.pid

if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    echo "airflow-webserver service exists...., pid: $PID" 
    kill -QUIT $PID
    rm $PIDFILE
fi

airflow db init

airflow users create --username lg --firstname L --lastname G --role Admin --email ourantech@163.com --password f3f6948e1f08f0ecc9864456fc16ff5d4d05d3602d542f84587eef5f5771

# cd to /mnt/f/08_Stock_Analysis/stock_analysis/airflow
airflow webserver --port 8088

# cd to /mnt/f/08_Stock_Analysis/stock_analysis
airflow scheduler