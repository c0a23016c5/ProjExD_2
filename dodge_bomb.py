import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1200, 700
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect，または，爆弾Rect
    戻り値：真理値タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def get_rotated_images(img):
    """
    引数：こうかとんの元画像
    戻り値：各方向に対応したrotozoom画像の辞書
    """
    kk_images = {
        (0, -5): pg.transform.rotozoom(pg.transform.flip(img, False, True),-90,1.0),   # 上
        (0, 5): pg.transform.rotozoom(pg.transform.flip(img,False,True),90,1.0),  # 下
        (-5, 0): pg.transform.rotozoom(img,0,1.0),  # 左
        (5, 0): pg.transform.rotozoom(pg.transform.flip(img, True, False),0,1.0),  # 右
        (-5, -5): pg.transform.rotozoom(pg.transform.flip(img, True, True),-240,1.0),  # 左上
        (-5, 5): pg.transform.rotozoom(pg.transform.flip(img, True, True), 240,1.0),  # 左下
        (5, -5): pg.transform.rotozoom(pg.transform.flip(img, False, True),-120,1.0),  # 右上
        (5, 5): pg.transform.rotozoom(pg.transform.flip(img, False, True),120,1.0),  # 右下
    }
    return kk_images


def game_over(screen, kk_rct):
    """
    ゲームオーバー画面を表示する関数
    """
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    black_surface = pg.Surface((WIDTH, HEIGHT))
    black_surface.set_alpha(128)  # 半透明にする
    black_surface.fill((0, 0, 0))
    crying_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)  # 泣いているこうかとん画像
    crying_rct = crying_img.get_rect(center=kk_rct.center)
    crying_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)  # 泣いているこうかとん画像
    crying_rct2 = crying_img.get_rect(center= (WIDTH - kk_rct[0], HEIGHT - kk_rct[1]))

    screen.blit(black_surface, (0, 0))
    screen.blit(crying_img, crying_rct)
    screen.blit(crying_img2, crying_rct2)
    screen.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(5000)  # 5秒間表示する


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg",)
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_images = get_rotated_images(kk_img)
    kk_rct = kk_images[(0, -5)].get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 1辺が20の空のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 空のSurfaceに赤い円を描く
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の横方向速度，縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if kk_rct.colliderect(bb_rct):  # 衝突判定
            game_over(screen, kk_rct)
            return  # ゲームオーバー

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        # 方向を計算
        direction = (0, 0)
        if sum_mv[0] != 0 or sum_mv[1] != 0:
            direction = (sum_mv[0], sum_mv[1])

        if direction != (0, 0):
            kk_img = kk_images[direction]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()