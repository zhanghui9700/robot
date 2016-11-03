#!/bin/bash

PYTHON=/usr/bin/python2.7
cd /opt/yunmall/robot/iroman
set -eu

while [ true ];
do
    #sudo pon dsl-provider
    sleep 2
    echo `date` 
    echo `ip r`
    $PYTHON manage.py register
    #sudo poff
done
