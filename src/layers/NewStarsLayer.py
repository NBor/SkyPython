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

from FileBasedLayer import FileBasedLayer

class NewStarsLayer(FileBasedLayer):
    '''
    Displays stars in the renderer
    '''

    def get_layer_id(self):
        return -100
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.0"

    def __init__(self):
        '''
        Constructor
        '''
        FileBasedLayer.__init__(self, "assets/stars.binary")
        
if __name__ == "__main__":
    '''
    For debugging purposes
    '''
    import os
    os.chdir("../../")
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