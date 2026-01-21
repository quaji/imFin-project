import numpy as np
from quaternions import *
import pygame


class Camera:
    # コンストラクタ
    def __init__ (self, position=np.array([0.,0.,0.]), lookat=np.array([0.,0.,1.]),top=1, bottom=-1, left=-1, right=1, near=1.0):
        self.position = position
        self.lookat = lookat
        self.orientation = np.array([1., 0., 0., 0.])
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.near = near
        self.setPPMatrix()
        


    # perspective projection matrix 設定
    def setPPMatrix(self):
        self.PPM = np.array([[2*self.near/(self.left-self.right), 0, (self.right + self.left)/(self.left-self.right), 0],
                            [0, 2*self.near/(self.top - self.bottom), (self.top + self.bottom)/(self.top - self.bottom), 0],
                            [0, 0, - 1, -2*self.near],
                            [0, 0, -1, 0]])
        
    def ViewMatrix(self):
        f = (self.lookat - self.position)/np.linalg.norm(self.lookat - self.position)
        s = np.cross(f, np.array([0,1,0]))
        u = np.cross(s, f)
        # カメラ座標系変換行列の作成
        return np.array([[s[0], s[1], s[2], -np.dot(s, self.position)],
                      [u[0], u[1], u[2], -np.dot(u, self.position)],    
                      [-f[0], -f[1], -f[2], np.dot(f, self.position)],
                      [0, 0, 0, 1]])

    # クォータニオン回転
    # 引数
    # axis:回転軸ベクトル
    # angle:回転角度(ラジアン)
    def quaternion_rotate(self, axis, angle):
        q = np.concatenate([[np.cos(angle/2)], axis/np.linalg.norm(axis)*np.sin(angle/2)])
        q_inv = inverse_quaternion(q)
        # p = np.concatenate([[0.], self.position])
        p = np.concatenate([[0.], self.lookat])
        p_rot = mult_quaternion(mult_quaternion(q, p), q_inv)
        self.lookat = p_rot[1:4]
        # self.position = p_rot[1:4]
        
        
    def FPS(self, obj_position, target_position):
        self.position = obj_position
        self.lookat = target_position
        
    # キー入力処理
    # 引数
    # keys:キー入力情報
    # Key_vel:キー入力による移動量
    # quate_control:クォータニオン回転/ロドリゲス回転切り替え
    def input(self,keys, Key_vel,quate_control:bool=True):

        # u d l r translate
        if not keys[pygame.K_LCTRL]:
            A = np.zeros(3)
            if keys[pygame.K_a]: 
                A[1] += 1
            if keys[pygame.K_d]: 
                A[1] += -1
            if keys[pygame.K_w]: 
                A[0] += 1
            if keys[pygame.K_s]: 
                A[0] += -1
            # front back translate 
            if keys[pygame.K_q]: 
                A[2] += 1
            if keys[pygame.K_e]: 
                A[2] += -1

            if np.linalg.norm(A) > 0:
                # self.position -= self.lookat
                if quate_control:
                    self.quaternion_rotate(A, Key_vel)
                else:
                    RotationM = np.array([[(1-np.cos(Key_vel))*A[0]**2+np.cos(Key_vel),  (1-np.cos(Key_vel))*A[0]*A[1]-A[2]*np.sin(Key_vel), (1-np.cos(Key_vel))*A[0]*A[2]+A[1]*np.sin(Key_vel)],
                                        [(1-np.cos(Key_vel))*A[0]*A[1]+A[2]*np.sin(Key_vel), (1-np.cos(Key_vel))*A[1]**2+np.cos(Key_vel), (1-np.cos(Key_vel))*A[1]*A[2]-A[0]*np.sin(Key_vel)],
                                        [(1-np.cos(Key_vel))*A[2]*A[0]-A[1]*np.sin(Key_vel), (1-np.cos(Key_vel))*A[1]*A[2]+A[0]*np.sin(Key_vel), (1-np.cos(Key_vel))*A[2]**2+np.cos(Key_vel)]
                                ])
                    self.position = RotationM @ self.position
                # self.position += self.lookat
        else:   
            # u d l r translate
            if keys[pygame.K_a] : 
                self.position[0] -= Key_vel
                self.lookat[0] -= Key_vel
            if keys[pygame.K_d] : 
                self.position[0] += Key_vel
                self.lookat[0] += Key_vel
            if keys[pygame.K_w] : 
                self.position[1] += Key_vel
                self.lookat[1] += Key_vel
            if keys[pygame.K_s] : 
                self.position[1] -= Key_vel
                self.lookat[1] -= Key_vel

            # front back translate 
            if keys[pygame.K_q] : 
                self.position[2] += Key_vel
                self.lookat[2] += Key_vel
            if keys[pygame.K_e] : 
                self.position[2] -= Key_vel
                self.lookat[2] -= Key_vel
                
    def print_info(self):
        print("Position:\t", self.position)
        print("Lookat:\t\t", self.lookat)
        # print("Orientation:\t", self.orientation)
        # print("PPM:\t", self.PPM)
      
