'''
// Copyright 2008 Google Inc.
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
// Original Author: Brent Bryan
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-16

@author: Neil Borle
'''

from Source import Source
from src.utils.Colors import colors

class LineSource(Source):
    '''
    classdocs
    '''

    def __init__(self, gcvs, new_color=colors.WHITE, lw=1.5):
        '''
        Constructor
        '''
        Source.__init__(self, new_color)
        self.ra_decs = []
        self.line_width = lw
        self.gc_vertices = gcvs
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''