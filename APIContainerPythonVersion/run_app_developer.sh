#!/bin/bash

if [ E${EXTURL} = "E" ]; then
  echo "EXTURL not set - Set it to something like 'http://mymachinehostname'"
  exit 1
fi
if [ E${EXTPORT} = "E" ]; then
  echo "EXTPORT not set - Set it to something like '8098'"
  exit 1
fi

APP_DIR=.

export APIAPP_MODE=DEVELOPER
export APIAPP_FRONTEND=_
export APIAPP_APIURL=${EXTURL}:${EXTPORT}/api
export APIAPP_APIDOCSURL=${EXTURL}:${EXTPORT}/apidocs
export APIAPP_FRONTENDURL=${EXTURL}:${EXTPORT}/frontend
export APIAPP_APIACCESSSECURITY=[]
export APIAPP_PORT=8098

if [ ! -f ./run_app_developer_secret.sh ]; then
  echo "ERROR"
  echo "run_app_developer_secret.sh dosen't exist. If you just cloned the repo you will need to"
  echo "copy run_app_developer_secret_example.sh to run_app_developer_secret.sh and fill in"
  echo "the values"
  exit 1
fi

source ./run_app_developer_secret.sh

export APIAPP_VERSION=
if [ -f ${APP_DIR}/VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/VERSION)
fi
if [ -f ${APP_DIR}/../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${APIAPP_VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi


#Python app reads parameters from environment variables
python3 ./src/app.py
