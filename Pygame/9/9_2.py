# -*- coding: cp936 -*-
from gameobjects.vector2 import *
A = Vector2(10.0, 20.0)
B = Vector2(30.0, 35.0)
AB = Vector2.from_points(A, B)
print "Vector AB is", AB
print "AB * 2 is", AB * 2
print "AB / 2 is", AB / 2
print "AB + (-10, 5) is", AB + Vector2(-10, 5)
print "AB - (-10, 5) is", AB - Vector2(-10, 5)
print "Magnitude of AB is", AB.get_magnitude()
print "AB normalized is", AB.get_normalized()

 
# 结果是下面
# Vector AB is (20.0, 15.0)
# AB * 2 is (40.0, 30.0)
# AB / 2 is (10.0, 7.5)
# AB + (-10, 5) is (10.0, 20.0)
# AB - (-10, 5) is (30.0, 10.0)
# Magnitude of AB is 25.0
# AB normalized is (0.8, 0.6)
