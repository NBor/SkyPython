'''
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
