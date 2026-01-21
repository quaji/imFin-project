import numpy as np
import pygame


# 文字列描画クラス
class StringsBlock:
    # コンストラクタ
    # 引数
    # strings:表示する文字列
    # font_size:文字サイズ
    # position:文字描画開始位置(左上)
    # color:文字色(RGB)
    def __init__(self, strings:str = "",font_size:float=0.075,position:np.array=np.array([-0.995,-0.92]),color:tuple=(255,255,0)):
        self.str_strings = strings
        self.font_size = font_size
        self.position = position
        self.strings = []
        self.color = color
        for i in range(len(strings)):
            char_func = getattr(self, strings[i].upper(), None)
            if callable(char_func):
                self.strings.append(char_func(index=i))
    # 文字列描画関数
    # 引数
    # buf:描画先バッファ
    # scrcentr:画面中心座標
    # scale:ピクセル単位への変換拡大率
    def display(self, buf, scrcentr=np.array([0,0]), scale=1):
        for char in self.strings:
            self.print_char(buf, char=char, scrcentr=scrcentr, scale=scale)
    # 2D文字描画関数
    # 引数
    # buf:描画先バッファ
    # font_size:文字サイズ
    # point:文字描画開始位置(左上)
    def print_char(self, buf, char=np.array(None), scrcentr=np.array([0,0]), scale=0):
        for i in range(len(char)-1):
            pygame.draw.line(buf, self.color, scale * char[i] + scrcentr, scale * char[i+1] + scrcentr, 1)   # 直線の描画
            
    # A-Zの文字定義関数
    # 引数
    # index:文字列中の文字位置(0オリジン)
    def A(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,-self.font_size],[self.font_size/2,0],[self.font_size,-self.font_size],[self.font_size*3/4,-self.font_size/2],[self.font_size/4,-self.font_size/2]])
    def B(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,-self.font_size],[0,0],[self.font_size*2/3,0],[self.font_size*5/6,-self.font_size/6],[self.font_size*5/6,-self.font_size/3],[self.font_size*2/3,-self.font_size/2],[0,-self.font_size/2],[self.font_size*5/6,-self.font_size/2],[self.font_size,-self.font_size*2/3],[self.font_size,-self.font_size*5/6],[self.font_size*5/6,-self.font_size],[0,-self.font_size]])
    def C(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[self.font_size,-self.font_size/3],[self.font_size*2/3,0],[self.font_size/3,0],[0,-self.font_size/3],[0,-self.font_size*2/3],[self.font_size/3,-self.font_size],[self.font_size*2/3,-self.font_size],[self.font_size,-self.font_size*2/3]])
    def D(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,-self.font_size],[0,0],[self.font_size*2/3,0],[self.font_size,-self.font_size/3],[self.font_size,-self.font_size*2/3],[self.font_size*2/3,-self.font_size],[0,-self.font_size]])
    def E(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[self.font_size,-self.font_size],[0,-self.font_size],[0,-self.font_size/2],[self.font_size,-self.font_size/2],[0,-self.font_size/2],[0,0],[self.font_size,0]])
    def F(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,-self.font_size],[0,-self.font_size/2],[self.font_size*3/4,-self.font_size/2],[0,-self.font_size/2],[0,0],[self.font_size,0]])
    def G(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[self.font_size,-self.font_size/3],[self.font_size*2/3,0],[self.font_size/3,0],[0,-self.font_size/3],[0,-self.font_size*2/3],[self.font_size/3,-self.font_size],[self.font_size*2/3,-self.font_size],[self.font_size,-self.font_size*2/3],[self.font_size,-self.font_size/2],[self.font_size/2,-self.font_size/2]])
    def H(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[0,-self.font_size],[0,-self.font_size/2],[self.font_size,-self.font_size/2],[self.font_size,0],[self.font_size,-self.font_size]])
    def I(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[self.font_size,0],[self.font_size/2,0],[self.font_size/2,-self.font_size],[0,-self.font_size],[self.font_size,-self.font_size]])
    def J(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[self.font_size,0],[self.font_size,-self.font_size*2/3],[self.font_size*2/3,-self.font_size],[self.font_size/3,-self.font_size],[0,-self.font_size*2/3]])
    def K(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[0,-self.font_size],[0,-self.font_size/2],[self.font_size,0],[0,-self.font_size/2],[self.font_size,-self.font_size]])
    def L(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[0,-self.font_size],[self.font_size,-self.font_size]])
    def M(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,-self.font_size],[0,0],[self.font_size/2,-self.font_size*3/4],[self.font_size,0],[self.font_size,-self.font_size]])
    def N(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,-self.font_size],[0,0],[self.font_size,-self.font_size],[self.font_size,0]])
    def O(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[self.font_size,-self.font_size/3],[self.font_size*2/3,0],[self.font_size/3,0],[0,-self.font_size/3],[0,-self.font_size*2/3],[self.font_size/3,-self.font_size],[self.font_size*2/3,-self.font_size],[self.font_size,-self.font_size*2/3],[self.font_size,-self.font_size/3]])
    def P(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,-self.font_size],[0,0],[self.font_size,0],[self.font_size,-self.font_size/2],[0,-self.font_size/2]])
    def Q(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[self.font_size,-self.font_size/3],[self.font_size*2/3,0],[self.font_size/3,0],[0,-self.font_size/3],[0,-self.font_size*2/3],[self.font_size/3,-self.font_size],[self.font_size*2/3,-self.font_size],[self.font_size,-self.font_size*2/3],[self.font_size,-self.font_size/3],[self.font_size/2,-self.font_size/2],[self.font_size,-self.font_size]])
    def R(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,-self.font_size],[0,0],[self.font_size,0],[self.font_size,-self.font_size/2],[0,-self.font_size/2],[self.font_size,-self.font_size*3/4],[self.font_size,-self.font_size]])
    def S(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[self.font_size,-self.font_size/6],[self.font_size*5/6,0],[self.font_size/6,0],[0,-self.font_size/6],[0,-self.font_size/3],[self.font_size,-self.font_size*2/3],[self.font_size,-self.font_size*5/6],[self.font_size*5/6,-self.font_size],[self.font_size/6,-self.font_size],[0,-self.font_size*5/6]])
    def T(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[self.font_size,0],[self.font_size/2,0],[self.font_size/2,-self.font_size]])
    def U(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[0,-self.font_size*3/4],[self.font_size/3,-self.font_size],[self.font_size*2/3,-self.font_size],[self.font_size, -self.font_size*3/4],[self.font_size,0]])
    def V(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[self.font_size/2,-self.font_size],[self.font_size,0]])
    def W(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[self.font_size/4,-self.font_size],[self.font_size/2,-self.font_size/2],[self.font_size*3/4,-self.font_size],[self.font_size,0]])
    def X(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[self.font_size,-self.font_size],[self.font_size/2,-self.font_size/2],[self.font_size,0],[0,-self.font_size]])
    def Y(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[self.font_size/2,-self.font_size/2],[self.font_size,0],[self.font_size/2,-self.font_size/2],[self.font_size/2,-self.font_size]])
    def Z(self,index=0)->np.array:
        return self.position+np.array([self.font_size*1.2*index,0])+np.array([[0,0],[self.font_size,0],[0,-self.font_size],[self.font_size,-self.font_size]])
