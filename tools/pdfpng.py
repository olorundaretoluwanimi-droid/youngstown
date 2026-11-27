# usage: pdfpng.py <pdf> <outprefix> <dpi> [first] [last]
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pylib"))
import pypdfium2 as pdfium
pdf = pdfium.PdfDocument(sys.argv[1]); dpi = float(sys.argv[3])
a = int(sys.argv[4]) if len(sys.argv) > 4 else 1; b = int(sys.argv[5]) if len(sys.argv) > 5 else len(pdf)
for i in range(a - 1, min(b, len(pdf))):
    pdf[i].render(scale=dpi / 72).to_pil().save(f"{sys.argv[2]}-{i+1}.png")
print(len(pdf), "pages")
