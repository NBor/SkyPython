'''
Created on 2013-05-24

@author: Neil
'''
import math
from ..utils.VectorUtil import dot_product
from ..utils.Geometry import degrees_to_radians
from ..units.GeocentricCoordinates import GeocentricCoordinates

class ActiveRegionData(object):
    '''
    classdocs
    '''
    
    def region_is_active(self, region_num, coverage_angle):
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
    classdocs
    '''
    
    class ObjectRegionData(object):
        '''
        classdata
        '''
        
        def __init__(self):
            '''
            constructor
            '''
            self.region = SkyRegionMap().CATCHALL_REGION_ID
            self.region_center_dot_product = -1
               
    class RegionDataFactory(object):
        '''
        classdocs
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
        return self.get_object_region_data(gc_coords).region
    
    def get_object_region_data(self, gc_coords):
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
        if self.region_coverage_angles == None:
            self.region_coverage_angles = [self.REGION_COVERAGE_ANGLE_IN_RADIANS] * \
                len(self.REGION_CENTERS32)
        self.region_coverage_angles[r_id] = angle_in_radians
        
    def get_region_data(self, r_id):
        '''
        gets generic RenderingRegionData as specified by ObjectManager
        which instantiated this class
        '''
        data = None
        
        if r_id in self.region_data.keys():
            data = self.region_data[r_id]
        elif self.region_data_factory != None:
            data = self.region_data_factory.construct()
            self.set_region_data(r_id, data)
        
        return data
    
    def get_data_for_active_regions(self, active_region_data):
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