#!/bin/bash

PYTHON=/usr/bin/python2.7
cd /opt/yunmall/robot/iroman
set -eu
#!/bin/env bash
while [ true ]; do
    sleep 3
    $PYTHON manage.py register
done
