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
// Original Author: Brent Bryan
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


Created on 2013-05-20

@author: Neil Borle

These constants are used in calculations, ex. movement of planets.
'''

MILLISECONDS_PER_SECOND =    1000
MILLISECONDS_PER_MINUTE =   60000
MILLISECONDS_PER_HOUR =   3600000
MILLISECONDS_PER_DAY =   86400000
MILLISECONDS_PER_WEEK = 604800000
SECONDS_PER_SECOND = 1
SECONDS_PER_MINUTE = 60
SECONDS_PER_10MINUTE = 600
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR
SECONDS_PER_WEEK = 7 * SECONDS_PER_DAY
SECONDS_PER_SIDEREAL_DAY = 86164.0905
MILLISECONDS_PER_SIDEREAL_DAY = MILLISECONDS_PER_SECOND * SECONDS_PER_SIDEREAL_DAY
SECONDS_PER_SIDERIAL_WEEK = 7 * 86164.0905