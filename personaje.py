from PIL import Image, ImageDraw

NEGRO = (35, 35, 40)
CREMA = (255, 246, 226)
CREMA2 = (255, 236, 200)
ROJO = (229, 57, 53)
AMARILLO = (255, 193, 7)
NARANJA = (242, 150, 40)
BLANCO = (255, 255, 255)
L = 14  # grosor del contorno (a tamano doble)


def elipse(d, cx, cy, rx, ry, color, borde=True):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color,
              outline=NEGRO if borde else None, width=L if borde else 0)


def dibujar(pecho=1.0, cara="normal", brazos="abajo"):
    """Dibuja a Pechuga y devuelve una imagen RGBA de 700x900."""
    W, H = 1400, 1800
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = 700
    rx = int(330 * pecho)  # el cuerpo crece con el pecho

    # piernas finisimas (el chiste del personaje)
    for x in (cx - 70, cx + 70):
        d.line([x, 1250, x, 1620], fill=NARANJA, width=16)
        for dx in (-45, 0, 45):
            d.line([x, 1620, x + dx, 1665], fill=NARANJA, width=14)

    # alas / brazos
    if brazos == "arriba":  # sacando musculo
        for s in (-1, 1):
            hombro = (cx + s * int(rx * 0.75), 860)
            codo = (cx + s * (rx + 110), 700)
            mano = (cx + s * (rx + 60), 470)
            for a, b in ((hombro, codo), (codo, mano)):
                d.line([a, b], fill=NEGRO, width=150)
                d.line([a, b], fill=CREMA, width=122)
            elipse(d, codo[0] - s * 20, codo[1] - 70, 95, 80, CREMA)  # biceps
            elipse(d, mano[0], mano[1], 65, 65, CREMA)
    else:
        for s in (-1, 1):
            elipse(d, cx + s * (rx + 30), 1000, 75, 170, CREMA)

    # cuerpo y pechuga
    elipse(d, cx, 950, rx, 360, CREMA)
    pr = int(165 * pecho)
    for s in (-1, 1):
        elipse(d, cx + s * int(150 * pecho), 900, pr, int(130 * pecho), CREMA2)

    # cabeza
    elipse(d, cx - 90, 330, 70, 70, ROJO)
    elipse(d, cx, 300, 80, 80, ROJO)
    elipse(d, cx + 90, 330, 70, 70, ROJO)
    elipse(d, cx, 520, 240, 230, CREMA)
    # cinta del pelo (su seña de identidad)
    d.rectangle([cx - 238, 380, cx + 238, 440], fill=ROJO, outline=NEGRO, width=L)
    d.rectangle([cx - 230, 402, cx + 230, 418], fill=BLANCO)

    # ojos
    for s in (-1, 1):
        ox = cx + s * 85
        if cara == "orgulloso":
            d.arc([ox - 55, 470, ox + 55, 580], 200, 340, fill=NEGRO, width=L + 4)
            d.line([ox - 55, 465, ox + 50, 455 + (s * 12)], fill=NEGRO, width=L)
        else:
            elipse(d, ox, 525, 58, 62, BLANCO)
            pr2 = 14 if cara == "miedo" else 28
            elipse(d, ox, 530, pr2, pr2, NEGRO, borde=False)
            if cara == "miedo":
                d.line([ox - 50, 440 + 5, ox + 50, 452 - s * 14], fill=NEGRO, width=L)

    # pico
    d.polygon([(cx - 55, 600), (cx + 55, 600), (cx, 690)], fill=AMARILLO,
              outline=NEGRO, width=L)
    if cara == "miedo":
        d.line([cx - 40, 640, cx + 40, 640], fill=NEGRO, width=8)
    elipse(d, cx + 10, 725, 28, 40, ROJO)  # moco del pollo

    return img.resize((700, 900), Image.LANCZOS)
