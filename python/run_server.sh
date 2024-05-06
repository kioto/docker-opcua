#!/bin/sh

cd ${HOME}

. ./venv/bin/activate
python opcua_server.py
