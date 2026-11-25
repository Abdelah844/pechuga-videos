# Vídeo 2026-11-25: "El error de Pechuga en sentadilla"
# Formato: "haz la repetición mal y luego corrígela" (bad rep -> fix)
# Uso:
#   python3 video_2026-11-25.py prueba   -> guarda una imagen de cada escena
#   python3 video_2026-11-25.py          -> crea videos/2026-11-25.mp4 (con ritmo de fondo)
import math, os, subprocess, sys
from PIL import Image, ImageDraw
import personaje as P
from video_ejemplo import FONDO, texto, pegar, gota, fuente, W, H, FPS

SALIDA = "videos/2026-11-25.mp4"
SUELO = 1560  # donde apoyan los pies


def cuerpo_sin_piernas(**kw):
    """Pechuga recortado justo encima de las piernas, para dibujarlas dobladas."""
    pj = P.dibujar(**kw)
    return pj.crop((0, 0, pj.width, 650))


NORMAL = cuerpo_sin_piernas()
MIEDO = cuerpo_sin_piernas(cara="miedo")
ORGULLO = cuerpo_sin_piernas(cara="orgulloso")
ESC = 1.25  # escala del personaje


def pechuga_sentadilla(img, cx, prof, cuerpo, barra=True, tiembla=0.0):
    """Dibuja a Pechuga con las piernas dobladas. prof: 0 = de pie, 1 = muslo paralelo."""
    d = ImageDraw.Draw(img)
    s_ = ESC
    espinilla, muslo = 110 * s_, 100 * s_
    ys = SUELO
    alto_rodilla = espinilla * (1 - 0.15 * prof)
    alto_cadera = alto_rodilla + muslo * (1 - 0.95 * prof)
    cadera_y = ys - alto_cadera
    for s in (-1, 1):
        t = tiembla * math.sin(pygame_t[0] * 60 + s)  # temblor de piernas
        pie = (cx + s * 55 * s_, ys)
        rodilla = (cx + s * (55 + 85 * prof) * s_ + t, ys - alto_rodilla)
        cadera = (cx + s * 35 * s_, cadera_y)
        d.line([cadera, rodilla, pie], fill=P.NARANJA, width=10, joint="curve")
        for dx in (-25, 0, 25):
            d.line([pie, (pie[0] + dx * s_, pie[1] + 22)], fill=P.NARANJA, width=8)
    c = cuerpo.resize((int(cuerpo.width * s_), int(cuerpo.height * s_)), Image.LANCZOS)
    top = int(cadera_y + 15 - c.height)
    if barra:  # barra por detrás de la cabeza, a la altura de los hombros
        by = top + int(330 * s_)
        d.line([cx - 340, by, cx + 340, by], fill=(190, 190, 200), width=18)
        for x in (cx - 310, cx + 310):
            d.rectangle([x - 28, by - 110, x + 28, by + 110], fill=P.ROJO, outline=(0, 0, 0), width=6)
    img.paste(c, (int(cx - c.width / 2), top), c)


pygame_t = [0.0]  # tiempo actual, para el temblor


def sello(img, simbolo, cx, cy, r, color):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color, outline=(0, 0, 0), width=10)
    if simbolo == "x":
        k = r * 0.5
        for a, b in (((cx - k, cy - k), (cx + k, cy + k)), ((cx - k, cy + k), (cx + k, cy - k))):
            d.line([a, b], fill="white", width=int(r * 0.22))
    else:
        d.line([(cx - r * 0.5, cy), (cx - r * 0.12, cy + r * 0.4), (cx + r * 0.55, cy - r * 0.45)],
               fill="white", width=int(r * 0.22), joint="curve")


