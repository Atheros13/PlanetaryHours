from astral import LocationInfo
from astral.sun import sun
from astral import moon

import datetime

## CLASS ##

class SunMoonPhases():

    ''' '''

    def __init__(self, timezone, lat, long, date, *args, **kwargs):

        ''' '''

        self.date = date 
        city = LocationInfo("City", "Region", timezone, lat, long)
        self.sun = sun(city.observer, date=date, tzinfo=timezone)

    ## GET METHODS ##

    def get_moonphase(self, string=False):

        '''Returns a the raw moon phase value (0 - 27.99) unless passed 
        string=True when it returns a string value of the moon phase (and the raw value).'''

        phase = round(moon.phase(date=self.date), 2)

        if not string:
            return phase

        phases = [
            [1, "New Moon"], [6, "Waxing Crescent"], [8, "First Quarter"],
            [13, "Waxing Gibbous"], [15, "Fullmoon"], [20, "Waning Gibbous"],
            [22, "Third Quarter"], [27, "Waning Crescent"], [29, "New Moon"]
            ]

        for p in phases:
            if phase < p[0]:
                return "%s: %s" % (p[1], phase)

    def get_sunrise(self, string=False):

        '''Returns a datetime object for the sunrise on the self.date. If 
        string=True this returns a string value in the H:M:S format. '''

        if string:
            return self.sun["sunrise"].strftime("%H:%M:%S")
        return self.sun["sunrise"]

    def get_sunset(self, string=False):

        '''Returns a datetime object for the sunset on the self.date. If 
        string=True this returns a string value in the H:M:S format. '''

        if string:
            return self.sun["sunset"].strftime("%H:%M:%S")
        return self.sun["sunset"]

## ENGINE ##

if __name__ == "__main__":

    spheres = SunMoonPhases("NZ", -41.27, 174.77, datetime.date(2022, 10, 25))
    print(spheres.get_sunset(string=True))
    print(spheres.get_moonphase())
