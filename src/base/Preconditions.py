'''
Created on 2013-05-20

@author: Neil

Functions for asserting that parameters or other variables equal
specific values.
'''

def check(boolean_value):
    '''
    Ensures that the given boolean state is true. If false, throws a
    PreconditionException with a generic error message.
    '''
    if not boolean_value:
        raise Exception("Unexpected State Encountered")
    
def check_not_none(input_val):
    '''
    Ensures that the given reference is not None.
    '''
    if input_val == None:
        raise Exception("Expected non-None, but got None.")

def check_not_empty(in_string):
    '''
    Ensures that the specified String is not None, or equal to the empty string
    ("") after all whitespace characters have been removed.
    '''
    if (in_string == None) or "".join(in_string.split()) == "":
        raise Exception("Observed string was empty")

def check_equal(observed, expected):
    '''
    Ensures that the two specified objects are (object) equal. This will not
    throw a Precondition check if two objects are ".equals", but not "==". If
    you want to test "==" equals, use checkSame.
    '''
    if observed != expected:
        raise Exception("inputs are not the same")

def check_not_equal(observed, expected):
    '''
    Ensures that the two specified objects are not equals (either "==" or
    ".equals").
    '''
    if observed == expected:
        raise Exception("expected inputs to be different")

def check_between(value, minimum, maximum):
    '''
    Ensures that the given value is between the min and max values (inclusive).
    That is, min <= value <= max
    '''
    if (value < minimum) or (value > maximum):
        raise Exception("value is not in expected range")
    
if __name__ == "__main__":
    '''
    Run Checks
    '''
    check(False)