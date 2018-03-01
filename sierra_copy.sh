#!/bin/bash

# Update sierra_data in local dev environment
cd ~/repo/e-mini
git pull
cp ~/repo/e-mini/sierrafiles/* ~/PycharmProjects/ES/.sierra_data/

# Update sierra_data in Production environment
cp /app/e-mini/sierrafiles/* /app/ES/.sierra_data/