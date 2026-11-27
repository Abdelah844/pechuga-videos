# Vídeo 2026-11-27b: "El trend del corazón con el bíceps, versión Pechuga" (SIN voz)
# Tendencia: #BicepHeart (flexionar el brazo para que el bíceps dibuje un corazón).
# Idea original: Pechuga lo intenta con el bíceps (le sale roto), con las piernas
# (no llega) y al final lo hace con... la pechuga.
#   python3 video_2026-11-27b.py prueba   -> guarda una imagen por escena en prueba/
#   python3 video_2026-11-27b.py          -> crea videos/2026-11-27b.mp4 (con ritmo propio)
import math, os, subprocess, sys
from PIL import Image, ImageDraw
import personaje as P
from video_ejemplo import FONDO, texto, pegar, gota, fuente, W, H, FPS

SALIDA = "videos/2026-11-27b.mp4"
Y_TITULO = 330  # más abajo para que no se corte en la cuadrícula del perfil
ROSA = (255, 80, 140)

NORMAL = P.dibujar()
MIEDO = P.dibujar(cara="miedo")
FLEX = P.dibujar(cara="orgulloso", brazos="arriba")
CHETADO = P.dibujar(pecho=1.5, cara="orgulloso", brazos="arriba")


def corazon(d, cx, cy, tam, color=ROSA, roto=False, borde=8):
    """Corazón con la curva clásica. tam = medio ancho aprox."""
    k = tam / 17
    pts = []
    for n in range(80):
        a = 2 * math.pi * n / 80
        x = 16 * math.sin(a) ** 3
        y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((cx + x * k, cy - y * k))
    d.polygon(pts, fill=color, outline=(0, 0, 0), width=borde)
    if roto:  # grieta en zigzag
        z = [(cx, cy - 5 * k), (cx - 3 * k, cy), (cx + 3 * k, cy + 4 * k), (cx - 2 * k, cy + 8 * k),
             (cx, cy + 14 * k)]
        d.line(z, fill=(0, 0, 0), width=borde + 2)


def titulo(img, frase, color=(255, 255, 255), tam=80):
    texto(img, frase, Y_TITULO, tam=tam, color=color)


def flash(img, i):
    if i < 2:
        img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.7 if i == 0 else 0.35)
    return img


def golpe(i):
    return 1 + 0.12 * math.exp(-(i / FPS) * 8)


def escena1(i):  # gancho: el bíceps no da para corazón
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    pegar(img, FLEX, W / 2 + 20, 1640 + 6 * math.sin(t * 6), 1.0)
    if t > 1.0:  # aparece un corazón roto y pequeño
        z = min(1, (t - 1.0) * 4)
        corazon(ImageDraw.Draw(img), 160, 1100, 75 * z, roto=True, borde=6)
        d.text((160, 1230), "¿?", font=fuente(70), fill="white", anchor="mm",
               stroke_width=6, stroke_fill=(0, 0, 0))
    titulo(img, "El trend del corazón con el bíceps, versión Pechuga:")
    return flash(img, i)


def escena2(i):  # con las piernas: imposible
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    sx = 8 * math.sin(t * 60)  # tiembla
    pegar(img, MIEDO, W / 2 - 40 + sx, 1640, 1.15)
    # lupa sobre las piernas
    lx, ly = W / 2 - 40, 1470
    d.ellipse([lx - 110, ly - 110, lx + 110, ly + 110], outline=(240, 240, 240), width=16)
    d.line([lx + 78, ly + 78, lx + 190, ly + 190], fill=(240, 240, 240), width=26)
    corazon(d, lx, ly, 22 + 2 * math.sin(t * 8), borde=4)
    for k, (x, y) in enumerate([(250, 820), (700, 780)]):
        gota(d, x, y + ((t * 260) + k * 150) % 300)
    titulo(img, "Con las piernas… no hay material")
    return flash(img, i)


