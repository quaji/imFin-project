import numpy as np
import pygame

# 直線が画面に映るかどうかを判定し、映る場合はその2D座標を返す関数
# 引数
# p1:物体の始点の同次座標(np.array([x,y,z,w]))
# p2:物体の終点の同次座標(np.array([x,y,z,w]))
# 戻り値
# 映る場合:np.array([[x1,y1,w1],[x2,y2,w2]])  (x/w,y/wが画面上の座標)
# 映らない場合:None
def solid2plane(p1:np.array, p2:np.array)->np.array:
    if p1[3] > 1e-3 and p2[3] > 1e-3:
        return np.array([p1, p2])
    elif p1[3] > 1e-3 and p2[3] <= 1e-3:
        t = (1e-3 - p1[3])/(p2[3]-p1[3])
        inter = p1 + t*(p2 - p1)
        return np.array([p1, inter])
    elif p1[3] <= 1e-3 and p2[3] > 1e-3:
        t = (1e-3 - p1[3])/(p2[3]-p1[3])
        inter = p1 + t*(p2 - p1)
        return np.array([inter, p2])
    else:
        return None
    
# x-z平面上の円を取得する関数
# 引数
# radius:円の半径
# segment:円の分割数
# 戻り値
# 円周上の点のリスト[np.array([0.,x1,0.,z1]), np.array([0.,x2,0.,z2]), ...]
def get_circle(radius, segment):
    points = []
    for i in range(segment):
        theta = 2.0 * np.pi * i / segment
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        points.append(np.array([0., x, 0., y]))
    return points
    