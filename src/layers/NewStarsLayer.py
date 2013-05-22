'''
Created on 2013-05-22

@author: Neil
'''

from FileBasedLayer import FileBasedLayer

class NewStarsLayer(FileBasedLayer):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        FileBasedLayer.__init__(self, "../../assets/stars.binary")
        
if __name__ == "__main__":
    '''
    For debugging purposes
    '''
    SL = NewStarsLayer()
    SL.initialize()
    first_protobuf_source = SL.file_sources[0]
    gc = first_protobuf_source.get_geo_coords()
    print gc.x, gc.y, gc.z
    print first_protobuf_source.names
    print first_protobuf_source.get_points()
    print first_protobuf_source.get_labels()
    print first_protobuf_source.get_lines()
    point = first_protobuf_source.get_points()[0]
    label = first_protobuf_source.get_labels()[0]
    #line = first_protobuf_source.get_lines()[0]
    print point.size, point.color, point.geocentric_coords, point.point_shape
    print label.label, label.geocentric_coords, label.color, label.offset, label.font_size
    #print line.color, line.line_width, line.gc_verticies