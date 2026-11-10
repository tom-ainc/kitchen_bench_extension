import math, random
from sdlib import *

PLYC = "#ecd9b8"
STEELD = "#aebccb"


def drawbar_section(V, du=14.0, z0=0.0):
    """Drawbar cross-section (from the STEP file): u from the wall, z up with the plate top at z0."""
    V.rect(du, z0 - 1.5, du + 19.2, z0, fc=STEELD, lw=0.6, z=4)                 # top plate
    V.rect(du, z0 - 16.2, du + 1.5, z0, fc=STEELD, lw=0.6, z=4)                 # outer web (wall side)
    V.rect(du, z0 - 16.2, du + 9.7, z0 - 14.7, fc=STEELD, lw=0.6, z=4)          # wide bottom flange
    V.rect(du + 17.7, z0 - 16.2, du + 19.2, z0, fc=STEELD, lw=0.6, z=4)         # inner web


def side_section(V, hmax=48.0, notch=False, screw=False, tab=False):
    # wall, fixing plate, runner block
    V.rect(-5, -52, 0, 52, fc="#e6e6e6", hatch="////", lw=0.5)
    V.rect(0, -45, 3, 0, fc="#9fb0c0", lw=0.6)
    V.rect(3, -45, 14, 0, fc=STEEL, lw=0.6)
    drawbar_section(V)
    # box side with groove (inner face at u = 31)
    pts = [(16, 0), (31, 0), (31, 12.75), (23, 12.75), (23, 28.25), (31, 28.25), (31, hmax), (16, hmax)]
    if notch:
        pts = [(16, 0), (23.9, 0), (23.9, 4.6), (31, 4.6), (31, 12.75), (23, 12.75), (23, 28.25), (31, 28.25), (31, hmax), (16, hmax)]
    V.poly(pts, fc=PLYC, lw=0.8, z=3)
    V.line(16, hmax, 31, hmax, lw=0.8, z=4)
    # base in the groove
    V.rect(23, 13, 60, 28, fc="#f1dfb9", lw=0.6, z=3)
    V.line(34, hmax - 0, 36, hmax + 2, lw=0.3, c=GREY) if False else None
    if screw:
        V.rect(27.7 - 2.1, -1.5, 27.7 + 2.1, 0, fc="white", lw=0.4, z=5)          # clearance hole in the plate
        V.rect(27.7 - 1.75, -1.5, 27.7 + 1.75, 10.5, fc="#555", lw=0.5, z=6)       # shank
        V.rect(27.7 - 3.5, -4.1, 27.7 + 3.5, -1.5, fc="#555", lw=0.5, z=6)         # head
    if tab:
        V.rect(24.55, 0, 30.45, 4.0, fc=STEELD, lw=0.6, z=5)


