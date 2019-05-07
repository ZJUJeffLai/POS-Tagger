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
y = [0.108258344342797,0.0814367973676995,
     0.0702943889124311,0.0655831692300023,
     0.0612707829598425,0.0571827404840841,
     0.0559862402472767,0.0540917815389984]

# plotting the points
plt.plot(x,y)

# naming the x axis
plt.xlabel('training dataset size')
plt.ylabel('error rate')
plt.title('Learning Curve')
plt.show()
