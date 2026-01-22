import sys
import pygame
import numpy as np
from Camera import *
from Frame import *
from Fish import *
from StringsBlock import *
from ChineseEel import *
from GameManager import GameManager
#魚を泳がせてチンアナゴをよけるゲーム
#現状はチンアナゴに触れるとゲームオーバーってだけですが、
#得点システムとか、餌を食べて糞をするとか、対戦要素とかを入れるつもりでした。
#操作方法はW:上、S:下、A:左、D:右、R:リセット、ESC:終了です。
#スペースキーで加速ができますが、餌システムが未実装なのであまり意味はありません。
#魚の向きは移動方向に合わせて自動で変わります。
#



# 定数の設定
WIDTH,HEIGHT=1000, 1000                        # 画面の幅と高さ
scrcentr=np.array([(WIDTH-1)/2, (HEIGHT-1)/2]) # 画面の中心の座標
scale = (WIDTH-1)/2                            # 画面サイズの座標に変換する際の拡大率
fps = 60                                       # フレーム/秒
dt = 1/fps                                     # 秒/フレーム

def main():
    # Pygameの初期化
    pygame.init()
    
    control_que = []
    game_manager = GameManager()
    # 画面の生成
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # 描画バッファの作成
    buf = pygame.Surface((WIDTH, HEIGHT))

    # タイトルバーの設定（表示する文字を指定）
    pygame.display.set_caption("Fish Simulation") 

    clock = pygame.time.Clock()     # 時計作成

    Key_vel = 1e-2

    running = True  # ループ処理の実行を継続するフラグ

    while running:

        buf.fill((0, 0, 0))  # 描画バッファを背景色(RGB)で塗りつぶす     

        game_manager.update(key_input=pygame.key.get_pressed(), key_vel=Key_vel, buf=buf, scrcentr=scrcentr, scale=scale)
        
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
