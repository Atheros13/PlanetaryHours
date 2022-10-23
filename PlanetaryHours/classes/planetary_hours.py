## NOTES ##

'''
Though I rarely have need to find out the Planetary Hours of a given day, whenever I do
I have to calculate it manually. This program will calculate them for me instead.

I will only have to create an instance of PlanetaryHours() and pass it arguments for 
the day, sunrise, sunset, sunrise the next day, or as required. 

20/10/22 - Future Idea: It may be possible to add further functionality by using 
the Python package 'astral' (or something similar) to produce the sunrise/sunset times 
for a given location on a specific day. This would mean PlanetaryHours() could be rewritten so 
that the only arguments required are the location and date. 

'''

## IMPORTS ##

from datetime import datetime
import re

## CLASSES ##

class PlanetaryHours():

    '''Returns a print out of the Planetary Hours of a given Day, based on 
    the day and/or night  '''

    sphere_order = ["Sol", "Venus", "Mercury", "Luna", "Saturn", "Jupiter", "Mars"]
    day_to_sphere = ['Sunday', 'Friday', 'Wednesday', 'Monday', 'Saturday', 'Thursday', 'Tuesday']

    def __init__(self, *args, **kwargs):

        '''This class is is passed three to four arguments, depending on whether 
        the user requires only the day hours (sunrise1 and sunset), 
        only the night hours (sunset and sunrise2), or the whole day (sunrise 1, sunset, sunrise2). 

        The time arguments passed to these parameters must be in 24 hour time in the string format: 13:45

        The day value is always required.'''

        self.day = kwargs.get('day')
        if self.day == None or self.day not in self.day_to_sphere:
            return "Either no day argument was passed, or it is not in the correct format e.g. 'Sunday'."

        # (I know how messy this section is, but I was coding after 2 big nights of drinking,
        # no sleep for 36+ hours, and an outrageous cocktail of chemical indulgences.)
        # Assigns time based arguments to variables, checks they are in the correct string format, 
        # and then converts them into datetime objects.
        self.sunrise1 = kwargs.get('sunrise1', None)
        self.sunset = kwargs.get('sunset', None)
        self.sunrise2 = kwargs.get('sunrise2', None)
        if not self.check_time_format():
            return "All time values need to be in the format '13:46'."
        self.sunrise1 = self.convert_time(self.sunrise1)
        self.sunset = self.convert_time(self.sunset)
        self.sunrise2 = self.convert_time(self.sunrise2)

        # This is a dictionary of the 24 hours in a day and night period. 
        # Depending on what time period is required, later methods will populate this dict.
        self.hours = {}
        for n in range(1,25):
            self.hours[n] = None # non-null values will be [Start Time, End Time, Sphere]

        # Calculates hour lengths, hour start and end times, and their associated sphere,
        # then poplulates self.hours with the data.
        if self.calculate_day_hour():
            self.build_day_hours()
        if self.calculate_night_hour():
            self.build_day_hours() 

    ## FUNCTIONS ##

    def display(self):

        '''Returns a formatted string of the data contained in the self.hours dict. '''

        text = "CHART OF PLANETARY HOURS\n\n"
        text += "Day: %s (%s)\n\n" % (self.day, self.sphere_order[self.day_to_sphere.index(self.day)])

        for h in range(1,13):
            data = self.hours[h]
            if data == None:
                break
            if h == 1:
                text += "DAY HOURS - Hour Length: %s\n\n" % self.day_hour_length
            text += "Hour %s\t%s\t%s - %s\n" % (h, data[2], data[0], data[1])

        for h in range(13,25):
            data = self.hours[h]
            if data == None:
                break
            if h == 13:
                text += "\nNIGHT HOURS - Hour Length: %s\n\n" % self.night_hour_length
            text += "Hour %s\t%s\t%s - %s\n" % (h, data[2], data[0], data[1])

        return text


    ## METHODS ## 

    def check_time_format(self):

        '''Returns False if any of the times provided are not in the correct string format e.g. '13:45'
        otherwise it returns True. '''

        for time in [self.sunrise1, self.sunset, self.sunrise2]: 
            if not None:
                if not re.search('^[0-9][0-9]:[0-9][0-9]$', time):
                    return False

        return True

    def convert_time(self, clock):

        '''Returns a datetime object of a given time in string format. '''

        if clock != None:
           return datetime.strptime(clock, "%H:%M")

    def calculate_sphere_hour(self, hour):

        '''Counts through the sphere list (pattern) till it finds the sphere
        that is associated with a given hour on the given self.day. '''

        # establish the index of the day which will correlate to the index of
        # the sphere in the 1st hour that day.
        sphere_index = self.day_to_sphere.index(self.day)
        
        for h in range(hour):

            if h == hour-1:
                sphere = self.sphere_order[sphere_index]
                return sphere

            if sphere_index == 6:
                sphere_index = 0
            else:
                sphere_index += 1
            
    def calculate_day_hour(self):

        '''Populates the self.hours dict with data for each hour of the daytime. 
        The data is in the form of a list [start_time, end_time, sphere]. '''

        # check if day hours are required
        if self.sunrise1 == None:
            return False

        # calculate total daytime minutes (returns a timedelta object)
        total = self.sunset-self.sunrise1

        # divide by 12 and establish the length of a daytime hour
        self.day_hour_length = total/12

        # for each daytime hour, build a list containing the start time, end time, 
        # and the associated sphere, then assign it to the correct hour in the dict self.hours
        start_time = self.sunrise1
        for h in range(1,13):

            end_time = start_time + self.day_hour_length
            sphere = self.calculate_sphere_hour(h)
            
            self.hours[h] = [start_time.strftime("%H:%M"), 
                                end_time.strftime("%H:%M"),
                                sphere]


            start_time = end_time

    def calculate_night_hour(self):

        '''Populates the self.hours dict with data for each hour of the nighttime. 
        The data is in the form of a list [start_time, end_time, sphere]. '''

        # check if night hours are required
        if self.sunrise2 == None:
            return False
 
        # calculate total nighttime minutes (which is time between sunset and midnight 
        # added to the time of sunrise2)
        midnightish = datetime.strptime("23:59", "%H:%M")
        midnight = datetime.strptime("00:00", "%H:%M")
        total = (midnightish-self.sunset) + (self.sunrise2 - midnight)

        # divide by 12 and establish the length of a nighttime hour
        self.night_hour_length = total/12

        # for each nighttime hour, build a list containing the start time, end time, 
        # and the associated sphere, then assign it to the correct hour in the dict self.hours
        start_time = self.sunset
        for h in range(13,25):

            end_time = start_time + self.night_hour_length
            sphere = self.calculate_sphere_hour(h)

            self.hours[h] = [start_time.strftime("%H:%M"), 
                                end_time.strftime("%H:%M"),
                                sphere]

            start_time = end_time

## ENGINE ##

'''This is where the PlanetaryHours() class is instantiated with the data provided. '''

# Change the values below for the day you wish to calculate
day = "Tuesday"
sunrise1="06:09"
sunset="20:00"
sunrise2="06:08"

# The following lines create and display the data
planetary_hours = PlanetaryHours(day=day, sunrise1=sunrise1, sunset=sunset, sunrise2=sunrise2)
print(planetary_hours.display())