def sheet8(pdf, png=None):
    sh = Sheet(pdf, 8, "DRAWER BOX ON THE DRAWBARS: SECTIONS AND FIXING OPTIONS", "Scale 1:1 (sections), 15 mm ply sides, drawbar 19.2 wide from the STEP file")
    s = 1.0
    # (a) typical section
    V = View(sh, 20, 190, s)
    side_section(V)
    V.title(-5, 66, "A: TYPICAL SECTION", "through a side, at any point along the box")
    V.dim_h(0, 14, -52, -6, "14")
    V.dim_h(14, 16, -52, -6, "2") if False else None
    V.dim_h(16, 31, 48, 6, "15 side")
    V.dim_h(14, 33.2, -16.2, -22 if False else -4, "19.2") if False else None
    V.dim_v(0, 12.75, 62, 6, "12.75"); V.dim_v(12.75, 28.25, 62, 6, "15.5") if False else None
    V.dim_v(-45, 0, -6, -5, "45")
    V.leader(8, -30, 18, -24, "runner: 3 plate + 11 block\n(steel stack hangs 45 below)", size=4.6, ha="left")
    V.leader(24, -8, 12, -10, "drawbar, plate top = box bottom", size=4.6, ha="left")
    V.leader(40, 20, 6, 10, "base 15 in the 15.5 x 8 groove", size=4.6, ha="left")
    V.leader(0, 40, 8, 10, "cabinet side", size=4.6, ha="left")
    V.dim_h(23, 31, 28.25, 4, "8") if False else None
    # (b) option 2: screw from below
    V = View(sh, 115, 190, s)
    side_section(V, screw=True)
    V.title(-5, 66, "B: OPTION 2, SCREW FROM BELOW", "drawbar hole 4.2 dia; screw No.6 x 12")
    V.dim_h(14, 27.7, -4.1, -8, "13.7")
    V.dim_h(27.7, 31, -4.1, -8, "3.3")
    V.leader(27.7, 8, 12, 14, "3.5 dia pilot, 10.5 deep", size=4.6, ha="left")
    V.leader(27.7, -3, 8, -18, "head 7 dia clears the 8 mm\nopening (17.7 to 31.7... 0.5 each side)", size=4.4, ha="left") if False else None
    V.leader(27.7, -3, -25, -40, "7 dia head inside the channel (0.5 clear)", size=4.6, ha="left")
    # (c) option 1: rear tab in the notch
    V = View(sh, 210, 190, s)
    side_section(V, notch=True, tab=True)
    V.title(-5, 66, "C: OPTION 1, REAR TAB IN THE NOTCH", "section through the tab (481.9 from the front end)")
    V.dim_h(23.9, 31, 4.6, 6, "7.1")
    V.dim_v(0, 4.6, 40, 6, "4.6")
    V.dim_v(0, 4.0, 18, -6, "4") if False else None
    V.leader(27.5, 3.5, -10, -24, "drawbar tab 4 high x 6 wide", size=4.6, ha="left")
    V.leader(24, 2, -14, 16, "notch in the inner bottom edge", size=4.6, ha="right")
    # (d) option 1: front clip, longitudinal section: u = distance from the front end of the side, z up (side bottom z = 0)
    V = View(sh, 305, 190, 2.0)
    V.rect(-15, -2, 0, 20, fc=PLYC, lw=0.8)                       # drawer front (back part)
    V.rect(0, 0, 40, 20, fc=PLYC, lw=0.8)                         # side (cut)
    V.line(0, 20, 40, 20, lw=0.5, ls=(0, (3, 2)))
    # bracket (approximate profile from the STEP file): stem at the front, arm along the bottom of the side
    V.poly([(0, 0), (26.5, 0), (26.5, -10.5), (11, -10.5), (3.5, -20), (3.5, -31), (0, -31)], fc="#7aa0d1", lw=0.6, z=3)
    # clip: plate 0.6 under the side, legs down into the bracket pocket, ears 2.4 up into the side
    V.rect(3.2, -0.6, 23.5, 0, fc="#e08a1e", lw=0.6, z=5)
    V.rect(20.5, 0, 23.5, 2.4, fc="#e08a1e", lw=0.5, z=5)
    V.rect(3.2, -12.2 + 0, 4.2, -0.6, fc="#e08a1e", lw=0.5, z=5)
    V.rect(22.5, -12.2 + 0, 23.5, -0.6, fc="#e08a1e", lw=0.5, z=5)
    # screw
    V.rect(10.7 - 1.75, -0.6, 10.7 + 1.75, 10.8, fc="#555", lw=0.5, z=6)
    V.rect(10.7 - 3.5, -3.2, 10.7 + 3.5, -0.6, fc="#555", lw=0.5, z=6)
    V.title(-17, 38, "D: OPTION 1, FRONT CLIP", "longitudinal section, scale 2:1")
    V.dim_h(3.2, 23.5, 2.4, 9 if False else 5, "20.3")
    V.dim_h(0, 3.2, -0.6, -8 if False else -5, "3.2") if False else None
    V.dim_h(0, 10.7, -3.2, -6, "10.7")
    V.leader(10.7, 8, 8, 6, "No.6 x 12 into a 3.5 pilot", size=4.2, ha="left")
    V.leader(22, 1.2, 4, 12, "ears 2.4 bite the ply", size=4.2, ha="left")
    V.leader(14, -6, 6, -6, "snap clip, legs in the\nbracket pocket", size=4.2, ha="left")
    V.leader(2, -26, -2, -6, "front bracket (profile\napproximate)", size=4.2, ha="left") if False else None
    V.txt(-7, 8, "FRONT", size=4, rot=90, c=GREY)
    # notes
    notes = [
        "The drawbar section is taken from the supplied STEP file; the bracket outline in D is approximate. The fixed runner block is shown as 14 x 45 (steel stack, true section not modelled).",
        "Drawbar outer face is 14 from the cabinet wall (11 to the fixing plates + 3 plate). The 8 mm underside opening faces away from the wall, and the rear tab sits 3.9 toward it from the drawbar centre.",
        "The side sits on the 15.2 flat of the drawbar, its outer face 16 from the wall. Left and right assemblies are mirror images. Option 1 notch is on the inner face; option 2 pilots are 3.3 from the inner face.",
        "Choose one option per build (DB_FIX in the model). Option 1 needs no cutting of the steel; option 2 needs the tabs ground off and 2 holes per drawbar (36.5 behind the bracket, 38 from the rear end).",
    ]
    for i, t in enumerate(notes):
        sh.ax.text(20, 105 - i * 5.0, t, fontsize=5.0, va="center")
    if png:
        sh.png(png)
    sh.save()


