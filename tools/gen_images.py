"""
gen_images.py
サウンドノベル風背景の手続き的生成。
人物はシルエットでのみ描く。
出力: /home/user/novel/assets/bg/*.jpg  (1920x1080, JPEG 85)

各シーンは別関数。`make(<chapter>)` で章単位で実行する。
"""
from __future__ import annotations
import os
import math
import random
import argparse
from typing import Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

OUT_DIR = '/home/user/novel/assets/bg'
W, H = 1920, 1080
JPEG_Q = 85

# ---------- 基本ユーティリティ ----------

def _seed(s: int):
    random.seed(s); np.random.seed(s)


def _arr(rgb=(0, 0, 0)):
    a = np.zeros((H, W, 3), dtype=np.float32)
    a[..., 0] = rgb[0]; a[..., 1] = rgb[1]; a[..., 2] = rgb[2]
    return a


def grad_v(top, bot):
    """縦方向リニアグラデーション"""
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    top = np.array(top, dtype=np.float32)[None, None, :]
    bot = np.array(bot, dtype=np.float32)[None, None, :]
    g = top * (1 - t) + bot * t
    return np.broadcast_to(g, (H, W, 3)).copy()


def grad_radial(center_color, edge_color, cx, cy, radius):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    t = np.clip(dist / radius, 0, 1)[..., None]
    c = np.array(center_color, dtype=np.float32)
    e = np.array(edge_color, dtype=np.float32)
    return c * (1 - t) + e * t


def add_radial_light(arr, color, cx, cy, radius, strength=1.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    t = np.clip(1 - dist / radius, 0, 1)
    t = t ** 2
    arr += np.array(color, dtype=np.float32)[None, None, :] * t[..., None] * strength
    return arr


def add_noise(arr, scale=4):
    n = np.random.randn(H, W).astype(np.float32) * scale
    return arr + n[..., None]


def add_grain(arr, strength=10):
    n = np.random.randn(H, W, 3).astype(np.float32) * strength
    return arr + n


def vignette(arr, strength=0.55, soft=1.6):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, H / 2
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    md = math.sqrt(cx ** 2 + cy ** 2)
    t = np.clip(dist / md, 0, 1) ** soft
    factor = (1 - t * strength)[..., None]
    return arr * factor


def darken_bottom(arr, height_ratio=0.42, strength=0.55):
    """テキストボックス領域を暗化"""
    fade = np.zeros(H, dtype=np.float32)
    start = int(H * (1 - height_ratio))
    for y in range(start, H):
        u = (y - start) / max(1, (H - start))
        fade[y] = u * strength
    factor = (1 - fade)[:, None, None]
    return arr * factor


def to_image(arr) -> Image.Image:
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def from_image(img: Image.Image) -> np.ndarray:
    return np.array(img, dtype=np.float32)


def blur(img: Image.Image, radius=2) -> Image.Image:
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def overlay_alpha(base_arr, overlay_img: Image.Image):
    """RGBAオーバーレイを乗せる"""
    base = to_image(base_arr).convert('RGBA')
    out = Image.alpha_composite(base, overlay_img)
    return from_image(out.convert('RGB'))


def save(img_or_arr, name: str, q: int = JPEG_Q) -> str:
    if isinstance(img_or_arr, np.ndarray):
        img = to_image(img_or_arr)
    else:
        img = img_or_arr.convert('RGB') if img_or_arr.mode != 'RGB' else img_or_arr
    path = os.path.join(OUT_DIR, name)
    img.save(path, format='JPEG', quality=q, optimize=True)
    print(f'  -> {path}  ({os.path.getsize(path)//1024} KB)')
    return path


# ---------- 形状ヘルパ ----------

def _stamp_layer(base: Image.Image, draw_callable, blur_radius=0.8) -> Image.Image:
    """別レイヤーに draw して、エッジを軽くぼかしてから合成"""
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_callable(d)
    if blur_radius > 0:
        layer = layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    base.alpha_composite(layer)
    return base


def silhouette_standing(target: Image.Image, cx: int, cy_feet: int,
                         height: int = 480, color=(0, 0, 0, 235),
                         lean: float = 0.0, profile: bool = False):
    """より自然なフォルムの直立シルエット。
       lean: -1〜1 で左右への傾き / profile=True で側面（うつむき気味）"""
    h = height
    head_w = int(h * 0.085)
    head_h = int(h * 0.105)
    head_top = cy_feet - h
    head_cx = cx + int(lean * 30)

    sh_y    = head_top + int(head_h * 1.85)
    sh_half = int(h * 0.20)
    waist_y = cy_feet - int(h * 0.45)
    waist_half = int(h * 0.155)
    knee_y  = cy_feet - int(h * 0.20)
    knee_half = int(h * 0.085)
    foot_half = int(h * 0.06)

    def draw_body(d: ImageDraw.ImageDraw):
        # 頭（縦に長い楕円）
        if profile:
            d.ellipse([head_cx - head_w + 4, head_top + 4,
                       head_cx + head_w + 4, head_top + head_h * 2 + 4],
                       fill=color)
        else:
            d.ellipse([head_cx - head_w, head_top,
                       head_cx + head_w, head_top + head_h * 2],
                       fill=color)
        # 首
        d.polygon([
            (head_cx - head_w * 0.45, head_top + head_h * 1.7),
            (head_cx + head_w * 0.45, head_top + head_h * 1.7),
            (head_cx + head_w * 0.55, sh_y - 4),
            (head_cx - head_w * 0.55, sh_y - 4),
        ], fill=color)
        # 肩〜胴体（なで肩風の多角形）
        d.polygon([
            (cx - sh_half * 0.6, sh_y),
            (cx - sh_half,       sh_y + 12),
            (cx - waist_half,    waist_y),
            (cx + waist_half,    waist_y),
            (cx + sh_half,       sh_y + 12),
            (cx + sh_half * 0.6, sh_y),
        ], fill=color)
        # 腕（自然に下ろした、わずかに広がる）
        arm_w = int(h * 0.055)
        d.polygon([
            (cx - sh_half + 2,        sh_y + 14),
            (cx - sh_half + arm_w,    sh_y + 14),
            (cx - waist_half + 4,     waist_y + 8),
            (cx - waist_half - arm_w, waist_y + 24),
            (cx - waist_half - arm_w + 4, waist_y + int(h * 0.25)),
            (cx - waist_half - arm_w - 6, waist_y + int(h * 0.27)),
        ], fill=color)
        d.polygon([
            (cx + sh_half - 2,        sh_y + 14),
            (cx + sh_half - arm_w,    sh_y + 14),
            (cx + waist_half - 4,     waist_y + 8),
            (cx + waist_half + arm_w, waist_y + 24),
            (cx + waist_half + arm_w - 4, waist_y + int(h * 0.25)),
            (cx + waist_half + arm_w + 6, waist_y + int(h * 0.27)),
        ], fill=color)
        # 脚（膝でくびれ、足首で広がる）
        d.polygon([
            (cx - waist_half + 4, waist_y),
            (cx - 6,              waist_y),
            (cx - 6,              knee_y),
            (cx - knee_half,      knee_y),
            (cx - foot_half,      cy_feet),
            (cx - waist_half - 2, cy_feet),
        ], fill=color)
        d.polygon([
            (cx + waist_half - 4, waist_y),
            (cx + 6,              waist_y),
            (cx + 6,              knee_y),
            (cx + knee_half,      knee_y),
            (cx + foot_half,      cy_feet),
            (cx + waist_half + 2, cy_feet),
        ], fill=color)

    _stamp_layer(target, draw_body, blur_radius=1.2)


def silhouette_seated_at_table(target: Image.Image, cx: int, table_y: int,
                                height: int = 320, color=(0, 0, 0, 235),
                                lean_forward: float = 0.0):
    """テーブルの向こう側に座る人物。机より上の上半身＋頭だけ見える想定。"""
    h = height
    head_w = int(h * 0.18)
    head_h = int(h * 0.22)
    head_cx = cx
    head_top = table_y - int(h * 0.90)
    sh_y = table_y - int(h * 0.30)
    sh_half = int(h * 0.34)

    # 前傾でうなだれた表現
    head_top += int(lean_forward * 18)

    def draw_body(d: ImageDraw.ImageDraw):
        # 頭
        d.ellipse([head_cx - head_w, head_top,
                   head_cx + head_w, head_top + head_h * 2], fill=color)
        # 肩〜胴上部（机に隠れる前提で台形）
        d.polygon([
            (head_cx - head_w * 0.6, head_top + head_h * 1.65),
            (head_cx + head_w * 0.6, head_top + head_h * 1.65),
            (cx + sh_half,           sh_y),
            (cx + sh_half + 6,       table_y),
            (cx - sh_half - 6,       table_y),
            (cx - sh_half,           sh_y),
        ], fill=color)

    _stamp_layer(target, draw_body, blur_radius=1.0)


def silhouette_at_desk(target: Image.Image, cx: int, desk_y: int,
                        height: int = 280, color=(0, 0, 0, 235),
                        slouch: float = 0.15):
    """デスクの机面より上に出ている部分（頭＋背中）だけを描く。
       height は机から頭頂までの可視ピクセル。"""
    h = height
    head_w = int(h * 0.20)
    head_h = int(h * 0.24)
    head_top = desk_y - h
    head_cx  = cx + int(slouch * 8)
    sh_y     = head_top + int(head_h * 1.85)
    sh_half  = int(h * 0.36)
    bot_half = int(h * 0.42)

    def draw_body(d: ImageDraw.ImageDraw):
        # 頭（後頭部）
        d.ellipse([head_cx - head_w, head_top,
                   head_cx + head_w, head_top + head_h * 2], fill=color)
        # 首
        d.polygon([
            (head_cx - head_w * 0.45, head_top + head_h * 1.7),
            (head_cx + head_w * 0.45, head_top + head_h * 1.7),
            (head_cx + head_w * 0.55, sh_y - 4),
            (head_cx - head_w * 0.55, sh_y - 4),
        ], fill=color)
        # 背中（机面で切れる台形）
        d.polygon([
            (cx - sh_half * 0.7,  sh_y),
            (cx - sh_half,        sh_y + 12),
            (cx - bot_half,       desk_y + 4),
            (cx + bot_half,       desk_y + 4),
            (cx + sh_half,        sh_y + 12),
            (cx + sh_half * 0.7,  sh_y),
        ], fill=color)

    _stamp_layer(target, draw_body, blur_radius=1.0)


def silhouette_slumped_on_table(draw: ImageDraw.ImageDraw, cx: int, table_y: int,
                                 size: float = 1.0, color=(0, 0, 0, 230)):
    """机に伏した人物。table_y は机面の Y。"""
    s = size
    # 頭（横向き / 倒れた状態）
    head_r = int(60 * s)
    cy = table_y - head_r // 2
    draw.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r],
                 fill=color)
    # 肩（机に乗る）
    sh_w = int(150 * s)
    sh_h = int(50 * s)
    draw.polygon([
        (cx + head_r - 10,  table_y - 30),
        (cx + sh_w,         table_y - 10),
        (cx + sh_w + 80,    table_y + 20),
        (cx + head_r - 30,  table_y + 30),
    ], fill=color)
    # 腕
    draw.polygon([
        (cx - head_r + 20, table_y),
        (cx + 100,         table_y - 10),
        (cx + 110,         table_y + 20),
        (cx - head_r + 30, table_y + 30),
    ], fill=color)


