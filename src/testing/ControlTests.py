'''
// Copyright 2010 Google Inc.
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
// Original Author: John Taylor
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


Created on 2013-07-26

@author: Alyson Wu and Morgan Redshaw
'''

#AstronomerModelTest

import math
tol_angle = float(0.001)
tol_length = float(0.001)
SQRT2 = math.sqrt(2)

def assertVectorEquals(v1, v2, tol_angle, tol_length):
    import src.utils.Geometry as Geometry
    import math
    normv1 = v1.length()
    normv2 = v2.length()
    if abs(normv1 - normv2) > tol_length:
        return False 
    cosineSim = Geometry.cosine_similarity(v1, v2)
    cosTol = math.cos(tol_angle)
    return cosineSim >= cosTol 

def testAssertVectorEquals_sameVector():
    # Checks that our assertion method works as intended.
    '''
    >>> from src.units.Vector3 import Vector3
    >>> v1 = Vector3(0, 0, 1)
    >>> v2 = Vector3(0, 0, 1)
    >>> assertVectorEquals(v1,v2, 0.0001, 0.0001)
    True
    ''' 
    pass
    
def testAssertVectorEquals_differentLengths():
    # Checks that our assertion method works as intended.
    '''
    >>> from src.units.Vector3 import Vector3  
    >>> v1 = Vector3(0,0,1.0)
    >>> v2 = Vector3(0,0,1.1)
    >>> assertVectorEquals(v1,v2, 0.0001, 0.0001)
    False
    '''
    pass

def testAssertVectorEquals_differentDirections():
    # Checks that our assertion method works as intended.
    '''
    >>> from src.units.Vector3 import Vector3  
    >>> v1 = Vector3(0,0,1)
    >>> v2 = Vector3(0,1,0)
    >>> assertVectorEquals(v1,v2, 0.0001, 0.0001) 
    False
    '''
    pass

def testSetPhoneSensorValues_phoneFlatAtLat0Long90():
    # The phone is flat, long side pointing North at lat,long = 0, 90.
    '''
    >>> from src.units.LatLong import LatLong
    >>> from src.units.Vector3 import Vector3
    >>> location = LatLong(0, 90) 
    >>> acceleration = Vector3(0, 0, -10)
    >>> magneticField = Vector3(0, -1, 10)
    >>> expectedZenith = Vector3(0, 1, 0)
    >>> expectedNadir = Vector3(0, -1, 0)
    >>> expectedNorth = Vector3(0, 0, 1)
    >>> expectedEast = Vector3(-1, 0, 0)
    >>> expectedSouth = Vector3(0, 0, -1)
    >>> expectedWest = Vector3(1, 0, 0)
    >>> expectedPointing = expectedNadir
    >>> expectedUpAlongPhone = expectedNorth
    >>> checkModelOrientation(location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
    '''
    pass

def testSetPhoneSensorValues_phoneFlatAtLat45Long0():
    # As previous test, but at lat, long = (45, 0)
    '''
    >>> from src.units.LatLong import LatLong
    >>> from src.units.Vector3 import Vector3
    >>> location = LatLong(45, 0)
    >>> acceleration = Vector3(0, 0, -10)
    >>> magneticField = Vector3(0, -10, 0)
    >>> expectedZenith = Vector3(1 / SQRT2, 0, 1 / SQRT2)
    >>> expectedNadir = Vector3(-1 / SQRT2, 0, -1 / SQRT2)
    >>> expectedNorth = Vector3(-1 / SQRT2, 0, 1 / SQRT2)
    >>> expectedEast = Vector3(0, 1, 0)
    >>> expectedSouth = Vector3(1 / SQRT2, 0, -1 / SQRT2)
    >>> expectedWest = Vector3(0, -1, 0)
    >>> expectedPointing = expectedNadir
    >>> expectedUpAlongPhone = expectedNorth
    >>> checkModelOrientation(location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
    '''
    pass

def testSetPhoneSensorValues_phoneFlatOnEquatorAtMeridian():
    # As previous test, but at lat, long = (0, 0)
    '''
    >>> from src.units.LatLong import LatLong
    >>> from src.units.Vector3 import Vector3
    >>> location = LatLong(0, 0) 
    >>> acceleration = Vector3(0, 0, -10)
    >>> magneticField = Vector3(0, -1, 10)
    >>> expectedZenith = Vector3(1, 0, 0)
    >>> expectedNadir = Vector3(-1, 0, 0)
    >>> expectedNorth = Vector3(0, 0, 1)
    >>> expectedEast = Vector3(0, 1, 0)
    >>> expectedSouth = Vector3(0, 0, -1)
    >>> expectedWest = Vector3(0, -1, 0)
    >>> expectedPointing = expectedNadir
    >>> expectedUpAlongPhone = expectedNorth
    >>> checkModelOrientation(location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
    
    '''
    pass

