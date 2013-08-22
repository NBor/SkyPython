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
// Original Author: Brent Bryan
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-07-24

@author: Alyson Wu and Morgan Redshaw
'''

#VectorUtilTest

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
    pass
    
def assertVectorsEqual(v1,v2):
    DELTA = 0.00001 
    same = True
    same = abs(v1.x - v2.x) < DELTA & same
    same = abs(v1.y - v2.y) < DELTA & same
    same = abs(v1.z - v2.z) < DELTA &same
    return same
 
def testDotProduct():
    '''
    >>> from src.units.Vector3 import Vector3
    >>> from src.utils.VectorUtil import dot_product
    >>> DELTA = 0.00005
    >>> v1 = Vector3(1, 2, 3)    
    >>> v2 = Vector3(0.3, 0.4, 0.5)
    >>> dp = float(dot_product(v1,v2))
    >>> abs(2.6 - dp) < DELTA
    True
    '''
    pass

# Matrix 4x4 Test

def assert_vectors_equal(v1, v2, delta):
    '''
    Is a needed function for testing Matrix4x4. This is the only place in the code base that this function occurs.
    '''
    equal = True
    equal = (abs(v1.x - v2.x) < delta) & equal
    equal = (abs(v1.y - v2.y) < delta) & equal
    equal = (abs(v1.z - v2.z) < delta) & equal
    return equal

def assert_mat_equal(mat1, mat2, delta):
    '''
    Is a needed function for testing Matrix4x4. This is the only place in the code base that this function occurs.
    '''
    m1 = mat1.values;
    m2 = mat2.values;
    equal = True
    equal = (abs(m1[0] - m2[0]) < delta) & equal
    equal = (abs(m1[1] - m2[1]) < delta) & equal
    equal = (abs(m1[2] - m2[2]) < delta) & equal
    equal = (abs(m1[3] - m2[3]) < delta) & equal
    equal = (abs(m1[4] - m2[4]) < delta) & equal
    equal = (abs(m1[5] - m2[5]) < delta) & equal
    equal = (abs(m1[6] - m2[6]) < delta) & equal
    equal = (abs(m1[7] - m2[7]) < delta) & equal
    equal = (abs(m1[8] - m2[8]) < delta) & equal
    equal = (abs(m1[9] - m2[9]) < delta) & equal
    equal = (abs(m1[10] - m2[10]) < delta) & equal
    equal = (abs(m1[11] - m2[11]) < delta) & equal
    equal = (abs(m1[12] - m2[12]) < delta) & equal
    equal = (abs(m1[13] - m2[13]) < delta) & equal
    equal = (abs(m1[14] - m2[14]) < delta) & equal
    equal = (abs(m1[15] - m2[15]) < delta) & equal
    return equal

def Matrix4x4Testing():
    '''
    # Needed imports
    >>> import src.utils.VectorUtil as VectorUtil
    >>> from src.utils.Matrix4x4 import Matrix4x4, create_rotation, create_identity, create_scaling, create_translation,\
                 multiply_MM, multiply_MV
    >>> from src.units.Vector3 import Vector3
    
    
    # Test multiply by identity
    >>> identity = create_identity()
    >>> m = Matrix4x4([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 ] )
    >>> assert_mat_equal(m, multiply_MM(identity, m), 0.00001)
    True
    >>> assert_mat_equal(m, multiply_MM(m, identity), 0.00001)
    True
    
    #Test multiply by scaling
    >>> m = Matrix4x4([1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 0, 0, 0, 0])
    >>> scaling = create_scaling(2, 2, 2)
    >>> expected = Matrix4x4([ 2, 4, 6, 0, 10, 12, 14, 0, 18, 20, 22, 0, 0, 0, 0, 0 ] )
    >>> assert_mat_equal(expected, multiply_MM(scaling, m), 0.00001)
    True
    >>> assert_mat_equal(expected, multiply_MM(m, scaling), 0.00001)
    True
    
    # Test multiply by translation
    >>> v = Vector3(1, 1, 1);
    >>> trans = create_translation(1, 2, 3);
    >>> expected = Vector3(2, 3, 4);
    >>> assert_vectors_equal(expected, multiply_MV(trans, v), 0.00001);
    True
    
    # Test rotation 3x3 parallel rotation has no effect
    >>> import math
    >>> m = create_rotation(math.pi, Vector3(0, 1, 0))
    >>> v = Vector3(0, 2, 0)
    >>> assert_vectors_equal(v, multiply_MV(m, v), 0.00001)
    True
    
    # Test rotation 3x3 perpendicular rotation
    >>> m = create_rotation(math.pi * 0.25, Vector3(0, -1, 0))
    >>> v = Vector3(1, 0, 0)
    >>> oneOverSqrt2 = 1.0 / math.sqrt(2.0)
    >>> assert_vectors_equal(Vector3(oneOverSqrt2, 0, oneOverSqrt2), multiply_MV(m, v), 0.00001)
    True
    
    # Test rotation 3x3 Unaligned axis
    >>> axis = Vector3(1, 1, 1)
    >>> axis = VectorUtil.normalized(axis)
    >>> numRotations = 5
    >>> m = create_rotation(math.pi * 2 / numRotations, axis)
    >>> start = Vector3(2.34, 3, -17.6)
    >>> v = start
    >>> for i in range(5):
    ...    v = multiply_MV(m, v)
    >>> assert_vectors_equal(start, v, 0.00001)
    True
    
    '''
    pass

#Matrix 33 Test

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

# GeometryTest

def GeometryTests():
    '''
    # All imports needed
    >>> import math
    >>> from src.units.Matrix33 import Matrix33
    >>> from src.utils.Geometry import calculate_rotation_matrix, matrix_multiply, matrix_vector_multiply,\
                vector_product, scalar_product, getXYZ, degrees_to_radians
    >>> from src.units.RaDec import RaDec
    >>> from src.units.Vector3 import Vector3
    
    >>> allTestValues = [[0, 0, 1, 0, 0],\
                        [90, 0, 0, 1, 0],\
                        [0, 90, 0, 0, 1],\
                        [180, 0, -1, 0, 0],\
                        [0, -90, 0, 0, -1],\
                        [270, 0, 0, -1, 0] ]
    
    # Test speherical to cartesians. This will run through 6 times
    >>> for testValues in allTestValues:
    ...    ra = testValues[0];
    ...    dec = testValues[1];
    ...    x = testValues[2];
    ...    y = testValues[3];
    ...    z = testValues[4];
    ...    result = getXYZ(RaDec(ra, dec));
    ...    correct = True
    ...    correct = (abs(x - result.x) < 0.00001) & correct
    ...    correct = (abs(y - result.y) < 0.00001) & correct
    ...    correct = (abs(z - result.z) < 0.00001) & correct
    ...    correct
    True
    True
    True
    True
    True
    True
    
    # Test vector product
    
    >>> x = Vector3(1, 0, 0)
    >>> y = Vector3(0, 1, 0)
    >>> z = vector_product(x, y)
    >>> assert_vectors_equal(z, Vector3(0, 0, 1), 0.00001)
    True
    
    # Check that a X b is perpendicular to a and b
    >>> a = Vector3(1, -2, 3)
    >>> b = Vector3(2, 0, -4)
    >>> c = vector_product(a, b)
    >>> aDotc = scalar_product(a, c)
    >>> bDotc = scalar_product(b, c)
    >>> abs(0 - aDotc) < 0.00001
    True
    
    >>> abs(0 - aDotc) < 0.00001
    True

    # Check that |a X b| is correct
    >>> v = Vector3(1, 2, 0)
    >>> ww = vector_product(x, v)
    >>> wwDotww = scalar_product(ww, ww)
    >>> abs( ( math.pow(1 * math.sqrt(5) * math.sin(math.atan(2)), 2) ) - wwDotww) < 0.00001
    True
    
    # Test matrix inversion.... This would just prints out information (which isnt very helpful for me)
    >>> m = Matrix33 (1, 2, 0, 0, 1, 5, 0, 0, 1)
    >>> inv = m.get_inverse();
    >>> product = matrix_multiply(m, inv)
    
    # Test Calculate Rotation Matrix
    >>> noRotation = calculate_rotation_matrix(0, Vector3(1, 2, 3));
    >>> identity = Matrix33(1, 0, 0, 0, 1, 0, 0, 0, 1);
    >>> assert_matrices_equal(identity, noRotation, 0.00001);
    True
    >>> rotAboutZ = calculate_rotation_matrix(90, Vector3(0, 0, 1));
    >>> assert_matrices_equal(Matrix33(0, 1, 0, -1, 0, 0, 0, 0, 1), rotAboutZ, 0.00001);
    True
    >>> axis = Vector3(2, -4, 1)
    >>> axis.normalize()
    >>> rotA = calculate_rotation_matrix(30, axis)
    >>> rotB = calculate_rotation_matrix(-30, axis)
    >>> shouldBeIdentity = matrix_multiply(rotA, rotB)
    >>> assert_matrices_equal(identity, shouldBeIdentity, 0.00001);
    True
    >>> axisPerpendicular = Vector3(4, 2, 0);
    >>> rotatedAxisPerpendicular = matrix_vector_multiply(rotA, axisPerpendicular);

    # Should still be perpendicular
    >>> abs(0 - scalar_product(axis, rotatedAxisPerpendicular)) < 0.00001
    True
    
    # And the angle between them should be 30 degrees
    >>> axisPerpendicular.normalize();
    >>> rotatedAxisPerpendicular.normalize();
    >>> expectedValue = math.cos(degrees_to_radians(30.0))
    >>> actualValue = scalar_product(axisPerpendicular, rotatedAxisPerpendicular)
    >>> abs( expectedValue - actualValue) < 0.00001
    True
    
    # Test martix multiply
    >>> m1 = Matrix33(1, 2, 4, -1, -3, 5, 3, 2, 6)
    >>> m2 = Matrix33(3, -1, 4, 0, 2, 1, 2, -1, 2)
    >>> v1 = Vector3(0, -1, 2)
    >>> v2 = Vector3(2, -2, 3)

    >>> assert_matrices_equal(Matrix33(11, -1, 14, 7, -10, 3, 21, -5, 26), matrix_multiply(m1, m2), 0.00001)
    True
    >>> assert_vectors_equal(Vector3(6, 13, 10), matrix_vector_multiply(m1, v1), 0.00001)
    True
    >>> assert_vectors_equal(Vector3(10, 19, 20), matrix_vector_multiply(m1, v2), 0.00001)
    True
    '''
    pass

#TimeUtilTest

TOL = 0.0001      # Tolerance for Julian Date calculations
LMST_TOL = 0.15   # Tolerance for LMST calculation
HOURS_TO_DEGREES = 360.0/24.0  # Convert from hours to degrees

def testJulianDate2000AD():
    '''
    >>> import time
    >>> import datetime as dt   
    >>> import calendar
    >>> from src.utils.TimeUtil import calculate_julian_day
    >>> unix2000 = 946684800
    >>> setTime = dt.datetime(2000, 1, 1, 0, 0, 0).timetuple()
    >>> GMT = calendar.timegm(setTime)
    >>> print abs(unix2000 - GMT) < TOL
    True
    >>> abs(2451544.5 - calculate_julian_day(setTime)) < TOL
    True
    '''
    #  January 1, 2000 at midday corresponds to JD = 2451545.0, according to http://en.wikipedia.org/wiki/Julian_day#Gregorian_calendar_from_Julian_day_number.
    # So midnight before is half a day earlier.
    pass

def testJulianDate():

    # Make sure that we correctly generate Julian dates. Standard values were obtained from the USNO web site: http://www.usno.navy.mil/USNO/astronomical-applications/data-services/jul-date
    '''
    >>> import time
    >>> import datetime as dt
    >>> import calendar
    >>> from src.utils.TimeUtil import calculate_julian_day

    #  Jan 1, 2009, 12:00 UT1 
    >>> Time1 = dt.datetime(2009, 1, 1, 12, 0, 0).timetuple()
    >>> abs(2454833.0 - calculate_julian_day(Time1)) < TOL
    True

    # Jul 4, 2009, 12:00 UT1
    >>> Time2 = dt.datetime(2009, 7, 4, 12, 0, 0).timetuple()
    >>> abs(2455017.0 - calculate_julian_day(Time2)) < TOL
    True

    # Sep 20, 2009, 12:00 UT1
    >>> Time3 = dt.datetime(2009, 9, 20, 12, 0, 0).timetuple()
    >>> abs(2455095.0 - calculate_julian_day(Time3)) < TOL
    True

    # Dec 25, 2010, 12:00 UT1
    >>> Time4 = dt.datetime(2010, 12, 25, 12, 0, 0).timetuple()
    >>> abs(2455556.0 - calculate_julian_day(Time4)) < TOL
    True
    '''
    pass

def testJulianCenturies():
    # Make sure that we correctly generate Julian dates. Standard values were obtained from the USNO web site. http://www.usno.navy.mil/USNO/astronomical-applications/data-services/jul-date
    '''
    >>> import time
    >>> import datetime as dt
    >>> import calendar
    >>> from src.utils.TimeUtil import julian_centuries

    # Jan 1, 2009, 12:00 UT1
    >>> Time1 = dt.datetime(2009, 1, 1, 12, 0, 0).timetuple()       
    >>> abs(0.09002 - julian_centuries(Time1)) < TOL
    True

    # Jul 4, 2009, 12:00 UT1
    >>> Time2 = dt.datetime(2009, 7, 4, 12, 0, 0).timetuple()      
    >>> abs(0.09506 - julian_centuries(Time2)) < TOL
    True

    # Sep 20, 2009, 12:00 UT1
    >>> Time3 = dt.datetime(2009, 9, 20, 12, 0, 0).timetuple()    
    >>> abs(0.09719 - julian_centuries(Time3)) < TOL
    True

    # Dec 25, 2010, 12:00 UT1
    >>> Time4 = dt.datetime(2010, 12, 25, 12, 0, 0).timetuple()    
    >>> abs(0.10982 - julian_centuries(Time4)) < TOL
    True
    '''
    pass

def testMeanSiderealTime():
    # Verify that we are calculating the correct local mean sidereal time.
    '''
    >>> import time
    >>> import datetime as dt
    >>> import calendar
    >>> from src.utils.TimeUtil import mean_sidereal_time

    # Longitude of selected cities
    >>> pit = -79.97    # W 79 58'12.0"
    >>> lon = -0.13     # W 00 07'41.0"
    >>> tok = 139.77    # E139 46'00.0"

    # A couple of select dates:
    # Jan  1, 2009, 12:00 UT1
    >>> Time1 = dt.datetime(2009, 1, 1, 12, 0, 0).timetuple()  
    >>> abs((13.42 * HOURS_TO_DEGREES) - mean_sidereal_time(Time1, pit)) < LMST_TOL
    True
    >>> abs((18.74 * HOURS_TO_DEGREES) - mean_sidereal_time(Time1, lon)) < LMST_TOL
    True
    >>> abs((4.07 * HOURS_TO_DEGREES) - mean_sidereal_time(Time1, tok)) < LMST_TOL
    True

    # Sep 20, 2009, 12:00 UT1
    >>> Time2 = dt.datetime(2009, 9, 20, 12, 0, 0).timetuple()
    >>> abs((6.64 * HOURS_TO_DEGREES) - mean_sidereal_time(Time2, pit)) < LMST_TOL
    True
    >>> abs((11.96 * HOURS_TO_DEGREES) - mean_sidereal_time(Time2, lon)) < LMST_TOL
    True
    >>> abs((21.29 * HOURS_TO_DEGREES) - mean_sidereal_time(Time2, tok)) < LMST_TOL
    True

    # Dec 25, 2010, 12:00 UT1
    >>> Time3 = dt.datetime(2010, 12, 25, 12, 0, 0).timetuple()
    >>> abs((12.92815 * HOURS_TO_DEGREES) - mean_sidereal_time(Time3, pit)) < LMST_TOL
    True
    >>> abs((18.25 * HOURS_TO_DEGREES) - mean_sidereal_time(Time3, lon)) < LMST_TOL
    True
    >>> abs((3.58 * HOURS_TO_DEGREES) - mean_sidereal_time(Time3, tok)) < LMST_TOL
    True
    '''
    pass

