# Kitchen bench extension: 3-drawer unit. World coordinates are those of bench.step (mm, Z up).
# Drawer fronts face -X.

BUILD_DRAWERS = True

# ---- datum from bench.step placeholders ----
X_EDGE = 2440.885      # benchtop front edge (drawer-front side)
X_BACK = 3040.885      # back / right end, flush with main bench end
Y_A = -389.421         # free end of BenchtopExt
Y_B = 430.579          # joint with main benchtop
Z_TOP = 109.602        # underside of benchtop
Z_FLOOR = -745.398
Z_PLINTH_TOP = -630.398

T = 16.0               # carcass / plinth / drawer side ply
FRONT_T = 19.0

# ---- carcass ----
FREE_OVERHANG = 15.0
X_CARC_FRONT = X_EDGE + 23.0            # 2463.885
Y_SIDE_A0 = Y_A + FREE_OVERHANG          # free-end side outer face
Y_SIDE_A1 = Y_SIDE_A0 + T
Y_SIDE_B1 = Y_B                          # back-end side outer face (flush with joint)
Y_SIDE_B0 = Y_SIDE_B1 - T
OPEN_W = Y_SIDE_B0 - Y_SIDE_A1           # 773 clear between sides
YC = (Y_SIDE_B0 + Y_SIDE_A1) / 2.0
X_BACKP0 = X_BACK - T
Z_BOT_TOP = Z_PLINTH_TOP + T


