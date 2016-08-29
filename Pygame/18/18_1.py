from gameobjects.vector3 import *

A = (-6, 2, 2)
B = (7, 5, 10)
plasma_speed = 100.
AB = Vector3.from_points(A, B)
print "Vector to droid is ", AB
distance_to_target = AB.get_magnitude()
print "Distance to droid is ", distance_to_target, "meters"
plasma_heading = AB.get_normalised()
print "heading is ", plasma_heading


def perspective_project(vector3, d):
    x, y, z = vector3
    return (x * d/z, ¨Cy * d/z)

from math import tan


def calculate_viewing_distance(fov, screen_width):
    d = (screen_width/2.0) / tan(fov/2.0)
    return d