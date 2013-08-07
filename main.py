'''
Created on 2013-05-14

@author: Neil
'''

import sys
from src.skypython.SkyPython import start_application

def run_all_tests():
    '''
    Created on 2013-07-23
    
    @author: Morgan Redshaw
    '''
    
    print "Running all."
    import doctest
    
    import src.testing.UnitsTesting as UnitsTesting
    doctest.testmod(UnitsTesting)    
    
    import src.testing.UtilsTesting as UtilsTesting
    doctest.testmod(UtilsTesting)
    
    import src.testing.SanityChecks as SanityChecks
    doctest.testmod(SanityChecks)
    
    import src.testing.ControlTests as ControlTests
    doctest.testmod(ControlTests)
    
    import src.testing.ProviderTests as ProviderTests
    doctest.testmod(ProviderTests)
    
    import src.testing.BaseTests as BaseTests
    doctest.testmod(BaseTests)
    
    print "Completed."
    

if __name__ == '__main__':
    
    if '-d' in sys.argv and 'images' in sys.argv:
        run_all_tests()
        start_application(mode='Debug')
    elif '-d' in sys.argv:
        run_all_tests()
    else:
        start_application()
    
