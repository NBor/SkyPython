'''
Created on 2013-05-22

@author: Neil
'''

from SourceLayer import SourceLayer
from ..sourceProto import SourceProto
from ..sourceProto.ProtobufAstronomicalSource import ProtobufAstronomicalSource

class FileBasedLayer(SourceLayer):
    '''
    NEED TO FINISH IMPLEMENTING
    '''
    executor_for_multiple_threads = None
    file_name = ""
    
    def initialize(self):
        # Need to execute this in a background thread
        self.read_source_file(self.file_name)
        SourceLayer.initialize(self)
        
    def initialize_astro_sources(self, sources):
        sources += self.file_sources
        
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
        self.file_sources = []
        
if __name__ == "__main__":
    '''
    For debugging purposes
    '''
    import os
    os.chdir("../..")
    FBL = FileBasedLayer("assets/stars.binary")
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