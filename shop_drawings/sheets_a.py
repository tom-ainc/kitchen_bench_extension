import textwrap as _tw
import math
_R3, _D3 = 3.0, 3.0 / math.tan(math.radians(22.5))
_K3 = _D3 - 2.0
_XI = ((_R3 + _K3) - math.sqrt((_R3 + _K3) ** 2 - 2.0 * _K3 ** 2)) / 2.0
_L = 12.0 - _XI                      # apex depth of the mitre below the top edge (9.68)
_ZC = -(_L + _D3) + 2.0              # roundover bit centre height (arc starts here, 14.9 below the top)
_AI = math.degrees(math.atan2(-_L - _XI - _ZC, _XI - _R3))
_RF = 1.0
_CC = -_L - math.sqrt(2.0) * _RF
_QB = -2.0 * _R3 - 2.0 * (_CC - _ZC)
_QC = _R3 ** 2 + (_CC - _ZC) ** 2 - (_R3 - _RF) ** 2
_FX = (-_QB - math.sqrt(_QB ** 2 - 8.0 * _QC)) / 4.0
_F = (_FX, _CC - _FX)
_TA = (_R3 + (_F[0] - _R3) * _R3 / (_R3 - _RF), _ZC + (_F[1] - _ZC) * _R3 / (_R3 - _RF))
_TL = (_F[0] + _RF / math.sqrt(2.0), _F[1] + _RF / math.sqrt(2.0))
_AA = math.degrees(math.atan2(_TA[1] - _ZC, _TA[0] - _R3))
_F1, _F2 = math.atan2(_TL[1] - _F[1], _TL[0] - _F[0]), math.atan2(_TA[1] - _F[1], _TA[0] - _F[0])
_FD = (_F2 - _F1 + math.pi) % (2.0 * math.pi) - math.pi
_FILP = [(_F[0] + _RF * math.cos(_F1 + _FD * k / 8.0), _F[1] + _RF * math.sin(_F1 + _FD * k / 8.0)) for k in range(9)]   # (u, v) from the mitre tangent point to the arc tangent point
_ARCP = [(_R3 + _R3 * math.cos(math.radians(_AA + (180 - _AA) * k / 12.0)), _ZC + _R3 * math.sin(math.radians(_AA + (180 - _AA) * k / 12.0))) for k in range(13)]   # from the fillet to the face
_BK = math.tan(math.radians(22.5))
_BTT = 2.0 / _BK                    # tangent distance of the R2 on the back edge (4.83)
_BTF = 3.0 * _BK                    # and of the R3 on the face arris (1.24)
_BOTP = [(13.0 + 2.0 * math.cos(math.radians(360.0 - 135.0 * k / 12.0)), _BTT + 2.0 * math.sin(math.radians(360.0 - 135.0 * k / 12.0))) for k in range(13)] \
    + [(3.0 + 3.0 * math.cos(math.radians(225.0 - 45.0 * k / 8.0)), 15.0 + _BTF + 3.0 * math.sin(math.radians(225.0 - 45.0 * k / 8.0))) for k in range(9)]   # (u, v up from the bottom) from the back edge up to the face
from sdlib import *

# ---------------- geometry from the model (unit coordinates: d depth from benchtop front edge, w width from joint end, h height above floor)
H_PLINTH, H_CBOT, H_TOP = 125.0, 140.0, 874.0
D_CARC_F, D_BACK_IN, D_END = 38.0, 545.0, 560.0
W_CARC = 805.0
FRONTS = [("D1", 639.0, 212.7), ("D2", 436.3, 212.7), ("D3", 120.0, 326.3)]     # name, bottom h, height
BOX = [("D1", 674.0, 153.0), ("D2", 471.0, 153.0), ("D3", 190.0, 231.0)]       # name, side bottom h (= drawbar plate top), side height
D_FRONT0, D_FRONT1 = 17.0, 32.0
D_BOX_END = 527.0
RUN_DROP = 45.0


