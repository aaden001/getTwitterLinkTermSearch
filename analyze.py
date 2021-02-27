# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:44:02 2021

@author: adeni
"""
import pandas as pd
import json
from json.decoder import JSONDecodeError
from collections import OrderedDict
letCount = {}
count = 1
previous =0
MAX_MOMENTOUS = []

for x in range(1000):
    #configure file ordering
    file = "json/"+ str(count) + ".json"
    try:
        with open(file, "rb") as f:
           #load file in a variable
           data = json.load(f)
           if(letCount.get(len(data['mementos']['list'])) != None):
               #get length mememto and increase count of see same number of memento by one
               previous =  len(data['mementos']['list'])
               letCount[len(data['mementos']['list'])]=letCount.get(len(data['mementos']['list'])) + 1
           else:
               #get length of memento and store a new number of mementos found
               letCount[len(data['mementos']['list'])] = 1
               previous =  len(data['mementos']['list'])
           #Gets the highest 10000 mementos urls     
           if(previous> 10000):
                #saved in a list
                MAX_MOMENTOUS.append(data['original_uri'])
    except JSONDecodeError  as e:
        #Takes care of error file therefore giving it a 0 mememtos 
        if(letCount.get(0) != None):
            #increments by one when more errors zero mememtos are found
            letCount[0] = letCount.get(0) +1
        else:
            #store new error as a zero key with 1 value
            letCount[0] = 1
    #change to a new file number
    count = count +1
#sort and store
dict1 = OrderedDict(sorted(letCount.items()))

[print(key,':',value) for key,value in dict1.items()]
print("\n\n")
print(len(MAX_MOMENTOUS))

