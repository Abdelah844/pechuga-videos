# Vídeo 2026-11-27: "El del móvil en el banco de press" (CON voz)
# Formato: POV de situación del gym que todos han vivido + plan B con consejo correcto.
# Crea una imagen por escena en assets/2026-11-27/ (para vidiq_compose)
#   python3 video_2026-11-27.py
import math, os
from PIL import Image, ImageDraw, ImageOps
import personaje as P
from video_ejemplo import FONDO, texto, pegar, gota, fuente, W, H

CARPETA = "assets/2026-11-27"
os.makedirs(CARPETA, exist_ok=True)
Y = 330  # títulos más abajo para que no se corten en el perfil


def pollo_gris(cara="normal"):
    """Otro pollo del gym (gris) para que no se confunda con Pechuga."""
    pj = P.dibujar(cara=cara)
    alfa = pj.getchannel("A")
    gris = ImageOps.colorize(pj.convert("L"), black=P.NEGRO, white=(190, 200, 215)).convert("RGBA")
    gris.putalpha(alfa)
    return gris


def banco(d, x=560):
    """Banco de press con barra y discos (como en video_ejemplo)."""
    d.rectangle([x, 1290, x + 440, 1350], fill=(40, 40, 46), outline=(0, 0, 0), width=6)
    d.rectangle([x + 40, 1350, x + 70, 1480], fill=(30, 30, 34))
    d.rectangle([x + 370, 1350, x + 400, 1480], fill=(30, 30, 34))
    d.rectangle([x + 140, 1000, x + 160, 1290], fill=(30, 30, 34))
    d.rectangle([x + 280, 1000, x + 300, 1290], fill=(30, 30, 34))
    d.line([x, 1000, x + 440, 1000], fill=(190, 190, 200), width=18)
    for xx in (x + 25, x + 415):
        d.rectangle([xx - 25, 900, xx + 25, 1100], fill=P.ROJO, outline=(0, 0, 0), width=6)


def movil(d, x, y):
    """Móvil con brillo azul en la cara."""
    d.rounded_rectangle([x - 45, y - 75, x + 45, y + 75], 14, fill=(30, 30, 36), outline=(0, 0, 0), width=6)
    d.rounded_rectangle([x - 33, y - 60, x + 33, y + 60], 8, fill=(120, 200, 255))


def reloj(img, cx, cy, txt):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], fill="white", outline=(0, 0, 0), width=10)
    d.line([cx, cy, cx, cy - 75], fill=(0, 0, 0), width=10)
    d.line([cx, cy, cx + 55, cy + 20], fill=P.ROJO, width=10)
    d.text((cx, cy + 160), txt, font=fuente(58), fill=P.AMARILLO, anchor="mm",
           stroke_width=7, stroke_fill=(0, 0, 0))


def bocadillo(img, frase, x0, y0, x1, y1, cola):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x1, y1], 40, fill="white", outline=(0, 0, 0), width=8)
    d.polygon(cola, fill="white", outline=(0, 0, 0))
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), frase, font=fuente(50), fill=(0, 0, 0), anchor="mm")


GRIS = pollo_gris()

# 1. Gancho: Pechuga esperando
img = FONDO.copy()
d = ImageDraw.Draw(img)
banco(d)
pegar(img, GRIS, 780, 1300, 0.62)
movil(d, 850, 1030)
pegar(img, P.dibujar(cara="miedo"), 290, 1620, 0.85)
reloj(img, 290, 760, "20 min")
texto(img, "POV: llevas 20 minutos esperando el banco", Y, tam=80)
img.save(f"{CARPETA}/1.png")

# 2. Primer plano del del móvil
img = FONDO.copy()
d = ImageDraw.Draw(img)
banco(d, 320)
pegar(img, GRIS, 540, 1330, 0.9)
movil(d, 620, 1010)
for k in range(5):  # destellos del móvil
    a = -math.pi / 2 + (k - 2) * 0.35
    d.line([620 + 100 * math.cos(a), 900 + 100 * math.sin(a),
            620 + 170 * math.cos(a), 900 + 170 * math.sin(a)], fill=(120, 200, 255), width=10)
texto(img, "Y él… con el móvil", Y, tam=84)
img.save(f"{CARPETA}/2.png")

# 3. "Me queda una serie" (hace 15 min)
img = FONDO.copy()
d = ImageDraw.Draw(img)
banco(d)
pegar(img, GRIS, 780, 1300, 0.62)
movil(d, 850, 1030)
bocadillo(img, "«Me queda una serie»", 260, 640, 1020, 780, [(700, 776), (780, 776), (800, 880)])
pegar(img, P.dibujar(cara="miedo"), 290, 1620, 0.85)
for x, y in ((150, 1100), (440, 1060)):
    gota(d, x, y)
texto(img, "Hace 15 minutos…", Y, tam=84)
img.save(f"{CARPETA}/3.png")

# 4. Plan B: press con mancuernas (consejo correcto)
img = FONDO.copy()
d = ImageDraw.Draw(img)
pegar(img, P.dibujar(pecho=1.3, cara="orgulloso", brazos="arriba"), W / 2, 1640, 1.0)
for x in (295, 785):  # mancuernas en las manos
    y = 960
    d.rectangle([x - 75, y - 12, x + 75, y + 12], fill=(150, 150, 160), outline=(0, 0, 0), width=5)
    for dx in (-75, 75):
        d.rectangle([x + dx - 22, y - 55, x + dx + 22, y + 55], fill=(40, 40, 46), outline=(0, 0, 0), width=5)
texto(img, "Plan B: press con mancuernas", Y, tam=84, color=P.AMARILLO)
texto(img, "También trabaja el pecho", 560, tam=66)
img.save(f"{CARPETA}/4.png")

# 5. Cierre con pregunta
img = FONDO.copy()
d = ImageDraw.Draw(img)
for k in range(10):
    a = k * math.pi / 5
    d.regular_polygon((W / 2 + 460 * math.cos(a), 1180 + 400 * math.sin(a), 24), 4,
                      rotation=45, fill=P.AMARILLO)
pegar(img, P.dibujar(cara="normal"), W / 2, 1640, 1.0)
texto(img, "¿Qué haces tú cuando te ocupan la máquina?", Y, tam=80, color=P.AMARILLO)
img.save(f"{CARPETA}/5.png")
print("hecho")