def cove_pts(dx0, dx1, ztop, r, n=14):
    """Front panel outline (d horizontal, h vertical) with the front-top cove, between dx0 and dx1, top at ztop."""
    pts = [(dx0, ztop - r)]
    for i in range(n + 1):
        a = math.pi / 2 * i / n
        pts.append((dx0 + r * math.sin(a), ztop - r * math.cos(a)))
    pts.append((dx1, ztop))
    return pts


def sheet1(pdf):
    sh = Sheet(pdf, 1, "COVER SHEET AND SCHEDULES", "Parts schedule, hardware, general notes")
    a = sh.ax
    a.text(20, 280, "EXTENSION UNIT: SHOP DRAWINGS", fontsize=15, weight="bold", va="center")
    a.text(20, 272, "Three-drawer base unit under the bench extension. Plywood carcass, plinth and drawers on Hafele Alto runner drawbars.",
           fontsize=6.5, va="center")
    rows = [
        ("Ref", "Part", "Qty", "Length", "Width", "Thick", "Notes"),
        ("C1", "Side, free end", "1", "749", "522", "15", "Full height"),
        ("C2", "Side, joint end", "1", "749", "522", "15", "Two 6.5 wide link-bolt slots, open to the top edge"),
        ("C3", "Bottom", "1", "775", "507", "15", "Sits on the plinth between the sides"),
        ("C4", "Back", "1", "775", "749", "15", "Full height, between the sides on the ends of the plinth side rails; C3 butts its front face"),
        ("C9", "Top rail, front", "1", "775", "60", "15", "Between the sides at the top, under the benchtop"),
        ("P1", "Plinth rail, front", "1", "767", "125", "15", "Pocket-screwed up into C3"),
        ("P2", "Plinth rail, rear", "1", "767", "125", "15", "Fully under C3; pocket-screwed up into it"),
        ("P3, P4", "Plinth rail, side", "2", "461", "125", "15", "P3 free end, P4 joint end; screwed up into the sides"),
        ("Kb", "Kickboard cover", "1", "852", "115", "15", "Screwed on from inside the plinth"),
        ("D1, D2", "Drawer front", "2", "802", "212.7", "15", "45 deg mitre top (R3 nose, R1 sanded), 15 high bottom mitre; no base groove"),
        ("D3", "Drawer front", "1", "802", "326.3", "15", "45 deg mitre top (R3 nose); bottom level with the existing doors"),
        ("D1, D2", "Drawer side", "4", "495", "153", "15", "Through base groove; pocket holes; fixing details"),
        ("D3", "Drawer side", "2", "495", "231", "15", "As D1, D2"),
        ("D1, D2", "Drawer back", "2", "713", "148", "15", "Base groove 15.5 x 8; 5 above side bottoms"),
        ("D3", "Drawer back", "1", "713", "226", "15", "As D1, D2"),
        ("TS", "Top strip", "1", "802", "32.3", "15", "False front above D1: bottom mitre as D1, D2; plain top"),
        ("TP", "Strip packer", "1", "775", "15", "6", "6 mm ply or hardwood; glued behind TS and to C9"),
        ("D1-D3", "Drawer base", "3", "728.5", "487.5", "15", "Butts the front; rear edge in the back groove"),
    ]
    x0, y0 = 20, 255
    cw = [18, 34, 8, 14, 14, 11, 80]
    xs = [x0]
    for w in cw:
        xs.append(xs[-1] + w)
    a.text(x0, y0 + 6, "PARTS SCHEDULE (15 mm plywood; grain along the length)", fontsize=7, weight="bold", va="center")
    for i, r in enumerate(rows):
        y = y0 - i * 6.0
        for j, t in enumerate(r):
            ha = "right" if j in (2, 3, 4, 5) else "left"
            xx = xs[j + 1] - 1.2 if ha == "right" else xs[j] + 1.2
            if j == 6:
                t = "\n".join(_tw.wrap(t, 62))
            a.text(xx, y, t, fontsize=5.6, ha=ha, va="center", weight="bold" if i == 0 else "normal", linespacing=0.95)
        a.plot([x0, xs[-1]], [y - 3.0, y - 3.0], lw=0.3 if i else 0.7, c=INK)
    a.plot([x0, xs[-1]], [y0 + 3.0, y0 + 3.0], lw=0.7, c=INK)

    hw = [
        ("Hafele Alto 86 x 500 mm set", "3", "Runners, drawbars, front brackets and snap clips; steel sides not used"),
        ("Snap clips (in the Alto set)", "6", "2 per drawer; fixing option 1"),
        ("No.6 x 12 pan-head screws", "12", "Option 2 drawbar fixing (6 for option 1 clip screws)"),
        ("Pocket-hole screws, 25 mm, coarse", "70", "Drawer boxes 28; carcass and plinth 42 (C3 8, C4 10, C9 4, plinth rail joints 8, plinth to carcass 12)"),
        ("Steel angle brackets 25 x 25 x 2, 40 long", "9", "Benchtop: 3 each side, 3 on the back"),
        ("M6 x 65 bolts, washers", "2", "Link to the main run's framing rail"),
        ("No.8 x 25 screws", "4", "Kickboard cover"),
        ("No.8 x 12 and No.8 x 16 screws", "18 + 18", "Benchtop brackets: x12 into the carcass, x16 up into the benchtop"),
    ]
    y1 = y0 - len(rows) * 6.0 - 9
    a.text(x0, y1 + 4, "HARDWARE AND FIXINGS", fontsize=7, weight="bold", va="center")
    for i, (n, q, nt) in enumerate(hw):
        y = y1 - i * 6.0
        a.text(x0 + 1.2, y, n, fontsize=5.6, va="center")
        a.text(x0 + 84, y, q, fontsize=5.6, va="center", ha="right")
        a.text(x0 + 88, y, "\n".join(_tw.wrap(nt, 62)), fontsize=5.6, va="center", linespacing=0.95)
        a.plot([x0, x0 + 190], [y - 3.0, y - 3.0], lw=0.3, c=INK)

    notes = [
        "GENERAL NOTES",
        "1. Material: 15 mm structural CD plywood (Bunnings STRUCTAply); all parts 15 mm. Cut square to +/-0.5 mm.",
        "2. Hand routing only. No CNC. Base slot 15.5 wide x 8 deep, lower edge 13 above the bottom edge of the side: through the sides and across the back.",
        "Build each box front-last: sides and back first, slide the base in from the front, then fit the front.",
        "3. Drawer pulls: a 45 degree mitre on the front 7.5 mm of the top edge of each front (R3 nose) with a 7.5 mm catch wall behind it (half-thickness rebate from the back), and a 45 degree mitre (15 mm high on the face, about 15 mm clear to the mitre below) on the bottom edge of D1 and D2. The nose of each front stays 5 mm below the lowest point of the front above (after rounding), so the fronts overlap by 10 mm and each drawer opens without catching the one below.",
        "Pull profiles and the gaps between fronts are on sheet 9.",
        "4. Drawer fixing shown: option 1 (snap clip + rear tab notch). Option 2 (screws from below), sheet 8.",
        "5. Runners: the steel stack hangs 45 mm below each drawbar plate, drawbar outer face 14 mm from the cabinet wall,",
        "8 mm underside opening facing away from the wall. Box sides sit on the 15.2 mm drawbar flat, 16 mm from the wall.",
        "6. Drawer fronts: bracket holes to the Hafele front pattern (datasheet page 1); not dimensioned here.",
        "7. The fixed runner is modelled as a 14 x 45 block; the real section is not drawn. Check it on the first fitted drawer.",
        "8. Benchtop (existing placeholder) rests on the carcass sides, back and front top rail C9; 9 angle brackets fix it (sheet 3).",
        "9. Carcass and plinth joints: glued pocket-screw butt joints, 25 mm coarse screws (42 in all, positions in the guide); 12 of them fix the plinth P1 to P4 up into C3 and the sides from inside the frame.",
        "10. Unit height floor to benchtop underside 874 (top surface 900 with the 26 mm timber top). The extension top has a 12 mm hem under the front edge only and overhangs the carcass 38 mm at the front. Plinth frame 125 (kickboard cover 115, as the existing kickboard). Drawer fronts overlay the carcass 1.5 mm in from each end.",
        "11. Carcass and plinth stop 40 mm short of the wall to clear a skirting board (20 to 25 projection). The benchtop keeps its full 600 depth.",
    ]
    yy = 252.0
    for i, t in enumerate(notes):
        if i == 0:
            a.text(235, yy, t, fontsize=7, va="center", weight="bold"); yy -= 5.5
            continue
        ls = _tw.wrap(t.strip(), 100)
        for k, ln in enumerate(ls):
            a.text(235 + (0 if k == 0 else 4), yy, ln, fontsize=5.4, va="center"); yy -= 3.6
        yy -= 1.2
    a.text(20, 63, "SHEET INDEX", fontsize=7, weight="bold", va="center")
    idx = ["1 Cover, schedules", "2 General arrangement: front elevation, side section A-A", "3 Plan and cross-section B-B",
           "4 Carcass parts C1 to C4 and C9", "5 Plinth P1 to P4 and kickboard Kb", "6 Drawer sides", "7 Drawer fronts, backs and bases",
           "8 Drawer box assembly and drawbar fixing options", "9 Mitre pull profiles and gaps", "10 Cutting diagrams (exact sizes, 2 sheets)", "11 Cutting diagrams for store cuts on 100 mm multiples (3 sheets)"]
    for i, t in enumerate(idx):
        a.text(20, 57 - i * 4.4, t, fontsize=5.6, va="center")
    sh.save()


