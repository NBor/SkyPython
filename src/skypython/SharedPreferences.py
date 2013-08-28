'''
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


Created on 2013-08-12

@author: Neil Borle
'''

class SharedPreferences(object):
    '''
    The users preferences which are instantiated in 
    the SkyPython class. Since Android Shared Preferences
    are not available in Python, this class simply acts as
    a container for the state that would have been in 
    Shared Preferences. 
    '''

    PREFERENCES = {"source_provider.0" : True,
                   "source_provider.1" : True,
                   "source_provider.2" : True,
                   "source_provider.3" : True,
                   "source_provider.4" : True,
                   "source_provider.5" : True,
                   "source_provider.6" : True,
                   "source_provider.7" : True,
                   "source_provider.8" : True }
    ALLOW_ROTATION = False

    def __init__(self):
        '''
        Constructor
        '''
        