import numpy as np
import pygame
from quaternions import *
from object_module import solid2plane

# 魚クラス
class Fish:
    # コンストラクタ
    # 引数
    # position:魚の中心位置
    # velocity:魚の速度ベクトル
    # color:魚の色(RGB)
    # size:魚の大きさ
    # segment:魚の分割数
    # orientation:魚の回転クォータニオン
    # メンバ変数
    # position:魚の中心位置(4次元ベクトル)
    # color:魚の色(RGB)
    # size:魚の大きさ
    # segment:魚の分割数
    # segments:魚の各セグメント位置(4次元ベクトル)リスト
    # display_segments:表示用魚の各セグメント位置(4次元ベクトル)リスト
    def __init__(self, position = None, velocity = None, color = (0, 0, 255), size = 0.1, segment = 2, orientation = np.array([1., 0., 0., 0.])):
        self.position = np.concatenate([[0.],position]) # 魚の中心位置
        self.color = color # 魚の色(RGB)
        self.size = size
        self.segment = segment
        self.segments = [np.array([0,0,0,size*_/segment-size/2]) for _ in range(segment)]
        self.display_segments = [np.array([0,0,0,size*_/segment-size/2]) for _ in range(segment)]
        self.quaternion = orientation
        self.velocity = (self.segments[0]-self.segments[-1])/np.linalg.norm(self.segments[0]-self.segments[-1])*np.linalg.norm(velocity) if np.linalg.norm(velocity) > 0 else np.array([0.,0.,0.,0.])
        self.v_MAX = np.linalg.norm(self.velocity) * 5
        self.v_MIN = np.linalg.norm(self.velocity) * 1
        self.decorations = []
        self.set_decoration()
        self.display_mode = True
    
    # さかなの形をデコレーションするメソッド 
    def set_decoration(self):
        tmp = []
        for _ in range(self.segment):
            tmp.append(self.segments[_] - np.array([0.,0.,np.sin(_*np.pi/(self.segment-1))*self.size*0.25, 0.]))
        self.decorations.append(tmp)
        tmp = []
        for _ in range(self.segment):
            tmp.append(self.segments[_] - np.array([0.,np.sin(_*np.pi/(self.segment-1))*self.size*0.1,0., 0.]))
        self.decorations.append(tmp)
        tmp = []
        for _ in range(self.segment):
            tmp.append(self.segments[_] + np.array([0.,0.,np.sin(_*np.pi/(self.segment-1))*self.size*0.25, 0.]))
        self.decorations.append(tmp)
        tmp = []
        for _ in range(self.segment):
            tmp.append(self.segments[_] + np.array([0.,np.sin(_*np.pi/(self.segment-1))*self.size*0.1,0., 0.]))
        self.decorations.append(tmp)
        tmp = []
        tmp.append(self.segments[-2])
        tmp.append(self.segments[-1] + np.array([0.,0.,self.size*0.2, 0.]))
        tmp.append(self.segments[-1] + np.array([0.,0.,-self.size*0.2, 0.]))
        tmp.append(self.segments[-2])
        self.decorations.append(tmp)
    
    # 魚表示関数
    # 引数
    # buf:描画先バッファ
    # V:ビュー変換行列
    # PPM:射影変換行列
    # scrcentr:画面中心座標
    # scale:画面サイズの変換拡大率
    def display(self, buf, V, PPM, scrcentr, scale):
        if not self.display_mode:return
        inv_q = inverse_quaternion(self.quaternion)
        for i in range(self.segment-1):
            p1 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[i]), inv_q)
            p2 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[i+1]), inv_q)
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
        self.display_decoration(buf, V, PPM, scrcentr, scale)
        self.display_shadow(buf, V, PPM, scrcentr, scale)
    
    # 魚のデコレーション表示関数
    # 引数
    # buf:描画先バッファ
    # V:ビュー変換行列
    # PPM:射影変換行列
    # scrcentr:画面中心座標
    # scale:画面サイズの変換拡大率
    def display_decoration(self, buf, V, PPM, scrcentr, scale):
        if not self.display_mode:return 
        inv_q = inverse_quaternion(self.quaternion)
        for decoration in self.decorations:
            for i in range(len(decoration)-1):
                p1 = mult_quaternion(mult_quaternion(self.quaternion, decoration[i]), inv_q)
                p2 = mult_quaternion(mult_quaternion(self.quaternion, decoration[i+1]), inv_q)
                p1 = PPM @ V @ np.concatenate([(p1+self.position)[1:4], [1.]])
                p2 = PPM @ V @ np.concatenate([(p2+self.position)[1:4], [1.]])
                line_points = solid2plane(p1, p2)
                if line_points is not None:
                    p1 = line_points[0][0:2]/line_points[0][3]
                    p1 = scale * p1 + scrcentr
                    p2 = line_points[1][0:2]/line_points[1][3]
                    p2 = scale * p2 + scrcentr
                    pygame.draw.line(buf, self.color, p1, p2, 1)
        for i in range(len(self.decorations[0])):
            for j in range(4):
                jter = j%4
                p1 = mult_quaternion(mult_quaternion(self.quaternion, self.decorations[jter][i]), inv_q)
                jter = (j+1)%4
                p2 = mult_quaternion(mult_quaternion(self.quaternion, self.decorations[jter][i]), inv_q)
                p1 = PPM @ V @ np.concatenate([(p1+self.position)[1:4], [1.]])
                p2 = PPM @ V @ np.concatenate([(p2+self.position)[1:4], [1.]])
                line_points = solid2plane(p1, p2)
                if line_points is not None:
                    p1 = line_points[0][0:2]/line_points[0][3]
                    p1 = scale * p1 + scrcentr
                    p2 = line_points[1][0:2]/line_points[1][3]
                    p2 = scale * p2 + scrcentr
                    pygame.draw.line(buf, self.color, p1, p2, 1)
    
    # 魚の目印表示関数
    # 引数
    # buf:描画先バッファ
    # V:ビュー変換行列
    # PPM:射影変換行列
    # scrcentr:画面中心座標
    # scale:画面サイズの変換拡大率
    # color:目印の色(RGB)
    def display_landmark(self,buf,V,PPM,scrcentr,scale,color=(255,0,0)):
        if not self.display_mode:return 
        inv_q = inverse_quaternion(self.quaternion)
        p1 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[0]), inv_q)
        p2 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[1]+np.array([0.,0.,self.size/5,0.])), inv_q)
        p1 = PPM @ V @ np.concatenate([(p1+self.position)[1:4], [1.]])
        p2 = PPM @ V @ np.concatenate([(p2+self.position)[1:4], [1.]])
        line_points = solid2plane(p1, p2)
        if line_points is not None:
            p1 = line_points[0][0:2]/line_points[0][3]
            p1 = scale * p1 + scrcentr
            p2 = line_points[1][0:2]/line_points[1][3]
            p2 = scale * p2 + scrcentr
            pygame.draw.line(buf, color, p1, p2, 2)
    
    # 魚の状態更新関数
    # 引数
    # key_input:キーボード入力情報
    # key_vel:速度変化量
    def update(self,key_input=None, key_vel=0.0):
        if key_input is not None and key_vel > 0.0:
            self.input(key_input, key_vel)
            
        v1 = mult_quaternion(mult_quaternion(self.quaternion, self.velocity), inverse_quaternion(self.quaternion))
        self.position += v1
        if self.segment >= 2:
            temp = np.linalg.norm(self.velocity)
            self.velocity = self.segments[0]-self.segments[-1]
            self.velocity = self.velocity/np.linalg.norm(self.velocity)*temp
    
    # 魚の入力処理関数
    # 引数
    #  key_input:キーボード入力情報
    # key_vel:速度変化量
    def input(self, key_input, key_vel):
        leng = np.linalg.norm(self.segments[0]-self.segments[-1])
        # 加速減速の制御
        if key_input[pygame.K_SPACE]:
            if np.linalg.norm(self.velocity) < self.v_MAX:
                self.velocity *= 1.05
            else:
                self.velocity = self.velocity/np.linalg.norm(self.velocity)*self.v_MAX
        else:
            if np.linalg.norm(self.velocity) > self.v_MIN:
                self.velocity *= 0.95
            else:
                self.velocity = self.velocity/np.linalg.norm(self.velocity)*self.v_MIN            
            
        if key_input[pygame.K_w]:
            self.quaternion = mult_quaternion(self.quaternion, np.array([np.cos(key_vel/2), np.sin(key_vel/2), 0., 0.]))
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_] - np.array([0.,0.,key_vel*leng*(np.sin(_*np.pi/self.segment) - 0.5*0), 0.])*10
        if key_input[pygame.K_s]:
            self.quaternion = mult_quaternion(self.quaternion, np.array([np.cos(-key_vel/2), np.sin(-key_vel/2), 0., 0.]))
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_] + np.array([0.,0.,key_vel*leng*(np.sin(_*np.pi/self.segment) - 0.5*0), 0.])*10
        if key_input[pygame.K_a]:
            self.quaternion = mult_quaternion(self.quaternion, np.array([np.cos(-key_vel/2), 0., np.sin(-key_vel/2), 0.]))
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_] - np.array([0.,key_vel*leng*(np.sin(_*np.pi/self.segment) - 0.5*0), 0.,0.])*10
        if key_input[pygame.K_d]:
            self.quaternion = mult_quaternion(self.quaternion, np.array([np.cos(key_vel/2), 0., np.sin(key_vel/2), 0.]))
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_] + np.array([0.,key_vel*leng*(np.sin(_*np.pi/self.segment) - 0.5*0), 0.,0.])*10
        if not key_input[pygame.K_w] and not key_input[pygame.K_s] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
            for _ in range(self.segment):
                self.display_segments[_] = self.segments[_]

    # 魚の情報表示関数
    def print_info(self):
        print("Position:\t", self.position)
        print("Velocity:\t", self.velocity)
        print("Color:\t", self.color)
        print("Size:\t", self.size)
        print("Segment:\t", self.segment)
        print("Segments:\t", self.segments)
        
    def death_judge(self, position:np.array,radius:float):
        if np.sqrt(np.pow(self.position[1]-position[1],2)+np.pow(self.position[3]-position[3],2)) < radius and self.position[2] < position[2]:
            return True
        else:
            return False
        
    def display_shadow(self, buf, V, PPM, scrcentr, scale):
        if not self.display_mode:return
        inv_q = inverse_quaternion(self.quaternion)
        for i in range(self.segment-1):
            p1 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[i]), inv_q)
            p2 = mult_quaternion(mult_quaternion(self.quaternion, self.display_segments[i+1]), inv_q)
            p1 = p1+self.position
            p2 = p2+self.position
            p1[2] = 0.
            p2[2] = 0.
            p1 = PPM @ V @ np.concatenate([(p1)[1:4], [1.]])
            p2 = PPM @ V @ np.concatenate([(p2)[1:4], [1.]])
            line_points = solid2plane(p1, p2)
            if line_points is not None:
                p1 = line_points[0][0:2]/line_points[0][3]
                p1 = scale * p1 + scrcentr
                p2 = line_points[1][0:2]/line_points[1][3]
                p2 = scale * p2 + scrcentr
                pygame.draw.line(buf, (255, 0, 0), p1, p2, 2)

        
# テスト用メイン実行部
if __name__ == "__main__":
    fish = Fish()
    fish.print_info()