def sheet2(pdf, png=None):
    sh = Sheet(pdf, 2, "GENERAL ARRANGEMENT", "Front elevation and side section A-A. Scale 1:5")
    s = 0.2
    # --- front elevation: u = w (joint end at left), v = h
    V = View(sh, 30, 70, s)
    ox = 53.0   # shift so the kickboard cover (starts at w = -53) fits
    def U(w): return w + ox
    V.line(U(-60), 0, U(830), 0, lw=0.9)                                    # floor
    V.rect(U(-53), 0, U(799), 115, fc=LIGHT, lw=0.6)                          # kickboard cover Kb
    V.txt(U(370), 57, "Kb KICKBOARD COVER", size=5)
    V.rect(U(0), 125, U(15), 874, fc=PLY, lw=0.6)                             # sides
    V.rect(U(790), 125, U(805), 874, fc=PLY, lw=0.6)
    V.rect(U(1.5), 841.7, U(803.5), 862, fc="#e6d3ad", lw=0.7, z=2)                       # top strip (false front), visible below the hem
    V.txt(U(402), 852, "TOP STRIP", size=5, c="#6b5a3c")
    for n, b, hgt in FRONTS:
        V.rect(U(1.5), b, U(803.5), b + hgt - 12.0, fc="#ecd9b8", lw=0.7, z=3)               # visible face up to the nose of the mitre
        V.line(U(1.5), b + hgt - 15.0, U(803.5), b + hgt - 15.0, lw=0.3, ls=(0, (4, 2)), z=4)   # where the R3 meets the flat face
        if n != "D3":
            V.line(U(1.5), b + 15.0, U(803.5), b + 15.0, lw=0.3, ls=(0, (4, 2)), z=4)           # bottom mitre meets the face
        V.txt(U(402), b + hgt / 2 - 10, n, size=9, weight="bold", c="#6b5a3c")
    V.rect(U(0), 862, U(820), 874, fc="#e3cf9f", lw=0.6, z=1)                 # 12 mm hem (front edge)
    V.rect(U(0), 874, U(820), 900, fc="#efe0bd", lw=0.9, z=1)                 # 26 mm timber top
    V.txt(U(410), 887, "BENCHTOP EXTENSION: 26 TIMBER TOP + 12 FRONT HEM", size=5, c=GREY)
    # section marks
    V.line(U(402.5), -12, U(402.5), 925, lw=0.4, ls=(0, (10, 3, 2, 3)), c=RED)
    V.txt(U(402.5), -17, "A", size=7, c=RED, weight="bold"); V.txt(U(402.5), 930, "A", size=7, c=RED, weight="bold")
    # dims
    V.dim_h(U(1.5), U(803.5), 0, -9, "802 (fronts)")
    V.dim_h(U(0), U(805), 0, -17, "805 (carcass)")
    V.dim_h(U(-53), U(799), 0, -25, "852 (kickboard cover)")
    V.dim_h(U(0), U(820), 900, 8, "820 (benchtop)")
    xr = U(830)
    V.dim_v(0, 125, xr, 8, "125 plinth frame (Kb 115)")
    V.dim_v(120, 446.3, xr, 24, "326.3")
    V.dim_v(436.3, 649, xr, 40, "212.7")
    V.dim_v(639, 851.7, xr, 56, "212.7")
    V.dim_v(841.7, 874, xr, 24, "32.3 (top strip)")
    V.dim_v(0, 120, xr, 40, "120 (level with the doors)")
    V.dim_v(0, 900, U(-53), -8, "900 to top, 874 to underside")
    V.leader(U(500), 850, 30, 36, "45 deg mitre, R3 nose (top edges); 45 deg bottom mitre (D1, D2)", ha="left")
    V.title(U(-53), 965, "FRONT ELEVATION", "SCALE 1:5")

    # --- side section A-A: u = d, v = h; placed to the right
    S = View(sh, 262, 70, s)
    def draw_cut(v, u0, v0, u1, v1, fc=PLY, hatch="////"):
        v.rect(u0, v0, u1, v1, fc=fc, hatch=hatch, lw=0.6)
    S.line(-20, 0, 620, 0, lw=0.9)
    # plinth parts cut
    draw_cut(S, 62, 0, 77, 115, fc=LIGHT)    # Kb
    draw_cut(S, 77, 0, 92, 125)               # P1
    draw_cut(S, 530, 0, 545, 125)             # P2
    draw_cut(S, D_CARC_F, 125, D_BACK_IN, 140)   # C3
    draw_cut(S, D_BACK_IN, 125, D_END, 874)      # C4
    # far side panel outline
    S.rect(D_CARC_F, 125, D_END, 874, ls=(0, (6, 3)), lw=0.35, ec=GREY, z=1)
    # runners / drawbars beyond (hidden)
    for n, zb, hh in BOX:
        S.rect(34, zb - RUN_DROP, 534, zb, ls=(0, (6, 2)), lw=0.4, ec=GREY, z=2)
        S.rect(D_FRONT1, zb - 31, D_FRONT1 + 26.5, zb, ls=(0, (6, 2)), lw=0.4, ec=GREY, z=2)
        S.rect(D_FRONT1, zb, D_BOX_END, zb + hh, ls=(0, (3, 2)), lw=0.35, ec=GREY, z=2)      # far side (not cut)
        # base and back cut
        S.poly([(512, zb + 5), (527, zb + 5), (527, zb + hh), (512, zb + hh), (512, zb + 28.25), (520, zb + 28.25), (520, zb + 12.75), (512, zb + 12.75)],
               fc=PLY, lw=0.6, z=3)
        draw_cut(S, D_FRONT1, zb + 13, 519.5, zb + 28, fc="#e8d5b0", hatch="////")
    def front_profile(top, b, cove):
        """Side profile of a front: 45 degree mitre across the full thickness on top (R3 nose), 45 degree bottom mitre, 15 high on the face, on the bottom when cove is set."""
        x0 = D_FRONT0
        pts = [(x0 + 15, b)]
        if cove:
            pts += [(x0 + u, b + v) for (u, v) in _BOTP]
        else:
            pts.append((x0, b))
        pts.append((x0, top + _ZC))
        pts += [(x0 + u, top + v) for (u, v) in reversed(_ARCP)]
        pts += [(x0 + u, top + v) for (u, v) in reversed(_FILP[1:])]
        pts += [(x0 + 7.5, top - _L - 7.5), (x0 + 7.5, top - _L - 15.0), (x0 + 15, top - _L - 15.0)]      # 45 deg lip, catch wall, shelf
        return pts

    for n, b, hgt in FRONTS:
        S.poly(front_profile(b + hgt, b, n != "D3"), fc="#ecd9b8", lw=0.7, z=4)
        S.txt(30, b + hgt / 2, n, size=8, weight="bold", c="#6b5a3c")
    S.poly([(D_FRONT0 + 15, 874), (D_FRONT0, 874)] + [(D_FRONT0 + u, 841.7 + v) for (u, v) in reversed(_BOTP)], fc="#e6d3ad", lw=0.7, z=4)   # top strip
    S.rect(D_FRONT0 + 15, 859, D_FRONT0 + 21, 874, fc=PLY, hatch="////", lw=0.5, z=3)    # 6 mm packer to C9
    S.rect(0, 874, 600, 900, fc="#efe0bd", hatch="....", lw=0.8, z=1)         # 26 mm timber top
    S.rect(0, 862, 12, 874, fc="#e3cf9f", hatch="////", lw=0.6, z=1)   # 12 mm hem, front edge only
    # section dims
    S.dim_h(0, 600, 900, 10, "600 (benchtop depth)")
    S.dim_h(D_CARC_F, D_BACK_IN, 125, -9, "507 (carcass bottom)")
    S.dim_h(D_FRONT1, D_BOX_END, 0, -17, "495 (drawer box)", ext=1.0)
    S.dim_h(D_BOX_END, D_BACK_IN, 874, 4, "18")
    S.txt(548, 560, "18 mm behind the box", size=4.6, c=RED, rot=90)
    S.dim_v(0, 874, 622, 6, "874")
    for n, zb, hh in BOX:
        S.dim_v(zb, zb + hh, 17, -7, "%d" % hh) if False else None
    # plate height chain at the left of the section
    S.txt(290, 120, "C3", size=5); S.txt(592, 400, "C4", size=5, rot=90)
    S.title(-20, 965, "SECTION A-A (looking toward the main run)", "SCALE 1:5")
    for i, t in enumerate(["Drawbar plate tops (= box side bottoms): D1 h=674, D2 h=471, D3 h=190 above the floor (534 / 331 / 50 above the top of the carcass bottom).",
                           "Hidden grey: drawbar, bracket and runner block (hang 45 below each plate). Base slides in from the front into the side grooves and the back groove."]):
        sh.ax.text(30, 36 - i * 4.0, t, fontsize=4.8, va="center")
    if png:
        sh.png(png)
    sh.save()


