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


Created on 2013-05-20

@author: Neil Borle
'''
import sys

handle = open(sys.argv[1], 'r')
handle2 = open(sys.argv[2], 'w')


for line in handle.readlines():
	'''
	used for parsing color xml file from 
	http://stackoverflow.com/questions/3769762/android-color-xml-resource-file
	'''
	split_line = line.split('"')
	color_code_int = split_line[2].split('<')[0]
	color_code = color_code_int.split('#')[1]
	print split_line[1].upper() + "=" + color_code +", \\"
	handle2.write(split_line[1].upper() + "=0x" + color_code +", \\" + "\n")

handle.close()
handle2.close()
