#!/usr/bin/env bash

cd deployment/app_src

python3 -m venv covid_testing

source covid_testing/bin/activate

pip install -r requirements.txt

python src/app.py 