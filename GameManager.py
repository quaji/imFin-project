import sys
import pygame
import numpy as np
from Camera import *
from Frame import *
from Fish import *
from StringsBlock import *
from ChineseEel import *
import random, time

class GameManager:
    def __init__(self):
        self.size = 1.0
        self.camera = Camera(position=np.array([0.,0.4,0.]), lookat=np.array([0.,0.,1.]))
        self.frame = Frame(position=np.array([0.,0.,1.]), vertical_segment=30, horizontal_segment=30, vertical_size=self.size, horizontal_size=self.size)
        self.fish = Fish(position=np.array([0.,0.3,1.]), velocity=np.array([0.001,0.,0.]),segment=10,color=(255,255,0),orientation=deg2quat(90, np.array([0.,1.,0.])))
        self.eels = []
        self.strings = []
        self.strings.append(StringsBlock(strings="Test mode", position=np.array([-0.95,-0.8]), font_size=0.05, color=(255,255,255)))
        self.iter_count:int = 100
        self.flag = False
        
        
    def add_eel(self, position, velocity=0.004, radius=0.01, length=0.4, color=(0,0,255)):
        eel = ChineseEel(position=position, velocity=velocity, radius=radius, length=length, color=color)
        self.eels.append(eel)
        
    def add_string(self, string, position, font_size=0.05, color=(255,255,255)):
        string_block = StringsBlock(strings=string, position=position, font_size=font_size, color=color)
        self.strings.append(string_block)
        
    def update(self, key_input, key_vel, buf, scrcentr, scale):
        self.camera.setViewMatrix()
        VM = self.camera.ViewMatrix()
        PPM = self.camera.PPMatrix()
        
        if key_input is not None:
            self.iter_count -= 1
            random.seed(time.time())
            if self.iter_count < 50 :
                self.iter_count = 50
            if random.randint(0, self.iter_count) <= 1:
                self.add_eel(position = np.array([random.uniform(-self.size/2+self.frame.position[1], self.size/2+self.frame.position[1]),random.uniform(-self.size/2+self.frame.position[3], self.size/2+self.frame.position[3])]),velocity = random.uniform(0.002, 0.01), radius = random.uniform(0.008, 0.015)*10*0.5, length = random.uniform(0.2, 0.4))
        else:
            self.iter_count = 200
            
        key = pygame.key.get_pressed()
        self.fish.update(key_input=key, key_vel=key_vel)
        for eel in self.eels:
            f = eel.update()
            if f:
                del eel
                
        for eel in self.eels:
            self.flag = self.flag or self.fish.death_judge(eel.get_position(), eel.get_radius())

        if self.flag:
            self.springs = []
            self.strings.append(StringsBlock(strings="Game Over", position=np.array([-0.4,0.05]), font_size=0.1, color=(0,105,0)))
        else:
            self.frame.display(buf, VM, PPM, scrcentr, scale)
            self.fish.display(buf, VM, PPM, scrcentr, scale)
            for eel in self.eels:
                eel.display(buf, VM, PPM, scrcentr, scale)
        for string in self.strings:
            string.display(buf, scrcentr, scale)
            
        
        
        
        # camera.input(pygame.key.get_pressed(), Key_vel, True)