def draw_window_lights(draw: ImageDraw.ImageDraw, y_top: int, y_bot: int,
                        n: int, color=(255, 240, 210), alpha=110, jitter=True):
    """ビル窓のような点光源を一段に並べる"""
    step = W // (n + 1)
    for i in range(1, n + 1):
        x = step * i + (random.randint(-step // 4, step // 4) if jitter else 0)
        size = random.randint(8, 22)
        draw.rectangle([x - size, y_top, x + size, y_bot],
                       fill=(*color, alpha))


# ---------- 各シーン ----------

def title():
    _seed(11)
    arr = grad_v((22, 14, 18), (4, 2, 4))
    arr = add_radial_light(arr, (160, 30, 30), W * 0.5, H * 0.3, 700, 0.65)
    arr = add_radial_light(arr, (240, 220, 200), W * 0.5, H * 0.3, 220, 0.45)

    # 散らばった紙片
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for _ in range(36):
        x = random.randint(40, W - 200)
        y = random.randint(int(H * 0.35), H - 80)
        w = random.randint(120, 320)
        h = random.randint(80, 180)
        ang = random.uniform(-25, 25)
        rect = Image.new('RGBA', (w, h), (245, 240, 228, random.randint(70, 140)))
        rd = ImageDraw.Draw(rect)
        # 罫線・赤字風
        for ly in range(10, h - 10, 16):
            rd.line([(8, ly), (w - 8, ly)], fill=(60, 50, 50, 80), width=1)
        if random.random() < 0.35:
            rd.line([(10, h // 2), (w - 10, h // 2 + random.randint(-20, 20))],
                    fill=(190, 30, 30, 180), width=3)
        rect = rect.rotate(ang, resample=Image.BICUBIC, expand=True)
        overlay.paste(rect, (x, y), rect)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 8)
    arr = vignette(arr, strength=0.65, soft=1.4)
    arr = darken_bottom(arr, height_ratio=0.30, strength=0.45)
    return to_image(arr)


def office_day():
    _seed(21)
    arr = grad_v((242, 230, 200), (180, 160, 130))
    arr = add_radial_light(arr, (255, 240, 210), W * 0.30, H * 0.15, 900, 0.65)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 天井ライト帯
    od.rectangle([0, 0, W, int(H * 0.08)], fill=(255, 240, 210, 90))
    # 中景デスク列（一段上）
    mid_y = int(H * 0.56)
    od.rectangle([int(W * 0.05), mid_y, int(W * 0.95), mid_y + 14],
                 fill=(80, 60, 42, 200))
    for i in range(5):
        x = int(W * 0.08) + i * int(W * 0.18)
        od.rectangle([x, mid_y - 100, x + 130, mid_y - 8],
                     fill=(30, 26, 22, 215))
        od.rectangle([x + 6, mid_y - 92, x + 124, mid_y - 14],
                     fill=(80, 110, 130, 195))
    # 中景の同僚（机の後ろに立つ、上半身だけ見える）
    silhouette_seated_at_table(overlay, int(W * 0.86), mid_y + 6, height=160,
                                color=(20, 18, 14, 210), lean_forward=0.1)
    # 手前のデスク（横一直線）
    front_y = int(H * 0.78)
    od2 = ImageDraw.Draw(overlay)
    od2.rectangle([0, front_y, W, front_y + 22],
                  fill=(56, 42, 30, 240))
    od2.rectangle([0, front_y + 22, W, H],
                  fill=(38, 28, 20, 230))
    # モニタ（手前デスクの上）
    od2.rectangle([int(W * 0.10), front_y - 200, int(W * 0.10) + 240, front_y - 10],
                  fill=(20, 18, 16, 240))
    od2.rectangle([int(W * 0.10) + 10, front_y - 190, int(W * 0.10) + 230, front_y - 22],
                  fill=(120, 150, 180, 215))
    # 散らばった書類
    for _ in range(6):
        x = random.randint(int(W * 0.55), int(W * 0.92))
        y = random.randint(front_y - 40, front_y + 6)
        w = random.randint(80, 160); h = random.randint(50, 90)
        ang = random.uniform(-15, 15)
        rect = Image.new('RGBA', (w, h), (235, 225, 205, 210))
        rd = ImageDraw.Draw(rect)
        for ly in range(8, h - 8, 12):
            rd.line([(6, ly), (w - 6, ly)], fill=(80, 70, 60, 70), width=1)
        rect = rect.rotate(ang, resample=Image.BICUBIC, expand=True)
        overlay.paste(rect, (x, y), rect)
    # 主人公の後ろ姿（手前デスクの後ろ）
    silhouette_at_desk(overlay, int(W * 0.30), front_y, height=300,
                       color=(10, 8, 6, 245), slouch=0.4)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 6)
    arr = vignette(arr, strength=0.55, soft=1.5)
    arr = darken_bottom(arr, height_ratio=0.38, strength=0.45)
    return to_image(arr)


def meeting_room():
    _seed(22)
    arr = grad_v((38, 42, 50), (10, 12, 16))
    arr = add_radial_light(arr, (255, 235, 200), W * 0.5, H * 0.35, 600, 0.55)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # ホワイトボード（プロジェクタの光を受ける）
    od.rectangle([int(W * 0.20), int(H * 0.16), int(W * 0.80), int(H * 0.46)],
                 fill=(220, 218, 212, 65))
    od.rectangle([int(W * 0.20), int(H * 0.16), int(W * 0.80), int(H * 0.46)],
                 outline=(110, 110, 110, 160), width=2)
    # 投影されたグラフ・図表のヒント（薄いブロック）
    for i in range(3):
        x = int(W * 0.26) + i * int(W * 0.18)
        od.rectangle([x, int(H * 0.30), x + int(W * 0.10), int(H * 0.42)],
                     fill=(255, 220, 180, 35))
    # 長机（透視）
    table_top_y = int(H * 0.62)
    table_bot_y = int(H * 0.98)
    od.polygon([
        (int(W * 0.05), table_top_y),
        (int(W * 0.95), table_top_y),
        (int(W * 1.10), table_bot_y),
        (int(W * -0.10), table_bot_y),
    ], fill=(18, 16, 20, 235))
    # 机のハイライト（プロジェクタ光の反射）
    od.polygon([
        (int(W * 0.40), table_top_y + 4),
        (int(W * 0.60), table_top_y + 4),
        (int(W * 0.65), table_top_y + 26),
        (int(W * 0.35), table_top_y + 26),
    ], fill=(140, 130, 110, 70))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.6))
    # 着席シルエット（机の向こう側、頭と肩だけ見える）
    seats = [
        (int(W * 0.18), 0.0),
        (int(W * 0.34), 0.2),
        (int(W * 0.66), 0.0),
        (int(W * 0.82), -0.1),
    ]
    for x, lean in seats:
        silhouette_seated_at_table(overlay, x, table_top_y, height=320,
                                    color=(0, 0, 0, 235), lean_forward=lean)
    # 立って説明する人物（中央奥、少し小さい）
    silhouette_standing(overlay, int(W * 0.50), int(H * 0.62), height=380,
                        color=(0, 0, 0, 240), lean=0.0)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 7)
    arr = vignette(arr, strength=0.62)
    arr = darken_bottom(arr, height_ratio=0.42, strength=0.50)
    return to_image(arr)