def escena3(i):  # plan B: con la pechuga
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    for k in range(12):  # rayos
        a = k * math.pi / 6 + t * 1.2
        d.polygon([(W / 2, 1150), (W / 2 + 1100 * math.cos(a), 1150 + 1100 * math.sin(a)),
                   (W / 2 + 1100 * math.cos(a + 0.16), 1150 + 1100 * math.sin(a + 0.16))],
                  fill=(80, 60, 95))
    s = 1.25 * golpe(i)
    base = 1690
    pegar(img, CHETADO, W / 2 - 40, base, s)
    # corazón latiendo en el pecho (el pecho en el dibujo está a y≈900 de 1800)
    late = 1 + 0.08 * max(0, math.sin(t * 9))
    alto = 900 * s
    cy = base - alto + 450 * s
    corazon(ImageDraw.Draw(img), W / 2 - 40, cy, 170 * s * late, borde=10)
    for k in range(6):  # corazoncitos que suben
        x = 160 + k * 150
        y = 1300 - ((t * 220 + k * 90) % 600)
        corazon(d, x, y, 26, borde=4)
    titulo(img, "Plan B: con la PECHUGA", color=P.AMARILLO, tam=88)
    return flash(img, i)


def escena4(i):  # cierre con pregunta
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    pegar(img, CHETADO, 420 + 5 * math.sin(t * 6), 1640, 0.9)
    corazon(d, 820, 1050, 90 * (1 + 0.08 * max(0, math.sin(t * 9))), borde=8)
    texto(img, "Pierna: 0", Y_TITULO - 20, tam=80)
    texto(img, "Pecho: 100", Y_TITULO + 80, tam=80, color=P.AMARILLO)
    if t > 0.6:
        texto(img, "¿A quién le mandas este corazón?", 640, tam=70, color=P.AMARILLO)
    return flash(img, i)


# Cortes en múltiplos de 0,5 s (ritmo de 120 ppm)
ESCENAS = [(escena1, 3.0), (escena2, 3.0), (escena3, 3.5), (escena4, 4.0)]


def ritmo(segundos, ruta):
    """Ritmo original con ffmpeg (sin música con derechos): bombo, palmada, charles
    y una melodía nueva en tonos medios para que se oiga en el móvil."""
    b = 0.5
    notas = [523, 659, 784, 659, 587, 698, 880, 698]
    n = "floor(mod(t,2)*4)"
    f = str(notas[-1])
    for k in range(len(notas) - 2, -1, -1):
        f = f"if(eq({n},{k}),{notas[k]},{f})"
    env = "exp(-mod(t,0.25)*9)"
    expr = (f"0.45*sin(2*PI*mod(t,{b})*(60+140*exp(-mod(t,{b})*30)))*exp(-mod(t,{b})*9)"
            f"+0.35*(random(0)*2-1)*exp(-mod(t+0.5,1)*22)"
            f"+0.16*(random(1)*2-1)*exp(-mod(t+0.125,0.25)*70)"
            f"+0.22*(sin(2*PI*({f})*t)+0.3*sin(4*PI*({f})*t))*{env}")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    f"aevalsrc='{expr}':s=44100:d={segundos}",
                    "-af", f"loudnorm=I=-14:TP=-1.5,afade=t=out:st={segundos - 1}:d=1",
                    "-ar", "44100", ruta], check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prueba":
        os.makedirs("prueba", exist_ok=True)
        for n, (fn, dur) in enumerate(ESCENAS):
            fn(int(dur * FPS * 0.6)).convert("RGB").save(f"prueba/{n + 1}.png")
        sys.exit()
    os.makedirs("videos", exist_ok=True)
    total = sum(d for _, d in ESCENAS)
    ritmo(total, "tmp_ritmo.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "tmp_ritmo.wav",
                          "-c:v", "libx264", "-crf", "21", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", SALIDA],
                         stdin=subprocess.PIPE)
    for fn, dur in ESCENAS:
        for i in range(int(dur * FPS)):
            p.stdin.write(fn(i).convert("RGB").tobytes())
    p.stdin.close()
    p.wait()
    os.remove("tmp_ritmo.wav")
    print("hecho:", SALIDA)
