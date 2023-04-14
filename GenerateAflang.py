import math
import sys

"""
Spiral generator.
Inputs:
Radius - maximum radius of the spiral from the center.
  Defines the distance of the tail end from the center.
Step - amount the current radius increases between each point.
  Larger = spiral expands faster
Resolution - distance between 2 points on the curve.
  Defines amount radius rotates between each point.
  Larger = smoother curves, more points, longer time to calculate.
Angle - starting angle the pointer starts at on the interior
Start - starting distance the radius is from the center.
"""


print(spiral(100, 1))