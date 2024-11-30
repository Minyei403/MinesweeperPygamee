#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:37:21 2024

@author: varvaralitvinova
"""

def problem2(string, type_of_collection='list'):
    if type(string) != str:
        return None
    else:
        new_list=list(string)
        print(new_list)
    
    
def problem3(classes_student_1, classes_student_2):
    if type(classes_student_1) != set or type(classes_student_2) != set or type(set(classes_student_1)) != str or type(set(classes_student_2)) != str :
        return None
    else:
        type(classes_student_1) == tuple and type(classes_student_2) == tuple
        for i in classes_student_1 and classes_student_2:
            if classes_student_1.intersection(classes_student_2) != 0:
                same_courses = list(classes_student_1.intersection(classes_student_2))
                return (True,same_courses)
            else:
                return False
        
def problem4(music_dictionary):
    if type(music_dictionary) != dict:
        return None
    else: 
        type(music_dictionary) == set()
        same_songs = str(music_dictionary.intersection(music_dictionary))
        values = 
        new_dictionary ={'same_songs': values}
        return new_dictionary  


def problem5(item, collection):
 
t1 = time.perf_counter()
    find_func(lst)
    t2 = time.perf_counter()
    
    return (t2 - t1)  