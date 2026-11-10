import math, random
from sdlib import *

PLYC = "#ecd9b8"


def sheet6(pdf, png=None):
    sh = Sheet(pdf, 6, "DRAWER SIDES", "Scale 1:3.3. 6 off: 4 x D1/D2 (153 high), 2 x D3 (231 high). 15 mm ply. Pairs are mirrored")
    s = 0.3
    zs12, zs3 = [45, 75], [60, 115.5, 171]
    for (oy, hb, zs, name) in ((204, 153, zs12, "D1, D2 SIDE (153 HIGH), 4 OFF"), (110, 231, zs3, "D3 SIDE (231 high), 2 OFF")):
        # outer-face view (left) and inner-face view (right); front end at the left
        V = View(sh, 22, oy, s)
        V.rect(0, 0, 495, hb, fc=PLY, lw=0.8)
        V.title(0, hb + 24, name + ": OUTER FACE", "pocket holes for the front (15 deg, 25 mm screws)")
        for z in zs:
            V.circ(31, z, 4.75, fc="white", lw=0.6)
            V.center_h(10, 60, z)
        V.dim_h(0, 495, 0, -8, "495")
        V.dim_v(0, hb, 0, -8, "%d" % hb)
        V.dim_h(0, 31, zs[-1], 12, "31")
        prev = 0
        V.chain_v([0] + zs, 62, 9, labels=["%g" % zs[0]] + ["%g" % (zs[i] - zs[i - 1]) for i in range(1, len(zs))]) if False else None
        for z in zs:
            V.dim_v(0, z, 62 + 0, 8 + 6 * zs.index(z), "%g" % z) if False else None
        V.leader(31, zs[0], 60, 14, "Pocket bore 9.5 dia, centres 31 from the front end", size=4.6, ha="left")
        for i, z in enumerate(zs):
            V.dim_v(0, z, 8 + 0, 10 + 6 * i, "%g" % z)
        V2 = View(sh, 215, oy, s)
        V2.rect(0, 0, 495, hb, fc=PLY, lw=0.8)
        V2.title(0, hb + 44, "INNER FACE", "base groove, through, open at both ends")
        V2.rect(0, 12.75, 495, 28.25, fc="#c9b690", hatch="////", lw=0.5)
        V2.dim_v(0, 12.75, 495, 8, "12.75")
        V2.dim_v(12.75, 28.25, 495, 22, "15.5")
        V2.dim_h(0, 495, hb, 8, "495")
        V2.leader(150, 20.5, 40, 16 if hb < 200 else 30, "groove 15.5 x 8 deep (hand-routed, fence)", size=4.6, ha="left")
        V2.txt(250, hb - 12 if hb > 200 else hb - 10, "FRONT END AT THE LEFT", size=4.4, c=GREY)
    # underside strips (bottom edge, 495 x 15): v = across the thickness from the OUTER face (0) to the INNER face (15)
    s2 = 0.45
    A = View(sh, 22, 70, s2)
    A.rect(0, 0, 495, 15, fc=PLY, lw=0.8)
    A.title(0, 46, "OPTION 1 (snap clip): BOTTOM EDGE", "left side shown; the right side is a mirror (notch on the inner face side)")
    A.circ(10.7, 7.5, 1.75, fc="white", lw=0.6)
    A.rect(476.9, 7.9, 486.9, 15, fc="white", lw=0.6)
    A.dim_h(0, 10.7, 15, 4, "10.7"); A.dim_h(476.9, 486.9, 15, 4, "10")
    A.dim_h(486.9, 495, 15, 4, "8.1") if False else None
    A.dim_v(7.9, 15, 495, 4, "7.1")
    A.dim_v(0, 7.5, 0, -4, "7.5") if False else None
    A.leader(10.7, 7.5, 12, -16, "3.5 dia x 11.4 deep (clip screw)", size=4.5, ha="left")
    A.leader(481.9, 11.4, -30, -16, "notch 10 long x 7.1 into the face x 4.6 high; 481.9 from the front end", size=4.5, ha="right")
    B = View(sh, 22, 22, s2)
    B.rect(0, 0, 495, 15, fc=PLY, lw=0.8)
    B.title(0, 46, "OPTION 2 (screws from below): BOTTOM EDGE", "mark through the holes drilled in the drawbar")
    for u in (36.5, 456.5):
        B.circ(u, 11.7, 1.75, fc="white", lw=0.6)
    B.dim_h(0, 36.5, 0, -4, "36.5"); B.dim_h(456.5, 495, 0, -4, "38.5")
    B.dim_v(0, 11.7, 495, 4, "11.7")
    B.leader(36.5, 11.7, 22, -12, "3.5 dia x 10.5 deep, 11.7 from the outer face (3.3 from the inner face)", size=4.5, ha="left")
    if png:
        sh.png(png)
    sh.save()