def office_night():
    _seed(23)
    arr = grad_v((22, 28, 44), (4, 6, 12))
    arr = add_radial_light(arr, (60, 120, 180), W * 0.30, H * 0.55, 500, 0.7)
    arr = add_radial_light(arr, (60, 120, 180), W * 0.70, H * 0.55, 500, 0.5)
    arr = add_radial_light(arr, (90, 120, 160), W * 0.5, H * 0.15, 800, 0.35)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 窓枠 + 雨筋
    for i in range(6):
        x = 200 + i * 280
        od.rectangle([x, int(H * 0.06), x + 200, int(H * 0.30)],
                     fill=(40, 60, 90, 90))
        od.rectangle([x, int(H * 0.06), x + 200, int(H * 0.30)],
                     outline=(150, 170, 200, 140), width=2)
        for r in range(8):
            rx = x + random.randint(0, 200)
            ry = random.randint(int(H * 0.06), int(H * 0.30))
            od.line([(rx, ry), (rx - 4, ry + 18)],
                    fill=(180, 200, 230, 80), width=1)
    # デスクとモニタ列
    desk_y = int(H * 0.66)
    od.rectangle([0, desk_y, W, desk_y + 14], fill=(8, 8, 12, 220))
    for i in range(6):
        x = 180 + i * 280
        od.rectangle([x, desk_y - 150, x + 200, desk_y - 10],
                     fill=(8, 10, 14, 230))
        od.rectangle([x + 8, desk_y - 142, x + 192, desk_y - 18],
                     fill=(60, 110, 170, 220))
        od.rectangle([x + 8, desk_y - 142, x + 60, desk_y - 100],
                     fill=(140, 200, 255, 90))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.5))
    # 一人だけ残っている美澄（ひとつのデスクに）
    silhouette_at_desk(overlay, int(W * 0.46), int(H * 0.85), height=440,
                       color=(6, 8, 14, 245))

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 6)
    arr = vignette(arr, strength=0.72, soft=1.6)
    arr = darken_bottom(arr, height_ratio=0.42, strength=0.42)
    return to_image(arr)


