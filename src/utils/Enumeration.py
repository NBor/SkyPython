'''
Created on 2013-05-20

@author: Neil Borle
'''

def enum(**enums):
    '''
    implementation of an enum
    '''
    return type('Enum', (), enums)