def sheet9(pdf, png=None):
    sh = Sheet(pdf, 9, "MITRE PULL PROFILES AND GAPS", "45 deg mitre pulls: top edge of D1 to D3, bottom edge of D1, D2 and the top strip. Sections at 3:1 and 2:1")
    import math as _m
    # (a) mitre top edge, 1.5:1. u = depth from the front face, v = height below the original top edge (0)
    V = View(sh, 22, 258, 1.5)
    top = 0.0
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
    # ---- A: top mitre, 3:1
    V = View(sh, 24, 246, 3.0)
    V.poly([(15, -32), (15, top - _L - 15.0), (7.5, top - _L - 15.0), (7.5, top - _L - 7.5)] + [(u, top + v) for (u, v) in _FILP] + [(u, top + v) for (u, v) in _ARCP[1:]] + [(0, -32)], fc=PLYC, lw=0.9)
    V.title(-2, 9, "A: TOP EDGE, 45 DEG MITRE WITH CATCH WALL (D1, D2, D3)", "section through a front, 3:1")
    V.dim_h(0, 15, -32, -6, "15")
    V.dim_v(top, top - 12.0, -2, -8, "12 to nose top")
    V.dim_v(top - _L - 7.5, top - _L - 15.0, 15, 8, "7.5 catch wall")
    V.dim_h(0, 7.5, top - _L - 15.0 - 3, 0, "7.5") if False else None
    V.dim_v(top, top - _L, 15, 8, "9.7 to apex")
    V.dim_v(top, top + _ZC, 15, 20, "14.9 to R3 start")
    V.line(-4, top, 19, top, lw=0.3, ls=(0, (4, 2)), c=GREY)
    V.leader(7.2, top - 9.2, 38, 10, "45 deg wall over the front 7.5 mm\nonly, then a vertical catch wall\n(rebate from the back, half thickness)", size=4.6, ha="left")
    V.leader(0, top + _ZC, 15, -18, "R3 roundover bit, tangent to the face\n14.9 below the top edge. It meets the\nmitre face at an edge: sand an R1\nfillet there by hand", size=4.6, ha="left")
    # ---- A2: bottom mitre, 3:1
    W = View(sh, 128, 124, 3.0)
    W.poly([(15, 36)] + _BOTP + [(0, 36)], fc=PLYC, lw=0.9)
    W.title(-2, 41, "A2: BOTTOM EDGE, 45 DEG MITRE (D1, D2)", "section through a front, 3:1")
    W.dim_v(0, 15, -2, -8, "15 high on the face")
    W.dim_h(0, 15, 0, -6, "15")
    W.leader(0.6, _BTF + 15.0, -9, 8, "R3 on the face arris", size=4.6, ha="right")
    W.leader(15 - 0.3, 1.2, 8, -9, "R2 on the thin back edge\n(no sharp edge: the runners\nself-close)", size=4.6, ha="left")
    W.leader(8, 8, 8, 14, "45 deg through the full 15 mm;\nD3 has a plain bottom edge", size=4.6, ha="left")
    # ---- C: the stack at the top of the unit, 2:1. u = distance back from the benchtop front edge, v = height above the benchtop underside
    C = View(sh, 224, 242, 2.0)
    vt = (128.602 - 106.279) * -1.0        # D1 top edge, 22.3 below the benchtop underside
    bs = -(128.602 - 96.298)               # bottom edge of the top strip (32.3 below the underside)
    C.rect(0, 0, 60, 12, fc="#efe0bd", hatch="....", lw=0.8)                      # benchtop (26, cut off)
    C.rect(0, -12, 12, 0, fc="#e3cf9f", hatch="////", lw=0.6)                     # 12 mm front hem
    C.rect(38, -15, 60, 0, fc=PLY, hatch="////", lw=0.6)                          # top rail C9
    C.rect(32, -15, 38, 0, fc="#f1dfb9", hatch="////", lw=0.5)                    # 6 mm packer
    C.poly([(32, 0), (17, 0)] + [(17 + u, bs + v) for (u, v) in reversed(_BOTP)], fc=PLYC, lw=0.9)    # top strip (false front)
    C.poly([(32, vt - 55), (32, vt - _L - 15.0), (24.5, vt - _L - 15.0), (24.5, vt - _L - 7.5)] + [(17 + u, vt + v) for (u, v) in _FILP] + [(17 + u, vt + v) for (u, v) in _ARCP[1:]] + [(17, vt - 55)], fc=PLYC, lw=0.9)   # D1
    C.line(12, -12, 46, -46, lw=0.5, ls=(0, (5, 2)), c=RED)                       # 45 deg plane through the back-bottom edge of the hem
    C.line(17, vt - _L, 46, vt - _L - 29, lw=0.5, ls=(0, (5, 2)), c=RED)          # D1 mitre plane
    C.title(-2, 17, "C: THE STACK AT THE TOP (D1 UNDER THE TOP STRIP)", "section through the front edge, 2:1; D2 sits under D1 in the same way")
    C.txt(46.5, 14, "BENCHTOP", size=4.4, c=GREY)
    C.txt(6, -6, "HEM", size=4.2, c=GREY)
    C.txt(49, -7.5, "C9", size=4.4, c=GREY)
    C.txt(35, -7.5, "6", size=4.0, c=GREY)
    C.txt(23, -12, "TOP\nSTRIP", size=4.4, c="#6b5a3c")
    C.txt(24, vt - 36, "D1", size=6.5, c="#6b5a3c", weight="bold")
    C.dim_v(-61.0, -46.0, 47, 0, "15 finger gap\n(vertical)")
    C.dim_v(bs, vt, 9, -8, "10 overlap")
    C.dim_v(vt - 12.16, bs + 2.83, 33, 12, "5 closed gap")
    C.leader(12, -12, -14, -10, "hem back-bottom edge:\n45 deg plane runs from here", size=4.4, ha="right")
    # ---- notes
    notes = ["Pulls: every front has a 45 degree mitre on the front 7.5 mm of its top edge (R3 nose, R1 sanded) and a vertical 7.5 mm catch wall behind it, a rebate from the back at half thickness, down to the shelf 24.7 below the top edge. The fingertip hooks the catch wall. D1 and D2 also have a 45 degree mitre on the bottom edge (15 high on the face, R3 and R2 rounded). D3 has a plain bottom edge.",
             "Fingertips go into the gap between the bottom mitre of a front (or of the top strip) and the top mitre of the front below, then hook the catch wall. The faces are parallel, 15 mm apart vertically (about 10.5 square to the faces). Measured with calipers: 15 gets a finger past the first knuckle, 10 only the tip.",
             "Each nose stays 5 mm below the lowest point of the front above (after rounding the thin edge) and fronts overlap 10 mm, so a drawer cannot catch the one below as it opens. The fronts fix to the boxes through 6 mm oversize holes (about 1 mm of play each way), set on 2 mm spacers.",
             "D1's top edge is placed so that its mitre plane is 15 mm (vertical) below a parallel 45 degree plane through the back-bottom edge of the benchtop hem. The top strip (802 x 32.3, glued to a 6 mm packer on C9) has the same bottom mitre as D1 and D2.",
             "Rout the rebate from the back first (straight bit, 7.5 wide, to the shelf), then cut the 45 degree lip with the chamfer cutter; an optional 14 degree dovetail pass into the catch wall undercuts it. Bottom mitres on a tilted saw or with the chamfer bit and a fence. Round the R3 and R2 with roundover bits, then sand the R1 edge by hand. Test the profile on an offcut first; the nose is a 45 degree wedge: handle with care."]
    stack(sh.ax, 24, 96, notes, fs=5.0, width=165, gap=1.6)
    if png:
        sh.png(png)
    sh.save()


