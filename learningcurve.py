# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 22:21:51 2019
Python3.7
@author: JeffLai @ UC Davis
"""
# importing the required module
import matplotlib.pyplot as plt

# x axis values
x = [5000,10000,15000,20000,
     25000,30000,35000,40000]
# corresponding y axis values
# error rate by word
y = [0.108258344342797,0.0814367973676995,
     0.0702943889124311,0.0655831692300023,
     0.0612707829598425,0.0571827404840841,
     0.0559862402472767,0.0540917815389984]
# error rate by sentence
s = [0.8,0.749411764705882,
	0.727058823529412,0.703529411764706,
	0.69,0.667647058823529,
	0.659411764705882,0.655882352941176]

# plotting the points
word = plt.plot(x,y,label='Error rate by word')
plt.legend()
sentence = plt.plot(x,s,label='Error rate by sentence')
plt.legend()

# naming the x axis
plt.xlabel('training dataset size')
plt.ylabel('error rate')
plt.title('Learning Curve')
plt.show()
