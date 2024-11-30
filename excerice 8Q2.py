# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:12:07 2024

@author: ninas
"""
"""
def problem2(string, type_of_collection='list'):
    '''
    (str, str)->collection
    >>>problem2('hello')
    ['h', 'e', 'l', 'l', 'o']
    >>>problem2('hello','tuple')
    ('h', 'e', 'l', 'l', 'o')
    >>>problem2('hello','tup')
    None
    '''
    if type(string) != str:
        return None#NM: If it is an int or float the function returns none.
    if type_of_collection != 'list' and type_of_collection != 'tuple' and type_of_collection != 'set':
        return None #NM: If it is neither list, tuple, set the function returns none.
    if type_of_collection == 'list':
        return list(string)
    elif type_of_collection == 'tuple':
        return tuple(string)
    elif type_of_collection == 'set':
        return set(string)
print(problem2("hello"))  # Default: returns a list ['h', 'e', 'l', 'l', 'o']
print(problem2("hello", "tuple"))  # Returns a tuple ('h', 'e', 'l', 'l', 'o')
print(problem2("hello", "set"))  # Returns a set {'h', 'e', 'l', 'o'}
print(problem2("hello", "dict"))  # Invalid input, returns None
print(problem2(12345))  # Invalid input, returns None
"""

"""def problem3(classes_student_1, classes_student_2):
    '''
    (set,set)-> tuple
    >>>problem3({'ME100','CHE102','MATH115','MATH116','PHYS115'},{'CHE100','CHE102','CHE120','CHE180','MATH115','MATH116'})
    (True, ['CHE102','MATH115','MATH116'])
    >>>problem3({'NE100','NE109','NE111','NE121','MATH117'},{'CHE100','CHE102','CHE120','CHE180','MATH115','MATH116'})
    False
    >>>problem3({1,2,3,4,5,6},{'CHE100','CHE102','CHE120','CHE180','MATH115','MATH116'})
    None
    >>>problem3(['NE100','NE109','NE111','NE121','MATH117'],{'CHE100','CHE102','CHE120','CHE180','MATH115','MATH116'})
    None
    '''

    if type(classes_student_1) != set:
        return None
    if type(classes_student_2) != set:
        return None 
    for clz in classes_student_1:
        if type(clz) != str:
            return None
    for clz in classes_student_2:
        if type(clz) != str:
            return None
    shared_classes = set()
    for clz in classes_student_1:
        if clz in classes_student_2:
            shared_classes.add(clz)

    # Determine output
    if shared_classes:
        return True, sorted(shared_classes)
    else:
        return False """
    
def problem4(music_dictionary):
    '''
    (dict) -> dict
    Returns a dictionary with the bands as keys and the number of students liking those bands as values.
    
    >>> problem4({'PM': ['Metallica', 'The Cranberries', 'Hozier'], 
                  'AS': ['MONO', 'Metallica', 'Alcest']})
    {'Metallica': 2, 'The Cranberries': 1, 'Hozier': 1, 'MONO': 1, 'Alcest': 1}

    >>> problem4({'PM': ['Metallica'], 
                  'AS': ['Metallica'], 
                  'JK': ['The Cranberries', 'Hozier']})
    {'Metallica': 2, 'The Cranberries': 1, 'Hozier': 1}

    >>> problem4({'PM': ['Metallica', 'The Cranberries'], 
                  'AS': ['The Cranberries', 'Alcest'], 
                  'JK': ['Alcest']})
    {'Metallica': 1, 'The Cranberries': 2, 'Alcest': 2}

    >>> problem4({})
    {}
    '''
"""
    if type(music_dictionary) != dict:
        return None
    band_counts = {}
    for bands in music_dictionary.values():
        if type(bands) != list:
            return None
        for band in bands:
            if band in band_counts:
                band_counts[band] += 1
            else:
                band_counts[band] = 1

    return band_counts

# Examples
print(problem4({'PM': ['Metallica', 'The Cranberries', 'Hozier'], 
                'AS': ['MONO', 'Metallica', 'Alcest']}))  
# Output: {'Metallica': 2, 'The Cranberries': 1, 'Hozier': 1, 'MONO': 1, 'Alcest': 1}

print(problem4({'PM': ['Metallica'], 
                'AS': ['Metallica'], 
                'JK': ['The Cranberries', 'Hozier']}))  
# Output: {'Metallica': 2, 'The Cranberries': 1, 'Hozier': 1}

print(problem4({'PM': ['Metallica', 'The Cranberries'], 
                'AS': ['The Cranberries', 'Alcest'], 
                'JK': ['Alcest']}))  
# Output: {'Metallica': 1, 'The Cranberries': 2, 'Alcest': 2}

print(problem4({}))  
# Output: {}
"""
import time

def problem5(item, collection):
    '''
    (object, collection) -> float
    Returns the time in seconds that the 'in' operator takes to check if 'item' is in 'collection'.
    
    >>> problem5('a', 'apple')
    <some small float value>   # The time it takes to check if 'a' is in the string 'apple'
    
    >>> problem5(3, [1, 2, 3, 4])
    <some small float value>   # The time it takes to check if 3 is in the list [1, 2, 3, 4]
    
    >>> problem5('Metallica', {'PM': ['Metallica', 'The Cranberries'], 'AS': ['MONO', 'Metallica']})
    <some small float value>   # The time it takes to check if 'Metallica' is in the values of the dictionary
    '''

    # Check if the collection type is valid
    if type(collection) != str and type(collection) != tuple and type(collection) != list and type(collection) != set and type(collection) != dict:
        return None

    # Start the timer
    start_time = time.perf_counter()

    # Perform the 'in' check based on the collection type
    if type(collection) == str or type(collection) == tuple or type(collection) == list or type(collection) == set:
        item_in_collection = item in collection
    elif type(collection) == dict:
        item_in_collection = item in collection.values()

    # End the timer
    end_time = time.perf_counter()

    # Return the time it took for the 'in' operation
    return end_time - start_time

# Examples
print(problem5('a', 'apple'))  # Timing the 'in' operator for string
print(problem5(3, [1, 2, 3, 4]))  # Timing the 'in' operator for list
print(problem5('Metallica', {'PM': ['Metallica', 'The Cranberries'], 'AS': ['MONO', 'Metallica']}))  # Timing the 'in' operator for dictionary values