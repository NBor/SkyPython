'''
Created on 2013-07-26

@author: Alyson Wu and Morgan Redshaw
'''

# Equivalent of the Java programs EqualsTester

class smallClass:
    value = 0
    
    def equals(self, other):
        return self.value == other.value
    
def EqualsTester():
    '''
    >>> groups = [[smallClass for i in range(5)] for x in range(3)]
    
    # Test equals
    >>> allCorrect = True
    
    >>> for group in groups:
    ...    for obj1 in group:
    ...        allCorrect = (obj1 == obj1) & allCorrect
    ...        
    ...        for obj2 in group:
    ...            if obj1 != obj2:
    ...                allCorrect = obj1.equals(obj2) & allCorrect
    
    >>> allCorrect
    True
    
    >>> allCorrect = True
    
    >>> for group1 in groups:
    ...    for group2 in groups:
    ...        if group1 != group2:
    ...            for obj1 in group1:
    ...                for obj2 in group2:
    ...                    allCorrect = (not obj1.equals(obj2)) & allCorrect
    
    >>> allCorrect
    True
    '''
    pass