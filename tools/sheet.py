# sheet.py <out.jpg> <cols> <thumb_px> <files...>: labelled contact sheet of images
import sys, os
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
out, cols, tp, files = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
rows = (len(files) + cols - 1) // cols; sheet = Image.new('RGB', (cols * tp, rows * (tp + 18)), (30, 26, 22)); d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f)
    if im.mode == 'RGBA': bg = Image.new('RGB', im.size, (228, 213, 177)); bg.paste(im, mask=im.split()[3]); im = bg
    im = im.convert('RGB'); im.thumbnail((tp - 6, tp - 6)); X, Y = (i % cols) * tp, (i // cols) * (tp + 18)
    sheet.paste(im, (X + (tp - im.width) // 2, Y + (tp - im.height) // 2)); d.text((X + 4, Y + tp + 2), os.path.splitext(os.path.basename(f))[0], fill=(240, 220, 180))
sheet.save(out, quality=85); print(out, sheet.size)
