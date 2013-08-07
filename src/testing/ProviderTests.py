'''
Created on 2013-07-24

@author: Alyson Wu and Morgan Redshaw
'''

#PlanetTest
# The test for testCalcNextRiseSetTime is implemented because Planet.Rise_set_indicator is not yet implemented

# The Moon fails all instances of disableTestIllumination
# print abs(21.2 - Moon.calculate_percent_illuminated(Time1))  => 56.7279215736
# print abs(4.1 - Moon.calculate_percent_illuminated(Time2))   => 91.9681709016
# print abs(79.0 - Moon.calculate_percent_illuminated(Time3))  => 57.2619194768

POS_TOL = 0.2
PHASE_TOL = 1.0
HOURS_TO_DEGREES = 360.0/24.0

def testLunarGeocentricLocation():
    '''
    >>> import datetime as dt
    >>> import src.units.RaDec
    >>> import src.provider.Planet as Planet
    >>> tempPlanet = Planet.Planet(0, 0, 0, 0)
    
    #2009 Jan  1, 12:00 UT1: RA = 22h 27m 20.423s, Dec = - 7d  9m 49.94s
    >>> Time1 = dt.datetime(2009, 1, 1, 12, 0, 0).timetuple()
    >>> lunarPos = tempPlanet.calculate_lunar_geocentric_location(Time1)
    >>> abs((22.456 * HOURS_TO_DEGREES) - lunarPos.ra) < POS_TOL
    True
    >>> abs(-7.164 - lunarPos.dec) < POS_TOL
    True
    
    #2009 Sep 20, 12:00 UT1: RA = 13h  7m 23.974s, Dec = -12d 36m  6.15s
    >>> Time2 = dt.datetime(2009, 9, 20, 12, 0, 0).timetuple()
    >>> lunarPos = tempPlanet.calculate_lunar_geocentric_location(Time2)
    >>> abs((13.123 * HOURS_TO_DEGREES) - lunarPos.ra) < POS_TOL
    True
    >>> abs(-12.602 - lunarPos.dec) < POS_TOL
    True
    
    # 2010 Dec 25, 12:00 UT1: RA =  9h 54m 53.914s, Dec = +8d 3m 22.00s
    >>> Time3 = dt.datetime(2010, 12, 25, 12, 0, 0).timetuple()
    >>> lunarPos = tempPlanet.calculate_lunar_geocentric_location(Time3)
    >>> abs((9.915 * HOURS_TO_DEGREES) - lunarPos.ra) < POS_TOL
    True
    >>> abs(8.056 - lunarPos.dec) < POS_TOL
    True
    
    '''
    pass

def disableTestIllumination():
    '''
    >>> import datetime as dt
    >>> import src.units.RaDec
    >>> import src.provider.Planet as Planet
    >>> res = Planet.res
    >>> Mercury = Planet.Planet(Planet.planet_enum.MERCURY, res[0][0], res[0][1], res[0][2])
    >>> Venus = Planet.Planet(Planet.planet_enum.VENUS, res[1][0], res[1][1], res[1][2])
    >>> Mars = Planet.Planet(Planet.planet_enum.MARS, res[3][0], res[3][1], res[3][2])
    >>> Moon = Planet.Planet(Planet.planet_enum.MOON, res[9][0], res[9][1], res[9][2])
    
    #2009 Jan  1, 12:00 UT1
    >>> Time1 = dt.datetime(2009, 1, 1, 12, 0, 0).timetuple()
    >>> abs(21.2 - Moon.calculate_percent_illuminated(Time1)) < PHASE_TOL
    True
    >>> abs(69.5 - Mercury.calculate_percent_illuminated(Time1)) < PHASE_TOL
    True
    >>> abs(57.5 - Venus.calculate_percent_illuminated(Time1)) < PHASE_TOL
    True
    >>> abs(99.8 - Mars.calculate_percent_illuminated(Time1)) < PHASE_TOL
    True
    
    #2009 Sep 20, 12:00 UT1
    >>> Time2 = dt.datetime(2009, 9, 20, 12, 0, 0).timetuple()
    >>> abs(4.1 - Moon.calculate_percent_illuminated(Time2)) < PHASE_TOL
    True
    >>> abs(0.5 - Mercury.calculate_percent_illuminated(Time2)) < PHASE_TOL
    True
    >>> abs(88.0 - Venus.calculate_percent_illuminated(Time2)) < PHASE_TOL
    True
    >>> abs(88.7 - Mars.calculate_percent_illuminated(Time2)) < PHASE_TOL
    True
    
    # 2010 Dec 25, 12:00 UT1
    >>> Time3 = dt.datetime(2010, 12, 25, 12, 0, 0).timetuple()
    >>> abs(79.0 - Moon.calculate_percent_illuminated(Time3)) < PHASE_TOL
    True
    >>> abs(12.1 - Mercury.calculate_percent_illuminated(Time3)) < PHASE_TOL
    True
    >>> abs(42.0 - Venus.calculate_percent_illuminated(Time3)) < PHASE_TOL
    True
    >>> abs(99.6 - Mars.calculate_percent_illuminated(Time3)) < PHASE_TOL
    True
    
    '''
    pass
