import gpxpy

WEEKDAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']


class Effort:
    """ Class for single training units. """

    def __init__(self, gpx: gpxpy):
        self.__gpx = gpx
        self.uphill = self.__gpx.get_uphill_downhill().uphill
        self.downhill = self.__gpx.get_uphill_downhill().downhill
        self.distance = self.__gpx.length_3d()
        self.duration = self.__gpx.get_duration()
        self.start_time = self.__gpx.get_time_bounds().start_time
        self.end_time = self.__gpx.get_time_bounds().end_time

        # time stuff:
        self.year, self.week_number, self.weekday_number = self.start_time.isocalendar()
        self.weekday = WEEKDAYS[self.weekday_number - 1]  # minus one because ``isocalendar`` counts from 1

    def __eq__(self, other):
        return ((self.distance - other.distance) / self.distance < 1e-2
                and self.year == other.year
                and self.week_number == other.week_number
                and self.weekday_number == other.weekday_number
                and self.end_time > other.start_time # other starts before self ends
                and other.end_time > self.start_time) # self starts before other ends
