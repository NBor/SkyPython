'''
// Copyright 2008 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// 
// Original Author: Kevin Serafini, Brent Bryan
// 
// Notification of Change: The original java source code has been
// modified in that it has been rewritten in the python programming
// language and additionally, may contain components and ideas that are 
// not found in the original source code.


   Copyright 2013 Neil Borle and Paul Lu

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


Created on 2013-05-19

@author: Neil Borle
'''

import time
import math

def julian_centuries(t_struct=time.gmtime()):
    '''
    Calculate the number of Julian Centuries from the epoch 2000.0
    (equivalent to Julian Day 2451545.0).
    t_struct is a structure representing the current date (ex. time.gmtime())
    '''
    jd = calculate_julian_day(t_struct)
    delta = jd - 2451545.0
    return delta / 36525.0

def calculate_julian_day(t_struct=time.gmtime()):
    '''
    Calculate the Julian Day for a given date using the following formula:
    JD = 367 * Y - INT(7 * (Y + INT((M + 9)/12))/4) + INT(275 * M / 9)
         + D + 1721013.5 + UT/24
    Note that this is only valid for the year range 1900 - 2099.
    t_struct is a structure representing the current date (ex. time.gmtime())
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

def mean_sidereal_time(t_struct, longitude):
    '''
    Calculate local mean sidereal time in degrees. Note that longitude is
    negative for western longitude values.
    t_struct is a structure representing the current date (ex. time.gmtime())
    '''
    jd = calculate_julian_day(t_struct)
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
    '''
    from units.LatLong import LatLong
    print time.gmtime()
    print mean_sidereal_time(time.gmtime(), LatLong(20, 16).longitude)
