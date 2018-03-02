#!/bin/bash

if [ "${SIERRA_ENV}" == "PROD" ]
then
   echo "Prod environment variable set"
   # Update sierra_data in Production environment
   cd /source/e-mini/sierrafiles
   git pull
   cp /source/e-mini/sierrafiles/* /app/.sierra_data/
else
   echo "Test environment variable set"
   # Update sierra_data in local dev environment
   cd ~/repo/e-mini
   git pull
   cp ~/repo/e-mini/sierrafiles/* ~/PycharmProjects/ES/.sierra_data/
fi