import numpy as np
import pygame
from quaternions import *
from object_module import solid2plane

class Fish:
    def __init__(self, position = None, velocity = None, color = (0, 0, 255), size = 0.1, segment = 2, orientation = np.array([1., 0., 0., 0.])):
        self.position = np.concatenate([[0.],position])
        self.color = color
        self.size = size
        self.segment = segment
        self.segments = [np.array([0,0,0,size*_/segment-size/2]) for _ in range(segment)]
        self.display_segments = [np.array([0,0,0,size*_/segment-size/2]) for _ in range(segment)]
        # self.segments = [np.array([0.,0.,0.,0.2]),np.array([0.,0.,0.,-0.2])]
        self.quaternion = orientation
        self.velocity = (self.segments[0]-self.segments[-1])/np.linalg.norm(self.segments[0]-self.segments[-1])*np.linalg.norm(velocity) if np.linalg.norm(velocity) > 0 else np.array([0.,0.,0.,0.])

    def display(self, buf, V, PPM, scrcentr, scale):
        for i in range(self.segment-1):
            p1 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[i]), inverse_quaternion(self.quaternion))
            p2 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[i+1]), inverse_quaternion(self.quaternion))
            p1 = PPM @ V @ np.concatenate([(p1+self.position)[1:4], [1.]])
            p2 = PPM @ V @ np.concatenate([(p2+self.position)[1:4], [1.]])
            line_points = solid2plane(p1, p2)
            if line_points is not None:
                p1 = line_points[0][0:2]/line_points[0][3]
                p1 = scale * p1 + scrcentr
                p2 = line_points[1][0:2]/line_points[1][3]
                p2 = scale * p2 + scrcentr
                pygame.draw.line(buf, self.color, p1, p2, 2)
            self.display_landmark(buf, V, PPM, scrcentr, scale)
    
    def display_landmark(self,buf,V,PPM,scrcentr,scale,color=(255,0,0)):
        
        p1 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[0]), inverse_quaternion(self.quaternion))
        p2 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[1]+np.array([0.,0.,self.size/5,0.])), inverse_quaternion(self.quaternion))
        p1 = PPM @ V @ np.concatenate([(p1+self.position)[1:4], [1.]])
        p2 = PPM @ V @ np.concatenate([(p2+self.position)[1:4], [1.]])
        line_points = solid2plane(p1, p2)
        if line_points is not None:
            p1 = line_points[0][0:2]/line_points[0][3]
            p1 = scale * p1 + scrcentr
            p2 = line_points[1][0:2]/line_points[1][3]
            p2 = scale * p2 + scrcentr
            pygame.draw.line(buf, 
                             color, p1, p2, 2)
            
    def update(self,key_input=None, key_vel=0.0):
        v1 = self.velocity
        if key_input is not None and key_vel > 0.0:
            v1 = self.input(key_input, key_vel)
            
        v1 = mult_quaternion(mult_quaternion(self.quaternion, v1), inverse_quaternion(self.quaternion))
        self.position += v1
        if self.segment >= 2:
            temp = np.linalg.norm(self.velocity)
            self.velocity = self.segments[0]-self.segments[-1]
            self.velocity = self.velocity/np.linalg.norm(self.velocity)*temp
    
    def input(self, key_input, key_vel):
        leng = np.linalg.norm(self.segments[0]-self.segments[-1])
        if key_input[pygame.K_SPACE]:
            v_local = self.velocity * 2
        else:
            v_local = self.velocity
            
        if key_input[pygame.K_w]:
            self.quaternion = mult_quaternion(self.quaternion, np.array([np.cos(key_vel/2), np.sin(key_vel/2), 0., 0.]))
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_] - np.array([0.,0.,key_vel*leng*(np.sin(_*np.pi/self.segment) - 0.5), 0.])*10
        if key_input[pygame.K_s]:
            self.quaternion = mult_quaternion(self.quaternion, np.array([np.cos(-key_vel/2), np.sin(-key_vel/2), 0., 0.]))
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_] + np.array([0.,0.,key_vel*leng*(np.sin(_*np.pi/self.segment) - 0.5), 0.])*10
        if key_input[pygame.K_a]:
            self.quaternion = mult_quaternion(self.quaternion, np.array([np.cos(-key_vel/2), 0., np.sin(-key_vel/2), 0.]))
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_] - np.array([0.,key_vel*leng*(np.sin(_*np.pi/self.segment) - 0.5), 0.,0.])*10
        if key_input[pygame.K_d]:
            self.quaternion = mult_quaternion(self.quaternion, np.array([np.cos(key_vel/2), 0., np.sin(key_vel/2), 0.]))
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_] + np.array([0.,key_vel*leng*(np.sin(_*np.pi/self.segment) - 0.5), 0.,0.])*10
        if not key_input[pygame.K_w] and not key_input[pygame.K_s] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_]
                
        return v_local
    
    def print_info(self):
        print("Position:\t", self.position)
        print("Velocity:\t", self.velocity)
        print("Color:\t", self.color)
        print("Size:\t", self.size)
        print("Segment:\t", self.segment)
        print("Segments:\t", self.segments)
        
if __name__ == "__main__":
    fish = Fish()
    fish.print_info()