def meeting_crime():
    _seed(24)
    arr = grad_v((28, 6, 8), (6, 2, 3))
    arr = add_radial_light(arr, (170, 30, 30), W * 0.5, H * 0.55, 700, 0.7)
    arr = add_radial_light(arr, (255, 220, 180), W * 0.5, H * 0.18, 380, 0.45)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 長机
    table_top_y = int(H * 0.50)
    table_bot_y = int(H * 0.92)
    od.polygon([
        (int(W * 0.08), table_top_y),
        (int(W * 0.92), table_top_y),
        (int(W * 1.10), table_bot_y),
        (int(W * -0.10), table_bot_y),
    ], fill=(14, 10, 12, 235))
    # 散らばった書類（机面に広く）
    for _ in range(18):
        x = random.randint(int(W * 0.12), int(W * 0.85))
        y = random.randint(table_top_y + 30, table_bot_y - 30)
        w = random.randint(110, 220)
        h = random.randint(70, 140)
        ang = random.uniform(-25, 25)
        rect = Image.new('RGBA', (w, h), (218, 212, 196, 215))
        rd = ImageDraw.Draw(rect)
        for ly in range(8, h - 8, 14):
            rd.line([(8, ly), (w - 8, ly)], fill=(80, 70, 60, 70), width=1)
        if random.random() < 0.35:
            rd.line([(8, h * 0.5), (w - 8, h * 0.55)],
                    fill=(190, 30, 30, 200), width=3)
        rect = rect.rotate(ang, resample=Image.BICUBIC, expand=True)
        overlay.paste(rect, (x, y), rect)
    # 倒れたコーヒー（暗いシミ）
    od.ellipse([int(W * 0.62), table_top_y + 40, int(W * 0.78), table_top_y + 110],
               fill=(20, 10, 8, 230))
    od.polygon([
        (int(W * 0.65), table_top_y + 80),
        (int(W * 0.85), table_top_y + 130),
        (int(W * 0.83), table_top_y + 160),
        (int(W * 0.66), table_top_y + 110),
    ], fill=(20, 10, 8, 200))
    # 赤字「このデザインは、まだ完成していない」風のかすれた線
    msg_x, msg_y = int(W * 0.18), table_top_y + 40
    for k in range(2):
        y = msg_y + k * 38
        for seg in range(5):
            x1 = msg_x + seg * 90 + random.randint(-6, 6)
            x2 = x1 + random.randint(60, 90)
            od.line([(x1, y + random.randint(-3, 3)),
                     (x2, y + random.randint(-3, 3))],
                    fill=(210, 30, 30, 230), width=5)
    # 倒れた人物（机に伏した形）
    od_slump = ImageDraw.Draw(overlay)
    silhouette_slumped_on_table(od_slump, int(W * 0.40), table_top_y + 18,
                                size=1.6, color=(0, 0, 0, 245))
    # 仕上げに微ブラー
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.7))

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 9)
    arr = vignette(arr, strength=0.78, soft=1.4)
    arr = darken_bottom(arr, height_ratio=0.42, strength=0.45)
    return to_image(arr)


# ---------- main ----------

def corridor():
    _seed(31)
    arr = grad_v((34, 38, 42), (10, 12, 14))
    arr = add_radial_light(arr, (210, 220, 230), W * 0.5, H * 0.42, 600, 0.45)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 一点透視の壁・天井・床
    cx, cy = W * 0.50, H * 0.46
    # 床（下の台形）
    od.polygon([
        (0, H), (W, H),
        (cx + 200, cy), (cx - 200, cy),
    ], fill=(28, 30, 32, 220))
    # 天井
    od.polygon([
        (0, 0), (W, 0),
        (cx + 200, cy), (cx - 200, cy),
    ], fill=(20, 22, 26, 220))
    # 左壁
    od.polygon([
        (0, 0), (0, H), (cx - 200, cy), (cx - 200, cy),
    ], fill=(38, 42, 46, 200))
    # 右壁
    od.polygon([
        (W, 0), (W, H), (cx + 200, cy), (cx + 200, cy),
    ], fill=(38, 42, 46, 200))
    # 天井の蛍光灯（一列）
    for i in range(6):
        t = (i + 0.5) / 6.0
        # 視点に近づくにつれ大きく
        depth = 1 - abs(t - 0.5) * 1.5
        light_w = int(60 + depth * 220)
        light_y = int(cy - 80 + depth * 40)
        x = int(t * W)
        od.rectangle([x - light_w // 2, light_y - 14,
                      x + light_w // 2, light_y + 14],
                     fill=(255, 250, 230, 220))
    # 奥のドア
    door_x = int(cx)
    door_y = int(cy + 30)
    od.rectangle([door_x - 60, door_y - 110, door_x + 60, door_y + 30],
                 fill=(14, 16, 20, 235))
    od.rectangle([door_x - 56, door_y - 106, door_x + 56, door_y + 26],
                 outline=(120, 120, 125, 200), width=2)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.6))
    # 廊下に立つ一人の人物（中景）
    silhouette_standing(overlay, int(W * 0.55), int(H * 0.85), height=420,
                        color=(0, 0, 0, 240), lean=-0.05)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 6)
    arr = vignette(arr, strength=0.75, soft=1.7)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.50)
    return to_image(arr)


