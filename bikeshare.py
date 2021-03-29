import time
import pandas as pd
import numpy as np
import calendar

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = str(input("\nPlease enter the city you would like to know more about: \n")).lower()
        """Ensures that the code continues even if the user input is not compliant with city name inputs
        """
        if city not in cities:
            print('Hmm I can only tell you about Chicago, New York City, or Washington. Try again with one of those instead')
            continue
        else:
            print('\nGreat. Let\'s take a look at data from {}.'.format(city.upper()))
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    """Repeats the exact same code as above but with months"""
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("\nPlease enter any month between January and June or for all the months simply type 'all': \n").lower()
        if month not in months:
            print("Are you sure that\'s a month between January and June? Try it again. If you\'re not sure and want to see all the months type 'all'")
            continue
        else:
            print('\nLet\'s look at ', month.upper(), 'in', city.upper())
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    """Repeats the exact same code as above with days"""
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day of the week would you like to look at? If you want all the days in a week type 'all': ").lower()
        if day not in days:
            print('You need to try again with a day of the week.')
            continue
        else:
            print('Great! Let\'s look at the data for', day.upper(), 'in', month.upper(), 'in', city.upper(), '.')
            break

    print('-'*40)
    return city, month, day

def display_data(df):
    """
    Displays 5 random rows of raw data if the user inputs 'yes'.
    Continues with the program is user inputs 'no'.
    """
    view_data = input('\nBefore we get started, would you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    # Ask the user if they want to see raw data 'yes/no'
    # While 'yes', show raw data and ask the user again
    # If 'no', the loop aborts
    while view_data == 'yes':
        print(df.iloc[start_loc: start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to see 5 more rows?: ").lower()

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

    #Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to_datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract the month, day, hour from Start Time to create new columns (month, day_of_week, hour)
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    #Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].value_counts().idxmax()
    common_month = calendar.month_name[common_month]
    print('The month common month is', common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    print('The most common day is', common_day)

    # TO DO: display the most common start hour
    common_start = df['start_hour'].mode()[0]
    print('The most common start time is',common_start,':00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print('\nThe most common start station is \n{}'.format(common_start_station.upper())

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print('\nThe most common end station is \n{}'.format(common_end_station.upper())

    # TO DO: display most frequent combination of start station and end station trip
    popular_start = df['Start Station'].mode()[0]
    popular_end = df['End Station'].mode()[0]
    common_combo = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nThe most common combination of starting and ending stations is \n{}'.format(common_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel duration time of all trips combined is', int(total_travel_time/60),'minutes')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel duration time of a bike ride is', int(mean_travel_time/60),'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User Type Stats:')
    user_types = df['User Type'].value_counts()
    print('Count of users by type:{}\n'.format(pd.DataFrame(user_types)))
    if city.lower() != 'washington':
        # TO DO: Display counts of gender
        print('Gender Stats:')
        gender_types = df ['Gender'].value_counts()
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('The earliest birth year is',int(earliest_birth_year))
        most_recent_birth_year = df['Birth Year'].max()
        print('The most recent birth year is',int(most_recent_birth_year))
        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
        print('The most common birth year is',int(most_common_birth_year))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
