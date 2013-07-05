'''
Created on 2013-06-26

@author: Neil
'''

import time
import math
from OrbitalElements import OrbitalElements
from ..base.TimeConstants import MILLISECONDS_PER_DAY, MILLISECONDS_PER_WEEK, MILLISECONDS_PER_HOUR
from ..units.RaDec import RaDec, calculate_ra_dec_dist
from ..units.GeocentricCoordinates import get_instance as gc_get_instance
from ..units.HeliocentricCoordinates import get_instance as hc_get_instance
from ..utils import Geometry as Geometry
from ..utils.Enumeration import enum
from ..utils.TimeUtil import julian_centuries, calculate_julian_day

#Enum that identifies whether we are interested in rise or set time.
rise_set_indicator = enum(RISE=0, SET=1)
    
planet_enum = enum(MERCURY=0, VENUS=1, SUN=2, MARS=3, 
              JUPITER=4, SATURN=5, URANUS=6, 
              NEPTUNE=7, PLUTO=8, MOON=9)

res = {0 : ["mercury", "Mercury", 1 * MILLISECONDS_PER_DAY],
       1 : ["venus", "Venus", 1 * MILLISECONDS_PER_DAY],
       2 : ["sun", "Sun", 1 * MILLISECONDS_PER_DAY],
       3 : ["mars", "Mars", 1 * MILLISECONDS_PER_DAY],
       4 : ["jupiter", "Jupiter", 1 * MILLISECONDS_PER_WEEK],
       5 : ["saturn", "Saturn", 1 * MILLISECONDS_PER_WEEK],
       6 : ["uranus", "Uranus", 1 * MILLISECONDS_PER_WEEK],
       7 : ["neptune", "Neptune", 1 * MILLISECONDS_PER_WEEK],
       8 : ["pluto", "Pluto", 1 * MILLISECONDS_PER_WEEK],
       9 : ["moon4", "Moon", 1 * MILLISECONDS_PER_HOUR]}

