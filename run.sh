#!/bin/bash

PYTHON=/usr/bin/python2.7
cd /opt/robot/robot/18m
set -eu
$PYTHON manage.py order
