#! /bin/bash

export AIRFLOW_HOME=/Users/liguang/WrokSpace/8888_stock_analysis/stock_analysis/airflow

PIDFILE=$AIRFLOW_HOME/airflow-webserver.pid

if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    echo "airflow-webserver service exists...., pid: $PID" 
    kill -QUIT $PID
    rm $PIDFILE
fi

airflow db init

airflow users create --username lg --firstname L --lastname G --role Admin --email ourantech@163.com --password f3f6948e1f08f0ecc9864456fc16ff5d4d05d3602d542f84587eef5f5771

airflow webserver --port 8088 -D

airflow scheduler