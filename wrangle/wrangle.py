import pandas as pd
from scipy import stats
from datetime import datetime, timedelta


def wrangle_function(dataframe):
    '''This function takes in the SleepCycle file name as an argument and
    cleans the respective CSV DataFrame.  It then generates a new dataframe
    with it's respective statistics pertaining to a specific set of parameters.
    The parameters are partitionaning of the dataframe given an arbitrary date.

    :example use:
    - from wrangle.wrangle import wrangle_function
    - t_stat, p_value, sleepcycle_df = wrangle_function('dataframe')

    Args:
        str: The argument used in this function is the SleepCycle csv file name
        as a string value.  The function will then search for that file in the
        repository and execute the analysis and cleaning.  In the future I'll
        be including argument to allow for date selection for the desired
        partitioning.

    Returns:
        Test-statistic
        P-Value
        Cleaned DataFrame
    '''

    # Imports the dataframe given the string name used as argument, and drops
    # a few columns
    df = pd.read_csv(f'../{dataframe}.csv', delimiter=';')
    df = df.drop(columns=[
                        'Heart rate',
                        'Wake up',
                        'Sleep Notes'
                        ])

    # Stripping the Sleepl quality percentage string, to turn it into a foat
    df['Sleep quality'] = df['Sleep quality'].str\
                                             .rstrip('%')\
                                             .astype('float')/100

    # 'Start' and 'End' columns turned into datetime types
    df['Start'] = pd.to_datetime(
                                df['Start'],
                                infer_datetime_format=True
                                )
    df['End'] = pd.to_datetime(
                                df['End'],
                                infer_datetime_format=True
                                )

    # For look: wkday_int list is the list that eventually becomes the new
    # 'Weekday to Bed (int)' column; column of weekdays per day of week
    wkday_int = []
    for elem in range(len(df['Start'])):
        if (df['Start'][elem].dayofweek == 0) and\
           (df['Start'][elem].dayofweek == df['End'][elem].dayofweek):
            wkday_int.append(6)
        elif df['Start'][elem].dayofweek == df['End'][elem].dayofweek:
            wkday_int.append(df['End'][elem].dayofweek - 1)
        else:
            wkday_int.append(df['Start'][elem].dayofweek)
    df['Weekday to Bed (int)'] = pd.DataFrame(wkday_int)

    # Dictionary that is used in mapping to go from weekday int to weekday name
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
    df['Time in bed'] = pd.to_datetime(df['Time in bed'])\
                          .dt\
                          .time
    df['Time in bed'] = df['Time in bed']\
                        .apply(lambda element: round(
                                                (float(element.minute)/60) +\
                                                (float(element.hour)),
                                                2))

    # For loop: list holds values that will become 'Date to bed' column;
    # the loop takes the values of the 'Start' and 'End' columns and compares
    # them to see if the two dates are the same, if so, it replaces the start
    # date to the appropriate previous date.  Having both start and end dates
    # be the same implies the individual went to bed past midnight, but the
    # but actually intended to go to bed the night prior; resulting in the
    # 'Date to bed' column
    date_lst = []
    for elem in range(len(df['Start'])):
        if df['Start'][elem].date() == df['End'][elem].date():
            date_lst.append(df['Start'][elem].date() - timedelta(days=1))
        else:
            date_lst.append(df['Start'][elem].date())
    df['Date to bed'] = date_lst

    # the previous for loop created some duplicates that need to be dropped.
    df['Date to bed'] = df['Date to bed'].drop_duplicates(keep='first')
    df.dropna(subset=['Date to bed'], inplace=True)

    # Setting up a colum to split the dataframe.
    df['Before and During'] = df[['Start']].isin(df[:401])
    df['Before and During'] = df['Before and During'].replace(
                                                            True,
                                                            'Before'
                                                    ).replace(
                                                            False,
                                                            'During'
                                                            )

    # Removes outliers; values in sleep quality < .2
    index_vals = df[df['Sleep quality'] < .2].index
    df.drop(index_vals, inplace=True)

    # Returned variables
    test_statistic, p_value = stats.ttest_ind(
                                            df['Sleep quality'][:401],
                                            df['Sleep quality'][401:],
                                            nan_policy='omit'
                                            )

    return test_statistic, p_value, df