class Planet(object):
    '''
    classdocs
    '''
    #Maximum number of times to calculate rise/set times. If we cannot
    # converge after this many iteretions, we will fail.
    MAX_ITERATIONS = 25
    
    def get_image_resource_id(self, time_struct):
        # Returns the resource id for the planet's image.
        if self.id == planet_enum.MOON:
            return self.get_lunar_phase_image_id(time_struct)
        
        return self.image_resource_id
    
    def get_lunar_phase_image_id(self, time_struct):
        # First, calculate phase angle:
        phase = self.calculate_phase_angle(time_struct)
        
        # Next, figure out what resource id to return.
        if phase < 22.5:
            # New moon.
            return "moon0"
        elif phase > 150.0:
            # Full moon.
            return "moon4"
        
        # Either crescent, quarter, or gibbous. Need to see whether we are
        # waxing or waning. Calculate the phase angle one day in the future.
        # If phase is increasing, we are waxing. If not, we are waning.
        tomorrow = time.gmtime(time.mktime(time_struct) + 24 * 3600 * 1000)
        phase2 = self.calculate_phase_angle(tomorrow)
        
        if phase < 67.5:
            # Crescent
            return "moon1" if phase2 > phase else "moon7"
        elif phase < 112.5:
            # Quarter
            return "moon2" if phase2 > phase else "moon6"
            
        # Gibbous
        return "moon3" if phase2 > phase else "moon5"
    
    # Taken from JPL's Planetary Positions page: http://ssd.jpl.nasa.gov/?planet_pos
    # This gives us a good approximation for the years 1800 to 2050 AD.
    def get_orbital_elements(self, t_struct):
        # Centuries since J2000
        jc = julian_centuries(t_struct)
        
        if self.id == planet_enum.MERCURY:
            a = 0.38709927 + 0.00000037 * jc
            e = 0.20563593 + 0.00001906 * jc
            i = Geometry.degrees_to_radians(7.00497902 - 0.00594749 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(252.25032350 + 149472.67411175 * jc))
            w = Geometry.degrees_to_radians(77.45779628 + 0.16047689 * jc)
            o = Geometry.degrees_to_radians(48.33076593 - 0.12534081 * jc)
            return OrbitalElements(a, e, i, o, w, l)
        elif self.id == planet_enum.VENUS:
            a = 0.72333566 + 0.00000390 * jc
            e = 0.00677672 - 0.00004107 * jc
            i = Geometry.degrees_to_radians(3.39467605 - 0.00078890 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(181.97909950 + 58517.81538729 * jc))
            w = Geometry.degrees_to_radians(131.60246718 + 0.00268329 * jc)
            o = Geometry.degrees_to_radians(76.67984255 - 0.27769418 * jc)
            return OrbitalElements(a, e, i, o, w, l)
        elif self.id == planet_enum.SUN:
            # Note that this is the orbital data for Earth.
            a = 1.00000261 + 0.00000562 * jc
            e = 0.01671123 - 0.00004392 * jc
            i = Geometry.degrees_to_radians(-0.00001531 - 0.01294668 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(100.46457166 + 35999.37244981 * jc))
            w = Geometry.degrees_to_radians(102.93768193 + 0.32327364 * jc)
            o = 0.0
            return OrbitalElements(a, e, i, o, w, l)
        elif self.id == planet_enum.MARS:
            a = 1.52371034 + 0.00001847 * jc
            e = 0.09339410 + 0.00007882 * jc
            i = Geometry.degrees_to_radians(1.84969142 - 0.00813131 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(-4.55343205 + 19140.30268499 * jc))
            w = Geometry.degrees_to_radians(-23.94362959 + 0.44441088 * jc)
            o = Geometry.degrees_to_radians(49.55953891 - 0.29257343 * jc)
            return OrbitalElements(a, e, i, o, w, l)
        elif self.id == planet_enum.JUPITER:
            a = 5.20288700 - 0.00011607 * jc
            e = 0.04838624 - 0.00013253 * jc
            i = Geometry.degrees_to_radians(1.30439695 - 0.00183714 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(34.39644051 + 3034.74612775 * jc))
            w = Geometry.degrees_to_radians(14.72847983 + 0.21252668 * jc)
            o = Geometry.degrees_to_radians(100.47390909 + 0.20469106 * jc)
            return OrbitalElements(a, e, i, o, w, l)
        elif self.id == planet_enum.SATURN:
            a = 9.53667594 - 0.00125060 * jc
            e = 0.05386179 - 0.00050991 * jc
            i = Geometry.degrees_to_radians(2.48599187 + 0.00193609 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(49.95424423 + 1222.49362201 * jc))
            w = Geometry.degrees_to_radians(92.59887831 - 0.41897216 * jc)
            o = Geometry.degrees_to_radians(113.66242448 - 0.28867794 * jc)
            return OrbitalElements(a, e, i, o, w, l)
        elif self.id == planet_enum.URANUS:
            a = 19.18916464 - 0.00196176 * jc
            e = 0.04725744 - 0.00004397 * jc
            i = Geometry.degrees_to_radians(0.77263783 - 0.00242939 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(313.23810451 + 428.48202785 * jc))
            w = Geometry.degrees_to_radians(170.95427630 + 0.40805281 * jc)
            o = Geometry.degrees_to_radians(74.01692503 + 0.04240589 * jc)
            return OrbitalElements(a, e, i, o, w, l)
        elif self.id == planet_enum.NEPTUNE:
            a = 30.06992276 + 0.00026291 * jc
            e = 0.00859048 + 0.00005105 * jc
            i = Geometry.degrees_to_radians(1.77004347 + 0.00035372 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(-55.12002969 + 218.45945325 * jc))
            w = Geometry.degrees_to_radians(44.96476227 - 0.32241464 * jc)
            o = Geometry.degrees_to_radians(131.78422574 - 0.00508664 * jc)
            return OrbitalElements(a, e, i, o, w, l)
        elif self.id == planet_enum.PLUTO:
            a = 39.48211675 - 0.00031596 * jc
            e = 0.24882730 + 0.00005170 * jc
            i = Geometry.degrees_to_radians(17.14001206 + 0.00004818 * jc)
            l = Geometry.mod_2_pi(Geometry.degrees_to_radians(238.92903833 + 145.20780515 * jc))
            w = Geometry.degrees_to_radians(224.06891629 - 0.04062942 * jc)
            o = Geometry.degrees_to_radians(110.30393684 - 0.01183482 * jc)
            return OrbitalElements(a, e, i, o, w, l)
        else:
            raise RuntimeError("Unknown Planet:" + str(self.id))
        
    def calculate_lunar_geocentric_location(self, t_struct):
        '''
        Calculate the geocentric right ascension and declination of the moon using
        an approximation as described on page D22 of the 2008 Astronomical Almanac
        All of the variables in this method use the same names as those described
        in the text: lambda = Ecliptic longitude (degrees) beta = Ecliptic latitude
        (degrees) pi = horizontal parallax (degrees) r = distance (Earth radii)
        
        NOTE: The text does not give a specific time period where the approximation
        is valid, but it should be valid through at least 2009.
        '''
        # First, calculate the number of Julian centuries from J2000.0.
        t = ((calculate_julian_day(t_struct) - 2451545.0) / 36525.0)
        
        # Second, calculate the approximate geocentric orbital elements.
        lambda_val = 218.32 + 481267.881 * t + 6.29 \
            * math.sin(Geometry.degrees_to_radians(135.0 + 477198.87 * t)) - 1.27 \
            * math.sin(Geometry.degrees_to_radians(259.3 - 413335.36 * t)) + 0.66 \
            * math.sin(Geometry.degrees_to_radians(235.7 + 890534.22 * t)) + 0.21 \
            * math.sin(Geometry.degrees_to_radians(269.9 + 954397.74 * t)) - 0.19 \
            * math.sin(Geometry.degrees_to_radians(357.5 + 35999.05 * t)) - 0.11 \
            * math.sin(Geometry.degrees_to_radians(186.5 + 966404.03 * t))
        beta = 5.13 \
            * math.sin(Geometry.degrees_to_radians(93.3 + 483202.02 * t)) + 0.28 \
            * math.sin(Geometry.degrees_to_radians(228.2 + 960400.89 * t)) - 0.28 \
            * math.sin(Geometry.degrees_to_radians(318.3 + 6003.15 * t)) - 0.17 \
            * math.sin(Geometry.degrees_to_radians(217.6 - 407332.21 * t))
            
        # Third, convert to RA and Dec.
        l = math.cos(Geometry.degrees_to_radians(beta)) \
            * math.cos(Geometry.degrees_to_radians(lambda_val))
        m = 0.9175 * math.cos(Geometry.degrees_to_radians(beta)) \
            * math.sin(Geometry.degrees_to_radians(lambda_val)) - 0.3978 \
            * math.sin(Geometry.degrees_to_radians(beta))
        n = 0.3978 * math.cos(Geometry.degrees_to_radians(beta)) \
            * math.sin(Geometry.degrees_to_radians(lambda_val)) + 0.9175 \
            * math.sin(Geometry.degrees_to_radians(beta))
        ra = Geometry.radians_to_degrees(Geometry.mod_2_pi(math.atan2(m, l)))
        dec = Geometry.radians_to_degrees(math.asin(n))
        
        return RaDec(ra, dec)
    
    def calculate_phase_angle(self, t_struct):
        '''
        Calculates the phase angle of the planet, in degrees.
        '''
        # For the moon, we will approximate phase angle by calculating the
        # elongation of the moon relative to the sun. This is accurate to within
        # about 1%.
        if self.id == planet_enum.MOON:
            moon_ra_dec = self.calculate_lunar_geocentric_location(t_struct)
            moon = gc_get_instance(moon_ra_dec.ra, moon_ra_dec.dec)
            
            sun_coords = hc_get_instance(t_struct=t_struct,
                                         planet=Planet(planet_enum.SUN, 
                                                       res[planet_enum.SUN][0], 
                                                       res[planet_enum.SUN][1], 
                                                       res[planet_enum.SUN][2]))
            sun_ra_dec = calculate_ra_dec_dist(sun_coords)
            sun = gc_get_instance(sun_ra_dec.ra, sun_ra_dec.dec)
            
            return 180.0 - \
                Geometry.radians_to_degrees(math.acos(sun.x * moon.x + sun.y * moon.y + sun.z * moon.z))
                
        # First, determine position in the solar system.
        planet_coords = hc_get_instance(planet=self, t_struct=t_struct)
        
        # Second, determine position relative to Earth
        earth_coords = hc_get_instance(t_struct=t_struct, 
                                       planet=Planet(planet_enum.SUN, 
                                                     res[planet_enum.SUN][0], 
                                                     res[planet_enum.SUN][1], 
                                                     res[planet_enum.SUN][2]))
        earth_distance = planet_coords.distance_from(earth_coords)
        
        # Finally, calculate the phase of the body.
        phase = Geometry.radians_to_degrees(\
                math.acos((earth_distance * earth_distance + \
                           planet_coords.radius * planet_coords.radius - \
                           earth_coords.radius * earth_coords.radius) / \
                           (2.0 * earth_distance * planet_coords.radius)))
                          
        return phase
    
    def calculate_percent_illuminated(self, t_struct):
        '''
        Calculate the percent of the body that is illuminated. The value returned
        is a fraction in the range from 0.0 to 100.0.
        '''
        phase_angle = self.calculate_phase_angle(t_struct)
        return 50.0 * (1.0 + math.cos(Geometry.degrees_to_radians(phase_angle)))
    
    def get_next_full_moon(self, now):
        '''
        Return the date of the next full moon after today.
        '''
        moon = Planet(planet_enum.MOON, res[planet_enum.MOON][0], 
                      res[planet_enum.MOON][1], res[planet_enum.MOON][2])
        # First, get the moon's current phase.
        phase = moon.calculate_phase_angle(now)
        
        # Next, figure out if the moon is waxing or waning.
        later = time.gmtime(time.mktime(now) + 1 * 3600 * 1000)
        phase2 = moon.calculate_phase_angle(later)
        is_waxing = phase2 > phase
        
        # If moon is waxing, next full moon is (180.0 - phase)/360.0 * 29.53.
        # If moon is waning, next full moon is (360.0 - phase)/360.0 * 29.53.
        LUNAR_CYCLE = 29.53  # In days.
        base_angle = 180.0 if is_waxing else 360.0
        num_days = (base_angle - phase) / 360.0 * LUNAR_CYCLE
        
        return time.gmtime(time.mktime(now) + (num_days * 24.0 * 3600.0 * 1000.0))
    
    def get_next_full_moon_slow(self, now):
        '''
        Return the date of the next full moon after today.
        Slow incremental version, only correct to within an hour.
        '''
        moon = Planet(planet_enum.MOON, res[planet_enum.MOON][0], 
                      res[planet_enum.MOON][1], res[planet_enum.MOON][2])
        
        full_moon = time.gmtime(time.mktime(now))
        phase = moon.calculate_phase_angle(now)
        waxing = False
        
        while True:
            full_moon = time.gmtime(time.mktime(full_moon) + MILLISECONDS_PER_HOUR)
            next_phase = moon.calculate_phase_angle(full_moon)
            if waxing and (next_phase < phase):
                full_moon = time.gmtime(time.mktime(full_moon) - MILLISECONDS_PER_HOUR)
                return full_moon
        
            waxing = (next_phase > phase)
            phase = next_phase
            
    def get_magnitude(self, t_struct):
        '''
        Calculates the planet's magnitude for the given date.
        '''
        if self.id == planet_enum.SUN:
            return -27.0
        if self.id == planet_enum.MOON:
            return -10.0
        
        # First, determine position in the solar system.
        planet_coords = hc_get_instance(planet=self, t_struct=t_struct)
        
        # Second, determine position relative to Earth
        earth_coords = hc_get_instance(t_struct=t_struct,
                                       planet=Planet(planet_enum.SUN, 
                                                     res[planet_enum.SUN][0], 
                                                     res[planet_enum.SUN][1], 
                                                     res[planet_enum.SUN][2]))
        earth_distance = planet_coords.distance_from(earth_coords)
        
        # Third, calculate the phase of the body.
        phase = Geometry.radians_to_degrees(\
                    math.acos((earth_distance * earth_distance + \
                    planet_coords.radius * planet_coords.radius - \
                    earth_coords.radius * earth_coords.radius) / \
                    (2.0 * earth_distance * planet_coords.radius)))
        p = phase/100.0     # Normalized phase angle
        
        # Finally, calculate the magnitude of the body.
        mag = -100.0      # Apparent visual magnitude
        
        if self.id == planet_enum.MERCURY:
            mag = -0.42 + (3.80 - (2.73 - 2.00 * p) * p) * p
        elif self.id == planet_enum.VENUS:
            mag = -4.40 + (0.09 + (2.39 - 0.65 * p) * p) * p
        elif self.id == planet_enum.MARS:
            mag = -1.52 + 1.6 * p
        elif self.id == planet_enum.JUPITER:
            mag = -9.40 + 0.5 * p
        elif self.id == planet_enum.SATURN:
            mag = -8.75
        elif self.id == planet_enum.URANUS:
            mag = -7.19
        elif self.id == planet_enum.NEPTUNE:
            mag = -6.87
        elif self.id == planet_enum.PLUTO:
            mag = -1.0
        else:
            mag = 100
        return (mag + 5.0 * math.log10(planet_coords.radius * earth_distance))
    
    def get_planetary_image_size(self):
        if self.id == planet_enum.SUN or self.id == planet_enum.MOON:
            return 0.02
        elif self.id == planet_enum.MERCURY or self.id == planet_enum.VENUS or \
        self.id == planet_enum.MARS or self.id == planet_enum.PLUTO:
            return 0.01
        elif self.id == planet_enum.JUPITER:
            return 0.025
        elif self.id == planet_enum.URANUS or self.id == planet_enum.NEPTUNE:
            return 0.015
        elif self.id == planet_enum.SATURN:
            return 0.035
        else:
            return 0.02
        
    def calc_next_rise_set_time(self, now, loc, indicator):
        '''
        Calculates the next rise or set time of this planet from a given observer.
        Returns null if the planet doesn't rise or set during the next day.
        
        @param now Calendar time from which to calculate next rise / set time.
        @param loc Location of observer.
        @param indicator Indicates whether to look for rise or set time.
        @return New Calendar set to the next rise or set time if within
                the next day, otherwise null.
        '''
        raise NotImplementedError("not done yet")
        # Make a copy of the calendar to return.
