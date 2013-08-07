'''
Created on 2013-05-22

@author: Neil
'''

import SourceProto
from src.source.AbstractAstronomicalSource import AbstractAstronomicalSource
from src.source.PointSource import shape_enum
from src.units.GeocentricCoordinates import get_instance
from src.source.PointSource import PointSource
from src.source.TextSource import TextSource
from src.source.LineSource import LineSource

def construct_id_to_string_map(filename, index_to_string):
    with open(filename, 'r') as f_handle:
        for line in f_handle:
            key_value = line.strip().split(',')
            index_to_string[int(key_value[0])] = key_value[1]

class ProtobufAstronomicalSource(AbstractAstronomicalSource):
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
    
    strings = {}
    
    def set_names(self, APS):
        '''
        Strings are loaded from strings.txt in the assets folder.
        '''
        for name_id in APS.name_ids:
            self.names.append(self.strings[name_id])
    
    def get_geo_coords(self):
        gc = self.astro_source_proto.search_location
        return get_instance(gc.right_ascension, gc.declination)
    
    #override(AbstractAstronomicalSource)
    def get_points(self):
        point_list = []
        for p in self.astro_source_proto.point:
            gc_proto = p.location
            gc = get_instance(gc_proto.right_ascension, gc_proto.declination)
            point_list.append(PointSource(p.color, p.size, gc, self.shape_map[p.shape]))
        return point_list
            
    #override(AbstractAstronomicalSource)
    def get_labels(self):
        '''
        Strings are loaded from strings.txt in the assets folder.
        '''
        label_list = []
        for l in self.astro_source_proto.label:
            gc_proto = l.location
            gc = get_instance(gc_proto.right_ascension, gc_proto.declination)
            label_list.append(TextSource(self.strings[l.string_index], l.color,
                                         gc, l.offset, l.font_size))
        return label_list
    
    #override(AbstractAstronomicalSource)
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
        AbstractAstronomicalSource.__init__(self)
        
        if len(self.strings.keys()) == 0:
            construct_id_to_string_map("assets/Strings.txt", self.strings)
            
        self.astro_source_proto = astronomical_source_proto
        self.set_names(astronomical_source_proto)
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    print SourceProto.STAR, ProtobufAstronomicalSource.shape_map[SourceProto.STAR]