def visualisations():
    '''This function will create visualizations of the sleep data acquired from
    the SleepCycle app.
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

    return print(f"{ax_4.legend()} \n{ax.legend()} \n{ax_1} \n{ax_2.legend()} \n{ax_3.set_title('Day to bed')}")
