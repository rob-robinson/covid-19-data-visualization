import pandas as pd
import datetime as dt

# US Population --> 329,500,000

DATA_DIR = '/Users/robrobinson/develop/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'

# from 03-10-2020 - 03-22-2020: do it the old way ...
model_one_dates = pd.date_range(start="2020-03-10", end="2020-03-21").to_pydatetime().tolist()

all_data = pd.DataFrame()

for date in model_one_dates:

    date_str = date.strftime("%m-%d-%Y")

    print("OLD:" + date_str)

    # open the proper file
    CONFIRMED = DATA_DIR + date_str + '.csv'
    df = pd.read_csv(CONFIRMED, skipinitialspace=False, usecols=['Province/State', 'Country/Region', 'Confirmed', 'Deaths'])

    df.rename(columns={'Confirmed': 'Confirmed-' + date_str + ''}, inplace=True)
    df.rename(columns={'Deaths': 'Deaths-' + date_str + ''}, inplace=True)

    df.rename(columns={'Province/State': 'Province_State'}, inplace=True)
    df.rename(columns={'Country/Region': 'Country_Region'}, inplace=True)

    us_data = df.query("Country_Region == 'US'")

    state_data = us_data.groupby('Province_State', as_index=False)

    tmp_df = state_data.sum()

    # print(tmp_df.info())

    if all_data.empty:
        all_data = tmp_df.copy()
    else:
        all_data = pd.merge(all_data, tmp_df, on='Province_State')


# otherwise do it the new way
model_two_dates = pd.date_range(start="2020-03-22", end=dt.datetime.today()).to_pydatetime().tolist()

for date in model_two_dates:

    date_str = date.strftime("%m-%d-%Y")

    print("NEW:" + date_str)

    CONFIRMED = DATA_DIR + date_str + '.csv'

    try:
        df = pd.read_csv(CONFIRMED, skipinitialspace=False, usecols=['Province_State', 'Country_Region', 'Confirmed', 'Deaths'])

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

print(all_data)