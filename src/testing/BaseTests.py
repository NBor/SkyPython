'''
Created on 2013-07-23

@author: Alyson Wu and Morgan Redshaw
'''

# PreconditionsTest

def testTestCheck():
    '''
    >>> from src.base.Preconditions import check
    >>> check(True)
    >>> check(False) 
    Traceback (most recent call last):
    ...
    Exception: Unexpected State Encountered
    '''
    pass

def testCheckNotNull():
    '''
    >>> from src.base.Preconditions import check_not_none
    >>> check_not_none('this')
    >>> check_not_none(None)
    Traceback (most recent call last):
    ...
    Exception: Expected non-None, but got None.
    '''
    pass

def testCheckNotEmpty():
    '''
    >>> from src.base.Preconditions import check_not_empty
    >>> check_not_empty('foo')
    >>> testStrings = [None, "", "  ", "\t"]
    >>> for strings in testStrings:
    ...     check_not_empty(strings)
    Traceback (most recent call last):
    ...
    Exception: Observed string was empty
    '''
    pass

def testCheckEqual():
    '''
    >>> from src.base.Preconditions import check_equal
    >>> check_equal(None, None)
    >>> check_equal("foo", "foo")
    >>> testInputOne = [None, "foo", "bar"]
    >>> testInputTwo = ["foo", None, "foo"]
    >>> for i in testInputOne and testInputTwo:
    ...     i = 0
    ...     s1 = testInputOne[i]
    ...     s2 = testInputTwo[i]
    ...     check_equal(s1, s2)
    ...     i += 1
    Traceback (most recent call last):
    ...
    Exception: inputs are not the same
    '''
    pass

def testCheckNotEqual():
    '''
    >>> from src.base.Preconditions import check_not_equal
    >>> check_not_equal(None, "foo")
    >>> check_not_equal("foo", None)
    >>> check_not_equal("foo", "bar")
    >>> s = "foo"
    >>> check_not_equal(s,s)
    Traceback (most recent call last):
    ...
    Exception: expected inputs to be different
    >>> check_not_equal([], [])
    Traceback (most recent call last):
    ...
    Exception: expected inputs to be different
    '''
    pass

def testCheckBetween():
    '''
    >>> from src.base.Preconditions import check_between
    >>> check_between(3, 2, 4)
    >>> check_between(2, 2, 4)
    >>> check_between(4, 2, 4)
    >>> check_between(1, 2, 4)
    Traceback (most recent call last):
    ...
    Exception: value is not in expected range
    >>> check_between(5, 2, 4)
    Traceback (most recent call last):
    ...
    Exception: value is not in expected range
    '''
    pass
