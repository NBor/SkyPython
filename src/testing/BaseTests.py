'''
// Copyright 2009 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// 
// Original Author: Brent Bryan
// 
// Notification of Change: The original java source code has been
// modified in that it has been rewritten in the python programming
// language and additionally, may contain components and ideas that are 
// not found in the original source code.


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
