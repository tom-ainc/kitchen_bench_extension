import sys
sys.path.insert(0, "/home/user/CAD/kitchen_bench_extension/shop_drawings")
from matplotlib.backends.backend_pdf import PdfPages
import sheets_a, sheets_b, sheets_c, sheets_d

OUT = "/home/user/CAD/kitchen_bench_extension/shop_drawings/extension_unit_shop_drawings.pdf"
PNG = "/tmp/claude-1000/-home-user-CAD-kitchen-bench-extension/3e6a31c0-9529-4183-a0f6-928867b06ebc/scratchpad/pg%02d.png"
with PdfPages(OUT) as pdf:
    sheets_a.sheet1(pdf)
    sheets_a.sheet2(pdf, png=PNG % 2)
    sheets_a.sheet3(pdf, png=PNG % 3)
    sheets_b.sheet4(pdf, png=PNG % 4)
    sheets_b.sheet5(pdf, png=PNG % 5)
    sheets_c.sheet6(pdf, png=PNG % 6)
    sheets_c.sheet7(pdf, png=PNG % 7)
    sheets_d.sheet8(pdf, png=PNG % 8)
    sheets_d.sheet9(pdf, png=PNG % 9)
    sheets_d.sheet10(pdf, png=PNG % 10)
    sheets_d.sheet11(pdf, png=PNG % 11)
print("wrote", OUT)
