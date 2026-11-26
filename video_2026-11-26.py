# Vídeo 2026-11-26: "Las 3 excusas de Pechuga para no entrenar pierna" (CON voz)
# Formato: empezar con una frase que dice tu público y responderla.
# Crea una imagen por escena en assets/2026-11-26/ (para vidiq_compose)
#   python3 video_2026-11-26.py
import math, os
from PIL import Image, ImageDraw
import personaje as P
from video_ejemplo import FONDO, texto, pegar, gota, fuente, W, H

CARPETA = "assets/2026-11-26"
os.makedirs(CARPETA, exist_ok=True)
AZUL = (52, 92, 170)


def con_pantalon(pj):
    """Le pone a Pechuga un pantalón largo que tapa sus piernas finísimas."""
    pj = pj.copy()
    d = ImageDraw.Draw(pj)
    d.rounded_rectangle([262, 600, 438, 700], 20, fill=AZUL, outline=P.NEGRO, width=7)
    for x0 in (262, 356):
        d.rectangle([x0, 660, x0 + 82, 815], fill=AZUL, outline=P.NEGRO, width=7)
    return pj


def etiqueta(img, txt, y=600, color=P.ROJO):
    """Cartel rojo tipo «EXCUSA 1» inclinado."""
    f = fuente(70)
    capa = Image.new("RGBA", (560, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.rounded_rectangle([10, 10, 550, 140], 24, fill=color, outline=(0, 0, 0), width=8)
    d.text((280, 75), txt, font=f, fill="white", anchor="mm")
    capa = capa.rotate(6, expand=True, resample=Image.BICUBIC)
    img.paste(capa, (int(W / 2 - capa.width / 2), y), capa)


def bocadillo(img, frase, y, tam=60):
    """Bocadillo blanco con la frase de la excusa."""
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, y - 30, W - 90, y + 200], 50, fill="white", outline=(0, 0, 0), width=8)
    d.polygon([(330, y + 196), (420, y + 196), (300, y + 300)], fill="white", outline=(0, 0, 0))
    d.line([(330, y + 196), (420, y + 196)], fill="white", width=10)
    lineas, linea = [], ""
    f = fuente(tam)
    for p in frase.split():
        prueba = (linea + " " + p).strip()
        if d.textlength(prueba, font=f) > W - 230:
            lineas.append(linea)
            linea = p
        else:
            linea = prueba
    lineas.append(linea)
    yy = y + 85 - (len(lineas) - 1) * tam * 0.6
    for l in lineas:
        d.text((W / 2, yy), l, font=f, fill=(0, 0, 0), anchor="mm")
        yy += tam * 1.2


def sol(d, x, y, r=80):
    for k in range(12):
        a = k * math.pi / 6
        d.line([x + (r + 15) * math.cos(a), y + (r + 15) * math.sin(a),
                x + (r + 55) * math.cos(a), y + (r + 55) * math.sin(a)], fill=P.AMARILLO, width=12)
    d.ellipse([x - r, y - r, x + r, y + r], fill=P.AMARILLO, outline=(0, 0, 0), width=6)


# 1. Gancho
img = FONDO.copy()
d = ImageDraw.Draw(img)
for k in range(12):  # rayos de alarma
    a = k * math.pi / 6
    d.polygon([(W / 2, 1150), (W / 2 + 900 * math.cos(a), 1150 + 900 * math.sin(a)),
               (W / 2 + 900 * math.cos(a + 0.18), 1150 + 900 * math.sin(a + 0.18))],
              fill=(60, 70, 95))
pegar(img, P.dibujar(cara="miedo"), W / 2, 1640, 1.15)
for x, y in ((250, 900), (830, 860), (290, 1120)):
    gota(d, x, y)
texto(img, "Las 3 EXCUSAS de Pechuga para no hacer pierna", 280, tam=86)
img.save(f"{CARPETA}/1.png")

# 2. Excusa 1: con pantalón no se ve -> hasta que llega el verano
img = FONDO.copy()
d = ImageDraw.Draw(img)
sol(d, 880, 1050)
pegar(img, con_pantalon(P.dibujar(cara="orgulloso")), 430, 1620, 1.1)
etiqueta(img, "EXCUSA 1", 260)
bocadillo(img, "«Con pantalón no se ve»", 470)
d.text((790, 870), "¿Y en verano?", font=fuente(52), fill=P.AMARILLO, anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
img.save(f"{CARPETA}/2.png")

# 3. Excusa 2: ya subo escaleras -> vive en un primero
img = FONDO.copy()
d = ImageDraw.Draw(img)
gris = (110, 110, 120)
d.rectangle([180, 1410, 940, 1480], fill=gris, outline=(0, 0, 0), width=6)
d.rectangle([380, 1340, 940, 1410], fill=gris, outline=(0, 0, 0), width=6)
d.rectangle([150, 1060, 330, 1180], fill="white", outline=(0, 0, 0), width=6)
d.text((240, 1120), "1º", font=fuente(70), fill=(0, 0, 0), anchor="mm")
pegar(img, P.dibujar(cara="orgulloso"), 660, 1355, 0.8)
etiqueta(img, "EXCUSA 2", 260)
bocadillo(img, "«Ya hago pierna: subo escaleras»", 470)
img.save(f"{CARPETA}/3.png")

# 4. Excusa 3: tengo agujetas -> de hace 3 semanas
img = FONDO.copy()
d = ImageDraw.Draw(img)
x0, y0 = 650, 1000
d.rectangle([x0, y0, x0 + 340, y0 + 300], fill="white", outline=(0, 0, 0), width=8)
d.rectangle([x0, y0, x0 + 340, y0 + 80], fill=P.ROJO, outline=(0, 0, 0), width=8)
d.text((x0 + 170, y0 + 40), "PIERNA", font=fuente(46), fill="white", anchor="mm")
d.text((x0 + 170, y0 + 150), "hace 3", font=fuente(58), fill=(0, 0, 0), anchor="mm")
d.text((x0 + 170, y0 + 225), "semanas", font=fuente(58), fill=(0, 0, 0), anchor="mm")
pegar(img, P.dibujar(cara="miedo"), 360, 1620, 1.05)
etiqueta(img, "EXCUSA 3", 260)
bocadillo(img, "«Es que tengo agujetas»", 470)
img.save(f"{CARPETA}/4.png")

# 5. Cierre: dato correcto + pregunta
img = FONDO.copy()
d = ImageDraw.Draw(img)
for k in range(10):
    a = k * math.pi / 5
    d.regular_polygon((W / 2 + 460 * math.cos(a), 1150 + 420 * math.sin(a), 24), 4,
                      rotation=45, fill=P.AMARILLO)
pegar(img, P.dibujar(cara="normal"), W / 2, 1640, 1.1)
# flechas señalando las piernas
for s in (-1, 1):
    a, b = (W / 2 + s * 330, 1330), (W / 2 + s * 130, 1470)
    d.line([a, b], fill=P.AMARILLO, width=16)
    d.polygon([b, (b[0] + s * 55, b[1] - 5), (b[0] + s * 20, b[1] - 50)], fill=P.AMARILLO)
texto(img, "Las piernas tienen los músculos más grandes del cuerpo", 260, tam=70)
texto(img, "¿Cuál es TU excusa?", 560, tam=84, color=P.AMARILLO)
img.save(f"{CARPETA}/5.png")
print("hecho")
