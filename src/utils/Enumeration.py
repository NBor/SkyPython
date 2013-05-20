'''
Created on 2013-05-20

@author: Neil
'''

def enum(**enums):
    return type('Enum', (), enums)

