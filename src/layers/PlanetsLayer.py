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


Created on 2013-06-26

@author: Neil Borle
'''

from SourceLayer import SourceLayer
from src.provider.PlanetSource import PlanetSource
from src.provider.Planet import Planet, res

class PlanetsLayer(SourceLayer):
    '''
    Manages displaying the other planets, the sun and the moon.
    '''
    def initialize_astro_sources(self, sources):
        for key in res.keys():
            p = Planet(key, res[key][0], res[key][1], res[key][2])
            sources.append(PlanetSource(p, self.model))
    
    def get_layer_id(self):
        return -103
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.3"

    def __init__(self, model):
        '''
        Constructor
        '''
        SourceLayer.__init__(self, True)
        self.model = model