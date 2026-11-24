# Pechuga — vídeos de gimnasio

Código para crear los vídeos animados de **Pechuga**, el pollo que nunca entrena pierna.

## Archivos

- `personaje.py` — dibuja a Pechuga. La función `dibujar()` devuelve una imagen del personaje:
  - `pecho`: tamaño del pecho (1.0 normal, 1.5 enorme).
  - `cara`: `"normal"`, `"miedo"` u `"orgulloso"`.
  - `brazos`: `"abajo"` o `"arriba"` (sacando bíceps).
- `video_ejemplo.py` — primer vídeo («Día de pierna»). Sirve de plantilla: cada escena es una función que dibuja un fotograma.
- `perfil_pechuga.png` — foto de perfil de la cuenta.

## Cómo crear un vídeo

```bash
python3 video_ejemplo.py prueba   # guarda una imagen de cada escena para revisarlas
python3 video_ejemplo.py          # crea e0.mp4, e1.mp4... (una por escena)
```

Después se unen las escenas con ffmpeg:

```bash
printf "file e0.mp4\nfile e1.mp4\nfile e2.mp4\nfile e3.mp4\n" > lista.txt
ffmpeg -f concat -safe 0 -i lista.txt -c copy video_final.mp4
```

## Formato

- Vertical 1080x1920, 30 fps.
- Textos grandes arriba, lejos de la parte de abajo y de la derecha (ahí TikTok pone sus botones).
