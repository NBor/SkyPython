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
// Original Author: James Powell
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-24

@author: Neil Borle
'''
import math
from src.utils.VectorUtil import dot_product
from src.utils.Geometry import degrees_to_radians
from src.units.GeocentricCoordinates import GeocentricCoordinates

class ActiveRegionData(object):
    '''
    This stores data that we only want to compute once per frame about
    which regions are on the screen.  We don't want to compute these
    regions for every manager separately, since we can share them
    between managers.
    '''
    
    def region_is_active(self, region_num, coverage_angle):
        '''
        Tests to see if a particular region is active.
        '''
        return self.region_center_dot_products[region_num] > \
            math.cos(coverage_angle + self.screen_angle)
    
    def __init__(self, dot_products, angles, active_regions):
        '''
        constructor
        '''
        self.region_center_dot_products = dot_products
        self.screen_angle = angles #default at 45 degrees
        self.active_standard_regions = active_regions

class SkyRegionMap(object):
    '''
    This is a utility class which divides the sky into a fixed set of regions
    and maps each of the regions into a generic data object which contains the
    data for rendering that region of the sky.  For a given frame, this class
    will determine which regions are on-screen and which are totally
    off-screen, and will return only the on-screen ones (so we can avoid paying
    the cost of rendering the ones that aren't on-screen).  There should
    typically be one of these objects per type of object being rendered: for
    example, points and labels will each have their own SkyRegionMap.
    
    Each region consists of a center (a point on the unit sphere) and an angle,
    and should contain every object on the unit sphere within the specified
    angle from the region's center.
    
    This also allows for a special "catchall" region which is always rendered
    and may contain objects from anywhere on the unit sphere.  This is useful
    because, for small layers, it is cheaper to just render the
    whole layer than to break it up into smaller pieces.
    
    The center of all regions is fixed for computational reasons.  This allows
    us to find the distance between each region and the current look direction
    once per frame and share that between all SkyRegionMaps.  For most types
    of objects, they can also use regions with the same radius, which means
    that they are the same exact part of the unit sphere.  For these we can
    compute the regions which are on screen ("active regions") once per frame,
    and share that between all SkyRegionMaps.  These are called "standard
    regions", as opposed to "non-standard regions", where the region's angle
    may be greater than that of the standard region.  Non-standard regions
    are necessary for some types of objects, such as lines, which may not be
    fully contained within any standard region.  For lines, we can find the
    region center which is closest to fully containing the line, and simply
    increase the angle until it does fully contain it.
    '''
    
    class ObjectRegionData(object):
        '''
        Data representing an individual object's position in a region.
        We care about the region itself for obvious reasons, but we care about
        the dot product with the center because it is a measure of how
        close it is to the center of a region.
        '''
        
        def __init__(self):
            '''
            constructor
            '''
            self.region = SkyRegionMap().CATCHALL_REGION_ID
            self.region_center_dot_product = -1
               
    class RegionDataFactory(object):
        '''
        Factory class where the construct method is set during
        instantiation to produce RegionData objects
        '''
        def construct(self):
            raise Exception("This method must be overwritten")
        
        def __init__(self, construct_method):
            '''
            constructor
            '''
            self.construct = construct_method
    
    CATCHALL_REGION_ID = -1
    REGION_COVERAGE_ANGLE_IN_RADIANS = 0.396023592
    REGION_CENTERS32 = [ \
        GeocentricCoordinates(-0.850649066269, 0.525733930059, -0.000001851469),
        GeocentricCoordinates(-0.934170971625, 0.000004098751, -0.356825719588),
        GeocentricCoordinates(0.577349931933, 0.577346773818, 0.577354100533),
        GeocentricCoordinates(0.577350600623, -0.577350601554, -0.577349603176),
        GeocentricCoordinates(-0.577354427427, -0.577349954285, 0.577346424572),
        GeocentricCoordinates(-0.577346098609, 0.577353779227, -0.577350928448),
        GeocentricCoordinates(-0.577349943109, -0.577346729115, -0.577354134060),
        GeocentricCoordinates(-0.577350598760, 0.577350586653, 0.577349620871),
        GeocentricCoordinates(0.577354458161, 0.577349932864, -0.577346415259),
        GeocentricCoordinates(0.577346091159, -0.577353793196, 0.577350921929),
        GeocentricCoordinates(-0.850652559660, -0.525728277862, -0.000004770234),
        GeocentricCoordinates(-0.934173742309, 0.000002107583, 0.356818466447),
        GeocentricCoordinates(0.525734450668, 0.000000594184, -0.850648744032),
        GeocentricCoordinates(0.000002468936, -0.356819496490, -0.934173349291),
        GeocentricCoordinates(0.525727798231, -0.000004087575, 0.850652855821),
        GeocentricCoordinates(-0.000002444722, 0.356819517910, 0.934173340909),
        GeocentricCoordinates(-0.525727787986, 0.000004113652, -0.850652862340),
        GeocentricCoordinates(0.000004847534, 0.356824675575, -0.934171371162),
        GeocentricCoordinates(-0.000004885718, -0.850652267225, 0.525728750974),
        GeocentricCoordinates(-0.356825215742, -0.934171164408, -0.000003995374),
        GeocentricCoordinates(0.000000767410, 0.850649364293, 0.525733447634),
        GeocentricCoordinates(0.356825180352, 0.934171177447, 0.000003952533),
        GeocentricCoordinates(-0.000000790693, -0.850649344735, -0.525733478367),
        GeocentricCoordinates(0.356818960048, -0.934173554182, -0.000001195818),
        GeocentricCoordinates(0.850652555004, 0.525728284381, 0.000004773028),
        GeocentricCoordinates(0.934170960449, -0.000004090369, 0.356825748459),
        GeocentricCoordinates(-0.525734410621, -0.000000609085, 0.850648769177),
        GeocentricCoordinates(-0.000004815869, -0.356824668124, 0.934171373956),
        GeocentricCoordinates(0.000004877336, 0.850652255118, -0.525728769600),
        GeocentricCoordinates(-0.356819001026, 0.934173538350, 0.000001183711),
        GeocentricCoordinates(0.850649050437, -0.525733955204, 0.000001879409),
        GeocentricCoordinates(0.934173759073, -0.000002136454, -0.356818422675)]
    
    
    def get_active_regions(self, look_dir, fovy_in_degrees, aspect):
        '''
        Computes the data necessary to determine which regions on the screen
        are active.  This should be produced once per frame and passed to
        the getDataForActiveRegions method of all SkyRegionMap objects to
        get the active regions for each map.
        
        lookDir The direction the user is currently facing.
        fovyInDegrees The field of view (in degrees).
        aspect The aspect ratio of the screen.
        Returns a data object containing data for quickly determining the
        active regions.
        '''
        half_fovy = degrees_to_radians(fovy_in_degrees) / 2.0
        screen_angle = math.asin(math.sin(half_fovy) * math.sqrt(1 + aspect * aspect))
        angle_threshold = screen_angle + self.REGION_COVERAGE_ANGLE_IN_RADIANS
        dot_product_threshold = math.cos(angle_threshold)
        region_center_dot_products = [0] * len(self.REGION_CENTERS32)
        active_standard_regions = []
        
        i = 0
        for i in range(len(self.REGION_CENTERS32)):
            d_product = dot_product(look_dir, self.REGION_CENTERS32[i])
            region_center_dot_products[i] = d_product

            if d_product > dot_product_threshold:
                active_standard_regions.append(i)
            
        return ActiveRegionData(region_center_dot_products, \
                                screen_angle, active_standard_regions)
        
    def get_object_region(self, gc_coords):
        '''
        returns to region that contains the coordinate
        '''
        return self.get_object_region_data(gc_coords).region
    
    def get_object_region_data(self, gc_coords):
        '''
        returns the region a point belongs in, as well as the dot product of the
        region center and the position.  The latter is a measure of how close it
        is to the center of the region (1 being a perfect match).
        '''
        data = self.ObjectRegionData()
        
        i = 0
        for i in range(len(self.REGION_CENTERS32)):
            d_product = dot_product(self.REGION_CENTERS32[i], gc_coords)
            
            if d_product > data.region_center_dot_product:
                data.region_center_dot_product = d_product
                data.region = i
            
        return data
    
    def clear(self):
        self.region_data.clear()
        self.region_coverage_angles = None
        
    def set_region_data(self, r_id, data):
        '''
        sets generic RenderingRegionData as specified by ObjectManager
        which instantiated this class
        '''
        self.region_data[r_id] = data
        
    def get_region_coverage_angle(self, r_id):
        if self.region_coverage_angles == None:
            return self.REGION_COVERAGE_ANGLE_IN_RADIANS
        else:
            return self.region_coverage_angles[r_id]
        
    def set_region_coverage_angle(self, r_id, angle_in_radians):
        '''
        Sets the coverage angle for a sky region.  Needed for non-point objects.
        '''
        if self.region_coverage_angles == None:
            self.region_coverage_angles = [self.REGION_COVERAGE_ANGLE_IN_RADIANS] * \
                len(self.REGION_CENTERS32)
        self.region_coverage_angles[r_id] = angle_in_radians
        
    def get_region_data(self, r_id):
        '''
        Lookup the region data corresponding to a region ID.  If none exists,
        and a region data constructor has been set (see setRegionDataConstructor),
        that will be used to create a new region - otherwise, this will return
        None.  This can be useful while building or updating a region, but to get
        the region data when rendering a frame, use getDataForActiveRegions().
        '''
        data = None
        
        if r_id in self.region_data.keys():
            data = self.region_data[r_id]
        elif self.region_data_factory != None:
            data = self.region_data_factory.construct()
            self.set_region_data(r_id, data)
        
        return data
    
    def get_data_for_active_regions(self, active_region_data):
        '''
        returns the rendering data for the active regions.  When using a
        SkyRegionMap for rendering, this is the function will return the
        data for the regions you need to render.
        '''
        data = []
        
        if self.CATCHALL_REGION_ID in self.region_data.keys():
            data.append(self.region_data[self.CATCHALL_REGION_ID])
            
        if self.region_coverage_angles == None:
            for region in active_region_data.active_standard_regions:
                if region in self.region_data.keys():
                    data.append(self.region_data[region])
            return data
        else:
            for i in range(len(self.REGION_CENTERS32)):
                if active_region_data.region_is_active(i, self.region_coverage_angles[i])\
                    and i in self.region_data.keys():
                    data.append(self.region_data[i])
            return data

    def __init__(self):
        '''
        Constructor
        '''
        self.region_coverage_angles = None
        self.region_data = {}
        self.region_data_factory = None
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