def server_room():
    _seed(32)
    arr = grad_v((6, 14, 12), (2, 6, 6))
    arr = add_radial_light(arr, (40, 160, 100), W * 0.55, H * 0.55, 700, 0.55)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 床
    od.polygon([
        (0, H), (W, H),
        (int(W * 0.65), int(H * 0.55)),
        (int(W * 0.35), int(H * 0.55)),
    ], fill=(8, 12, 14, 230))
    # サーバラック群（左右）
    rack_color = (10, 14, 16, 240)
    # 左の3列（手前から奥）
    for i, depth in enumerate([1.0, 0.7, 0.45]):
        x_l = int(W * 0.05 + i * W * 0.10)
        x_r = int(x_l + W * 0.13 * depth)
        y_t = int(H * 0.20 + (1 - depth) * H * 0.18)
        y_b = int(H * 0.95 - (1 - depth) * H * 0.10)
        od.rectangle([x_l, y_t, x_r, y_b], fill=rack_color)
        # LED
        for j in range(8):
            ly = y_t + 30 + j * int((y_b - y_t - 60) / 8)
            led_color = (60, 220, 120, 200) if random.random() < 0.6 else (220, 120, 60, 200)
            od.rectangle([x_l + 4, ly, x_l + 12, ly + 6], fill=led_color)
            od.rectangle([x_r - 12, ly, x_r - 4, ly + 6], fill=led_color)
    # 右側ラック（鏡像）
    for i, depth in enumerate([1.0, 0.7, 0.45]):
        x_r = int(W * 0.95 - i * W * 0.10)
        x_l = int(x_r - W * 0.13 * depth)
        y_t = int(H * 0.20 + (1 - depth) * H * 0.18)
        y_b = int(H * 0.95 - (1 - depth) * H * 0.10)
        od.rectangle([x_l, y_t, x_r, y_b], fill=rack_color)
        for j in range(8):
            ly = y_t + 30 + j * int((y_b - y_t - 60) / 8)
            led_color = (60, 220, 120, 200) if random.random() < 0.6 else (220, 120, 60, 200)
            od.rectangle([x_l + 4, ly, x_l + 12, ly + 6], fill=led_color)
            od.rectangle([x_r - 12, ly, x_r - 4, ly + 6], fill=led_color)
    # 通路の奥（薄い緑光）
    od.rectangle([int(W * 0.42), int(H * 0.30), int(W * 0.58), int(H * 0.55)],
                 fill=(40, 160, 100, 80))
    # 雨宮（中央通路に立つ、横向き気味）
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.6))
    silhouette_standing(overlay, int(W * 0.50), int(H * 0.92), height=380,
                        color=(0, 0, 0, 245), lean=0.08, profile=True)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 6)
    arr = vignette(arr, strength=0.78, soft=1.5)
    arr = darken_bottom(arr, height_ratio=0.38, strength=0.45)
    return to_image(arr)


def bar():
    _seed(41)
    arr = grad_v((40, 22, 8), (10, 4, 2))
    arr = add_radial_light(arr, (255, 170, 80), W * 0.40, H * 0.50, 600, 0.80)
    arr = add_radial_light(arr, (255, 200, 120), W * 0.75, H * 0.30, 350, 0.55)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 背景の棚（ボトル群）
    shelf_y1 = int(H * 0.28); shelf_y2 = int(H * 0.55)
    for sy in [shelf_y1, shelf_y2]:
        od.rectangle([int(W * 0.10), sy, int(W * 0.90), sy + 8],
                     fill=(60, 30, 10, 220))
        for i in range(18):
            x = int(W * 0.12) + i * int(W * 0.045)
            bw = random.randint(20, 36)
            bh = random.randint(70, 110)
            color_choice = random.choice([
                (180, 110, 50, 200),
                (140, 60, 30, 200),
                (90, 50, 30, 220),
                (200, 150, 70, 180),
            ])
            od.rectangle([x, sy - bh, x + bw, sy], fill=color_choice)
            # ボトルラベル
            od.rectangle([x + 4, sy - bh // 2 - 8, x + bw - 4, sy - bh // 2 + 8],
                         fill=(20, 12, 6, 200))
    # カウンター（手前）
    counter_y = int(H * 0.72)
    od.rectangle([0, counter_y, W, H], fill=(28, 14, 6, 235))
    # カウンター上のグラスとボトル
    od.ellipse([int(W * 0.18) - 22, counter_y - 8,
                int(W * 0.18) + 22, counter_y + 8],
               fill=(60, 30, 10, 200))
    od.rectangle([int(W * 0.18) - 16, counter_y - 60,
                  int(W * 0.18) + 16, counter_y - 8],
                 fill=(180, 110, 50, 180))
    # ハイボールグラス
    od.polygon([
        (int(W * 0.38) - 18, counter_y - 60),
        (int(W * 0.38) + 18, counter_y - 60),
        (int(W * 0.38) + 14, counter_y - 4),
        (int(W * 0.38) - 14, counter_y - 4),
    ], fill=(220, 180, 100, 130))
    # 手前の灰皿（暗い円）
    od.ellipse([int(W * 0.62) - 30, counter_y - 16,
                int(W * 0.62) + 30, counter_y + 16],
               fill=(20, 10, 6, 210))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.6))
    # 黒瀬（カウンター越しに座る、上半身のみ）
    silhouette_seated_at_table(overlay, int(W * 0.50), counter_y, height=320,
                                color=(0, 0, 0, 240), lean_forward=0.3)
    # 美澄（左、後ろ姿）
    silhouette_at_desk(overlay, int(W * 0.18), counter_y, height=260,
                       color=(0, 0, 0, 220), slouch=0.2)
    # 煙草の煙（薄い縦の白）
    od2 = ImageDraw.Draw(overlay)
    for k in range(5):
        sx = int(W * 0.62) + random.randint(-10, 10)
        sy = counter_y - 16 - k * 25
        od2.ellipse([sx - 8, sy - 4, sx + 8, sy + 4],
                    fill=(220, 200, 180, max(10, 60 - k * 12)))

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 8)
    arr = vignette(arr, strength=0.78, soft=1.5)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.45)
    return to_image(arr)


