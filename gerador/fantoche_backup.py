from interpretador import interpretar_roteiro
"""
Fantoche falante: roteiro (+ áudio opcional) -> MP4 vertical 1080x1920 + legenda .srt
Uso:
  python3 fantoche.py roteiro.txt saida.mp4 [--audio voz.wav]
Formato do roteiro (uma fala por linha):
  expressao | texto da fala
Expressões: riso_boca_aberta, sorriso_fechado, fala_boca_aberta, serio_boca_reta,
            feliz_olhos_fechados, satisfeito_olhos_fechados, cansado_olhos_fechados, fala_olhos_fechados
Linhas em branco e iniciadas por # são ignoradas.
"""
import sys, os, subprocess, wave, math, textwrap, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "expressoes")
FONT = "/system/fonts/Roboto-Bold.ttf"
MOUTH_OPEN = "fala_boca_aberta"
PUPPET_H = 1150
PUPPET_Y = 380

def load_asset(name):
    im = Image.open(os.path.join(ASSETS, name + ".png")).convert("RGBA")
    scale = PUPPET_H / im.height
    return im.resize((int(im.width * scale), PUPPET_H), Image.LANCZOS)

def parse_script(path):
    lines = []
    for raw in open(path, encoding="utf-8"):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        expr, _, text = raw.partition("|")
        lines.append((expr.strip(), text.strip()))
    return lines

def line_duration(text):
    words = max(1, len(text.split()))
    return max(1.2, words / 2.5)  # ~150 palavras/min; ajustável

def audio_envelope(wav_path, n_frames):
    with wave.open(wav_path, "rb") as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    dtype = {1: np.uint8, 2: np.int16, 4: np.int32}[sw]
    data = np.frombuffer(raw, dtype=dtype).astype(np.float32)
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    if sw == 1:
        data -= 128
    data /= np.max(np.abs(data)) + 1e-9
    spf = sr / FPS
    env = []
    for i in range(n_frames):
        seg = data[int(i * spf):int((i + 1) * spf)]
        env.append(float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0)
    env = np.array(env)
    thr = np.percentile(env, 40)  # limiar relativo: acima = boca aberta
    return env > thr, sr

def wrap_sub(text, width=26):
    return "\n".join(textwrap.wrap(text, width)) or ""

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    script, out = sys.argv[1], sys.argv[2]
    audio = sys.argv[sys.argv.index("--audio") + 1] if "--audio" in sys.argv else None

    lines = interpretar_roteiro(script)
    durations = [line_duration(t) for _, t in lines]
    total = sum(durations)
    n_frames = int(math.ceil(total * FPS))

    # timeline: expressão e texto por frame
    timeline = []
    t = 0.0
    for (expr, text), d in zip(lines, durations):
        timeline.append((t, t + d, expr, text))
        t += d

    mouth_open = None
    if audio:
        mouth_open, sr = audio_envelope(audio, n_frames)
        n_frames = min(n_frames, len(mouth_open))

    assets = {}
    def get(name):
        if name not in assets:
            assets[name] = load_asset(name)
        return assets[name]

    font = ImageFont.load_default(size=58)
    tmp = tempfile.mkdtemp()
    for f in range(n_frames):
        now = f / FPS
        expr, text = timeline[-1][2], timeline[-1][3]
        for (a, b, e, tx) in timeline:
            if a <= now < b:
                expr, text = e, tx
                break
        # boca: se há áudio, usa envelope; senão, alterna a cada 0,25 s dentro da fala
        if mouth_open is not None:
            is_open = bool(mouth_open[f])
        else:
            is_open = (int(now / 0.25) % 2 == 0) and bool(text)
        if is_open:
            img_name = MOUTH_OPEN if not expr.startswith("fala") else expr
        else:
            img_name = "sorriso_fechado" if expr.startswith("fala") else expr
        if img_name not in [os.path.splitext(x)[0] for x in os.listdir(ASSETS)]:
            img_name = "sorriso_fechado"

        canvas = Image.new("RGB", (W, H), (255, 255, 255))
        p = get(img_name)
        canvas.paste(p, ((W - p.width) // 2, PUPPET_Y), p)
        if text:
            d = ImageDraw.Draw(canvas)
            sub = wrap_sub(text)
            bbox = d.multiline_textbbox((0, 0), sub, font=font, align="center", spacing=10)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x, y = (W - tw) // 2, 1600
            d.rectangle((x - 24, y - 16, x + tw + 24, y + th + 16), fill=(0, 0, 0))
            d.multiline_text((x, y), sub, font=font, fill=(255, 255, 255), align="center", spacing=10)
        canvas.save(os.path.join(tmp, f"f{f:06d}.png"))

    # vídeo
    silent = os.path.join(tmp, "silent.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", os.path.join(tmp, "f%06d.png"), "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "20", silent], check=True)
    if audio:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", audio,
               "-c:v", "copy", "-c:a", "aac", "-shortest", out]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-c:v", "copy", out]
    subprocess.run(cmd, check=True)

    # legenda SRT para importar no CapCut
    def ts(s):
        h, rem = divmod(s, 3600); m, rem = divmod(rem, 60); sec, ms = divmod(rem, 1)
        return f"{int(h):02}:{int(m):02}:{int(sec):02},{int(ms*1000):03}"
    srt = os.path.splitext(out)[0] + ".srt"
    with open(srt, "w", encoding="utf-8") as fh:
        for i, (a, b, _, text) in enumerate(timeline, 1):
            fh.write(f"{i}\n{ts(a)} --> {ts(b)}\n{text}\n\n")
    print("OK:", out, "|", srt, "| duração ~%.1fs" % (n_frames / FPS))

if __name__ == "__main__":
    main()
