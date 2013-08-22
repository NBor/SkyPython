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
// Original Author: John Taylor
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-23

@author: Neil Borle
'''

import math
import time
from Pointing import Pointing
from RealClock import RealClock
from src.skypython import ApplicationConstants
from src.utils import Geometry
from src.units.LatLong import LatLong
from src.units.Vector3 import Vector3
from src.units.Matrix33 import get_colmatrix_from_vectors, get_identity_matrix
from src.units.Matrix33 import get_rowmatrix_from_vectors
from src.units.GeocentricCoordinates import get_instance
from src.units.GeocentricCoordinates import get_instance_from_vector3

class AstronomerModel(object):
    '''
    Class responsible to modelling the astronomer
    
    This class has state on the location and orientation of the astronomer
    in space and performs calculations for obtaining directions and time.
    
    As stated in the android version: 
    
    There are 3 frames of reference:
    Celestial - a frame fixed against the background stars with
    x, y, z axes pointing to (RA = 90, DEC = 0), (RA = 0, DEC = 0), DEC = 90
    Phone - a frame fixed in the phone with x across the short side, y across
    the long side, and z coming out of the phone screen.
    Local - a frame fixed in the astronomer's local position. x is due east
    along the ground y is due north along the ground, and z points towards the
    zenith.
    
    We calculate the local frame in phone coords, and in celestial coords and
    calculate a transform between the two.
    In the following, N, E, U correspond to the local
    North, East and Up vectors (ie N, E along the ground, Up to the Zenith)
    
    In Phone Space: axesPhone = [N, E, U]
    
    In Celestial Space: axesSpace = [N, E, U]
    
    We find T such that axesCelestial = T * axesPhone
    
    Then, [viewDir, viewUp]_celestial = T * [viewDir, viewUp]_phone
    
    where the latter vector is trivial to calculate.
    '''
    
    POINTING_DIR_IN_PHONE_COORDS = Vector3(0, 0, -1)
    SCREEN_UP_IN_PHONE_COORDS = Vector3(0, 1, 0)
    AXIS_OF_EARTHS_ROTATION = Vector3(0, 0, 1)
    MINIMUM_TIME_BETWEEN_CELESTIAL_COORD_UPDATES_MILLIS = 60000.0
    
    magnetic_declination_calc = None
    auto_update_pointing = True
    field_of_view = 45  #Degrees
    location = LatLong(0, 0)
    clock = RealClock()
    celestial_coords_last_updated = -1

    def get_time(self):
        '''
        return a time struct of the current GM time
        '''
        return time.gmtime(self.clock.get_time())

    def set_location(self, lat_long):
        self.location = lat_long
        self.calculate_local_north_and_up_in_celestial_coords(True)
        
    def set_phone_sensor_values(self, accel, mag_field):
        self.acceleration.assign(vector3=accel)
        self.magnetic_field.assign(vector3=mag_field)
        
    def get_north(self):
        '''
        In celestial coordinates
        '''
        self.calculate_local_north_and_up_in_celestial_coords(False)
        return get_instance_from_vector3(self.true_north_celestial)
        
    def get_south(self):
        '''
        In celestial coordinates
        '''
        self.calculate_local_north_and_up_in_celestial_coords(False)
        v = Geometry.scale_vector(self.true_north_celestial, -1)
        return get_instance_from_vector3(v)
    
    def get_zenith(self):
        '''
        In celestial coordinates
        '''
        self.calculate_local_north_and_up_in_celestial_coords(False)
        return get_instance_from_vector3(self.up_celestial)
    
    def get_nadir(self):
        '''
        In celestial coordinates
        '''
        self.calculate_local_north_and_up_in_celestial_coords(False)
        v = Geometry.scale_vector(self.up_celestial, -1)
        return get_instance_from_vector3(v)
    
    def get_east(self):
        '''
        In celestial coordinates
        '''
        self.calculate_local_north_and_up_in_celestial_coords(False)
        return get_instance_from_vector3(self.true_east_celestial)
    
    def get_west(self):
        '''
        In celestial coordinates
        '''
        self.calculate_local_north_and_up_in_celestial_coords(False)
        v = Geometry.scale_vector(self.true_east_celestial, -1)
        return get_instance_from_vector3(v)
    
    def set_mag_dec_calc(self, calculator):
        self.magnetic_declination_calc = calculator
        self.calculate_local_north_and_up_in_celestial_coords(True)
        
    def calculate_pointing(self):
        '''
        update the direction that the phone is pointing and the up vector
        perpendicular to the phone (in celestial coords).
        '''
        if not (self.auto_update_pointing): 
            return
        
        transform = Geometry.matrix_multiply(self.axes_magnetic_celestial_matrix, \
                                             self.axes_phone_inverse_matrix)

        view_in_space_space = \
            Geometry.matrix_vector_multiply(transform, self.POINTING_DIR_IN_PHONE_COORDS)
        screen_up_in_space_space = \
            Geometry.matrix_vector_multiply(transform, self.SCREEN_UP_IN_PHONE_COORDS)
            
        self.pointing.update_line_of_sight(view_in_space_space)
        self.pointing.update_perpendicular(screen_up_in_space_space)
        
    def calculate_local_north_and_up_in_celestial_coords(self, force_update):
        current_time = self.get_time_in_millis()
        diff = math.fabs(current_time - self.celestial_coords_last_updated)
        if (not force_update) and diff < self.MINIMUM_TIME_BETWEEN_CELESTIAL_COORD_UPDATES_MILLIS:
            return
        
        self.celestial_coords_last_updated = current_time
        self.update_magnetic_correction()
        up_ra, up_dec = Geometry.calculate_RADec_of_zenith(self.get_time(), self.location)
        self.up_celestial = get_instance(up_ra, up_dec)
        z = self.AXIS_OF_EARTHS_ROTATION
        z_dotu = Geometry.scalar_product(self.up_celestial, z)
        self.true_north_celestial = \
            Geometry.add_vectors(z, Geometry.scale_vector(self.up_celestial, -z_dotu))
        self.true_north_celestial.normalize()
        self.true_east_celestial = Geometry.vector_product(self.true_north_celestial, \
                                                           self.up_celestial)
        
        # Apply magnetic correction.  Rather than correct the phone's axes for
        # the magnetic declination, it's more efficient to rotate the
        # celestial axes by the same amount in the opposite direction.
        declination = self.magnetic_declination_calc.get_declination()
        rotation_matrix = Geometry.calculate_rotation_matrix(declination, self.up_celestial)
        magnetic_north_celestial = Geometry.matrix_vector_multiply(rotation_matrix, \
                                                                   self.true_north_celestial)
        magnetic_east_celestial = Geometry.vector_product(magnetic_north_celestial, \
                                                          self.up_celestial)
        self.axes_magnetic_celestial_matrix = get_colmatrix_from_vectors(magnetic_north_celestial, \
                                                                         self.up_celestial, \
                                                                         magnetic_east_celestial)
        
    def calculate_local_north_and_up_in_phone_coords(self):
        down = self.acceleration.copy()
        down.normalize()
        # Magnetic field goes *from* North to South, so reverse it.
        magnetic_field_to_north = self.magnetic_field.copy()
        magnetic_field_to_north.scale(-1)
        magnetic_field_to_north.normalize()
        
        # This is the vector to magnetic North *along the ground*.
        v2 = Geometry.scale_vector(down, -Geometry.scalar_product(magnetic_field_to_north, \
                                                                  down))
        magnetic_north_phone = Geometry.add_vectors(magnetic_field_to_north, v2)
        magnetic_north_phone.normalize()
        up_phone = Geometry.scale_vector(down, -1)
        magnetic_east_phone = Geometry.vector_product(magnetic_north_phone, up_phone)

        # The matrix is orthogonal, so transpose it to find its inverse.
        # Easiest way to do that is to construct it from row vectors instead
        # of column vectors.        
        self.axes_phone_inverse_matrix = \
            get_rowmatrix_from_vectors(magnetic_north_phone, 
                                       up_phone, 
                                       magnetic_east_phone)
    
    def update_magnetic_correction(self):
        self.magnetic_declination_calc.set_location_and_time(\
            self.location, self.get_time_in_millis())
    
    def get_pointing(self):
        self.calculate_local_north_and_up_in_phone_coords()
        self.calculate_pointing()
        return self.pointing
    
    def set_pointing(self, line_of_sight, perpendicular):
        '''
        Takes 2 vector3 objects as parameters
        '''
        self.pointing.update_line_of_sight(line_of_sight)
        self.pointing.update_perpendicular(perpendicular)

    def set_clock(self, clock):
        '''
        clock must have a get_time() method
        '''
        self.clock = clock
        self.calculate_local_north_and_up_in_celestial_coords(True)
        
    def get_time_in_millis(self):
        return int(self.clock.get_time() * 1000)

    def __init__(self, mag_dec_calc):
        '''
        Constructor
        '''
        # provides correction from true North to magnetic North 
        self.magnetic_declination_calc = mag_dec_calc
        
        #The pointing comprises a vector into the phone's screen expressed in
        #celestial coordinates combined with a perpendicular vector along the
        #phone's longer side.
        self.pointing = Pointing()
        
        #The sensor acceleration in the phone's coordinate system.
        self.acceleration = ApplicationConstants.INITIAL_DOWN
        
        #The sensor magnetic field in the phone's coordinate system.
        self.magnetic_field = ApplicationConstants.INITIAL_SOUTH
        
        #North along the ground in celestial coordinates.
        self.true_north_celestial = Vector3(1, 0, 0);
        
        #Up in celestial coordinates.
        self.up_celestial = Vector3(0, 1, 0)
        
        #East in celestial coordinates.
        self.true_east_celestial = self.AXIS_OF_EARTHS_ROTATION
        
        #[North, Up, East]^-1 in phone coordinates.
        self.axes_phone_inverse_matrix = get_identity_matrix();
        
        #[North, Up, East] in celestial coordinates. */
        self.axes_magnetic_celestial_matrix = get_identity_matrix();
        
if __name__ == "__main__":
    '''
    Do nothing
    '''
    