def client_office():
    _seed(51)
    arr = grad_v((220, 220, 224), (90, 100, 120))
    arr = add_radial_light(arr, (255, 255, 255), W * 0.50, H * 0.30, 700, 0.45)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 高層階の窓（広く取る）
    win_top = int(H * 0.06); win_bot = int(H * 0.62)
    od.rectangle([int(W * 0.05), win_top, int(W * 0.95), win_bot],
                 fill=(180, 200, 220, 90))
    # 窓枠（縦の桟）
    for i in range(7):
        x = int(W * 0.05) + i * int(W * 0.15)
        od.rectangle([x - 4, win_top, x + 4, win_bot], fill=(40, 50, 70, 220))
    # 横の桟
    for j in range(3):
        y = win_top + j * int((win_bot - win_top) / 3)
        od.rectangle([int(W * 0.05), y - 3, int(W * 0.95), y + 3],
                     fill=(40, 50, 70, 200))
    # 遠くのビル群（窓の向こう）
    for i in range(8):
        bx = int(W * 0.08) + i * int(W * 0.11) + random.randint(-15, 15)
        bw = random.randint(60, 110)
        bh = random.randint(180, 320)
        by = win_bot - bh
        od.rectangle([bx, by, bx + bw, win_bot - 4],
                     fill=(60, 75, 95, 180))
        # ビルの窓ポチポチ
        for r in range(0, bh, 30):
            for c in range(0, bw, 22):
                if random.random() < 0.55:
                    od.rectangle([bx + c + 4, by + r + 4,
                                  bx + c + 14, by + r + 12],
                                 fill=(180, 190, 210, 130))
    # 床（白い反射のあるフロア）
    od.rectangle([0, win_bot, W, H], fill=(60, 70, 90, 235))
    # ガラスの会議テーブル（手前）
    table_top_y = int(H * 0.74)
    od.polygon([
        (int(W * 0.18), table_top_y),
        (int(W * 0.82), table_top_y),
        (int(W * 0.95), int(H * 0.96)),
        (int(W * 0.05), int(H * 0.96)),
    ], fill=(200, 210, 230, 90))
    od.polygon([
        (int(W * 0.18), table_top_y),
        (int(W * 0.82), table_top_y),
        (int(W * 0.95), int(H * 0.96)),
        (int(W * 0.05), int(H * 0.96)),
    ], outline=(120, 130, 150, 180), width=2)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.5))
    # 瀬川（中央奥、立っている）
    silhouette_standing(overlay, int(W * 0.50), int(H * 0.94), height=520,
                        color=(0, 0, 0, 245), lean=0.0)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 5)
    arr = vignette(arr, strength=0.55, soft=1.4)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.55)
    return to_image(arr)


def rooftop():
    _seed(52)
    arr = grad_v((20, 24, 44), (4, 6, 12))
    # 月っぽい光
    arr = add_radial_light(arr, (180, 200, 230), W * 0.70, H * 0.18, 380, 0.55)
    # 都市の地平線オレンジ
    arr = add_radial_light(arr, (220, 130, 60), W * 0.50, H * 0.62, 800, 0.30)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 遠景のビル群（地平線、シルエット）
    horizon = int(H * 0.62)
    for i in range(40):
        bx = i * int(W / 40) + random.randint(-10, 10)
        bw = random.randint(20, 60)
        bh = random.randint(40, 140)
        od.rectangle([bx, horizon - bh, bx + bw, horizon],
                     fill=(8, 10, 16, 220))
        # ビルの灯り
        for r in range(0, bh, 14):
            for c in range(0, bw, 8):
                if random.random() < 0.30:
                    od.rectangle([bx + c + 2, horizon - bh + r + 2,
                                  bx + c + 6, horizon - bh + r + 6],
                                 fill=(255, 200, 100, 200))
    # 屋上の床
    od.rectangle([0, horizon, W, H], fill=(20, 22, 28, 235))
    # 鉄柵（手前）
    fence_y = int(H * 0.60)
    od.rectangle([0, fence_y - 4, W, fence_y + 4], fill=(40, 42, 46, 240))
    od.rectangle([0, fence_y + 60, W, fence_y + 68], fill=(40, 42, 46, 240))
    for i in range(40):
        x = i * int(W / 40)
        od.rectangle([x, fence_y, x + 4, fence_y + 64], fill=(40, 42, 46, 235))
    # 貯水槽のシルエット（左奥）
    od.polygon([
        (int(W * 0.05), int(H * 0.45)),
        (int(W * 0.20), int(H * 0.40)),
        (int(W * 0.20), horizon),
        (int(W * 0.05), horizon),
    ], fill=(8, 10, 16, 230))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.7))
    # 篠原（右、横顔気味、たたずむ）
    silhouette_standing(overlay, int(W * 0.65), int(H * 0.95), height=520,
                        color=(0, 0, 0, 245), lean=-0.05, profile=True)
    # 美澄（左、距離をあけて）
    silhouette_standing(overlay, int(W * 0.30), int(H * 0.96), height=480,
                        color=(0, 0, 0, 240), lean=0.05)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 7)
    arr = vignette(arr, strength=0.65, soft=1.6)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.45)
    return to_image(arr)


def cafe():
    _seed(61)
    arr = grad_v((90, 60, 36), (28, 18, 10))
    arr = add_radial_light(arr, (255, 200, 130), W * 0.50, H * 0.30, 600, 0.65)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 窓（左奥、外光）
    win_x1, win_x2 = int(W * 0.04), int(W * 0.36)
    win_y1, win_y2 = int(H * 0.12), int(H * 0.55)
    od.rectangle([win_x1, win_y1, win_x2, win_y2], fill=(220, 180, 130, 100))
    od.rectangle([win_x1, win_y1, win_x2, win_y2],
                 outline=(60, 36, 18, 220), width=4)
    # 窓の桟
    midx = (win_x1 + win_x2) // 2
    midy = (win_y1 + win_y2) // 2
    od.rectangle([midx - 2, win_y1, midx + 2, win_y2], fill=(60, 36, 18, 220))
    od.rectangle([win_x1, midy - 2, win_x2, midy + 2], fill=(60, 36, 18, 220))
    # 木の壁
    od.rectangle([0, win_y2, W, int(H * 0.78)], fill=(40, 24, 14, 180))
    # 木のテーブル（手前、丸ではなく木目の四角）
    table_y = int(H * 0.78)
    od.rectangle([0, table_y, W, H], fill=(56, 32, 16, 235))
    # 木目線
    for k in range(7):
        ly = table_y + 12 + k * 36
        od.line([(0, ly), (W, ly)], fill=(36, 22, 12, 110), width=1)
    # コーヒーカップ2つ
    od.ellipse([int(W * 0.30) - 36, table_y - 14, int(W * 0.30) + 36, table_y + 16],
               fill=(20, 12, 6, 230))
    od.ellipse([int(W * 0.30) - 28, table_y - 10, int(W * 0.30) + 28, table_y + 10],
               fill=(140, 90, 50, 220))
    od.ellipse([int(W * 0.62) - 36, table_y - 14, int(W * 0.62) + 36, table_y + 16],
               fill=(20, 12, 6, 230))
    od.ellipse([int(W * 0.62) - 28, table_y - 10, int(W * 0.62) + 28, table_y + 10],
               fill=(140, 90, 50, 220))
    # ペンダントライト（中央上）
    od.line([(int(W * 0.50), 0), (int(W * 0.50), int(H * 0.20))],
            fill=(20, 12, 6, 200), width=3)
    od.ellipse([int(W * 0.46), int(H * 0.18), int(W * 0.54), int(H * 0.26)],
               fill=(40, 24, 14, 230))
    od.ellipse([int(W * 0.47), int(H * 0.22), int(W * 0.53), int(H * 0.30)],
               fill=(255, 220, 160, 180))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.6))
    # 白石（左、横顔気味）
    silhouette_seated_at_table(overlay, int(W * 0.30), table_y, height=320,
                                color=(0, 0, 0, 245), lean_forward=0.0)
    # 美澄（右）
    silhouette_seated_at_table(overlay, int(W * 0.62), table_y, height=320,
                                color=(0, 0, 0, 245), lean_forward=0.15)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 7)
    arr = vignette(arr, strength=0.65, soft=1.5)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.50)
    return to_image(arr)


