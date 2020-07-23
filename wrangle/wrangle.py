import pandas as pd
from scipy import stats
from datetime import datetime, timedelta


def wrangle_function(dataframe):
    '''This function takes in the SleepCycle app csv file, creates and cleans a
    dataframe, and generates statistics given a the date specified.

    :example use:
    - from wrangle import wrangle_function
    - t_stat, p_value, df = wrangle_function('dataframe')

    Args:
        :str:dataframe: The dataframe argument taken in the CSV file name from
        the SleepCycle app as a string.

    Returns:
        Test-statistic
        P-Value
    '''
    import pandas as pd
    from scipy import stats
    from datetime import datetime, timedelta
    df = pd.read_csv(f'./{dataframe}.csv', delimiter=';')
    df = df.drop(columns=['Heart rate', 'Wake up', 'Sleep Notes'])
    df['Sleep quality'] = df['Sleep quality'].str.rstrip('%').astype('float')/100
    df['Start'] = pd.to_datetime(df['Start'], infer_datetime_format=True)
    df['End'] = pd.to_datetime(df['End'], infer_datetime_format=True)

    wkday_int = []

    for elem in range(len(df['Start'])):
        if (df['Start'][elem].dayofweek == 0) and (df['Start'][elem].dayofweek == df['End'][elem].dayofweek):
            wkday_int.append(6)
        elif df['Start'][elem].dayofweek == df['End'][elem].dayofweek:
            wkday_int.append(df['End'][elem].dayofweek -1)
        else:
            wkday_int.append(df['Start'][elem].dayofweek)

    df['Weekday to Bed (int)'] = pd.DataFrame(wkday_int)

    day = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
        }

    df['Weekday to bed (name)'] = df['Weekday to Bed (int)'].map(day)
    df['Time in bed'] = pd.to_datetime(df['Time in bed']).dt.time
    df['Time in bed'] = df['Time in bed'].apply(lambda element: round((float(element.minute)/60) + (float(element.hour)), 2))

    date_lst = []
    for elem in range(len(df['Start'])):
        if df['Start'][elem].date() == df['End'][elem].date():
            date_lst.append(df['Start'][elem].date() - timedelta(days=1))
        else:
            date_lst.append(df['Start'][elem].date())

    df['Date to bed'] = date_lst

    df['Date to bed'] = df['Date to bed'].drop_duplicates(keep='first')
    df.dropna(subset=['Date to bed'], inplace=True)

    df['Before and During'] = df[['Start']].isin(df[:401])
    df['Before and During'] = df['Before and During'].replace(True, 'Before').replace(False, 'During')

    index_vals = df[df['Sleep quality'] < .2].index
    df.drop(index_vals, inplace=True)

    test_statistic, p_value = stats.ttest_ind(df['Sleep quality'][:401], df['Sleep quality'][401:], nan_policy='omit')
    return test_statistic, p_value, df