def testSetPhoneSensorValues_phoneLandscapeFacingEastOnEquatorAtMeridian():
    # As previous test, but with the phone vertical, but in landscape mode and pointing east.
    '''
    >>> from src.units.LatLong import LatLong
    >>> from src.units.Vector3 import Vector3
    >>> location = LatLong(0, 0)
    >>> acceleration =  Vector3(10, 0, 0)
    >>> magneticField =  Vector3(-10, 1, 0)
    >>> expectedZenith = Vector3(1, 0, 0)
    >>> expectedNadir = Vector3(-1, 0, 0)
    >>> expectedNorth = Vector3(0, 0, 1)
    >>> expectedEast = Vector3(0, 1, 0)
    >>> expectedSouth = Vector3(0, 0, -1)
    >>> expectedWest = Vector3(0, -1, 0)
    >>> expectedPointing = expectedEast
    >>> expectedUpAlongPhone = expectedSouth
    >>> checkModelOrientation(location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
    '''

def testSetPhoneSensorValues_phoneStandingUpFacingNorthOnEquatorAtMeridian():
    # As previous test, but in portrait mode facing north.
    '''
    >>> from src.units.LatLong import LatLong
    >>> from src.units.Vector3 import Vector3
    >>> location = LatLong(0, 0)
    >>> acceleration = Vector3(0, -10, 0)
    >>> magneticField = Vector3(0, 10, 1)
    >>> expectedZenith = Vector3(1, 0, 0)
    >>> expectedNadir = Vector3(-1, 0, 0)
    >>> expectedNorth = Vector3(0, 0, 1)
    >>> expectedEast = Vector3(0, 1, 0)
    >>> expectedSouth = Vector3(0, 0, -1)
    >>> expectedWest = Vector3(0, -1, 0)
    >>> expectedPointing = expectedNorth
    >>> expectedUpAlongPhone = expectedZenith
    >>> checkModelOrientation(location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
    ''' 

def checkModelOrientation(location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone): 
    # For now only test a model with no magnetic correction.
    import datetime as dt
    import calendar
    import time
    from src.control.AstronomerModel import AstronomerModel
    from src.control.ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator as ZMDC
    Astronomer = AstronomerModel(ZMDC())
    Astronomer.set_location(location) 
    
    class myClock():
        clock = dt.datetime(2009, 3, 20, 12, 07, 24).timetuple()
        def get_time(self):
            return calendar.timegm(self.clock)
    # This date is special as RA, DEC = (0, 0) is directly overhead at the equator on the Greenwich meridian.
    # 12:07 March 20th 2009
    
    Astronomer.set_clock(myClock())
    Astronomer.set_phone_sensor_values(acceleration, magneticField)
    worked = True 
    worked = assertVectorEquals(expectedZenith, Astronomer.get_zenith(), tol_length, tol_angle) & worked
    worked = assertVectorEquals(expectedNadir, Astronomer.get_nadir(), tol_length, tol_angle) & worked
    worked = assertVectorEquals(expectedNorth, Astronomer.get_north(), tol_length, tol_angle) & worked
    worked = assertVectorEquals(expectedEast, Astronomer.get_east(), tol_length, tol_angle) & worked
    worked = assertVectorEquals(expectedSouth, Astronomer.get_south(), tol_length, tol_angle) & worked
    worked = assertVectorEquals(expectedWest, Astronomer.get_west(), tol_length, tol_angle) & worked
    worked = assertVectorEquals(expectedPointing, Astronomer.get_pointing().get_line_of_sight(), tol_length, tol_angle) & worked
    worked = assertVectorEquals(expectedUpAlongPhone, Astronomer.get_pointing().get_perpendicular(), tol_length, tol_angle) & worked

# AstronomerModelWithMagneticVariationTest

# def MagneticDeclinationCalculation(angle):
#     angle = angle
#     def get_declination(self): 
#         return angle

# def testAssertVectorEquals():
#     '''
#     >>> from units.Vector3 import Vector3 
#     >>> v1 = Vector3(0,0,1)
#     >>> v2 = Vector3(0,0,1)
#     >>> assertVectorEquals(v1,v2,0.0001,0.0001)
#     True
#     '''
#     pass

