import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import personaje as P

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fuente(t):
    return ImageFont.truetype(F, t)


def fondo():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([0, y, W, y], fill=(int(30 + 20 * t), int(42 + 20 * t), int(58 + 25 * t)))
    d.rectangle([0, 1480, W, H], fill=(58, 58, 64))
    d.line([0, 1480, W, 1480], fill=(30, 30, 34), width=8)
    # estanteria de mancuernas al fondo
    d.rectangle([60, 1230, 1020, 1250], fill=(25, 30, 40))
    for i in range(7):
        x = 120 + i * 135
        d.rectangle([x - 30, 1180, x - 10, 1230], fill=(20, 22, 28))
        d.rectangle([x + 10, 1180, x + 30, 1230], fill=(20, 22, 28))
        d.rectangle([x - 10, 1198, x + 10, 1212], fill=(20, 22, 28))
    return img


def texto(img, frase, y, tam=72, color=(255, 255, 255), ancho=900):
    d = ImageDraw.Draw(img)
    f = fuente(tam)
    lineas, linea = [], ""
    for p in frase.split():
        prueba = (linea + " " + p).strip()
        if d.textlength(prueba, font=f) > ancho:
            lineas.append(linea)
            linea = p
        else:
            linea = prueba
    lineas.append(linea)
    for l in lineas:
        w = d.textlength(l, font=f)
        d.text(((W - w) / 2, y), l, font=f, fill=color, stroke_width=8, stroke_fill=(0, 0, 0))
        y += int(tam * 1.2)


def pegar(img, pj, cx, base, escala=1.0):
    if escala != 1.0:
        pj = pj.resize((int(pj.width * escala), int(pj.height * escala)), Image.LANCZOS)
    img.paste(pj, (int(cx - pj.width / 2), int(base - pj.height)), pj)


def gota(d, x, y, r=22):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 200, 255), outline=(0, 0, 0), width=5)
    d.polygon([(x - r + 4, y - 6), (x + r - 4, y - 6), (x, y - r * 2.4)], fill=(120, 200, 255))


FONDO = fondo()
NORMAL = P.dibujar()
MIEDO = P.dibujar(cara="miedo")
ORGULLO = P.dibujar(cara="orgulloso")
CHETADO = P.dibujar(pecho=1.5, cara="orgulloso", brazos="arriba")


def escena1(i):  # 0-3 s
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    # calendario en la pared
    z = 1 + 0.08 * max(0, math.sin((t - 1.5) * 8)) if t > 1.5 else 1
    x0, y0 = 650, 640
    w, h = int(330 * z), int(300 * z)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 255, 255), outline=(0, 0, 0), width=8)
    d.rectangle([x0, y0, x0 + w, y0 + int(80 * z)], fill=P.ROJO, outline=(0, 0, 0), width=8)
    f = fuente(int(50 * z))
    d.text((x0 + w / 2, y0 + 40 * z), "HOY", font=f, fill="white", anchor="mm")
    d.text((x0 + w / 2, y0 + 190 * z), "PIERNA", font=fuente(int(62 * z)), fill=(0, 0, 0), anchor="mm")
    bob = 8 * math.sin(t * 6)
    pegar(img, NORMAL if t < 1.5 else MIEDO, 340, 1580 + bob, 1.1)
    texto(img, "Pechuga cuando ve que hoy toca pierna", 200)
    return img


def escena2(i):  # 2,5 s
    t = i / FPS
    img = FONDO.copy()
    sx = 10 * math.sin(t * 70)  # tiembla
    pegar(img, MIEDO, W / 2 + sx, 2050, 1.7)
    d = ImageDraw.Draw(img)
    for k, (x, y) in enumerate([(250, 700), (840, 760), (300, 1000)]):
        caida = ((t * 300) + k * 120) % 400
        gota(d, x, y + caida)
    texto(img, "*sudor frío*", 220, tam=90)
    return img


def escena3(i):  # 3,5 s
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    # banco de press
    d.rectangle([560, 1290, 1000, 1350], fill=(40, 40, 46), outline=(0, 0, 0), width=6)
    d.rectangle([600, 1350, 630, 1480], fill=(30, 30, 34))
    d.rectangle([930, 1350, 960, 1480], fill=(30, 30, 34))
    d.rectangle([700, 1000, 720, 1290], fill=(30, 30, 34))
    d.rectangle([840, 1000, 860, 1290], fill=(30, 30, 34))
    d.line([560, 1000, 1000, 1000], fill=(190, 190, 200), width=18)
    for x in (585, 975):
        d.rectangle([x - 25, 900, x + 25, 1100], fill=P.ROJO, outline=(0, 0, 0), width=6)
    bob = 6 * math.sin(t * 5)
    pegar(img, ORGULLO, 290, 1580 + bob, 1.0)
    texto(img, "«Hoy hago pecho otra vez. La pierna no se ve con pantalón»", 200, tam=66)
    return img


def escena4(i):  # 3,5 s
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    # destellos
    for k in range(8):
        a = k * math.pi / 4 + t
        r = 560 + 30 * math.sin(t * 6 + k)
        x, y = W / 2 + r * math.cos(a), 1000 + r * 0.9 * math.sin(a)
        d.regular_polygon((x, y, 22), 4, rotation=45, fill=P.AMARILLO)
    z = min(1, 0.6 + t * 2)  # aparece creciendo
    pegar(img, CHETADO, W / 2, 1640, 1.3 * z)
    texto(img, "6 meses después:", 200, tam=86)
    if t > 1.6:
        texto(img, "¿Tú también te saltas la pierna?", 1650, tam=60, color=P.AMARILLO)
    return img


ESCENAS = [(escena1, 3.0), (escena2, 2.5), (escena3, 3.5), (escena4, 3.5)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prueba":
        for n, (fn, dur) in enumerate(ESCENAS):
            fn(int(dur * FPS * 0.75)).save(f"prueba{n + 1}.png")
        sys.exit()
    for n, (fn, dur) in enumerate(ESCENAS):
        tmp, fin = f"tmp_e{n}.mp4", f"e{n}.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "20",
                              "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)):
            p.stdin.write(fn(i).tobytes())
        p.stdin.close()
        if p.wait() == 0:
            import os
            os.replace(tmp, fin)
