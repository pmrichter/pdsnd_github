import time
import pandas as pd
import numpy as np

CITY_DATA_FILES = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

DAY_INPUT_MAP={'all': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}

MONTH_INPUT_MAP={'all': 0, 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
MONTH_INPUT_MAP_INVERTED = {v: k for k, v in MONTH_INPUT_MAP.items()}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    while True:
        city=input("Enter name of city: ")
        if city.lower() in CITY_DATA_FILES:
            print(f"Filtering for city {city}.")
            break
        else:
            print(f"City {city} not supported. Please try again.")

    # Get user input for month (all, january, february, ... , june)
    while True:
        month=input("Enter name of month to filter by, or 'all' to apply no month filter: ")
        if month.lower() in MONTH_INPUT_MAP:
            print(f"Filtering for month {month}.")
            break
        else:
            print(f"Month {month} not supported. Please try again.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input("Enter name of weekday to filter by, or 'all' to apply no weekday filter: ")
        if day.lower() in DAY_INPUT_MAP:
            print(f"Filtering for day {day}.")
            break
        else:
            print(f"Day {day} not supported. Please try again.")

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
    df = pd.read_csv(CITY_DATA_FILES[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['Trip Duration'] = pd.to_numeric(df['Trip Duration'])

    month = month.lower()
    day = day.lower()
    
    if month != 'all':
        month = MONTH_INPUT_MAP[month]
        df = df[df['month']==month]

    if day != 'all':
        df = df[df['day_of_week']==day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = MONTH_INPUT_MAP_INVERTED[df['month'].mode()[0]].title()
    print('most common month:', most_common_month)

    # Display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('most common day of week:', most_common_day_of_week)

    # Display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('most common start hour:', most_common_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station_counts=df['Start Station'].value_counts()
    print('most commonly used start station: ',  most_common_start_station_counts.index[0], '( count:',most_common_start_station_counts[0],')')

    # Display most commonly used end station
    most_common_end_station_counts=df['End Station'].value_counts()
    print('most commonly used end station: ',  most_common_end_station_counts.index[0], '( count:',most_common_end_station_counts[0],')')

    # Display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+" to "+df['End Station']
    most_common_combination_count=df['combination'].value_counts()
    print('most frequent combination of start station and end station trip: ',  most_common_combination_count.index[0], '( count:',most_common_combination_count[0],')')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("total travel time: ", df['Trip Duration'].sum(), "seconds")

    # Display mean travel time
    print("mean travel time: ", df['Trip Duration'].mean(), "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("user type stats: ")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if city=='washington':
        print("\nGender data not available for Washington.")
    else:        
        print("\nuser gender stats: ")
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if city=='washington':
        print("\nBirth Year data not available for Washington.")
    else:        
        print("\nuser birth year stats: ")
        print("earliest birth year", df['Birth Year'].min())
        print("most common birth year", df['Birth Year'].mode()[0])
        print("most recent birth year", df['Birth Year'].max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        show_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
        if show_data.lower() == 'yes':
            show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

def show_raw_data(df):

    pd.set_option('display.max_columns',200)
    
    for start in range(0,df.size,5):
        print(df[start:start+5])
        more_data = input('\nWould you like to see more data? Enter yes or no.\n')
        if more_data.lower() != 'yes':
            break
            
if __name__ == "__main__":
	main()