def nest_sheets():
    SW, SH, K = 2400.0, 1200.0, 3.0
    parts = []
    def add(lbl, w, h, q=1, rot=True):
        for i in range(q):
            parts.append((lbl if q == 1 else "%s%d" % (lbl, i + 1), w, h, rot))
    add("C1", 749, 522); add("C2", 749, 522); add("C3", 775, 507); add("C4", 775, 749); add("C9", 775, 60)
    add("P1", 767, 125); add("P2", 767, 125); add("P3", 461, 125); add("P4", 461, 125); add("Kb", 852, 115, rot=False)
    add("D1F", 802, 212.7, rot=False); add("D2F", 802, 212.7, rot=False); add("D3F", 802, 326.3, rot=False); add("TS", 802, 32.3, rot=False)
    add("D1sL", 495, 153); add("D1sR", 495, 153); add("D2sL", 495, 153); add("D2sR", 495, 153)
    add("D3sL", 495, 231); add("D3sR", 495, 231)
    add("D1bk", 713, 148); add("D2bk", 713, 148); add("D3bk", 713, 226)
    for n in ("D1", "D2", "D3"):
        add(n + "base", 728.5, 487.5)

    def pack(order, rule):
        sheets = []
        for (name, w, h, rot) in order:
            placed = False
            for sh in sheets + [None]:
                if sh is None:
                    sh = {"free": [(0, 0, SW, SH)], "pl": []}; sheets.append(sh)
                best = None
                for idx, (x, y, fw, fh) in enumerate(sh["free"]):
                    for (pw, ph, r) in ((w, h, False),) + (((h, w, True),) if rot else ()):
                        if pw <= fw and ph <= fh:
                            sc = min(fw - pw, fh - ph) if rule & 1 else fw * fh - pw * ph
                            if best is None or sc < best[0]:
                                best = (sc, idx, pw, ph, r)
                if best:
                    _, idx, pw, ph, r = best
                    x, y, fw, fh = sh["free"].pop(idx)
                    sh["pl"].append((name, x, y, pw, ph, r))
                    if rule & 2:
                        if fw - pw - K > 0: sh["free"].append((x + pw + K, y, fw - pw - K, fh))
                        if fh - ph - K > 0: sh["free"].append((x, y + ph + K, pw, fh - ph - K))
                    else:
                        if fw - pw - K > 0: sh["free"].append((x + pw + K, y, fw - pw - K, ph))
                        if fh - ph - K > 0: sh["free"].append((x, y + ph + K, fw, fh - ph - K))
                    placed = True
                    break
        return sheets
    random.seed(5)
    best = None
    for t in range(6000):
        o = parts[:]
        o.sort(key=lambda p: -(p[1] * p[2]) * random.uniform(0.6, 1.4))
        for rule in range(4):
            r = pack(o, rule)
            if best is None or len(r) < len(best):
                best = r
        if len(best) <= 2:
            break
    return best, SW, SH


