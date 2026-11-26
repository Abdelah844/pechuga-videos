# Vídeo 2026-11-26b: "Siempre hay energía para el día de pecho" (SIN voz)
# Formato: cortes rápidos al ritmo, "mi energía para X:" (idea de la tendencia
# "Always energy for chest day", adaptada a Pechuga con una batería).
#   python3 video_2026-11-26b.py prueba   -> guarda una imagen por escena en prueba/
#   python3 video_2026-11-26b.py          -> crea videos/2026-11-26b.mp4 (con ritmo propio)
import math, os, subprocess, sys
from PIL import Image, ImageDraw
import personaje as P
from video_ejemplo import FONDO, texto, pegar, gota, fuente, W, H, FPS

SALIDA = "videos/2026-11-26b.mp4"
Y_TITULO = 330  # más abajo para que no se corte en la cuadrícula del perfil
VERDE = (76, 200, 80)

NORMAL = P.dibujar()
MIEDO = P.dibujar(cara="miedo")
CHETADO = P.dibujar(pecho=1.5, cara="orgulloso", brazos="arriba")


def bateria(img, cx, cy, nivel, etiqueta, color, z=1.0):
    """Batería grande. nivel de 0 a 1 (puede pasar de 1: se sale)."""
    d = ImageDraw.Draw(img)
    w, h = 420 * z, 200 * z
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], int(30 * z), fill=(30, 30, 36), outline="white", width=int(12 * z))
    d.rounded_rectangle([x0 + w, cy - 40 * z, x0 + w + 36 * z, cy + 40 * z], int(10 * z), fill="white")
    m = 24 * z
    largo = (w - 2 * m) * min(nivel, 1.0)
    if largo > 4:
        d.rounded_rectangle([x0 + m, y0 + m, x0 + m + largo, y0 + h - m], int(14 * z), fill=color)
    d.text((cx, cy), etiqueta, font=fuente(int(80 * z)), fill="white", anchor="mm",
           stroke_width=7, stroke_fill=(0, 0, 0))


def titulo(img, frase, color=(255, 255, 255)):
    texto(img, frase, Y_TITULO, tam=84, color=color)


def flash(img, i):
    """Destello blanco en los 2 primeros fotogramas de cada escena (corte rápido)."""
    if i < 2:
        capa = Image.new("RGB", img.size, (255, 255, 255))
        img = Image.blend(img, capa, 0.7 if i == 0 else 0.35)
    return img


def zoom_entrada(i):
    t = i / FPS
    return 1 + 0.12 * math.exp(-t * 8)  # pequeño "golpe" al entrar


def escena_baja(frase, nivel, etiqueta, cara, extra=None):
    def fn(i):
        t = i / FPS
        img = FONDO.copy()
        d = ImageDraw.Draw(img)
        z = zoom_entrada(i)
        parpadeo = (int(t * 4) % 2 == 0)
        bateria(img, 470, 660, nivel, etiqueta, P.ROJO if parpadeo else (150, 30, 30), z)
        caida = 6 * math.sin(t * 3)
        pegar(img, cara, 420, 1620 + caida, 0.95)
        if extra:
            extra(d, t)
        titulo(img, frase)
        return flash(img, i)
    return fn


def sudor(d, t):
    for k, (x, y) in enumerate([(220, 1080), (640, 1060)]):
        gota(d, x, y + ((t * 260) + k * 150) % 320)


def zzz(d, t):
    for k in range(3):
        y = 1150 - ((t * 120 + k * 70) % 210)
        d.text((660 + k * 40, y), "z", font=fuente(70 + k * 15), fill="white", anchor="mm",
               stroke_width=6, stroke_fill=(0, 0, 0))


escena1 = escena_baja("Mi energía para PIERNA:", 0.03, "1%", MIEDO, sudor)
escena2 = escena_baja("Mi energía para CARDIO:", 0.0, "0%", MIEDO, zzz)
escena3 = escena_baja("Mi energía para ESTIRAR:", 0.0, "-5%", NORMAL, zzz)


def escena4(i):  # día de pecho
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    for k in range(12):  # rayos de energía
        a = k * math.pi / 6 + t * 1.5
        d.polygon([(W / 2, 1150), (W / 2 + 1000 * math.cos(a), 1150 + 1000 * math.sin(a)),
                   (W / 2 + 1000 * math.cos(a + 0.16), 1150 + 1000 * math.sin(a + 0.16))],
                  fill=(70, 80, 110))
    z = zoom_entrada(i) * (1 + 0.03 * math.sin(t * 25))
    bateria(img, 470, 660, 1.0, "999%", VERDE, z)
    for x, y in ((150, 640), (800, 640)):  # rayos a los lados de la batería
        y += 10 * math.sin(t * 20)
        d.polygon([(x + 40, y - 70), (x - 10, y + 10), (x + 20, y + 10), (x - 10, y + 80),
                   (x + 60, y - 10), (x + 28, y - 10)], fill=P.AMARILLO, outline=(0, 0, 0), width=4)
    sx = 6 * math.sin(t * 50)
    pegar(img, CHETADO, W / 2 - 40 + sx, 1650, 1.05)
    for k in range(8):
        a = k * math.pi / 4 + t * 2
        x, y = W / 2 - 40 + 480 * math.cos(a), 1200 + 380 * math.sin(a)
        d.regular_polygon((x, y, 22), 4, rotation=45, fill=P.AMARILLO)
    titulo(img, "Mi energía para PECHO:", P.AMARILLO)
    return flash(img, i)


def escena5(i):  # cierre con pregunta
    t = i / FPS
    img = FONDO.copy()
    d = ImageDraw.Draw(img)
    pegar(img, CHETADO, 420 + 5 * math.sin(t * 6), 1640, 0.9)
    texto(img, "Siempre hay energía para el día de pecho", Y_TITULO, tam=78)
    if t > 0.6:
        texto(img, "¿Y tú? ¿Para qué día SIEMPRE tienes energía?", 640, tam=66, color=P.AMARILLO)
    return flash(img, i)


# Cortes en múltiplos de 0,5 s para que caigan en el ritmo (120 ppm)
ESCENAS = [(escena1, 2.5), (escena2, 2.0), (escena3, 2.0), (escena4, 3.5), (escena5, 4.0)]


def ritmo(segundos, ruta):
    """Ritmo original hecho con ffmpeg (sin música con derechos): bombo + palmada +
    charles + melodía en tonos medios/agudos para que se oiga en el móvil.
    Melodía nueva, distinta de los vídeos anteriores."""
    b = 0.5
    notas = [440, 440, 523, 587, 659, 587, 523, 784]
    n = "floor(mod(t,2)*4)"
    f = str(notas[-1])
    for k in range(len(notas) - 2, -1, -1):
        f = f"if(eq({n},{k}),{notas[k]},{f})"
    env = "exp(-mod(t,0.25)*10)"
    expr = (f"0.45*sin(2*PI*mod(t,{b})*(60+140*exp(-mod(t,{b})*30)))*exp(-mod(t,{b})*9)"
            f"+0.35*(random(0)*2-1)*exp(-mod(t+0.5,1)*22)"
            f"+0.18*(random(1)*2-1)*exp(-mod(t+0.125,0.25)*70)"
            f"+0.22*(sin(2*PI*({f})*t)+0.35*sin(4*PI*({f})*t))*{env}")
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
