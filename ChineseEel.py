import numpy as np
import pygame
from quaternions import *
from object_module import solid2plane, get_circle
#チンアナゴクラス(敵)
class ChineseEel:
    def __init__(self, position = None, velocity = 0.004, radius = 0.01, length = 0.4, color = (200, 200, 0)):
        self.position = np.concatenate([[0.],[position[0]],[0.],[position[1]]])
        self.color = color
        self.radius = radius
        self.length = length
        self.velocity = velocity
        
        
    def display(self, buf, V, PPM, scrcentr, scale):
        if self.position[2]<0:
            return
        elif self.position[2] < self.radius*2:
            tmp = [np.array([0.,self.position[2]*0.5,0.,0.]),np.array([0.,-self.position[2]*0.5,0.,0.]),np.array([0.,0.,0.,self.position[2]*0.5]),np.array([0.,0.,0.,-self.position[2]*0.5])]
            for i in range(4):
                p1 = self.position
                p2 = self.position + tmp[i] - self.position[2]*np.array([0.,0.,1.,0.])
                p1 = PPM @ V @ np.concatenate([p1[1:4], [1.]])
                p2 = PPM @ V @ np.concatenate([p2[1:4], [1.]])
                line_points = solid2plane(p1, p2)
                if line_points is not None:
                    p1 = line_points[0][0:2]/line_points[0][3]
                    p1 = scale * p1 + scrcentr
                    p2 = line_points[1][0:2]/line_points[1][3]
                    p2 = scale * p2 + scrcentr
                    pygame.draw.line(buf, self.color, p1, p2, 2)
            circle_points = get_circle(self.radius, 20)
            for i in range(len(circle_points)):
                p1 = self.position + circle_points[i] - self.position[2]*np.array([0.,0.,1.,0.])
                p2 = self.position + circle_points[(i+1)%len(circle_points)] - self.position[2]*np.array([0.,0.,1.,0.])
                p1 = PPM @ V @ np.concatenate([p1[1:4], [1.]])
                p2 = PPM @ V @ np.concatenate([p2[1:4], [1.]])
                line_points = solid2plane(p1, p2)
                if line_points is not None:
                    p1 = line_points[0][0:2]/line_points[0][3]
                    p1 = scale * p1 + scrcentr
                    p2 = line_points[1][0:2]/line_points[1][3]
                    p2 = scale * p2 + scrcentr
                    pygame.draw.line(buf, self.color, p1, p2, 2)
        else:
            tmp = [np.array([0.,self.radius,0.,0.]),np.array([0.,-self.radius,0.,0.]),np.array([0.,0.,0.,self.radius]),np.array([0.,0.,0.,-self.radius])]
            for i in range(4):
                p1 = self.position
                p2 = self.position + tmp[i] - 2*self.radius*np.array([0.,0.,1.,0.])
                p3 = p2.copy()
                p3[2] = 0.
                p1 = PPM @ V @ np.concatenate([p1[1:4], [1.]])
                p2 = PPM @ V @ np.concatenate([p2[1:4], [1.]])
                p4 = p2.copy()
                p3 = PPM @ V @ np.concatenate([p3[1:4], [1.]])
                line_points = solid2plane(p1, p2)
                if line_points is not None:
                    p1 = line_points[0][0:2]/line_points[0][3]
                    p1 = scale * p1 + scrcentr
                    p2 = line_points[1][0:2]/line_points[1][3]
                    p2 = scale * p2 + scrcentr
                    pygame.draw.line(buf, self.color, p1, p2, 2)
                line_points = solid2plane(p3, p4)
                if line_points is not None:
                    p3 = line_points[0][0:2]/line_points[0][3]
                    p3 = scale * p3 + scrcentr
                    p4 = line_points[1][0:2]/line_points[1][3]
                    p4 = scale * p4 + scrcentr
                    pygame.draw.line(buf, self.color, p3, p4, 2)
            circle_points = get_circle(self.radius, 20)
            circle_points = circle_points + self.position - 2*self.radius*np.array([0.,0.,1.,0.])
            while circle_points[0][2] > 0:
                for i in range(len(circle_points)):
                    p1 = circle_points[i]
                    p2 = circle_points[(i+1)%len(circle_points)]
                    p1 = PPM @ V @ np.concatenate([p1[1:4], [1.]])
                    p2 = PPM @ V @ np.concatenate([p2[1:4], [1.]])
                    line_points = solid2plane(p1, p2)
                    if line_points is not None:
                        p1 = line_points[0][0:2]/line_points[0][3]
                        p1 = scale * p1 + scrcentr
                        p2 = line_points[1][0:2]/line_points[1][3]
                        p2 = scale * p2 + scrcentr
                        pygame.draw.line(buf, self.color, p1, p2, 2)
                circle_points = circle_points - np.array([0.,0.,0.02,0.])
            
            for i in range(len(circle_points)):
                circle_points[i][2] = max(circle_points[i][2], 0.)
            for i in range(len(circle_points)):
                p1 = circle_points[i]
                p2 = circle_points[(i+1)%len(circle_points)]
                p1 = PPM @ V @ np.concatenate([p1[1:4], [1.]])
                p2 = PPM @ V @ np.concatenate([p2[1:4], [1.]])
                line_points = solid2plane(p1, p2)
                if line_points is not None:
                    p1 = line_points[0][0:2]/line_points[0][3]
                    p1 = scale * p1 + scrcentr
                    p2 = line_points[1][0:2]/line_points[1][3]
                    p2 = scale * p2 + scrcentr
                    pygame.draw.line(buf, self.color, p1, p2, 2)
            
    def update(self):
        self.position[2] += self.velocity
        if self.position[2] > self.length:
            self.velocity *= -1
        if self.position[2] < -1e-3:
            return True
        return False
    
    def get_position(self):
        return self.position
    
    def get_radius(self):
        return self.radius