def sheet10(pdf, png=None):
    sh = Sheet(pdf, 10, "CUTTING DIAGRAMS: EXTENSION UNIT", "2 sheets of 2400 x 1200 x 15 ply. Scale 1:10. 3 mm kerf allowed")
    sheets, SW, SH = nest_sheets()
    area = sum(p[3] * p[4] for s_ in sheets for p in s_["pl"]) / 1e6
    oys = [157, 17]
    for i, sd in enumerate(sheets[:2]):
        V = View(sh, 20, oys[i] + 4, 0.095)
        V.rect(0, 0, SW, SH, fc="#faf6ee", lw=0.9)
        V.title(0, SH + 70, "SHEET %s" % "AB"[i], "fill %.0f%%" % (100 * sum(p[3] * p[4] for p in sd["pl"]) / (SW * SH)))
        for (n, x, y, w, h, r) in sd["pl"]:
            V.rect(x, y, x + w, y + h, fc=PLYC, lw=0.6)
            V.txt(x + w / 2, y + h / 2 + 8, n, size=5.5, weight="bold", c="#6b5a3c")
            V.txt(x + w / 2, y + h / 2 - 22, "%g x %g%s" % (max(w, h) if not r else w, min(w, h) if not r else h, " (rot)" if r else ""), size=4.2)
        V.dim_h(0, SW, 0, -5, "2400"); V.dim_v(0, SH, 0, -5, "1200")
    notes = [
        "Grain: fronts (D1F to D3F) and the kickboard cover (Kb) are kept with the long edge along the sheet length.",
        "Other parts may be rotated to fit, so the nesting is tight (about %.0f%% of two sheets). Check it before cutting;" % (100 * area / (2 * SW * SH / 1e6)),
        "if the grain must run the long way on every part, a third sheet may be needed.",
        "Bin drawer, bay panels and sliding door (not part of the extension unit) are cut from a third sheet.",
        "Sheet 11 is the alternative layout for a panel saw that only cuts on 100 mm multiples.",
        "Label: Cx carcass/plinth; Dnx drawer n: F front, sL/sR sides, bk back, base. 30 mm of clearance around each part is not shown.",
    ]
    notes = [notes[0], notes[1] + " " + notes[2]] + notes[3:]
    yn = stack(sh.ax, 272, 270, notes, fs=5.2, width=92, gap=2.0)
    # ---- cut list: identical pieces grouped, sizes as cut (length x width, 15 mm ply) ----
    import textwrap as _t2
    groups = {}
    for si_, s_ in enumerate(sheets[:2]):
        for (n_, x_, y_, pw_, ph_, r_) in s_["pl"]:
            L_, W_ = (ph_, pw_) if r_ else (pw_, ph_)
            groups.setdefault((L_, W_), []).append((n_, "AB"[si_]))
    a_ = sh.ax
    x0_, y0_ = 272, yn - 4
    a_.text(x0_, y0_, "CUT LIST (15 mm ply, as cut; every piece is also placed on the diagrams)", fontsize=6.4, weight="bold", va="top")
    y0_ -= 6.5
    cols_ = [(x0_, "Qty"), (x0_ + 9, "Length"), (x0_ + 24, "Width"), (x0_ + 38, "Parts (sheet)")]
    for xx_, tt_ in cols_:
        a_.text(xx_, y0_, tt_, fontsize=5.2, weight="bold", va="top")
    y0_ -= 3.9
    a_.plot([x0_, 410], [y0_ + 0.6, y0_ + 0.6], lw=0.5, c=INK)
    y0_ -= 1.2
    total_ = 0
    for (L_, W_), lst in sorted(groups.items(), key=lambda kv: (-kv[0][0] * kv[0][1])):
        txt_ = ", ".join("%s (%s)" % (n_, sh_) for n_, sh_ in sorted(lst))
        lines_ = _t2.wrap(txt_, 62)
        a_.text(x0_, y0_, "%d" % len(lst), fontsize=5.2, va="top")
        a_.text(x0_ + 9, y0_, "%g" % L_, fontsize=5.2, va="top")
        a_.text(x0_ + 24, y0_, "%g" % W_, fontsize=5.2, va="top")
        for k_, ln_ in enumerate(lines_):
            a_.text(x0_ + 38, y0_ - k_ * 3.5, ln_, fontsize=5.2, va="top")
        y0_ -= 3.5 * len(lines_) + 0.9
        total_ += len(lst)
    a_.plot([x0_, 410], [y0_ + 0.4, y0_ + 0.4], lw=0.5, c=INK)
    a_.text(x0_, y0_ - 1.0, "%d pieces from 2 sheets of 2400 x 1200 x 15. Length is the first number; the 3 mm kerf is not included in these sizes." % total_,
            fontsize=5.0, va="top")
    if png:
        sh.png(png)
    sh.save()
    return sheets


