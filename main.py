'''
Created on 2013-05-14

@author: Neil
'''

import sys
from src.skypython.SkyPython import start_application
from src.utils.DebugOptions import Debug, debug_opts

if __name__ == '__main__':
    
    if '-d' in sys.argv:
        start_application(mode='Debug')
    else:
        start_application()
    
    