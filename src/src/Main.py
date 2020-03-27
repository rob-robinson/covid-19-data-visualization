import pandas as pd
import datetime as dt

# population data from https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population_density
# and https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html ... specifically:
# https://www2.census.gov/programs-surveys/popest/tables/2010-2019/state/totals/nst-est2019-01.xlsx

DATA_DIR = '/Users/robrobinson/develop/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'

# from 03-10-2020 - 03-22-2020: do it the old way ...
model_one_dates = pd.date_range(start="2020-03-10", end="2020-03-21").to_pydatetime().tolist()

# initial load of states and popluations
all_data = pd.read_csv('../data/us_states_populations.csv')

for date in model_one_dates:

    date_str = date.strftime("%m-%d-%Y")

    # open the proper file
    CONFIRMED = DATA_DIR + date_str + '.csv'

    try:
        df = pd.read_csv(CONFIRMED, skipinitialspace=False,
                         usecols=['Province/State', 'Country/Region', 'Confirmed', 'Deaths'])

    except OSError as e:
        print('Note: '+date_str+'.csv was not found ... ' + e.strerror)
        continue  # will skip the rest of the block and move to next file

    df.rename(columns={'Confirmed': 'Confirmed-' + date_str}, inplace=True)
    df.rename(columns={'Deaths': 'Deaths-' + date_str}, inplace=True)

    df.rename(columns={'Province/State': 'Province_State'}, inplace=True)
    df.rename(columns={'Country/Region': 'Country_Region'}, inplace=True)

    us_data = df.query("Country_Region == 'US'")

    state_data = us_data.groupby('Province_State', as_index=False)

    tmp_df = state_data.sum()

    if all_data.empty:
        all_data = tmp_df.copy()
    else:
        all_data = pd.merge(all_data, tmp_df, on='Province_State')


# otherwise do it the new way
model_two_dates = pd.date_range(start="2020-03-22", end=dt.datetime.today()).to_pydatetime().tolist()

for date in model_two_dates:

    date_str = date.strftime("%m-%d-%Y")

    CONFIRMED = DATA_DIR + date_str + '.csv'

    try:
        df = pd.read_csv(CONFIRMED, skipinitialspace=False,
                         usecols=['Province_State', 'Country_Region', 'Confirmed', 'Deaths'])

    except OSError as e:
        print('Note: '+date_str+'.csv was not found ... ' + e.strerror)
        continue  # will skip the rest of the block and move to next file

    df.rename(columns={'Confirmed': 'Confirmed-' + date_str + ''}, inplace=True)
    df.rename(columns={'Deaths': 'Deaths-' + date_str + ''}, inplace=True)

    us_data = df.query("Country_Region == 'US'")

    state_data = us_data.groupby('Province_State', as_index=False)

    tmp_df = state_data.sum()

    if all_data.empty:
        all_data = tmp_df.copy()
    else:
        all_data = pd.merge(all_data, tmp_df, on='Province_State')


# I wonder if I can create new columns in all_data for the following calculations:
# -- deaths per confirmed
# -- confirmed per million people
# -- deaths per million people

# compression_opts = dict(method='zip', archive_name='out.csv')
#
# all_data.to_csv('out.zip', index=False,compression=compression_opts)

# compression_opts = dict(method='zip', archive_name='out.csv')

all_data.to_csv('out.csv')
