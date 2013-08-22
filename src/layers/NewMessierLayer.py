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
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-29

@author: Neil Borle
'''

from FileBasedLayer import FileBasedLayer

class NewMessierLayer(FileBasedLayer):
    '''
    Displays messier objects in the renderer
    '''
    
    def get_layer_id(self):
        return -102
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.2"

    def __init__(self):
        '''
        Constructor
        '''
        FileBasedLayer.__init__(self, "assets/messier.binary")

if __name__ == "__main__":
    '''
    Do nothing
    '''
    