# def testFlatOnEquatorMag0Degrees():
#     '''
#     >>> from units.LatLong import LatLong
#     >>> from units.Vector3 import Vector3 
#     >>> location = LatLong(0, 0)
#     >>> acceleration = Vector3(0, 0, -10)
#     >>> magneticField = Vector3(0, -5, -10)
#     >>> expectedZenith = Vector3(1, 0, 0)
#     >>> expectedNadir = Vector3(-1, 0, 0)
#     >>> expectedNorth = Vector3(0, 0, 1)
#     >>> expectedEast = Vector3(0, 1, 0)
#     >>> expectedSouth = Vector3(0, 0, -1)
#     >>> expectedWest = Vector3(0, -1, 0)
#     >>> expectedPointing = expectedNadir
#     >>> expectedUpAlongPhone = expectedNorth
#     >>> checkPointing(float(0.0), location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
#     '''
#     pass
# 
# def testFlatOnEquatorMagN45DegreesW(): 
#     '''
#     >>> from units.LatLong import LatLong
#     >>> from units.Vector3 import Vector3 
#     >>> location = LatLong(0, 0)
#     >>> acceleration = Vector3(0, 0, -10)
#     >>> magneticField = Vector3(1, -1, -10)
#     >>> expectedZenith = Vector3(1, 0, 0)
#     >>> expectedNadir = Vector3(-1, 0, 0)
#     >>> expectedNorth = Vector3(0, 0, 1)
#     >>> expectedEast = Vector3(0, 1, 0)
#     >>> expectedSouth = Vector3(0, 0, -1)
#     >>> expectedWest = Vector3(0, -1, 0)
#     >>> expectedPointing = expectedNadir
#     >>> expectedUpAlongPhone = expectedNorth
#     >>> checkPointing(float(-45.0), location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
#     '''
#     pass
# 
# def testStandingUpOnEquatorMagN10DegreesEast():
#     '''
#     >>> from units.LatLong import LatLong
#     >>> from units.Vector3 import Vector3 
#     >>> import utils.Geometry as Geometry
#     >>> import math
#     >>> location = LatLong(0, 0)
#     >>> acceleration = Vector3(0, -10, 0)
#     >>> magneticField = Vector3(-math.sin(Geometry.degrees_to_radians(10)), 10, math.cos(Geometry.degrees_to_radians(10)))
#     >>> expectedZenith = Vector3(1, 0, 0)
#     >>> expectedNadir = Vector3(-1, 0, 0)
#     >>> expectedNorth = Vector3(0, 0, 1)
#     >>> expectedEast = Vector3(0, 1, 0)
#     >>> expectedSouth = Vector3(0, 0, -1)
#     >>> expectedWest = Vector3(0, -1, 0)
#     >>> expectedPointing = expectedNorth
#     >>> expectedUpAlongPhone = expectedZenith
#     >>> checkPointing(10, location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
#     '''
# 
# def checkPointing(magDeclination, location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone):
#     import datetime as dt
#     import time
#     from control.AstronomerModel import AstronomerModel
#     from control.RealMagneticDeclinationCalculator import RealMagneticDeclinationCalculator as RMDC
#     Astronomer = AstronomerModel(RMDC())
#     MagneticDeclinationCalculation(magDeclination)
#     Astronomer.set_location(location)
#      
#     class myClock():
#         clock = dt.datetime(2009, 3, 20, 12, 07, 24).timetuple()
#         def get_time(self):
#             return calendar.timegm(self.clock)
#     
#     Astronomer.set_clock(myClock())
#     Astronomer.set_phone_sensor_values(acceleration, magneticField)
#     pointing = Astronomer.get_pointing().get_line_of_sight()
#     upAlongPhone = Astronomer.get_pointing().get_perpendicular()
#     north = Astronomer.get_north()
#     east = Astronomer.get_east()
#     south = Astronomer.get_south()
#     west = Astronomer.get_west()
#     zenith = Astronomer.get_zenith()
#     nadir = Astronomer.get_nadir()
#     assertVectorEquals(expectedZenith, zenith, tol_length, tol_angle)
#     assertVectorEquals(expectedNadir, nadir, tol_length, tol_angle)
#     assertVectorEquals(expectedNorth, north, tol_length, tol_angle)
#     assertVectorEquals(expectedEast, east, tol_length, tol_angle)
#     assertVectorEquals(expectedSouth, south, tol_length, tol_angle)
#     assertVectorEquals(expectedWest, west, tol_length, tol_angle)
#     assertVectorEquals(expectedPointing, pointing, tol_length, tol_angle)
#     assertVectorEquals(expectedUpAlongPhone, upAlongPhone, tol_length, tol_angle)
# 
# def testFlatLat45Long0MagN180Degrees():
#     '''
#     >>> from units.LatLong import LatLong
#     >>> from units.Vector3 import Vector3 
#     >>> location = LatLong(45, 0)
#     >>> acceleration = Vector3(0, 0, -10)
#     >>> magneticField = Vector3(0, 10, 0)
#     >>> expectedZenith = Vector3(1 / SQRT2, 0, 1 / SQRT2)
#     >>> expectedNadir = Vector3(-1 / SQRT2, 0, -1 / SQRT2)
#     >>> expectedNorth = Vector3(-1 / SQRT2, 0, 1 / SQRT2)
#     >>> expectedEast = Vector3(0, 1, 0)
#     >>> expectedSouth = Vector3(1 / SQRT2, 0, -1 / SQRT2)
#     >>> expectedWest = Vector3(0, -1, 0)
#     >>> expectedPointing = expectedNadir
#     >>> expectedUpAlongPhone = expectedNorth
#     >>> checkPointing(180, location, acceleration, magneticField, expectedZenith, expectedNadir, expectedNorth, expectedEast, expectedSouth, expectedWest, expectedPointing, expectedUpAlongPhone)
#     '''

#ControllerGroupTest

def ControllerGroupTests():
    '''
    >>> import src.control.Controller as Controller
    >>> import src.control.ControllerGroup as ControllerGroup
    
    
    >>> controllerGroup = ControllerGroup.create_controller_group()

    >>> controller1 = Controller.Controller()
    >>> controller2 = Controller.Controller()
    >>> controllerGroup.add_controller(controller1)
    >>> controllerGroup.add_controller(controller2)
    
    '''
    pass