#     Calendar riseSetTime = Calendar.getInstance();
#     double riseSetUt = calcRiseSetTime(now.getTime(), loc, indicator);
#     // Early out if no nearby rise set time.
#     if (riseSetUt < 0) {
#       return null;
#     }
#     
#     // Find the start of this day in the local time zone. The (a / b) * b
#     // formulation looks weird, it's using the properties of int arithmetic
#     // so that (a / b) is really floor(a / b).
#     long dayStart = (now.getTimeInMillis() / TimeConstants.MILLISECONDS_PER_DAY)
#                     * TimeConstants.MILLISECONDS_PER_DAY - riseSetTime.get(Calendar.ZONE_OFFSET);
#     long riseSetUtMillis = (long) (calcRiseSetTime(now.getTime(), loc, indicator)
#                                   * TimeConstants.MILLISECONDS_PER_HOUR);
#     long newTime = dayStart + riseSetUtMillis + riseSetTime.get(Calendar.ZONE_OFFSET);
#     // If the newTime is before the current time, go forward 1 day.
#     if (newTime < now.getTimeInMillis()) {
#       Log.d(TAG, "Nearest Rise/Set is in the past. Adding one day.");
#       newTime += TimeConstants.MILLISECONDS_PER_DAY;
#     }
#     riseSetTime.setTimeInMillis(newTime);
#     if (!riseSetTime.after(now)) {
#       Log.e(TAG, "Next rise set time (" + riseSetTime.toString()
#                  + ") should be after current time (" + now.toString() + ")");
#     }
#     return riseSetTime;

    def calc_rise_set_time(self, date, loc, indicator):
        # Internally calculate the rise and set time of an object.
        # Returns a double, the number of hours through the day in UT.
        raise NotImplementedError("not done yet")