def presentation():
    _seed(81)
    arr = grad_v((22, 12, 14), (4, 2, 4))
    arr = add_radial_light(arr, (200, 200, 220), W * 0.50, H * 0.30, 700, 0.70)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # スクリーン（最終キービジュアル）
    sx1, sy1 = int(W * 0.22), int(H * 0.12)
    sx2, sy2 = int(W * 0.78), int(H * 0.56)
    od.rectangle([sx1, sy1, sx2, sy2], fill=(240, 232, 218, 245))
    od.rectangle([sx1, sy1, sx2, sy2], outline=(20, 16, 14, 220), width=3)
    # キービジュアルのコンセプト（抽象的に：線と円）
    od.ellipse([sx1 + 60, sy1 + 60, sx2 - 60, sy2 - 60],
               outline=(180, 30, 30, 230), width=8)
    od.line([(sx1 + 100, sy2 - 100), (sx2 - 100, sy1 + 100)],
            fill=(20, 16, 14, 200), width=4)
    # スクリーンタイトル風の小さな帯
    od.rectangle([sx1 + 80, sy2 - 60, sx2 - 80, sy2 - 30],
                 fill=(20, 16, 14, 235))
    # 床のスポットライト
    od.polygon([
        (int(W * 0.36), sy2 + 10),
        (int(W * 0.64), sy2 + 10),
        (int(W * 0.78), int(H * 0.95)),
        (int(W * 0.22), int(H * 0.95)),
    ], fill=(180, 170, 150, 60))
    # 観客席（左右の暗い影）
    seat_y = int(H * 0.78)
    od.rectangle([0, seat_y, int(W * 0.30), H], fill=(8, 6, 8, 180))
    od.rectangle([int(W * 0.70), seat_y, W, H], fill=(8, 6, 8, 180))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.7))
    # 観客席のシルエット（左右）
    silhouette_seated_at_table(overlay, int(W * 0.10), seat_y, height=240,
                                color=(0, 0, 0, 235))
    silhouette_seated_at_table(overlay, int(W * 0.22), seat_y, height=230,
                                color=(0, 0, 0, 230))
    silhouette_seated_at_table(overlay, int(W * 0.78), seat_y, height=240,
                                color=(0, 0, 0, 235))
    silhouette_seated_at_table(overlay, int(W * 0.90), seat_y, height=230,
                                color=(0, 0, 0, 230))
    # 美澄（中央、立って告発する後ろ姿）
    silhouette_standing(overlay, int(W * 0.50), int(H * 0.96), height=520,
                        color=(0, 0, 0, 250), lean=0.0)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 8)
    arr = vignette(arr, strength=0.78, soft=1.5)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.45)
    return to_image(arr)


def ending_a():
    """A：校了 ― 小さなギャラリー、葵の作品が並ぶ朝の光"""
    _seed(91)
    arr = grad_v((230, 200, 150), (140, 100, 60))
    arr = add_radial_light(arr, (255, 230, 180), W * 0.55, H * 0.30, 800, 0.65)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 床
    od.rectangle([0, int(H * 0.78), W, H], fill=(120, 90, 50, 220))
    # ギャラリー壁
    wall_y = int(H * 0.78)
    od.rectangle([0, 0, W, wall_y], fill=(245, 230, 200, 60))
    # 額装作品（4枚並ぶ）
    for i in range(4):
        x1 = int(W * 0.10) + i * int(W * 0.21)
        x2 = x1 + int(W * 0.16)
        y1 = int(H * 0.20)
        y2 = int(H * 0.65)
        # 額
        od.rectangle([x1 - 8, y1 - 8, x2 + 8, y2 + 8],
                     fill=(60, 40, 24, 230))
        od.rectangle([x1, y1, x2, y2], fill=(248, 240, 220, 240))
        # 内部のラフな絵
        od.line([(x1 + 30, y1 + 80), (x2 - 30, y2 - 80)],
                fill=(60, 50, 40, 200), width=3)
        od.ellipse([x1 + 40, y1 + 30, x2 - 40, y2 - 80],
                   outline=(180, 30, 30, 200), width=4)
        # サインっぽい小さな文字（赤）
        od.line([(x2 - 70, y2 - 30), (x2 - 20, y2 - 30)],
                fill=(180, 30, 30, 220), width=2)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.5))
    # 鑑賞者シルエット（後ろ姿、1人）
    silhouette_standing(overlay, int(W * 0.50), int(H * 0.95), height=440,
                        color=(20, 14, 8, 240), lean=0.0)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 5)
    arr = vignette(arr, strength=0.45, soft=1.4)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.50)
    return to_image(arr)


