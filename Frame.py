import numpy as np
import pygame
from quaternions import *
from object_module import solid2plane

# 格子フレームクラス
# ステージの枠組みを表示するためのクラス
class Frame:
    # コンストラクタ
    # 引数
    # position:フレームの中心位置
    # orientation:フレームの回転クォータニオン
    # vertical_segment:垂直方向の分割数
    # horizontal_segment:水平方向の分割数
    # vertical_size:垂直方向の全体大きさ
    # horizontal_size:水平方向の全体大きさ
    def __init__(self, position = np.zeros(3), orientation = np.array([1., 0., 0., 0.]), vertical_segment = 10, horizontal_segment = 10, vertical_size = 1, horizontal_size = 1):
        self.position = np.concatenate([[0.],position])
        self.orientation = orientation
        self.vertical_edges = [[np.array([0., vertical_size*(_/vertical_segment-0.5), 0., horizontal_size*0.5]),np.array([0., vertical_size*(_/vertical_segment-0.5), 0., -horizontal_size*0.5])] for _ in range(vertical_segment+1)]
        self.horizontal_edges = [[np.array([0., vertical_size*0.5, 0., horizontal_size*(_/horizontal_segment-0.5)]),np.array([0., -vertical_size*0.5, 0., horizontal_size*(_/horizontal_segment -0.5)])] for _ in range(horizontal_segment+1)]
        
    # フレーム位置設定関数
    # 引数
    # position:フレームの中心位置
    def set_position(self, position:np.array):
        self.position = np.concatenate([[0.],position])
    
    # フレーム表示関数
    # 引数
    # buf:描画先バッファ
    # V:ビュー変換行列
    # PPM:射影変換行列
    # scrcentr:画面中心座標
    # scale:画面サイズへの変換拡大率
    # color:フレームの色(RGB)
    def display(self, buf, V, PPM, scrcentr, scale, color = (255, 255, 255)):
        for edge in self.vertical_edges:
            p1 = mult_quaternion(mult_quaternion(self.orientation, edge[0]), inverse_quaternion(self.orientation)) + self.position
            p2 = mult_quaternion(mult_quaternion(self.orientation, edge[1]), inverse_quaternion(self.orientation)) + self.position
            p1 = PPM @ V @ np.concatenate([p1[1:4], [1.]])
            p2 = PPM @ V @ np.concatenate([p2[1:4], [1.]])
            line_points = solid2plane(p1, p2)
            if line_points is not None:
                p1 = line_points[0][0:2]/line_points[0][3]
                p1 = scale * p1 + scrcentr
                p2 = line_points[1][0:2]/line_points[1][3]
                p2 = scale * p2 + scrcentr
                pygame.draw.line(buf, color, p1, p2, 2)
        for edge in self.horizontal_edges:
            p1 = mult_quaternion(mult_quaternion(self.orientation, edge[0]), inverse_quaternion(self.orientation)) + self.position
            p2 = mult_quaternion(mult_quaternion(self.orientation, edge[1]), inverse_quaternion(self.orientation)) + self.position
            p1 = PPM @ V @ np.concatenate([p1[1:4], [1.]])
            p2 = PPM @ V @ np.concatenate([p2[1:4], [1.]])
            line_points = solid2plane(p1, p2)
            if line_points is not None:
                p1 = line_points[0][0:2]/line_points[0][3]
                p1 = scale * p1 + scrcentr
                p2 = line_points[1][0:2]/line_points[1][3]
                p2 = scale * p2 + scrcentr
                pygame.draw.line(buf, color, p1, p2, 2)
        tmp_edges = [[self.horizontal_edges[0][0],self.horizontal_edges[0][0]+np.array([0.,0.,1.,0.])],
                    [self.horizontal_edges[0][1],self.horizontal_edges[0][1]+np.array([0.,0.,1.,0.])],
                    [self.horizontal_edges[-1][0],self.horizontal_edges[-1][0]+np.array([0.,0.,1.,0.])],
                    [self.horizontal_edges[-1][1],self.horizontal_edges[-1][1]+np.array([0.,0.,1.,0.])]]
        for edge in tmp_edges:
            p1 = mult_quaternion(mult_quaternion(self.orientation, edge[0]), inverse_quaternion(self.orientation)) + self.position
            p2 = mult_quaternion(mult_quaternion(self.orientation, edge[1]), inverse_quaternion(self.orientation)) + self.position
            p1 = PPM @ V @ np.concatenate([p1[1:4], [1.]])
            p2 = PPM @ V @ np.concatenate([p2[1:4], [1.]])
            line_points = solid2plane(p1, p2)
            if line_points is not None:
                p1 = line_points[0][0:2]/line_points[0][3]
                p1 = scale * p1 + scrcentr
                p2 = line_points[1][0:2]/line_points[1][3]
                p2 = scale * p2 + scrcentr
                pygame.draw.line(buf, color, p1, p2, 2)
            