#         Calendar cal = Calendar.getInstance(TimeZone.getTimeZone("UT"));
#     cal.setTime(d);
# 
#     float sign = (indicator == RiseSetIndicator.RISE ? 1.0f : -1.0f);
#     float delta = 5.0f;
#     float ut = 12.0f;
# 
#     int counter = 0;
#     while ((Math.abs(delta) > 0.008) && counter < MAX_ITERATIONS) {
#       cal.set(Calendar.HOUR_OF_DAY, (int) MathUtil.floor(ut));
#       float minutes = (ut - MathUtil.floor(ut)) * 60.0f;
#       cal.set(Calendar.MINUTE, (int) minutes);
#       cal.set(Calendar.SECOND, (int) ((minutes - MathUtil.floor(minutes)) * 60.f));
# 
#       // Calculate the hour angle and declination of the planet.
#       // TODO(serafini): Need to fix this for arbitrary RA/Dec locations.
#       Date tmp = cal.getTime();
#       HeliocentricCoordinates sunCoordinates =
#         HeliocentricCoordinates.getInstance(Planet.Sun, tmp);
#       RaDec raDec = RaDec.getInstance(this, tmp, sunCoordinates);
# 
#       // GHA = GST - RA. (In degrees.)
#       float gst = TimeUtil.meanSiderealTime(tmp, 0);
#       float gha = gst - raDec.ra;
# 
#       // The value of -0.83 works for the diameter of the Sun and Moon. We
#       // assume that other objects are simply points.
#       float bodySize = (this == Planet.Sun || this == Planet.Moon) ? -0.83f : 0.0f;
#       float hourAngle = calculateHourAngle(bodySize, loc.latitude, raDec.dec);
# 
#       delta = (gha + loc.longitude + (sign * hourAngle)) / 15.0f;
#       while (delta < -24.0f) {
#         delta = delta + 24.0f;
#       }
#       while (delta > 24.0f) {
#         delta = delta - 24.0f;
#       }
#       ut = ut - delta;
# 
#       // I think we need to normalize UT
#       while (ut < 0.0f) {
#         ut = ut + 24.0f;
#       }
#       while (ut > 24.0f) {
#         ut = ut - 24.0f;
#       }
# 
#       ++counter;
#     }
# 
#     // Return failure if we didn't converge.
#     if (counter == MAX_ITERATIONS) {
#       Log.d(TAG, "Rise/Set calculation didn't converge.");
#       return -1.0f;
#     }
# 
#     // TODO(serafini): Need to handle latitudes above 60
#     // At latitudes above 60, we need to calculate the following:
#     // sin h = sin phi sin delta + cos phi cos delta cos (gha + lambda)
#     return ut;

    def calculate_hour_angle(self, altitude, latitude, declination):
        '''
        Calculates the hour angle of a given declination for the given location.
        This is a helper application for the rise and set calculations. Its
        probably not worth using as a general purpose method.
        All values are in degrees.
        
        This method calculates the hour angle from the meridian using the
        following equation from the Astronomical Almanac (p487):
        cos ha = (sin alt - sin lat * sin dec) / (cos lat * cos dec)
        '''
        alt_rads = Geometry.degrees_to_radians(altitude)
        lat_rads = Geometry.degrees_to_radians(latitude)
        dec_rads = Geometry.degrees_to_radians(declination)
        cos_ha = (math.sin(alt_rads) - math.sin(lat_rads) * math.sin(dec_rads)) / \
            (math.cos(lat_rads) * math.cos(dec_rads))
    
        return Geometry.radians_to_degrees(math.acos(cos_ha))
        
    def __init__(self, new_id, image_resource_id, name_resource_id, update_freq_Ms):
        '''
        constructor
        '''
        self.id = new_id
        self.image_resource_id = image_resource_id
        self.name_resource_id = name_resource_id
        self.update_freq_Ms = update_freq_Ms
        
if __name__ == "__main__":
    pass