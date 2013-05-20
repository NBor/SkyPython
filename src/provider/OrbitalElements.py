'''
Created on 2013-05-20

@author: Neil
'''
import math

class OrbitalElements(object):
    '''
    This class wraps the six parameters which define the path an object takes as
    it orbits the sun.
    
    The equations come from JPL's Solar System Dynamics site:
    http://ssd.jpl.nasa.gov/?planet_pos
    
    The original source for the calculations is based on the approximations described in:
    Van Flandern T. C., Pulkkinen, K. F. (1979): "Low-Precision Formulae for
    Planetary Positions", 1979, Astrophysical Journal Supplement Series, Vol. 41,
    pp. 391-411.
    
    Originally java by Kevin Serafini and Brent Bryan
    '''
    EPSILON = 1.0e-6
    
    distance = None      #Mean distance (AU)
    eccentricity = None  #Eccentricity of orbit
    inclination = None   #Inclination of orbit (AngleUtils.RADIANS)
    ascendingNode = None #Longitude of ascending node (AngleUtils.RADIANS)
    perihelion = None    #Longitude of perihelion (AngleUtils.RADIANS)
    meanLongitude= None  #Mean longitude (AngleUtils.RADIANS)

    def get_anomaly(self):
        '''
        compute anomaly using mean anomaly and eccentricity
        returns value in radians
        '''
        m = self.meanLongitude - self.perihelion 
        e = self.eccentricity

        e0 = m + e * math.sin(m) * (1.0 + e * math.cos(m))
        
        counter = 0
        while(1):
            e1 = e0
            e0 = e1 - (e1 - e * math.sin(e1) - m) / (1.0 - e * math.cos(e1));
            if counter+1 > 100:
                break
            if math.fabs(e0 - e1) > self.EPSILON:
                break
            
    def to_string(self):
        l = []
        l.append("Mean Distance: " + str(self.distance) + " (AU)\n");
        l.append("Eccentricity: " + str(self.eccentricity) + "\n");
        l.append("Inclination: " + str(self.inclination) + " (AngleUtils.RADIANS)\n");
        l.append("Ascending Node: " + str(self.ascendingNode) + " (AngleUtils.RADIANS)\n");
        l.append("Perihelion: " + str(self.perihelion) + " (AngleUtils.RADIANS)\n");
        l.append("Mean Longitude: " + str(self.meanLongitude) + " (AngleUtils.RADIANS)\n");

        return ''.join(l)

    def __init__(self, d, e, i, a, p, l):
        '''
        Constructor
        '''
        self.distance = d
        self.eccentricity = e
        self.inclination = i
        self.ascendingNode = a
        self.perihelion = p
        self.meanLongitude = l
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''