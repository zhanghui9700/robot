#!/bin/bash

PYTHON=/opt/robot/.venv/bin/python
cd /opt/robot/i18m
set -eu

export DISPLAY=:1 
$PYTHON manage.py order