def sheet7(pdf, png=None):
    sh = Sheet(pdf, 7, "DRAWER FRONTS, BACKS AND BASES", "Scale 1:5. 15 mm ply. Fronts seen from the BACK face; backs seen from the FRONT face (the face toward the base)")
    s = 0.2
    for (name, hf, oy) in (("D1, D2 FRONT (2 off)", 212.7, 205), ("D3 FRONT (1 off)", 326.3, 85)):
        V = View(sh, 20, oy, s)
        V.rect(0, 0, 802, hf, fc=PLYC, lw=0.8)
        V.title(0, hf + 20, name, "back face. Top edge toward the top of the sheet")
        V.dim_h(0, 802, 0, -7, "802")
        V.dim_v(0, hf, 0, -7, "%d" % hf)
        V.line(0, hf - 9.7, 802, hf - 9.7, lw=0.3, ls=(0, (4, 2)), c=RED)
        V.txt(401, hf - 16, "top edge: 45 deg mitre, R3 nose; bottom edge: 45 deg mitre 15 high on D1, D2 (sheet 9)", size=4.4, c=RED)
        V.txt(401, hf / 2 + 6, "plain panel: no base groove (the base slot is in the sides and the back)", size=4.6, c=GREY)
        V.txt(401, hf / 2 - 6, "bracket holes to the Hafele front pattern (datasheet page 1)", size=4.4, c=GREY)
    for (name, hb, zk, oy) in (("D1, D2 BACK (2 off): 713 x 148", 148.0, [45.0, 75.0], 245), ("D3 BACK (1 off): 713 x 226", 226.0, [60.0, 125.5, 181.0], 180)):
        V = View(sh, 232, oy, s)
        V.rect(0, 0, 713, hb, fc=PLYC, lw=0.8)
        V.title(0, hb + 18, name, "front face (toward the base): base groove, full width, open at both ends")
        V.rect(0, 7.75, 713, 23.25, fc="#c9b690", hatch="////", lw=0.5)
        for z in zk:
            for u in (31, 682):
                V.circ(u, z, 4.75, fc="none", ec=GREY, lw=0.5)
        V.dim_h(0, 713, 0, -7, "713"); V.dim_v(0, hb, 0, -7, "%g" % hb)
        V.dim_v(0, 7.75, 713, 6, "7.75")
        V.dim_v(7.75, 23.25, 713, 20, "15.5")
        V.dim_v(23.25, zk[0], 713, 18, "") if False else None
        V.txt(356, hb / 2 + 8, "groove 15.5 x 8 deep, full width", size=4.4, c=GREY)
    sh.ax.text(232, 167, "Hidden grey circles: pocket bores in the rear face, 9.5 dia at 15 deg, 31 from each end, 25 mm screws.", fontsize=4.8, va="center")
    sh.ax.text(232, 163, "Pocket heights above the bottom edge: D1, D2 at 45 and 75; D3 at 60, 125.5 and 181.", fontsize=4.8, va="center")
    s3 = 0.15
    V = View(sh, 232, 76, s3)
    V.rect(0, 0, 728.5, 487.5, fc="#f1dfb9", lw=0.8)
    V.title(0, 487.5 + 36, "DRAWER BASE (3 off)", "15 mm ply, no machining. Long side is the depth. Scale 1:6.7")
    V.dim_h(0, 728.5, 0, -8, "728.5"); V.dim_v(0, 487.5, 0, -8, "487.5")
    V.txt(364, 244, "SLIDES IN FROM THE FRONT INTO THE SIDE GROOVES AND THE BACK GROOVE", size=4.4, c=GREY)
    sh.ax.text(232, 56, "Front edge butts the front panel, flush with the side ends. Rear edge ends 0.5 short of the bottom of the back groove (7.5 into the back).", fontsize=4.6, va="center")
    if png:
        sh.png(png)
    sh.save()
