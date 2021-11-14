import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
                         

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter the name of the City you would like to explore.\n'
                '\nWould you like to explore the data for Chicago (CH), New York (NY), or Washington (WA)?\n'
                '\nPlease enter the name of the city or its abreviation.').lower()

    while city not in ['chicago', 'ch', 'new york city','ny', 'washington', 'wa']:
        city = input('\nPlease enter the name of the city or its abreviation.\n').lower()

    # Handle input of shortcuts   
    else:
        if city == 'ch' or city == 'chicago':
            print('You have selected Chicago! Selecting bikeshare data of Chicago.')
            city = 'chicago'
        elif city == 'new york' or city == 'new york city' or city == 'ny':
            print('You have selected New York City! Selecting bikeshare data of New York City.')
            city = 'new york city'
        elif city == 'washington' or city == 'wa':
            print('You have selected Washington! Selecting bikeshare data of Washington.')
            city = 'washington'
        
    # get user input for month (all, january, february, ... , june)
    month = input('Would you like to filter the data by month?\n''\nPlease enter \"all\" for no filter or the month you would like to select.').lower() # ggf.auch none einbauen für keine filter oder all?)
    while month not in ['all', 'january', 'february', 'march', 'april','mai', 'june']:
        month = input('\nPlease enter \"all\" for no filter or the month you would like to select.').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Would you like to filter the data by day?\n''\nPlease enter \"all\" for no filter or the day of week you would like to select.').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('\nPlease enter \"all\" for no filter or the day of week you would like to select.').lower()

    print('-'*40)
    
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from Start Time to create new column
    df['month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month != 'all':

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # extract day of week form Start Time to create new column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()] # hier ggf. noch day of week ergänzen auf Day
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = int(df['month'].mode()[0])
    print('The most common month is: {}'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].value_counts().nlargest(1)
    print('\nThe most common day of week is:{}'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]
    print('\nThe most popular hour is:{}'.format(popular_hour))

    #display the time to compute stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is:{}'.format(pop_start_station))
    
    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is:{}'.format(pop_end_station))

    # display most frequent combination of start station and end station trip
    start_end_comb = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nThe most frequent combination of start station and end station respectively most popular trip is:\n{}'.format(start_end_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_t_time = df['Trip Duration'].sum() / 3600
    print('The total travel time in hours is: {}'.format(total_t_time))

    # display mean travel time
    mean_t_time = df['Trip Duration'].mean() / 60
    print('The mean of the travel time (in minutes) is: {}'.format(mean_t_time))   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('These are the different user types:\n{}'.format(user_types))

    # dfisplay counts of gender
    # exception handling in case coulum is missing
    try:
        gender = df['Gender'].value_counts()
    except KeyError:
        print('\nNo gender Data available!')
    else:
        gender = df['Gender'].value_counts()    
        print('\nThis is the gender distribution:\n{}'.format(gender))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = df['Birth Year'].min()
        most_recent_yob = df['Birth Year'].max()
        most_common_yob = df['Birth Year'].mode()[0]
    except KeyError:
        print('\nNo Data concerning the year of birth available!')
    else:
        # earliest year of birth
        earliest_yob = df['Birth Year'].min()
        print('\nThe earliest year of birth is: {}'.format(int(earliest_yob)))

        # most recent year of birth
        most_recent_yob = df['Birth Year'].max()
        print('The most recent year of birth is: {}'.format(int(most_recent_yob)))

        # most common year of birth
        most_common_yob = df['Birth Year'].mode()[0]
        print('The most common year of birth is: {}'.format(int(most_common_yob)))
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # displays raw data 

    # remove added columns from visualization to turn back to raw data
    df = df.drop(['month','hour', 'day_of_week'], axis = 1)

    x = 0

    display_raw_data = input('\n Would you like to see a few lines of raw data? Yes or No?: ').lower()

    while True:

        if display_raw_data == 'yes':
            x += 5
            print (df.head(x))

        if display_raw_data == 'no':
            return
        display_raw_data = input('Would you like to see 5 more lines of raw data? Yes or No?').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
