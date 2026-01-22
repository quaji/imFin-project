import numpy as np
import pygame
from quaternions import *
from object_module import solid2plane, get_circle

class Feed:
    def __init__(self, XZposition = None, radius = 0.02, color = (255, 0, 0)):
        self.position = np.concatenate([[0.],[XZposition[0]],[0.],[XZposition[1]]])
        self.color = color
        self.radius = radius
        self.velocity = np.zeros(4)
        