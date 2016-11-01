#!/bin/bash

PYTHON=/usr/bin/python2.7
cd /opt/yunmall/robot/iroman
set -eu

while [ true ];
do
    sleep 2
    echo `date`
    $PYTHON manage.py register
done
