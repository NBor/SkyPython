'''
Created on 2013-05-22

@author: Neil
'''

import sourceProto.SourceProto as SourceProto
from SourceLayer import SourceLayer
from source.AstronomicalSource import AstronomicalSource
from sourceProto.ProtobufAstronomicalSource import ProtobufAstronomicalSource

class FileBasedLayer(SourceLayer):
    '''
    NEED TO FINISH IMPLEMENTING
    '''
    executor_for_multiple_threads = None
    file_name = ""
    file_sources = []
    
    def initialize(self):
        self.read_source_file(self.file_name)
        self.init_astro_sources()
        self.init()
        
    def init_astro_sources(self):
        for proto_source in self.file_sources:
            new_astro = AstronomicalSource()
            new_astro.names = proto_source.names
            new_astro.geocentric_coords = proto_source.get_geo_coords()
            #new_astro.image_sources = proto_source. ???
            new_astro.point_sources = proto_source.get_points()
            new_astro.line_sources = proto_source.get_lines()
            new_astro.text_sources = proto_source.get_labels()
            self.astro_sources.append(new_astro)
        
    def read_source_file(self, file_name):
        astro_sources_proto = SourceProto.AstronomicalSourcesProto()
        try:
            f = open(file_name, "rb")
            astro_sources_proto.ParseFromString(f.read())
        except:
            raise IOError("Could not open file")
        finally:
            f.close()
        
        for source in astro_sources_proto.source:
            self.file_sources.append(ProtobufAstronomicalSource(source))

    def __init__(self, file_string):
        '''
        Constructor
        '''
        SourceLayer.__init__(self, False)
        self.file_name = file_string
        
if __name__ == "__main__":
    '''
    For debugging purposes
    '''
    FBL = FileBasedLayer("../../assets/constellations.binary")
    FBL.initialize()
    first_protobuf_source = FBL.file_sources[0]
    gc = first_protobuf_source.get_geo_coords()
    print gc.x, gc.y, gc.z
    print first_protobuf_source.names
    print first_protobuf_source.get_points()
    print first_protobuf_source.get_labels()
    print first_protobuf_source.get_lines()
    #point = first_protobuf_source.get_points()[0]
    #label = first_protobuf_source.get_labels()[0]
    #line = first_protobuf_source.get_lines()[0]
    #print point.size, point.color, point.geocentric_coords, point.point_shape
    #print label.label, label.geocentric_coords, label.color, label.offset, label.font_size
    #print line.color, line.line_width, line.gc_verticies