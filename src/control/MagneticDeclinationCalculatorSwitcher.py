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
// Original Author: John Taylor
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


Created on 2013-06-28

@author: Neil Borle
'''

from ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator
from RealMagneticDeclinationCalculator import RealMagneticDeclinationCalculator

class MagneticDeclinationCalculatorSwitcher(object):
    '''
    Aggregates the RealMagneticDeclinationCalculator and the
    ZeroMagneticDeclinationCalculator and switches them in the AstronomerModel.
    '''
    def set_the_models_calculator(self, use_real):
        if use_real:
            self.model.set_mag_dec_calc(self.real_calculator)
        else:
            self.model.set_mag_dec_calc(self.zero_calculator)

    def __init__(self, model, use_real=False):
        '''
        Constructor
        '''
        self.zero_calculator = ZeroMagneticDeclinationCalculator()
        self.real_calculator = RealMagneticDeclinationCalculator()
        self.model = model
        self.set_the_models_calculator(use_real)
        