def sheet3(pdf, png=None):
    sh = Sheet(pdf, 3, "PLAN AND CROSS-SECTION B-B", "Plan with benchtop removed, and section across the drawers. Scale 1:5")
    s = 0.2
    # --- plan: u = w (joint end at left), v = d (front at bottom)
    P = View(sh, 22, 70, s)
    P.line(-60, 0, 880, 0, lw=0.0)
    # plinth below, dashed
    P.rect(2, 92, 797, 553, ls=(0, (6, 3)), lw=0.4, ec=GREY, z=1)
    P.rect(-53, 77, 799, 92, ls=(0, (6, 3)), lw=0.4, ec=GREY, z=1)
    # carcass sides + back cut
    P.rect(0, D_CARC_F, 15, D_END, fc=PLY, hatch="////", lw=0.6)
    P.rect(790, D_CARC_F, 805, D_END, fc=PLY, hatch="////", lw=0.6)
    P.rect(15, D_BACK_IN, 790, D_END, fc=PLY, hatch="////", lw=0.6)
    P.rect(15, D_CARC_F, 790, D_CARC_F + 60, fc=PLY, hatch="////", lw=0.6, z=6)    # C9 front top rail
    # runner blocks (below top drawer plate) and drawbars, top drawer
    P.rect(15, 34, 29, 534, fc=STEEL, lw=0.5, z=2)
    P.rect(776, 34, 790, 534, fc=STEEL, lw=0.5, z=2)
    # top drawer box
    P.rect(31, D_FRONT1, 46, D_BOX_END, fc=PLY, lw=0.6, z=3)
    P.rect(759, D_FRONT1, 774, D_BOX_END, fc=PLY, lw=0.6, z=3)
    P.rect(46, D_BOX_END - 15, 759, D_BOX_END, fc=PLY, lw=0.6, z=3)
    P.rect(46, D_FRONT1, 759, D_BOX_END - 15, fc="#f7efdf", lw=0.4, z=2)       # base
    P.rect(1.5, D_FRONT0, 803.5, D_FRONT1, fc="#ecd9b8", lw=0.7, z=4)
    # benchtop brackets
    for d in (134.1, 294.1, 454.1):
        P.rect(15, d - 20, 40, d + 20, fc=STEEL, lw=0.4, z=5)
        P.rect(765, d - 20, 790, d + 20, fc=STEEL, lw=0.4, z=5)
    for w in (152.5, 402.5, 652.5):
        P.rect(w - 20, 520, w + 20, 545, fc=STEEL, lw=0.4, z=5)
    # link bolts
    for d in (494.1, 534.1):
        P.circ(7.5, d, 3.25, fc="white", lw=0.5, z=6)
    P.leader(7.5, 534.1, 30, -62, "2 x 6.5 slots (C2), M6 link bolts", ha="left")
    P.txt(402, 280, "TOP DRAWER BOX D1 SHOWN", size=6, c="#6b5a3c", weight="bold")
    P.txt(402, D_FRONT0 + 7.5, "D1 FRONT", size=5, c="#6b5a3c")
    P.leader(402.5, 572, 70, 26, "benchtop bracket (x3 back)", ha="left")
    P.leader(40, 134.1, 35, -6, "benchtop brackets (x3 each side)", ha="left")
    P.dim_h(0, 805, D_END, 9, "805 (carcass)")
    P.dim_h(1.5, 803.5, D_FRONT0, -8, "802 (front)")
    P.dim_h(31, 774, 300, 0, "743 (box)")
    P.dim_h(46, 759, 330, 0, "713 (inside)")
    P.dim_v(D_CARC_F, D_END, 810, 6, "522 (carcass)")
    P.dim_v(D_FRONT0, D_BOX_END, -10, -10, "510 (front face to box rear)")
    P.title(-53, 650 + 40, "PLAN (benchtop removed, section below the benchtop)", "SCALE 1:5")
    # --- cross-section B-B at d = 300: u = w, v = h
    S = View(sh, 222, 70, 0.2)
    S.line(-20, 0, 840, 0, lw=0.9)
    # plinth returns cut
    S.rect(2, 0, 17, 125, fc=LIGHT, hatch="////", lw=0.5); S.rect(782, 0, 797, 125, fc=LIGHT, hatch="////", lw=0.5)
    S.rect(15, 125, 790, 140, fc=PLY, hatch="////", lw=0.6)
    S.rect(0, 125, 15, 874, fc=PLY, hatch="////", lw=0.6)
    S.rect(790, 125, 805, 874, fc=PLY, hatch="////", lw=0.6)
    S.rect(0, 874, 820, 900, fc="#efe0bd", hatch="....", lw=0.8, z=1)
    for n, zb, hh in BOX:
        S.rect(15, zb - RUN_DROP, 29, zb, fc=STEEL, lw=0.5)          # runner blocks
        S.rect(776, zb - RUN_DROP, 790, zb, fc=STEEL, lw=0.5)
        S.rect(29, zb - 16.2, 48.2, zb, fc="#aebccb", lw=0.5, z=3)    # drawbars
        S.rect(756.8, zb - 16.2, 776, zb, fc="#aebccb", lw=0.5, z=3)
        # sides with groove
        for (w0, w1, gl) in ((31, 46, 46), (759, 774, 759)):
            S.rect(w0, zb, w1, zb + hh, fc=PLY, hatch="////", lw=0.6, z=4)
        S.rect(38.25, zb + 13, 766.75, zb + 28, fc="#f1dfb9", hatch="\\\\\\\\", lw=0.4, z=5)
        S.rect(46, zb + 28.25, 759, zb + hh, ls=(0, (4, 2)), lw=0.35, ec=GREY, z=2)    # back panel beyond
        S.txt(402, zb + 80, n, size=7, weight="bold", c="#6b5a3c")
    S.dim_h(15, 790, 900, 9, "775 (inside)")
    S.dim_h(31, 774, 674 + 153, 1, "743 (box)")
    S.dim_v(0, 874, 826, 6, "874")
    S.title(-20, 965, "SECTION B-B at 300 from the benchtop edge", "SCALE 1:5")
    S.note(-20, -50, ["Grey blocks: runner (14 x 45) and drawbar. Boxes sit on the drawbar flats, outer faces 16 from the walls."], size=4.8)
    if png:
        sh.png(png)
    sh.save()