def box(x0, x1, y0, y1, z0, z1):
    return Part.cuboid(x1 - x0, y1 - y0, z1 - z0).moved(
        Location.translation((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))


COL_PLY = (0.86, 0.72, 0.52)
COL_FRONT = (0.918, 0.918, 0.918)
COL_STEEL = (0.62, 0.64, 0.68)
COL_HANDLE = (0.498, 0.498, 0.498)
COL_BOARD = (0.93, 0.84, 0.64)

# ---------------- reference: main bench from bench.step ----------------
imp = import_step_file("/home/user/CAD/kitchen_bench_extension/bench.step")
KEEP = {"benchtop", "BenchtopExt", "framing", "Kickboard"}
rest = []
for p in imp.parts():
    n = p.name()
    if n == "KickboardExt":
        continue  # replaced by the plinth fascia below
    if n in KEEP:
        show(p, "ref_" + n, group="Reference bench")
    else:
        rest.append(p)
FULL_REF = False   # True for the final export: every bench.step part is shown
if FULL_REF:
    seen = {}
    for p in rest:
        n = p.name()
        seen[n] = seen.get(n, 0) + 1
        show(p, "ref_" + n.replace(" ", "_") + ("" if seen[n] == 1 else f"_{seen[n]}"), group="Reference bench")

# ---------------- carcass ----------------
side_a = box(X_CARC_FRONT, X_BACK, Y_SIDE_A0, Y_SIDE_A1, Z_PLINTH_TOP, Z_TOP)
side_b = box(X_CARC_FRONT, X_BACK, Y_SIDE_B0, Y_SIDE_B1, Z_PLINTH_TOP, Z_TOP)
bottom = box(X_CARC_FRONT, X_BACKP0, Y_SIDE_A1, Y_SIDE_B0, Z_PLINTH_TOP, Z_BOT_TOP)
backp = box(X_BACKP0, X_BACK, Y_SIDE_A1, Y_SIDE_B0, Z_BOT_TOP, Z_TOP)
STR_W = 60.0
str_front = box(X_CARC_FRONT, X_CARC_FRONT + STR_W, Y_SIDE_A1, Y_SIDE_B0, Z_TOP - T, Z_TOP)
str_rear = box(X_BACKP0 - STR_W, X_BACKP0, Y_SIDE_A1, Y_SIDE_B0, Z_TOP - T, Z_TOP)

# ---------------- plinth frame ----------------
RET_OUT = Y_SIDE_A0 + 6.0
fascia = box(X_EDGE + 9.0, X_EDGE + 9.0 + T, RET_OUT, 445.579, Z_FLOOR, Z_PLINTH_TOP)
FX1 = X_EDGE + 9.0 + T                                  # fascia back face
ret_free = box(FX1, X_BACKP0 + 8.0, RET_OUT, RET_OUT + T, Z_FLOOR, Z_PLINTH_TOP)
ret_back_y1 = Y_SIDE_B1 - 2.0
ret_joint = box(FX1, X_BACKP0 + 8.0, ret_back_y1 - T, ret_back_y1, Z_FLOOR, Z_PLINTH_TOP)
rail_rear = box(X_BACKP0 - 4.0, X_BACKP0 + 12.0, RET_OUT + T, ret_back_y1 - T, Z_FLOOR, Z_PLINTH_TOP)

grp = "Carcass"
show(side_a, "side_free_end", colour=COL_PLY, group=grp)
show(bottom, "carcass_bottom", colour=COL_PLY, group=grp)
show(backp, "carcass_back", colour=COL_PLY, group=grp)
show(str_front, "stretcher_front", colour=COL_PLY, group=grp)
show(str_rear, "stretcher_rear", colour=COL_PLY, group=grp)
grp = "Plinth"
show(fascia, "KickboardExt", colour=(0.65, 0.65, 0.65), group=grp)
show(ret_free, "plinth_return_free_end", colour=(0.65, 0.65, 0.65), group=grp)
show(ret_joint, "plinth_rail_joint_end", colour=(0.65, 0.65, 0.65), group=grp)
show(rail_rear, "plinth_rail_rear", colour=(0.65, 0.65, 0.65), group=grp)

print("opening width", OPEN_W, "yc", YC, "inside depth", X_BACKP0 - X_CARC_FRONT)

# ======================= drawers =======================
import math
from functools import reduce


def cyl(p0, d, length, r):
    n = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
    d = (d[0] / n, d[1] / n, d[2] / n)
    c = Part.cylinder(r, length)
    ax = (-d[1], d[0], 0.0)
    s = math.hypot(ax[0], ax[1])
    if s > 1e-9:
        c = c.moved(Location.about(Axis((0, 0, 0), (ax[0] / s, ax[1] / s, 0.0)), math.degrees(math.atan2(s, d[2]))))
    elif d[2] < 0:
        c = c.moved(Location.about(Axis((0, 0, 0), (1, 0, 0)), 180.0))
    m = (p0[0] + d[0] * length / 2, p0[1] + d[1] * length / 2, p0[2] + d[2] * length / 2)
    return c.moved(Location.translation(*m))


def add(p, k, d):
    return (p[0] + d[0] * k, p[1] + d[1] * k, p[2] + d[2] * k)


def fuse_list(lst):
    return reduce(lambda a, b: a + b, lst)


A15 = math.radians(15.0)
SCREW_L = 25.0


def pocket_set(E_list, d):
    """E_list: exit points on the end grain. Returns (cutter, screws) for the pocket holes."""
    cuts, screws = [], []
    for E in E_list:
        tip = add(E, 9.0, d)
        S = add(tip, -SCREW_L, d)
        cuts.append(cyl(add(S, -14.0, d), d, 14.0, 4.75))      # 9.5 mm pocket bore, open to the face
        cuts.append(cyl(S, d, 16.0 + 3.0, 1.9))                  # pilot to the end grain
        shaft = cyl(S, d, SCREW_L, 2.0)
        head = cyl(add(S, -3.0, d), d, 3.0, 4.0)
        screws.append(shaft + head)
    return fuse_list(cuts), screws


FRONT_FACE_X = X_EDGE + 2.0
XF = FRONT_FACE_X + FRONT_T                 # back face of the drawer front
NL = 550.0                                  # Blum TANDEM 563H5500B runner / drawer side length
BOX_W = OPEN_W - 10.0                       # 763 -> inside = opening - 42 = 731
SIDE_IN = BOX_W / 2.0 - T                   # 365.5 from centre
GROOVE_D = 8.0
BOT_T = 12.0
GR0, GR1 = 12.75, 25.25                     # groove z band above side bottom edge (board underside at +13)

FRONT_H = [165.0, 165.0, 394.0]             # drawers 1 (top), 2, 3 (bottom)
GAP = 3.0
BOX_H = [120.0, 120.0, 320.0]
fr_bottom = [0, 0, Z_PLINTH_TOP + 5.0]
fr_bottom[1] = fr_bottom[2] + FRONT_H[2] + GAP
fr_bottom[0] = fr_bottom[1] + FRONT_H[1] + GAP
OB = [b + 11.0 for b in fr_bottom]          # runner "opening bottom" of each drawer


def drawer(i):
    nm = f"drawer{i + 1}"
    zb = OB[i] + 14.0                       # side bottom edge
    hb = BOX_H[i]
    f0, f1 = fr_bottom[i], fr_bottom[i] + FRONT_H[i]
    xr = XF + NL                            # rear face of the box
    yl0, yr1 = YC - BOX_W / 2.0, YC + BOX_W / 2.0
    yl1, yr0 = yl0 + T, yr1 - T
    g0, g1 = zb + GR0, zb + GR1

    # --- front panel with stopped groove ---
    front = box(FRONT_FACE_X, XF, YC - 401.0, YC + 401.0, f0, f1)
    front = front - box(XF - GROOVE_D, XF + 0.1, YC - SIDE_IN - GROOVE_D, YC + SIDE_IN + GROOVE_D, g0, g1)

    # --- sides with through groove (open at the rear for the board) ---
    sl = box(XF, xr, yl0, yl1, zb, zb + hb)
    sr = box(XF, xr, yr0, yr1, zb, zb + hb)
    sl = sl - box(XF - 0.1, xr + 0.1, yl1 - GROOVE_D, yl1 + 0.1, g0, g1)
    sr = sr - box(XF - 0.1, xr + 0.1, yr0 - 0.1, yr0 + GROOVE_D, g0, g1)

    # --- back, bottom ---
    back = box(xr - T, xr, yl1, yr0, zb + GR1, zb + hb)
    bottom = box(XF - GROOVE_D + 0.5, xr, YC - SIDE_IN - GROOVE_D + 0.25, YC + SIDE_IN + GROOVE_D - 0.25, zb + 13.0, zb + 13.0 + BOT_T)

    # --- pocket holes: sides -> front (drilled in the outer face of the sides) ---
    zs = [zb + 50.0, zb + 90.0] if hb < 200 else [zb + 60.0, zb + 160.0, zb + 260.0]
    scr = []
    dl = (-math.cos(A15), math.sin(A15), 0.0)
    El = [(XF, yl0 + GROOVE_D, z) for z in zs]
    # left side outer face is yl0 (inward = +y); exit points on the end grain at depth 8
    dl = (-math.cos(A15), +math.sin(A15), 0.0)
    El = [(XF, yl0 + 9.0, z) for z in zs]
    cut_l, scr_l = pocket_set(El, dl)
    dr = (-math.cos(A15), -math.sin(A15), 0.0)
    Er = [(XF, yr1 - 9.0, z) for z in zs]
    cut_r, scr_r = pocket_set(Er, dr)
    sl = sl - cut_l
    sr = sr - cut_r
    scr += scr_l + scr_r

    # --- pocket holes: back -> sides (drilled in the rear face of the back) ---
    zk = [zb + 50.0, zb + 95.0] if hb < 200 else [zb + 60.0, zb + 170.0, zb + 270.0]
    dbl = (-math.sin(A15), -math.cos(A15), 0.0)
    cut_bl, scr_bl = pocket_set([(xr - 9.0, yl1, z) for z in zk], dbl)
    dbr = (-math.sin(A15), +math.cos(A15), 0.0)
    cut_br, scr_br = pocket_set([(xr - 9.0, yr0, z) for z in zk], dbr)
    back = back - cut_bl - cut_br
    scr += scr_bl + scr_br

    # --- handle (same style as the main run) ---
    zc = (f0 + f1) / 2.0
    HL = 300.0
    grip = box(FRONT_FACE_X - 36.0, FRONT_FACE_X - 24.0, YC - HL / 2, YC + HL / 2, zc - 6.0, zc + 6.0)
    st = [cyl((FRONT_FACE_X, YC + s * 120.0, zc), (-1, 0, 0), 26.683, 5.0) for s in (-1, 1)]
    handle = grip + st[0] + st[1]

    # --- Blum TANDEM 563H5500B runners (envelope model) ---
    rx0 = X_CARC_FRONT + 3.0
    zr0 = OB[i] + 2.0
    run_l = box(rx0, rx0 + NL, Y_SIDE_A1, Y_SIDE_A1 + 1.5, zr0, zr0 + 40.0) + \
        box(rx0, rx0 + NL, Y_SIDE_A1, Y_SIDE_A1 + 21.0, zr0, zr0 + 12.0)
    run_r = box(rx0, rx0 + NL, Y_SIDE_B0 - 1.5, Y_SIDE_B0, zr0, zr0 + 40.0) + \
        box(rx0, rx0 + NL, Y_SIDE_B0 - 21.0, Y_SIDE_B0, zr0, zr0 + 12.0)

    g = f"Drawer {i + 1}"
    show(front, f"{nm}_front", colour=COL_FRONT, group=g)
    show(sl, f"{nm}_side_L", colour=COL_PLY, group=g)
    show(sr, f"{nm}_side_R", colour=COL_PLY, group=g)
    show(back, f"{nm}_back", colour=COL_PLY, group=g)
    show(bottom, f"{nm}_bottom", colour=COL_BOARD, group=g)
    show(handle, f"{nm}_handle", colour=COL_HANDLE, group=g)
    show(fuse_list(scr), f"{nm}_pocket_screws", colour=COL_STEEL, group=g, solids=len(scr))
    g = "Hardware - Blum TANDEM 563H5500B"
    show(run_l, f"{nm}_runner_L", colour=COL_STEEL, group=g)
    show(run_r, f"{nm}_runner_R", colour=COL_STEEL, group=g)


if BUILD_DRAWERS:
    for i in range(3):
        drawer(i)
    print("OB", OB, "front bottoms", fr_bottom, "box w", BOX_W)


# ======================= fixings to the unit / benchtop =======================
def fixings():
    # six No.8 x 32 screws up through the stretchers into the benchtop (removable from below)
    tops = []
    for xs in (X_CARC_FRONT + 30.0, X_BACKP0 - 30.0):
        for dy in (-300.0, 0.0, 300.0):
            y = YC + dy
            tops.append(cyl((xs, y, Z_TOP - T - 3.0), (0, 0, 1), 3.0, 4.0) + cyl((xs, y, Z_TOP - T), (0, 0, 1), 32.0, 2.0))
    show(fuse_list(tops), "benchtop_screws", colour=COL_STEEL, group="Fixings", solids=len(tops))
    # two M6 x 50 link bolts from the joint-end side into the main run's front framing rail
    bolts = []
    holes = []
    for xb in (2640.0, 2860.0):
        z = 100.0
        holes.append(cyl((xb, Y_SIDE_B0 - 1.0, z), (0, 1, 0), T + 2.0, 3.25))
        bolts.append(cyl((xb, Y_SIDE_B0 - 5.0, z), (0, 1, 0), 5.0, 5.0) + cyl((xb, Y_SIDE_B0, z), (0, 1, 0), 50.0, 3.0))
    show(fuse_list(bolts), "link_bolts_to_main_run", colour=COL_STEEL, group="Fixings", solids=len(bolts))
    return fuse_list(holes)


_link_holes = fixings()
show(side_b - _link_holes, "side_joint_end", colour=COL_PLY, group="Carcass")
