import sys
import pygame
import numpy as np
from Camera import *
from Frame import *
from Fish import *
from StringsBlock import *

# 定数の設定
WIDTH,HEIGHT=500, 500                        # 画面の幅と高さ
scrcentr=np.array([(WIDTH-1)/2, (HEIGHT-1)/2]) # 画面の中心の座標
scale = (WIDTH-1)/2                            # ピクセル単位の座標に変換する際の拡大率
fps = 60                                       # フレーム/秒
dt = 1/fps                                     # 秒/フレーム

def main():
    # Pygameの初期化
    pygame.init()
    
    control_que = []
    # cameraの生成
    camera = Camera(position=np.array([0.,0.4,0.]), lookat=np.array([0.,0.,1.]))
    
    # frameの生成
    frame = Frame()
    frame.set_position(np.array([0.,0.,1.]))
    
    fish = Fish(position=np.array([0.,0.3,1.]), velocity=np.array([0.001,0.,0.]),segment=10,color=(255,255,0),orientation=deg2quat(90, np.array([0.,1.,0.])))
    
    #文字列表示オブジェクトの生成
    test_string = StringsBlock(strings="ABCDEFGHIJKLMNOPQRSTUVWXYZ", position=np.array([-0.95,-0.8]), font_size=0.025, color=(255,255,255))
    
    # 画面の生成
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # 描画バッファの作成
    buf = pygame.Surface((WIDTH, HEIGHT))

    # タイトルバーの設定（表示する文字を指定）
    pygame.display.set_caption("2D Square & Keyboard Operation Sample") 

    clock = pygame.time.Clock()     # 時計作成

    Key_vel = 1e-2

    running = True  # ループ処理の実行を継続するフラグ

    while running:

        buf.fill((0, 0, 0))  # 描画バッファを背景色(RGB)で塗りつぶす     

        f = camera.lookat - camera.position/np.linalg.norm(camera.lookat - camera.position)
        s = np.cross(f, np.array([0,1,0]))
        u = np.cross(s, f)
        # カメラ座標系変換行列の作成
        V = np.array([[s[0], s[1], s[2], -np.dot(s, camera.position)],
                      [u[0], u[1], u[2], -np.dot(u, camera.position)],    
                      [-f[0], -f[1], -f[2], np.dot(f, camera.position)],
                      [0, 0, 0, 1]])

        camera.print_info()

        frame.display(buf, V, camera.PPM, scrcentr, scale)
        fish.display(buf, V, camera.PPM, scrcentr, scale)
        camera.input(pygame.key.get_pressed(), Key_vel, True)
        test_string.display(buf, scrcentr, scale)
        key = pygame.key.get_pressed()
        fish.update(key_input=key, key_vel=Key_vel)
        
        # camera.FPS(fish.position[1:4]+fish.display_segments[0][1:4], fish.position[1:4]+fish.display_segments[0][1:4]*2)
        
        # 画像座標の左下を原点にするための上下反転処理
        flippedbuf = pygame.transform.flip(buf, 0, 1) # 画像全体の上下反転
        screen.blit(flippedbuf, (0,0))  # 反転した画像を画面へ転送


        pygame.display.update()   # 表示更新
        delta = clock.tick(fps)  # fps制限
        # print(delta, "ms")

        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:  
                pygame.quit()  # Pygameの終了(画面閉じられる)
                sys.exit() # スクリプト実行の終了
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()  # Pygameの終了(画面閉じられる)
                    sys.exit() # スクリプト実行の終了
                if event.key == pygame.K_r:
                    pygame.quit()  # Pygameの終了(画面閉じられる)
                    return # main()の終了 → main()の呼び出し元が無限ループなのでまた初めから実行
               
                
if __name__ == "__main__":
    while True:
        main()