def sheet11(pdf, png=None):
    """Bunnings layout: every store cut on a multiple of 100 mm; blanks trimmed to the final parts at home."""
    import json
    L = json.load(open("/home/user/CAD/kitchen_bench_extension/shop_drawings/round_layout.json"))
    SWd, SHd = 2400.0, 1200.0
    sh = Sheet(pdf, 11, "CUTTING DIAGRAMS: STORE CUTS ON 100 MM MULTIPLES",
               "3 sheets of 2400 x 1200 x 15 ply. Scale 1:13. Alternative to sheet 10 if the store only cuts to 100 mm")
    sc = 0.075
    origins = [(18, 186), (18, 66), (215, 186)]
    lines_cut = []
    lines_home = []
    for si, sheet in enumerate(L):
        ox, oy = origins[si]
        V = View(sh, ox, oy, sc)
        V.rect(0, 0, SWd, SHd, fc="#faf6ee", lw=0.9)
        tot = sum(s["h"] * s["used"] for s in sheet) / (SWd * SHd)
        V.title(0, SHd + 60, "SHEET %s" % "ABC"[si], "blanks fill %.0f%% of the sheet" % (100 * tot))
        y = 0.0
        rips = []
        for sti, st in enumerate(sheet):
            x = 0.0
            xcuts = []
            for bi, b in enumerate(st["blocks"]):
                lab = "%s%d" % ("ABC"[si], len([1 for s_ in sheet[:sti] for _ in s_["blocks"]]) + bi + 1)
                bw, bh = b["w"], b["h"]
                V.rect(x, y, x + bw, y + bh, fc="#efe3c6", lw=1.0)
                names = []
                for (n, px, py, pw, ph, prot) in b["parts"]:
                    if b["rot"]:
                        px, py, pw, ph = py, px, ph, pw
                    V.rect(x + px, y + py, x + px + pw, y + py + ph, fc=PLYC, lw=0.4)
                    V.txt(x + px + pw / 2, y + py + ph / 2, n, size=3.6, weight="bold", c="#6b5a3c")
                    names.append("%s %g x %g" % (n, max(pw, ph), min(pw, ph)))
                V.txt(x + 14, y + bh - 28, "%s  %g x %g" % (lab, bw, bh), size=3.8, ha="left", c="#2c6e2c")
                x += bw
                xcuts.append(x)
                if len(b["parts"]) > 1:
                    lines_home.append("%s (%g x %g): %s" % (lab, bw, bh, " + ".join(names)))
                else:
                    lines_home.append("%s (%g x %g): %s" % (lab, bw, bh, names[0]))
            y += st["h"]
            if y < SHd - 1:
                rips.append(y)
                V.line(0, y, SWd, y, lw=1.0, c="#2c6e2c")
            for xc in xcuts[:-1] + ([xcuts[-1]] if xcuts[-1] < SWd - 1 else []):
                V.line(xc, y - st["h"], xc, y, lw=1.0, c="#2c6e2c")
            lines_cut.append("Sheet %s strip %d (%g wide): cross-cut at %s" % ("ABC"[si], sti + 1, st["h"],
                                                                         ", ".join("%g" % c for c in xcuts if c < SWd - 1) or "no cross-cut"))
        lines_cut.insert(len([l for l in lines_cut if l.startswith("Sheet %s" % "ABC"[si])]) - len(sheet) if False else
                         len(lines_cut) - len(sheet), "Sheet %s: rip at %s from the long edge" % ("ABC"[si], ", ".join("%g" % r for r in rips) or "none (single strip)"))
        V.dim_h(0, SWd, 0, -5, "2400"); V.dim_v(0, SHd, 0, -5, "1200")
    tx, ty = 215, 175
    stack(sh.ax, tx, ty, ["STORE CUTS (all on multiples of 100, measured from the sheet edge or the last cut face)"], fs=6.4, width=80, weight="bold")
    ty2 = stack(sh.ax, tx, ty - 13, lines_cut, fs=5.6, width=95, gap=0.6) - 6
    ty2 = stack(sh.ax, tx, ty2, ["BLANKS AND WHAT TO TRIM AT HOME (green = cut at the store; stacked parts are separated at home, 3 mm kerf allowed)"], fs=5.8, width=90, weight="bold") - 1
    stack(sh.ax, tx, ty2, lines_home, fs=5.2, width=100, gap=0.4, indent=4)
    stack(sh.ax, 18, 26, ["Every part is cut oversize to a 100 mm blank and trimmed at home; blanks that hold two or more parts need a home cut between them. "
               "Grain: D1F to D3F and Kb stay with the long edge along the sheet. The saw kerf (about 3 mm) is taken from the waste side. "
               "Sheet C has room left for the bin drawer, bay and door parts."], fs=5.0, width=165, gap=0.0)
    if png:
        sh.png(png)
    sh.save()
