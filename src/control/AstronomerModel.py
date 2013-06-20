'''
Created on 2013-05-23

@author: Neil
'''

import math
import time
import utils.Geometry as Geometry
import skypython.ApplicationConstants as ApplicationConstants
from Pointing import Pointing
from RealClock import RealClock
from units.LatLong import LatLong
from units.Vector3 import Vector3
from units.Matrix33 import get_colmatrix_from_vectors, get_identity_matrix
from units.Matrix33 import get_rowmatrix_from_vectors
from units.GeocentricCoordinates import get_instance
from units.GeocentricCoordinates import get_instance_from_vector3

class AstronomerModel(object):
    '''
    classdocs
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
        return time.gmtime(self.clock.get_time())

    def set_location(self, lat_long):
        self.location = lat_long
        self.calculate_local_north_and_up_in_celestial_coords(True)
        
    def set_phone_sensor_values(self, accel, mag_field):
        self.acceleration.assign(vector3=accel)
        self.magnetic_field.assign(vector3=mag_field)
        
    def get_north(self):
        self.calculate_local_north_and_up_in_celestial_coords(False)
        return get_instance_from_vector3(self.true_north_celestial)
        
    def get_south(self):
        self.calculate_local_north_and_up_in_celestial_coords(False)
        v = Geometry.scale_vector(self.true_north_celestial, -1)
        return get_instance_from_vector3(v)
    
    def get_zenith(self):
        self.calculate_local_north_and_up_in_celestial_coords(False)
        return get_instance_from_vector3(self.up_celestial)
    
    def get_nadir(self):
        self.calculate_local_north_and_up_in_celestial_coords(False)
        v = Geometry.scale_vector(self.up_celestial, -1)
        return get_instance_from_vector3(v)
    
    def get_east(self):
        self.calculate_local_north_and_up_in_celestial_coords(False)
        return get_instance_from_vector3(self.true_east_celestial)
    
    def get_west(self):
        self.calculate_local_north_and_up_in_celestial_coords(False)
        v = Geometry.scale_vector(self.true_east_celestial, -1)
        return get_instance_from_vector3(v)
    
    def set_mag_dec_calc(self, calculator):
        self.magnetic_declination_calc = calculator
        self.calculate_local_north_and_up_in_celestial_coords(True)
        
    def calculate_pointing(self):
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
        current_time = int(self.clock.get_time() * 1000)
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
            self.location, int(self.clock.get_time() * 1000))
    
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
        self.clock = clock
        self.calculate_local_north_and_up_in_celestial_coords(True)

    def __init__(self, mag_dec_calc):
        '''
        Constructor
        '''
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
    For debugging purposes
    Ready for testing
    '''
    