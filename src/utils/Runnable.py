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


Created on 2013-06-07

@author: Neil Borle
'''

class Runnable(object):
    '''
    A Runnable class with a run method so that actions
    can be queued and then run uniformly. This substitutes
    for java's runnable interface.
    '''
    def run(self):
        raise Exception("This method must be overwritten")

    def __init__(self, run_method):
        '''
        Constructor
        '''
        self.run = run_method
        
if __name__ == "__main__":
    
    def run_method():
        print "Hello world"
    
    r = Runnable(run_method)
    r.run()