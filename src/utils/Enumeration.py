'''
Created on 2013-05-20

@author: Neil Borle
'''

def enum(**enums):
    return type('Enum', (), enums)