def escena1(i):  # gancho: la X roja aparece de golpe
    t = i / FPS
    pygame_t[0] = t
    img = FONDO.copy()
    pechuga_sentadilla(img, 440, 0.05 + 0.05 * abs(math.sin(t * 5)), ORGULLO)
    texto(img, "El ERROR que hace Pechuga en sentadilla", 200, tam=80)
    if t > 0.4:
        z = min(1.0, (t - 0.4) * 6)
        r = int(120 * (2 - z))  # entra grande y se asienta
        sello(img, "x", 880, 640, r, P.ROJO)
    return img


def escena2(i):  # la repetición mala: baja 2 cm
    t = i / FPS
    pygame_t[0] = t
    img = FONDO.copy()
    prof = 0.08 * (0.5 - 0.5 * math.cos(t * 4))
    pechuga_sentadilla(img, 440, prof, ORGULLO)
    d = ImageDraw.Draw(img)
    # flecha diminuta: "2 cm"
    d.line([800, 1150, 800, 1230], fill=P.AMARILLO, width=10)
    d.polygon([(780, 1230), (820, 1230), (800, 1260)], fill=P.AMARILLO)
    d.text((800, 1100), "2 cm", font=fuente(70), fill=P.AMARILLO, anchor="mm",
           stroke_width=6, stroke_fill=(0, 0, 0))
    texto(img, "Pechuga: «Sentadilla hecha»", 200, tam=80)
    if t > 1.6:
        texto(img, "Eso no cuenta", 420, tam=76, color=P.ROJO)
    return img


def escena3(i):  # la corrección
    t = i / FPS
    pygame_t[0] = t
    img = FONDO.copy()
    prof = 0.5 - 0.5 * math.cos(t * 2.2)
    pechuga_sentadilla(img, 440, prof, MIEDO, tiembla=4)
    sello(img, "ok", 900, 700, 90, (67, 160, 71))
    texto(img, "Así sí:", 180, tam=90, color=(120, 230, 120))
    for k, frase in enumerate(["Muslo paralelo al suelo", "Talones apoyados", "Pecho arriba"]):
        if t > 0.5 + k * 0.8:
            texto(img, "· " + frase, 320 + k * 90, tam=60, ancho=1000)
    return img


def escena4(i):  # cierre con pregunta
    t = i / FPS
    pygame_t[0] = t
    img = FONDO.copy()
    pechuga_sentadilla(img, W / 2 - 60, 0.35, MIEDO, barra=False, tiembla=14)
    d = ImageDraw.Draw(img)
    for k, (x, y) in enumerate([(260, 760), (720, 720), (300, 1000)]):
        gota(d, x, y + ((t * 300) + k * 120) % 300)
    texto(img, "Pechuga al día siguiente:", 200, tam=80)
    if t > 1.2:
        texto(img, "¿Tú bajas hasta abajo o haces 2 cm? Te leo", 400, tam=62, color=P.AMARILLO, ancho=900)
    return img


ESCENAS = [(escena1, 3.0), (escena2, 3.5), (escena3, 4.5), (escena4, 4.0)]


def ritmo(segundos, ruta):
    """Ritmo original hecho con ffmpeg: bombo + charles + bajo. Sin música con derechos."""
    b = 0.5  # 120 pulsaciones por minuto
    expr = (f"0.55*sin(2*PI*mod(t,{b})*(45+120*exp(-mod(t,{b})*30)))*exp(-mod(t,{b})*9)"
            f"+0.12*(random(0)*2-1)*exp(-mod(t+{b/2},{b})*45)"
            f"+0.18*sin(2*PI*(if(lt(mod(t,4),2),55,49))*t)*exp(-mod(t,{b/2})*5)")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    f"aevalsrc='{expr}':s=44100:d={segundos}",
                    "-af", f"afade=t=out:st={segundos - 1}:d=1,volume=0.8", ruta], check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prueba":
        os.makedirs("prueba", exist_ok=True)
        for n, (fn, dur) in enumerate(ESCENAS):
            fn(int(dur * FPS * 0.8)).save(f"prueba/{n + 1}.png")
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
