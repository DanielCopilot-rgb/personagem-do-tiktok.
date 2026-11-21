from PIL import Image, ImageOps
import numpy as np, glob

# Ordem pelos timestamps dos arquivos (conferida visualmente)
ordered = [
 ("70_Sem_Título_20261120192206.png", "riso_boca_aberta"),
 ("70_Sem_Título_20261120192224.png", "sorriso_fechado"),
 ("70_Sem_Título_20261120192252.png", "fala_boca_aberta"),
 ("70_Sem_Título_20261120192304.png", "serio_boca_reta"),
 ("70_Sem_Título_20261120192401.png", "feliz_olhos_fechados"),
 ("70_Sem_Título_20261120192421.png", "satisfeito_olhos_fechados"),
 ("70_Sem_Título_20261120192432.png", "cansado_olhos_fechados"),
 ("ibisPaint_X_20261120_192442.png",  "fala_olhos_fechados"),
]
src = "/mnt/user-data/uploads/"
imgs = {n: Image.open(src+f).convert("L") for f, n in ordered}

boxes = []
for im in imgs.values():
    ys, xs = np.where(np.array(im) < 128)
    boxes.append((xs.min(), ys.min(), xs.max(), ys.max()))
x0 = min(b[0] for b in boxes) - 20; y0 = min(b[1] for b in boxes) - 20
x1 = max(b[2] for b in boxes) + 20; y1 = max(b[3] for b in boxes) + 20
print("union bbox", x0, y0, x1, y1)

for name, im in imgs.items():
    crop = im.crop((x0, y0, x1, y1))
    rgba = Image.new("RGBA", crop.size, (0, 0, 0, 0))
    rgba.putalpha(ImageOps.invert(crop))
    rgba.save(f"assets/{name}.png")
    print("saved", name)
