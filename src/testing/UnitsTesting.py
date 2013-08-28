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
// Original Author: Not stated
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


Created on 2013-07-24

@author: Morgan Redshaw
'''

def GeocentricCoordinatesTests():
    '''
    >>> from src.units.GeocentricCoordinates import GeocentricCoordinates
    >>> one = GeocentricCoordinates(1, 2, 3)
    >>> two = GeocentricCoordinates(2, 4, 6)
    >>> one.scale(2)
    >>> one == two
    False
    >>> one.equals(two)
    True
    '''
    
    pass

def RaDecTests():
    '''
    
    >>> import datetime as dt
    >>> import src.units.RaDec as RaDec
    >>> import src.units.HeliocentricCoordinates as HeliocentricCoordinates
    >>> import src.provider.Planet as Planet
    >>> import src.utils.Geometry as Geometry
    
    # Runs through multiple tests for if the planets are at the correct position
    
    >>> EPSILON = 0.25;

    // Convert from hours to degrees
    >>> HOURS_TO_DEGREES = 360.0/24.0

    // 2009 Jan  1, 12:00 UT1
    // Sun       18h 48.8m  -22d 58m
    // Mercury   20h 10.6m  -21d 36m
    // Venus     22h 02.0m  -13d 36m
    // Mars      18h 17.1m  -24d 05m
    // Jupiter   20h 05.1m  -20d 45m
    // Saturn    11h 33.0m  + 5d 09m
    // Uranus    23h 21.7m  - 4d 57m
    // Neptune   21h 39.7m  -14d 22m
    // Pluto     18h 05.3m  -17d 45m
    
    >>> res = Planet.res
    >>> Mercury = Planet.Planet(Planet.planet_enum.MERCURY, res[0][0], res[0][1], res[0][2])
    >>> Venus = Planet.Planet(Planet.planet_enum.VENUS, res[1][0], res[1][1], res[1][2])
    >>> Sun = Planet.Planet(Planet.planet_enum.SUN, res[2][0], res[2][1], res[2][2])
    >>> Mars = Planet.Planet(Planet.planet_enum.MARS, res[3][0], res[3][1], res[3][2])
    >>> Jupiter = Planet.Planet(Planet.planet_enum.JUPITER, res[4][0], res[4][1], res[4][2])
    >>> Saturn = Planet.Planet(Planet.planet_enum.SATURN, res[5][0], res[5][1], res[5][2])
    >>> Uranus = Planet.Planet(Planet.planet_enum.URANUS, res[6][0], res[6][1], res[6][2])
    >>> Neptune = Planet.Planet(Planet.planet_enum.NEPTUNE, res[7][0], res[7][1], res[7][2])
    >>> Pluto = Planet.Planet(Planet.planet_enum.PLUTO, res[8][0], res[8][1], res[8][2])
    
    >>> now = dt.datetime(2009, 1, 1, 12, 0, 0).timetuple()
    >>> earthCoords = HeliocentricCoordinates.get_instance(planet=Sun, t_struct=now)
    
                 
    >>> pos = RaDec.get_instance(planet=Sun, time=now, earth_coord=earthCoords)
    
    >>> abs(18.813 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-22.97 - pos.dec) < EPSILON
    True
    
    >>> pos = RaDec.get_instance(planet=Mercury, time=now, earth_coord=earthCoords)
    >>> abs(20.177 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-21.60 - pos.dec) < EPSILON
    True
    
    >>> pos = RaDec.get_instance(planet=Venus, time=now, earth_coord=earthCoords)
    >>> abs(22.033 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-13.60  - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Mars, time=now, earth_coord=earthCoords)
    >>> abs(18.285 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-24.08  - pos.dec) < EPSILON
    True
    
    >>> pos = RaDec.get_instance(planet=Jupiter, time=now, earth_coord=earthCoords)
    >>> abs(20.085 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-20.75  - pos.dec) < EPSILON
    True
    
    #----------------------------------------------------------------------------#
    #NOTE: The following test fails in the original Stardroid junit tests as well.
    #----------------------------------------------------------------------------#
    
    >>> pos = RaDec.get_instance(planet=Saturn, time=now, earth_coord=earthCoords)
    >>> abs(11.550 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(5.15  - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Uranus, time=now, earth_coord=earthCoords)
    >>> abs(23.362 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-4.95  - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Neptune, time=now, earth_coord=earthCoords)
    >>> abs(21.662 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-14.37  - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Pluto, time=now, earth_coord=earthCoords)
    >>> abs(18.088 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-17.75  - pos.dec) < EPSILON
    True

    // 2009 Sep 20, 12:00 UT1
    // Sun       11h 51.4m  + 0d 56m
    // Mercury   11h 46.1m  - 1d 45m
    // Venus     10h 09.4m  +12d 21m
    // Mars       7h 08.6m  +23d 03m
    // Jupiter   21h 23.2m  -16d 29m
    // Saturn    11h 46.0m  + 3d 40m
    // Uranus    23h 41.1m  - 2d 55m
    // Neptune   21h 46.7m  -13d 51m
    // Pluto     18h 02.8m  -18d 00m
    
    >>> now = dt.datetime(2009, 9, 20, 12, 0, 0).timetuple() 
    >>> earthCoords = HeliocentricCoordinates.get_instance(planet=Sun, t_struct=now)

    >>> pos = RaDec.get_instance(planet=Sun, time=now, earth_coord=earthCoords)
    >>> abs(11.857 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(0.933  - pos.dec) < EPSILON
    True
    
    >>> pos = RaDec.get_instance(planet=Mercury, time=now, earth_coord=earthCoords)
    >>> abs(11.768 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-1.75 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Venus, time=now, earth_coord=earthCoords)
    >>> abs(10.157 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(12.35 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Mars, time=now, earth_coord=earthCoords)
    >>> abs(7.143 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(23.05 - pos.dec) < EPSILON
    True
    
    >>> pos = RaDec.get_instance(planet=Jupiter, time=now, earth_coord=earthCoords)
    >>> abs(21.387 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-16.48 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Saturn, time=now, earth_coord=earthCoords)
    >>> abs(11.767 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(3.67 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Uranus, time=now, earth_coord=earthCoords)
    >>> abs(23.685 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-2.92 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Neptune, time=now, earth_coord=earthCoords)
    >>> abs(21.778 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-13.85 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Pluto, time=now, earth_coord=earthCoords)
    >>> abs(18.047 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-18.00 - pos.dec) < EPSILON
    True


    // 2010 Dec 25, 12:00 UT1
    // Sun       18 15.6  -23 23
    // Mercury   17 24.2  -20 10
    // Venus     15 04.1  -13 50
    // Mars      18 58.5  -23 43
    // Jupiter   23 46.4  - 2 53
    // Saturn    13 03.9  - 4 14
    // Uranus    23 49.6  - 1 56
    // Neptune   21 55.8  -13 07
    // Pluto     18 21.5  -18 50
    
    >>> now = dt.datetime(2010, 12, 25, 12, 0, 0).timetuple()
    >>> earthCoords = HeliocentricCoordinates.get_instance(planet=Sun, t_struct=now)

    >>> pos = RaDec.get_instance(planet=Sun, time=now, earth_coord=earthCoords)
    >>> abs(18.260 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-23.38 - pos.dec) < EPSILON
    True
    
    >>> pos = RaDec.get_instance(planet=Mercury, time=now, earth_coord=earthCoords)
    >>> abs(17.403 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-20.17 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Venus, time=now, earth_coord=earthCoords)
    >>> abs(15.068 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-13.83 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Mars, time=now, earth_coord=earthCoords)
    >>> abs(18.975 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-23.72 - pos.dec) < EPSILON
    True
    
    >>> pos = RaDec.get_instance(planet=Jupiter, time=now, earth_coord=earthCoords)
    >>> abs(23.773 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-2.88 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Saturn, time=now, earth_coord=earthCoords)
    >>> abs(13.065 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-4.23 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Uranus, time=now, earth_coord=earthCoords)
    >>> abs(23.827 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-1.93 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Neptune, time=now, earth_coord=earthCoords)
    >>> abs(21.930 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True
    >>> abs(-13.12 - pos.dec) < EPSILON
    True

    >>> pos = RaDec.get_instance(planet=Pluto, time=now, earth_coord=earthCoords)
    >>> abs(18.358 * HOURS_TO_DEGREES - pos.ra) < EPSILON
    True

    
    '''
    pass
def latLongTests():
    '''
    >>> from src.units.LatLong import LatLong
    
    
    # Test distance from 90 degrees
    >>> l1 = LatLong(0, 0)
        
    >>> l2 = LatLong(0, 90)
    
    >>> abs(90.0 - l1.distance_from(l2)) < 0.0001
    True
        
        
    # Test distance from same pos
    >>> l1 = LatLong(30, 9)
    >>> l2 = LatLong(30, 9)
        
    >>> l1.distance_from(l2) < 0.0001
    True
        
        
    # Test distance from opposite poles
    >>> l1 = LatLong(-90, 45)
    >>> l2 = LatLong(90, 45)
        
    >>> abs(180 - l1.distance_from(l2)) < 0.0001
    True
        
        
    # Test distance from on Equator
    >>> l1 = LatLong(0, -20)
    >>> l2 = LatLong(0, 30)
        
    >>> abs(50 - l1.distance_from(l2)) < 0.0001
    True
        
    # Test distance from on merridian
    >>> l1 = LatLong(-10, 0)
    >>> l2 = LatLong(40, 0)
        
    >>> abs(50 - l1.distance_from(l2)) < 0.0001
    True
        
    '''
    pass


def assert_matrices_equal(m1, m2, delta):
    '''
    This is a specialized test for Matrix33Tests
    '''
    correct = True
    correct = (abs(m1.xx - m2.xx) < delta) & correct
    correct = (abs(m1.xy - m2.xy) < delta) & correct
    correct = (abs(m1.xz - m2.xz) < delta) & correct
    correct = (abs(m1.yx - m2.yx) < delta) & correct
    correct = (abs(m1.yy - m2.yy) < delta) & correct
    correct = (abs(m1.yz - m2.yz) < delta) & correct
    correct = (abs(m1.zx - m2.zx) < delta) & correct
    correct = (abs(m1.zy - m2.zy) < delta) & correct
    correct = (abs(m1.zz - m2.zz) < delta) & correct
    return correct

def Matrix33Tests():
    '''
    # All needed imports
    >>> from src.units.Matrix33 import Matrix33, get_identity_matrix, get_rowmatrix_from_vectors, get_colmatrix_from_vectors
    >>> from src.units.Vector3 import Vector3
    >>> from src.utils.Geometry import matrix_multiply
    
    # Test construct from row vectors
    
    >>> v1 = Vector3(1, 2, 3);
    >>> v2 = Vector3(4, 5, 6);
    >>> v3 = Vector3(7, 8, 9);
    >>> m = Matrix33(1, 4, 7,\
                     2, 5, 8,\
                     3, 6, 9);       
    >>> m.transpose();    
    >>> mt = get_rowmatrix_from_vectors(v1, v2, v3);
    >>> assert_matrices_equal(m, mt, 0.00001);
    True
    
    
    # Test construct from col vectors
    >>> v1 = Vector3(1, 2, 3)
    >>> v2 = Vector3(4, 5, 6)
    >>> v3 = Vector3(7, 8, 9)
    >>> m = Matrix33(1, 4, 7, \
                     2, 5, 8, \
                     3, 6, 9)
    >>> mt = get_colmatrix_from_vectors(v1, v2, v3)
    >>> assert_matrices_equal(m, mt, 0.00001)
    True
    
    
    # Test transpose
    >>> m = Matrix33(1, 2, 3, 4, 5, 6, 7, 8, 9)
    >>> m.transpose()
    >>> mt = Matrix33(1, 4, 7, 2, 5, 8, 3, 6, 9)
    >>> assert_matrices_equal(m, mt, 0.00001)
    True
    
    
    # Test get_determinant
    >>> abs(1 - get_identity_matrix().get_determinant()) < 0.00001
    True
    
    
    # Test id inverse
    >>> matrix1 = get_identity_matrix().get_inverse()
    >>> assert_matrices_equal(matrix1, get_identity_matrix(), 0.00001)
    True
        
    # Test inversion 1
    >>> m = Matrix33(1, 2, 0, 0, 1, 5, 0, 0, 1)
    >>> inv = m.get_inverse()
    >>> product = matrix_multiply(m, inv)
    >>> assert_matrices_equal(get_identity_matrix(), product, 0.00001)
    True
        
    # Test inversion 2
    >>> m = Matrix33(1, 2, 3, 6, 5, 4, 0, 0, 1)
    >>> inv = m.get_inverse()
    >>> product = matrix_multiply(m, inv)
    >>> assert_matrices_equal(get_identity_matrix(), product, 0.00001)
    True
    
    '''
    pass

def Vector3Test():
    '''
    >>> from src.units.Vector3 import Vector3 
    >>> one = Vector3(1,2,3)
    >>> two = Vector3(2,4,6)
    >>> one.scale(2)
    >>> one.equals(two)
    True
    >>> one == two
    False
    '''

def assertVectorsEqual(v1,v2):
    DELTA = 0.00005 
    same = True
    same = (abs(v1.x - v2.x) < DELTA) & same
    same = (abs(v1.y - v2.y) < DELTA) & same
    same = (abs(v1.z - v2.z) < DELTA) & same
    return same

def assertVectorEquals(v1, v2, tol_angle, tol_length):
    import utils.Geometry as Geometry
    import math
    cosineSim = Geometry.cosine_similarity(v1, v2);
    cosTol = math.cos(tol_angle);
    return cosineSim >= cosTol 

def testAssertVectorEquals_sameVector():
    '''
    >>> from src.units.Vector3 import Vector3
    
    >>> v1 = Vector3(0, 0, 1)
    >>> v2 = Vector3(0, 0, 1)
    >>> assertVectorsEqual(v1,v2)
    True
    
    '''
    pass

def testAssertVectorEquals_differentLengths():
    ''''
    from src.units.Vector3 import Vector3  
    from src.utils.VectorUtil import difference
    v1 = Vector3(0,0,1.0)
    v2 = Vector3(0,0,1.1)
    
    if not abs(difference(v1,v2)) > float(0.0001):
    
    '''
    pass

