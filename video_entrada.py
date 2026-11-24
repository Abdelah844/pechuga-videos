# Vídeo 2: "Cómo entra la gente normal al gym vs. cómo entra Pechuga"
# Crea una imagen por escena (1080x1920) en la carpeta assets/entrada/
import math, os
from PIL import Image, ImageDraw
import personaje as P
from video_ejemplo import FONDO, texto, pegar, gota, W, H

CARPETA = "assets/entrada"
os.makedirs(CARPETA, exist_ok=True)


def persona_normal(d, cx, base):
    # figura sencilla en gris: la "gente normal"
    gris, negro = (170, 175, 185), (35, 35, 40)
    d.ellipse([cx - 70, base - 560, cx + 70, base - 420], fill=gris, outline=negro, width=7)
    d.rounded_rectangle([cx - 90, base - 410, cx + 90, base - 160], 40, fill=gris, outline=negro, width=7)
    for dx in (-45, 45):
        d.line([cx + dx, base - 160, cx + dx, base], fill=negro, width=22)
    d.line([cx - 90, base - 380, cx - 140, base - 220], fill=negro, width=18)
    d.line([cx + 90, base - 380, cx + 140, base - 220], fill=negro, width=18)
    d.rectangle([cx + 120, base - 240, cx + 170, base - 170], fill=(60, 110, 200), outline=negro, width=5)  # botella


# Escena 1: la gente normal entra sin más
img = FONDO.copy()
persona_normal(ImageDraw.Draw(img), W / 2, 1560)
texto(img, "Cómo entra la gente normal al gym:", 220, tam=78)
img.save(f"{CARPETA}/1.png")

# Escena 2: Pechuga entra como el protagonista
img = FONDO.copy()
luz = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(luz).polygon([(W / 2 - 120, 0), (W / 2 + 120, 0), (W / 2 + 480, 1600), (W / 2 - 480, 1600)],
                            fill=(255, 230, 120, 70))
img.paste(luz, (0, 0), luz)
d = ImageDraw.Draw(img)
for k in range(10):
    a = k * math.pi / 5
    x, y = W / 2 + 470 * math.cos(a), 1050 + 430 * math.sin(a)
    d.regular_polygon((x, y, 26), 4, rotation=45, fill=P.AMARILLO)
pegar(img, P.dibujar(pecho=1.5, cara="orgulloso", brazos="arriba"), W / 2, 1640, 1.25)
texto(img, "Cómo entra Pechuga:", 220, tam=86)
img.save(f"{CARPETA}/2.png")

# Escena 3: Pechuga huye al ver que toca pierna
img = FONDO.copy()
d = ImageDraw.Draw(img)
d.rectangle([90, 640, 420, 940], fill="white", outline="black", width=8)
d.rectangle([90, 640, 420, 720], fill=P.ROJO, outline="black", width=8)
from video_ejemplo import fuente
d.text((255, 680), "HOY", font=fuente(50), fill="white", anchor="mm")
d.text((255, 830), "PIERNA", font=fuente(62), fill="black", anchor="mm")
for k in range(6):  # líneas de velocidad
    y = 1050 + k * 80
    d.line([80, y, 380, y], fill=(220, 220, 230), width=10)
pegar(img, P.dibujar(cara="miedo"), 700, 1600, 1.15)
for x, y in ((520, 900), (880, 950), (560, 1150)):
    gota(d, x, y)
texto(img, "Cómo sale Pechuga cuando ve que toca pierna:", 220, tam=72)
img.save(f"{CARPETA}/3.png")

# Escena 4: cierre
img = FONDO.copy()
pegar(img, P.dibujar(pecho=1.5, cara="orgulloso", brazos="arriba"), W / 2, 1600, 1.1)
texto(img, "¿Tú cuál eres?", 260, tam=96)
texto(img, "Sigue a Pechuga para más", 1690, tam=58, color=P.AMARILLO)
img.save(f"{CARPETA}/4.png")
print("hecho")
