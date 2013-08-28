'''
// Copyright 2009 Google Inc.
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
// Original Author: John Taylor, Brent Bryan
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


Created on 2013-05-22

@author: Neil Borle
'''

from SourceLayer import SourceLayer
from src.sourceProto import SourceProto
from src.sourceProto.ProtobufAstronomicalSource import ProtobufAstronomicalSource

class FileBasedLayer(SourceLayer):
    '''
    For stars, constellations and messier objects. This is an abstraction
    for all layers that obtain their data from files.
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
            raise IOError("Could not open file: " + file_name)
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