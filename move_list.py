# -*- coding: utf-8 -*-
"""
@author: Nina Mathew 
ID: 21127380
Created on Fri Nov 22 21:46:16 2024

"""
"""
a_list  is the original List
n is an integer that defines  how many indicies the list moves.
"""

def move_list(a_list, n):
    if type(a_list) != list:
        return None
    if type(n) != int:
        return None
    #for n in new_list:        
    new_list = list(a_list)  # Create a copy of the input list
    for num in range(len(a_list)):
        index = (num + n) % len(a_list)
        new_list[index] = a_list[num]

    return new_list

      
        
print(move_list([1,2,3,4,5], -3))

'''if num + n < len(a_list):
    new_list[num+n] = a_list[num]
elif  num + n > len(a_list):
    new_list[num - n -1 ] = a_list[num]
    new_list[num+n] = a_list[num]'''
'''new_list = list(a_list)
    for num in range(len(a_list)):
        index = num + (n)
        if (index >= len(a_list)):
            index = index % len(a_list)
            new_list[index] = a_list[num]
            return new_list
        elif (index < len(a_list)):
            index = num - n
            index = index % len(a_list)
            new_list[index] = a_list[num]
            return new_list'''
        