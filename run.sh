#!/bin/bash

set -eu

DIR=`pwd`
echo ${DIR}
echo `basename $0`
PYTHON=${DIR}/.venv/bin/python
PID=${DIR}/logs/order.running

export DISPLAY=:1 

if [ -f $PID ]; then
    echo "auto order is running."
else
    cd ${DIR}/i18m
    touch  $PID && echo $$ > $PID
    echo "start order program."
    sleep 5
    $PYTHON manage.py order || rm -rf $PID
    rm -rf $PID
fi
