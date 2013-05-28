'''
Created on 2013-05-22

@author: Neil
'''

import SourceProto
from source.PointSource import shape_enum
from units.GeocentricCoordinates import get_instance
from source.PointSource import PointSource
from source.TextSource import TextSource
from source.LineSource import LineSource

class ProtobufAstronomicalSource(object):
    '''
    classdocs
    '''
    shape_map = {SourceProto.CIRCLE : shape_enum.CIRCLE, \
                 SourceProto.STAR : shape_enum.CIRCLE, \
                 SourceProto.ELLIPTICAL_GALAXY : shape_enum.ELLIPTICAL_GALAXY, \
                 SourceProto.SPIRAL_GALAXY : shape_enum.SPIRAL_GALAXY, \
                 SourceProto.IRREGULAR_GALAXY : shape_enum.IRREGULAR_GALAXY, \
                 SourceProto.LENTICULAR_GALAXY : shape_enum.LENTICULAR_GALAXY, \
                 SourceProto.GLOBULAR_CLUSTER : shape_enum.GLOBULAR_CLUSTER, \
                 SourceProto.OPEN_CLUSTER : shape_enum.OPEN_CLUSTER, \
                 SourceProto.NEBULA : shape_enum.NEBULA, \
                 SourceProto.HUBBLE_DEEP_FIELD : shape_enum.HUBBLE_DEEP_FIELD}
    
    astro_source_proto = None
    names = []
    
    def set_names(self, APS):
        '''
        ISSUE!!! somehow we need to conver these numbers into
        actual stings! strings in a Strings.xml file
        '''
        for name_id in APS.name_ids:
            self.names.append(name_id)
    
    def get_geo_coords(self):
        gc = self.astro_source_proto.search_location
        return get_instance(gc.right_ascension, gc.declination)
    
    def get_images(self):
        return []
    
    def get_points(self):
        point_list = []
        for p in self.astro_source_proto.point:
            gc_proto = p.location
            gc = get_instance(gc_proto.right_ascension, gc_proto.declination)
            point_list.append(PointSource(p.color, p.size, gc, self.shape_map[p.shape]))
        return point_list
            
    
    def get_labels(self):
        '''
        ISSUE!!! somehow we need to conver these numbers into
        actual stings! strings in a Strings.xml file
        '''
        label_list = []
        for l in self.astro_source_proto.label:
            gc_proto = l.location
            gc = get_instance(gc_proto.right_ascension, gc_proto.declination)
            label_list.append(TextSource(str(l.string_index), l.color, \
                                         gc, l.offset, l.font_size))
        return label_list
    
    def get_lines(self):
        line_list = []
        for l in self.astro_source_proto.line:
            geocentric_verticies = []
            
            for gc_proto in l.vertex:
                gc = get_instance(gc_proto.right_ascension, \
                                  gc_proto.declination)
                geocentric_verticies.append(gc)
                
            line_list.append(LineSource(geocentric_verticies, l.color, \
                                        l.line_width))
        return line_list

    def __init__(self, astronomical_source_proto):
        '''
        Constructor
        '''
        self.astro_source_proto = astronomical_source_proto
        self.set_names(astronomical_source_proto)
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    print SourceProto.STAR, ProtobufAstronomicalSource.shape_map[SourceProto.STAR]