def ending_b():
    """B：差し戻し ― 雨に濡れた夜のビル、社名は変わっている"""
    _seed(92)
    arr = grad_v((34, 38, 44), (8, 10, 14))
    arr = add_radial_light(arr, (180, 190, 210), W * 0.50, H * 0.35, 600, 0.35)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 雨筋（背景全面）
    for _ in range(220):
        rx = random.randint(0, W)
        ry = random.randint(0, H)
        od.line([(rx, ry), (rx - 6, ry + 30)],
                fill=(180, 200, 230, 80), width=1)
    # ビル正面（中央〜手前）
    bx1, bx2 = int(W * 0.20), int(W * 0.80)
    by1, by2 = int(H * 0.10), int(H * 0.85)
    od.rectangle([bx1, by1, bx2, by2], fill=(20, 22, 28, 240))
    # 窓グリッド
    for r in range(8):
        for c in range(7):
            x = bx1 + 30 + c * int((bx2 - bx1 - 60) / 7)
            y = by1 + 50 + r * int((by2 - by1 - 100) / 8)
            if random.random() < 0.45:
                od.rectangle([x, y, x + 30, y + 30],
                             fill=(180, 190, 210, 130))
    # 看板（社名の暗い帯）
    od.rectangle([bx1, by1 - 10, bx2, by1 + 30], fill=(8, 8, 12, 240))
    # 看板の白い細い文字風（横棒の連続）
    for k in range(5):
        x = bx1 + 60 + k * int((bx2 - bx1 - 120) / 5)
        od.rectangle([x, by1 + 6, x + 50, by1 + 18],
                     fill=(220, 220, 220, 200))
    # 濡れた歩道（下）
    od.rectangle([0, by2, W, H], fill=(20, 22, 28, 240))
    # 街灯の反射
    od.ellipse([int(W * 0.25), by2 + 30, int(W * 0.45), by2 + 100],
               fill=(180, 190, 210, 80))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.6))
    # 傘を持つ人物（後ろ姿）
    silhouette_standing(overlay, int(W * 0.50), int(H * 0.96), height=420,
                        color=(0, 0, 0, 245), lean=0.0)
    # 傘
    od2 = ImageDraw.Draw(overlay)
    od2.polygon([
        (int(W * 0.50) - 90, int(H * 0.55)),
        (int(W * 0.50) + 90, int(H * 0.55)),
        (int(W * 0.50),       int(H * 0.42)),
    ], fill=(0, 0, 0, 245))

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 6)
    arr = vignette(arr, strength=0.65, soft=1.5)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.45)
    return to_image(arr)


def ending_c():
    """C：非公開案件 ― 別部署のオフィス、誰もいない"""
    _seed(93)
    arr = grad_v((180, 175, 165), (90, 86, 80))
    arr = add_radial_light(arr, (220, 215, 205), W * 0.50, H * 0.30, 800, 0.45)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 壁の薄い継ぎ目
    for k in range(0, W, 240):
        od.line([(k, 0), (k, int(H * 0.65))], fill=(60, 56, 50, 80), width=1)
    # 床
    od.rectangle([0, int(H * 0.65), W, H], fill=(120, 116, 108, 235))
    # デスク列（整然と並ぶ・均等）
    desk_y = int(H * 0.78)
    od.rectangle([0, desk_y, W, desk_y + 18], fill=(50, 46, 40, 240))
    od.rectangle([0, desk_y + 18, W, H], fill=(80, 74, 66, 235))
    for i in range(7):
        x = int(W * 0.04) + i * int(W * 0.135)
        # モニタ
        od.rectangle([x, desk_y - 130, x + 140, desk_y - 12],
                     fill=(20, 18, 16, 240))
        od.rectangle([x + 8, desk_y - 122, x + 132, desk_y - 20],
                     fill=(40, 100, 160, 200))
        # 通知の白いポップアップ（中央のモニタだけ）
        if i == 3:
            od.rectangle([x + 18, desk_y - 100, x + 122, desk_y - 60],
                         fill=(245, 240, 230, 235))
            # ファイル名のヒント帯
            od.rectangle([x + 24, desk_y - 92, x + 116, desk_y - 86],
                         fill=(40, 34, 28, 220))
            od.rectangle([x + 24, desk_y - 80, x + 100, desk_y - 74],
                         fill=(40, 34, 28, 200))
    # パーティション
    for i in range(6):
        x = int(W * 0.04) + i * int(W * 0.135) + int(W * 0.067)
        od.rectangle([x, desk_y - 150, x + 4, desk_y],
                     fill=(60, 56, 50, 200))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.5))
    # 椅子は空（人物なし）

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 5)
    arr = vignette(arr, strength=0.55, soft=1.4)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.40)
    return to_image(arr)


def ending_d():
    """D：白紙 ― 真っ白な空間に、赤字メッセージだけが浮かぶ"""
    _seed(94)
    arr = grad_v((250, 248, 244), (235, 232, 226))
    arr = add_radial_light(arr, (255, 252, 248), W * 0.50, H * 0.50, 700, 0.30)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 床の境界（うっすら）
    od.line([(0, int(H * 0.78)), (W, int(H * 0.78))],
            fill=(220, 215, 205, 180), width=2)
    # 赤字メッセージ風（中央のかすれた線）
    msg_x, msg_y = int(W * 0.20), int(H * 0.40)
    for k in range(2):
        y = msg_y + k * 56
        for seg in range(6):
            x1 = msg_x + seg * 100 + random.randint(-8, 8)
            x2 = x1 + random.randint(60, 100)
            alpha = random.randint(120, 200)
            od.line([(x1, y + random.randint(-3, 3)),
                     (x2, y + random.randint(-3, 3))],
                    fill=(190, 30, 30, alpha), width=6)
    # 真ん中下に小さな署名のような赤字
    od.line([(int(W * 0.45), int(H * 0.62)), (int(W * 0.55), int(H * 0.62))],
            fill=(190, 30, 30, 200), width=4)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.7))
    # 立ち尽くす一人の人物（小さく）
    silhouette_standing(overlay, int(W * 0.50), int(H * 0.92), height=320,
                        color=(20, 18, 18, 200), lean=0.0)

    arr = overlay_alpha(arr, overlay)
    arr = add_grain(arr, 4)
    arr = vignette(arr, strength=0.30, soft=1.3)
    arr = darken_bottom(arr, height_ratio=0.40, strength=0.20)
    return to_image(arr)


CHAPTER_BUILDERS = {
    'prologue': [
        ('title.jpg', title),
        ('office_day.jpg', office_day),
        ('meeting_room.jpg', meeting_room),
        ('office_night.jpg', office_night),
        ('meeting_crime.jpg', meeting_crime),
    ],
    'ch1': [
        ('corridor.jpg', corridor),
        ('server_room.jpg', server_room),
    ],
    'ch2': [
        ('bar.jpg', bar),
    ],
    'ch3': [
        ('client_office.jpg', client_office),
        ('rooftop.jpg', rooftop),
    ],
    'ch4': [
        ('cafe.jpg', cafe),
    ],
    'ch6': [
        ('presentation.jpg', presentation),
    ],
    'endings': [
        ('ending_a.jpg', ending_a),
        ('ending_b.jpg', ending_b),
        ('ending_c.jpg', ending_c),
        ('ending_d.jpg', ending_d),
    ],
}


def build(chapter: str):
    pairs = CHAPTER_BUILDERS.get(chapter)
    if not pairs:
        print(f'unknown chapter: {chapter}')
        return
    print(f'== building chapter: {chapter} ==')
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fn in pairs:
        print(f'  {name}')
        img = fn()
        save(img, name)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('chapter', nargs='?', default='prologue')
    args = p.parse_args()
    build(args.chapter)
