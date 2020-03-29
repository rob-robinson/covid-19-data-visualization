# CoViD-19 Data Visualization

This repo is my attempt to combine the data from Johns Hopkins in to datasets that I can work with to create data visualizations.

The data repo is maintained by Johns Hopkins University Center for Systems Science and Engineering, and is available here: https://github.com/CSSEGISandData/COVID-19 . 

This data repo must be cloned and up to date in order for this repo to work correctly.


#### Running Locally

```bash

# get the data
git clone https://github.com/CSSEGISandData/COVID-19

# get this repo
git clone https://github.com/rob-robinson/covid-19-data-visualization.git

cd covid-19-data-visualization/deployment/app_src

# create virtual environment with python 3.x:
python3 -m venv covid_testing

# activate the venv:
source covid_testing/bin/activate

# make sure you have the libs installed in the venv:
pip install -r requirements.txt

# make modifications to the configuration items in the deployment/app_src/src/app.py file to match your environment.

# Execute the program:
 
python ./src/app.py


```

#### Running with Docker Compose

Coming soon...

#### Data Sources:

* population data from https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population_density
* and https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html ... specifically:
* https://www2.census.gov/programs-surveys/popest/tables/2010-2019/state/totals/nst-est2019-01.xlsx