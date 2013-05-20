'''
Created on 2013-05-19

@author: Neil
'''

import time
import math

def julian_centuries(date=time.gmtime()):
    '''
    Calculate the number of Julian Centuries from the epoch 2000.0
    (equivalent to Julian Day 2451545.0).
    '''
    jd = calculate_julian_day(date)
    delta = jd - 2451545.0
    return delta / 36525.0

def calculate_julian_day(t_struct=time.gmtime()):
    '''
    Calculate the Julian Day for a given date using the following formula:
    JD = 367 * Y - INT(7 * (Y + INT((M + 9)/12))/4) + INT(275 * M / 9)
         + D + 1721013.5 + UT/24
    Note that this is only valid for the year range 1900 - 2099.
    '''
    hour = t_struct.tm_hour + (t_struct.tm_min / 60.0) + (t_struct.tm_sec / 3600.0)
    day = t_struct.tm_mday
    month = t_struct.tm_mon
    year = t_struct.tm_year
    
    tmp = math.floor(7.0 * (year + math.floor((month + 9.0) / 12.0)) / 4.0)
    
    return 367.0 * year - tmp + math.floor(275.0 * month / 9.0)\
        + day + 1721013.5 + (hour / 24.0)

def calc_gregorian_date(julian_day):
    '''
    Convert the given Julian Day to Gregorian Date (in UT time zone).
    Based on the formula given in the Explanitory Supplement to the
    Astronomical Almanac, pg 604.
    '''
    l = (julian_day + 68569) & 0xFFFFFFFF
    n = (((4 * l) & 0xFFFFFFFF) / 146097) & 0xFFFFFFFF
    l = l - (((146097 * n + 3) & 0xFFFFFFFF) / 4) & 0xFFFFFFFF
    i = (((4000 * (l + 1)) & 0xFFFFFFFF) / 1461001) & 0xFFFFFFFF
    l = (l - (((1461 * i) / 4) & 0xFFFFFFFF) + 31) & 0xFFFFFFFF
    j = (((80 * l) & 0xFFFFFFFF) / 2447) & 0xFFFFFFFF
    d = (l - (((2447 * j) & 0xFFFFFFFF) / 80) & 0xFFFFFFFF) & 0xFFFFFFFF
    l = (j / 11) & 0xFFFFFFFF
    m = (j + 2 - 12 * l) & 0xFFFFFFFF
    y = (((100 * (n - 49)) & 0xFFFFFFFF) + i + 1)
     
    fraction = julian_day - math.floor(julian_day)
    d_hours = fraction * 24.0
    hours = d_hours & 0xFFFFFFFF
    d_minutes = (d_hours - hours) * 60.0
    minutes = d_minutes & 0xFFFFFFFF
    seconds = ((d_minutes - minutes) * 60.0) & 0xFFFFFFFF
    # this needs to be in the UT time zone
    return [y, m, d, hours+12, minutes, seconds]

def mean_sidereal_time(date, longitude):
    '''
    Calculate local mean sidereal time in degrees. Note that longitude is
    negative for western longitude values.
    '''
    jd = calculate_julian_day(date)
    delta = jd - 2451545.0
    
    gst = 280.461 + 360.98564737 * delta
    return normalize_angle(gst + longitude)

def normalize_angle(angle):
    remainder = angle % 360
    if remainder < 0:
        remainder += 360
    return remainder

def normalize_hours(time):
    remainder = time % 24
    if remainder < 0:
        remainder += 24
    return remainder

def clock_time_from_hrs(ut):
    hours = math.floor(ut) & 0xFFFFFFFF
    r_min = 60 * (ut - hours)
    minutes = math.floor(r_min) & 0xFFFFFFFF
    seconds = math.floor(r_min - minutes) & 0xFFFFFFFF
    return [hours, minutes, seconds]

if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    from units.LatLong import LatLong
    print time.gmtime()
    print mean_sidereal_time(time.gmtime(), LatLong(20, 16).longitude)
