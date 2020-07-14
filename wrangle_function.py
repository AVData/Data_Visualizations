import numpy as np
import pandas as pd

from scipy import stats
from datetime import datetime, timedelta
from scipy.stats.distributions import chi2

import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

import plotly
import cufflinks as cf
import plotly.express as px
import plotly.graph_objs as go
import chart_studio.plotly as py
import plotly.figure_factory as ff
from IPython.display import IFrame


def wrangle_function(dataframe):
    '''This function takes in the SleepCycle app csv file, creates and cleans a dataframe, and generates statistics given a the date specified.
    Args:
        dataframe: the dataframe argument takes in/is the the CSV file from the SleepCycle app
        split_date: The split_date argument is the date where the user would like to split the data frame.  This useful in looking at the statistical difference between two stretches of time, given a specific split date.
    Returns:
        Test-statistic
        P-Value
    '''
    split_date = 0
    df = pd.read_csv(f'./{dataframe}.csv', delimeter=';')
    df = df.drop(columns=['Heart rate', 'Wake up', 'Sleep Notes'])
    df['Sleep quality'] = df['Sleep quality'].str.rstring('%').astype('float')/100
    df['Start'] = pd.to_datetime(df['Start'], infrer_datetime_format=True)
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
        
        test_statistic, p_value = stats.ttest_ind(df['Sleep quality'][:401], df['Sleep quality'][401:], nan_policy='omit')
        
        return f"Test Statistic: {test_statistic}, \np-value: {p_value} \nDataFrame {df}"
    
def visualisations():
    '''This function will create visualizations of the sleep data acquired from the SleepCycle app.
    
    '''
    index_vals = df[df['Sleep quality'] < .2].index
    df.drop(index_vals, inplace=True)
    
    # Subplots
    # sns.set_style('white')
    # Distributions plots:
    fig, ax_4 = plt.subplots()
    ax_4 = sns.distplot(
                        df['Time in bed'][:401],
                        hist=False, color='r',
                        label='Before'
                        )
    ax_4 = sns.distplot(
                        df['Time in bed'][401:],
                        hist=False,
                        label='During'
                        )
    ax_4 = sns.distplot(
                        df['Time in bed'],
                        hist=False,
                        color='black',
                        label='Overall'
                        )
    ax_4.legend()

    fig, ax = plt.subplots()
    ax = sns.distplot(
                        df['Sleep quality'][:401],
                        hist=False,
                        color='r',
                        label='Before'
                        )
    ax = sns.distplot(
                        df['Sleep quality'][401:],
                        hist=False,
                        label='During'
                        )
    ax = sns.distplot(
                        df['Sleep quality'],
                        hist=False,
                        color='black',
                        label='Overall'
                        )
    ax.legend()


    # Line plots
    fig_1, ax_1 = plt.subplots()
    ax_1 = sns.lineplot(
                        y=df['Sleep quality'],
                        x=df['End'].dt.hour,
                        hue=df['Before and During'],
                        err_style='bars'
                        )


    # Box plots
    fig_2, ax_2 = plt.subplots()
    ax_2 = sns.barplot(
                       x='Weekday to bed (name)',
                       y=df['Time in bed'],
                       data=df,
                       hue='Before and During',
                       order=[
                           'Sunday',
                           'Monday',
                           'Tuesday',
                           'Wednesday',
                           'Thursday',
                           'Friday',
                           'Saturday'
                               ],
                       color='salmon'
                        )
    ax_2.legend()


    # Barplots
    fig_3, ax_3 = plt.subplots()
    ax_3 = sns.barplot(
                       x='Weekday to bed (name)',
                       y=df['Sleep quality'],
                       data=df,
                       hue='Before and During',
                       order=[
                           'Sunday',
                           'Monday',
                           'Tuesday',
                           'Wednesday',
                           'Thursday',
                           'Friday',
                           'Saturday'
                               ],
                       color='salmon',
                        )
    ax_3.legend()
    sns.despine()
    ax_3.set_title('Day to bed')

    return f"{ax_4.legend()} \n{ax.legend()} \n{ax_1} \n{ax_2.legend()} \n{ax_3.set_title('Day to bed')}"