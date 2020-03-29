import pandas as pd
import datetime as dt

# configs:

# this is the directory in which the daily data files are locations from Johns Hopkins
# where the COVID-19 directory is the Johns Hopkins University repo base...
daily_data_dir = '/Users/robrobinson/develop/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'

# where to place our output csvs
output_dir = '/Users/robrobinson/develop/covid-19-data-visualization/deployment/app_src/output/'

# where to look for local csv data
local_data_dir = '/Users/robrobinson/develop/covid-19-data-visualization/deployment/app_src/data/'

# get a list of dates for which we use the older headers/labels
model_one_dates = pd.date_range(start="2020-03-01", end="2020-03-21").to_pydatetime().tolist()

# get a list of dates from March 3rd, to today
all_dates = pd.date_range(start="2020-03-10", end=dt.datetime.today()).to_pydatetime().tolist()

# initial load of just states
all_data = pd.read_csv(local_data_dir + 'us_states.csv')

# this will only be for the file saving process... default to March 1...
last_available_date = '2020-03-01'

for date in all_dates:

    # create a string version of the date for use in file creation and labels:
    date_str = date.strftime("%m-%d-%Y")

    # open the proper file
    daily_csv_data_full_file_path = daily_data_dir + date_str + '.csv'

    try:

        # use older header labels
        if date in model_one_dates:

            df = pd.read_csv(daily_csv_data_full_file_path, skipinitialspace=False,
                             usecols=['Province/State', 'Country/Region', 'Confirmed', 'Deaths'])

        # use new header labels
        else:
            df = pd.read_csv(daily_csv_data_full_file_path, skipinitialspace=False,
                             usecols=['Province_State', 'Country_Region', 'Confirmed', 'Deaths'])

        # for naming...
        last_available_date = date.strftime("%Y-%m-%d")

    except OSError as e:
        # print('Note: '+date_str+'.csv was not found ... ' + e.strerror)
        continue  # will skip the rest of the block and move to next file

    df.rename(columns={'Confirmed': 'Confirmed-' + date_str}, inplace=True)
    df.rename(columns={'Deaths': 'Deaths-' + date_str}, inplace=True)

    df.rename(columns={'Province/State': 'Province_State'}, inplace=True)
    df.rename(columns={'Country/Region': 'Country_Region'}, inplace=True)

    # Filter for just US Territories:
    us_data = df.query("Country_Region == 'US'")

    # Apply grouping, but don't use groupby field as the index:
    state_data = us_data.groupby('Province_State', as_index=False)

    # create new dataframe using aggregated group by...
    tmp_df = state_data.sum()

    # merge the current dataframe into the master
    all_data = pd.merge(all_data, tmp_df, on='Province_State')


def get_deaths(input_list):

    to_return = []

    for line in input_list:

        if line == 'Province_State':
            to_return.append(line)

        if 'Deaths-' in line:
            to_return.append(line)

    return to_return


def get_confirmed(input_list):

    to_return = []

    for line in input_list:

        if line == 'Province_State':
            to_return.append(line)

        if 'Confirmed-' in line:
            to_return.append(line)

    return to_return

all_columns = list(all_data.columns.values)

deaths_columns = get_deaths(all_columns)

confirmed_columns = get_confirmed(all_columns)

df_confirmed = all_data[confirmed_columns]
df_deaths = all_data[deaths_columns]

# compression_opts = dict(method='zip', archive_name='out.csv')
#
# all_data.to_csv('out.zip', index=False,compression=compression_opts)

current_date_time = dt.datetime.today()

dt_string = current_date_time.strftime('%Y-%m-%d-%H-%M-%S')

df_confirmed.to_csv(output_dir + 'out-confirmed-' + last_available_date + '-' + dt_string + '.csv')
df_deaths.to_csv(output_dir + 'out-deaths-' + last_available_date + '-' + dt_string + '.csv')
