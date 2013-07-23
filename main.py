'''
Created on 2013-05-14

@author: Neil
'''

import sys
from src.skypython.SkyPython import start_application

if __name__ == '__main__':
    
    if len(sys.argv) == 2 and sys.argv[1] == '-d':
        start_application(mode='Debug')
    else:
        start_application()
    
    