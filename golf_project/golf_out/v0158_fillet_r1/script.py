# Kitchen bench extension: 3-drawer unit. World coordinates are those of bench.step (mm, Z up).
# Drawer fronts face -X.

BUILD_DRAWERS = True
DRAWER_SYS = "drawbar"   # "timber" = plywood boxes on Blum TANDEM; "alto" = Hafele Alto steel sides + ply base/back;
                         # "drawbar" = plywood boxes fixed straight onto the Hafele Alto runner drawbars (no steel sides)
PULL = "mitre"           # drawbar boxes finger pull: "front_cove" (front-face cove, for push-to-open), "back_cove" (cove on the back
                         # of the top edge, 20 mm air gap above every front) or "slot" (finger-pull slot cutter, same gaps)
GRV_TOP, GRV_OPEN, GRV_D, GRV_ANG, GRV_LEN = 25.0, 17.32, 8.0, 14.0, 810.0   # GRV_OPEN = corner-to-corner opening; with the 3 mm radii the visible span is 25.0
GRV_RAD = 3.0
MIT_ANG, MIT_COVE_R = 45.0, 10.0   # PULL = "mitre": 45 degree undercut through the full 15 mm front on the top edge (R3 on the lip), plus an R10 cove on the bottom edge of D1 and D2
MIT_FIL = 1.0         # PULL = "mitre": R1 fillet, hand sanded, on the edge where the R3 arc meets the mitre face
MIT_BIT_UP = 2.0       # PULL = "mitre": the R3 roundover bit is set this much higher than the tangent position, so its arc meets the mitre face at a crisp edge
import math as _m
_md = GRV_RAD / _m.tan(_m.radians(MIT_ANG) / 2.0)   # tangent distance of an R3 on the 45 degree apex (7.243)
_mk = _md - MIT_BIT_UP
_mx = ((GRV_RAD + _mk) - _m.sqrt((GRV_RAD + _mk) ** 2 - 2.0 * _mk ** 2)) / 2.0
MIT_L = 12.0 - _mx     # depth of the (sharp) apex below the top edge so the nose top stays 12.0 below it
REB_SPAN = 15.0       # rebate pull: top edge to the radius tangent point on the face            # "groove": external radius (roundover) on the two edges of the opening   # "groove": undercut finger groove in the front face (dovetail bit):
                         # opening starts GRV_TOP below the top edge, GRV_OPEN tall at the face, GRV_D deep, GRV_ANG deg undercut, GRV_LEN long (centred;
                         # 810 > the 802 front width = full width, open at both ends)
SLOT_K = 6.0             # "slot": cutter setback, i.e. how far the cutter axis sits outside the edge minus its cove radius (mm)
# Silhouette of the 1/4" shank x 25.4 mm finger pull bit (user's photo): (height above the cutter bottom, radius from the axis).
# Overall 25.4 mm dia x 21 mm; points read off the photo's proportions, so good to about 0.5 mm.
SLOT_BIT = [(21.0, 10.0), (20.4, 11.7), (19.0, 12.6), (17.0, 12.7), (15.0, 12.3), (13.6, 11.0), (12.6, 8.8), (11.6, 7.2),
            (10.4, 6.2), (9.0, 5.8), (7.6, 6.0), (6.4, 6.9), (5.5, 8.2), (4.8, 9.6), (0.0, 9.6)]
BASE_SLOT = "back"       # drawbar boxes: which panel takes the routed base slot besides the sides: "back" (box built front-last, base slid in
                         # from the front, plain front panel) or "front" (original: groove in the front, base slid in from the back)
BACK_Z0 = 5.0            # back panel bottom edge above the side bottom edge when the base slot is in the back
COVE_R = 9.5              # drawbar boxes: radius of the routed cove finger pull along the top of each extension front (0 = none)
HANDLES = False          # drawbar boxes: bar handles on the extension fronts (False = cove pull instead)
DB_FIX = 1               # drawbar sets: 1 = snap clip at the front + rear tab in a notch; 2 = tab ground off + 2 screws from below

# ---- assembly-sequence staging: STAGE >= 10 shows everything ----
STAGE = 10
_golf_show = show


def _visible(name, group):
    if name == "ref_BenchtopExt":
        return STAGE >= 9
    g = group or ""
    if g == "Reference bench":
        return True
    if g == "Plinth":
        return STAGE >= 1
    if g == "Carcass":
        return STAGE >= 2
    if g.startswith("Hardware"):
        return STAGE >= 3
    if g == "Sliding door":
        return STAGE >= 10
    if g == "Fixings":
        return STAGE >= (9 if name == "benchtop_brackets" else 10)
    if g.startswith("Drawer"):
        if g.endswith("1"):
            if name.endswith("_bottom"):
                return STAGE >= 5
            if name.endswith("_back"):
                return STAGE >= 6
            if name.endswith("_pocket_screws") or name.endswith("_handle"):
                return STAGE >= 7
            return STAGE >= 4
        return STAGE >= 8
    return True


BIN_PULL = 0.0     # bin drawer travel toward the user (max ~550)
BASKET_PULL = 0.0  # extra travel of the wire basket on its own runners
_BIN_MOVING = {"bin_drawer_front", "bin_drawer_side_L", "bin_drawer_side_R", "bin_drawer_back", "bin_drawer_bottom",
               "bin_1", "bin_2"}
EXT_OPEN = [0.0, 0.0, 0.0, 0.0]   # extension drawers 1 (top) to 4 (bottom): fraction open, 0..1
EXT_TRAVEL = 500.0                 # travel at 100% open
PULL_OUT = 700.0   # drawer 1 is built on the bench in front of the unit during stages 4-7


DETAIL_X = [0.0, 0.0]   # [x0, x1] (x1 > x0 turns it on): show only drawer 1's left-side box/drawbar parts cropped to this x slice (close-up renders)
_DETAIL_CROP = ("drawer1_side_L", "drawer1_drawbar_L", "drawer1_drawbar_bracket_L")
_DETAIL_KEEP = ("drawer1_snap_clip_L", "drawer1_fixing_screw_1", "drawer1_fixing_screw_2")


# ---- assembly-guide step views (AV_STEP > 0): hide / explode / recolour parts per step; 0 = normal model ----
AV_STEP = 0
_BB = {}
_AV_CP = {"side_free_end", "side_joint_end", "carcass_bottom", "carcass_back", "top_rail_front"}
_AV_PL = {"P1_front_rail", "P3_side_rail_free_end", "P4_side_rail_joint_end", "P2_rear_rail"}
_AV_NEW, _AV_OLD = (0.96, 0.52, 0.10), (0.80, 0.82, 0.86)


def _av_rule(name):
    """returns (visible, (dx, dy, dz), is_new) for the current AV_STEP."""
    is_dr = name.startswith("drawer") and name[6:7] in "123"
    dk = name[6:7] if is_dr else ""
    part = name[8:] if is_dr else ""
    box_part = part in ("front", "side_L", "side_R", "back", "bottom")
    hw = part.startswith(("runner", "drawbar"))
    clip = part.startswith("snap_clip")
    low = part.endswith("_L")
    st = AV_STEP
    if st == 1:
        if name not in _AV_PL:
            return (False, (0, 0, 0), False)
        d = {"P1_front_rail": (0, 0, 0), "P2_rear_rail": (0, 0, 0),
             "P3_side_rail_free_end": (0, -130, 0), "P4_side_rail_joint_end": (0, 130, 0)}[name]
        return (True, d, True)
    if st == 2:
        if name in _AV_PL:
            return (True, (0, 0, 0), False)
        d = {"side_free_end": (0, -300, 0), "side_joint_end": (0, 300, 0), "carcass_bottom": (0, 0, 90),
             "carcass_back": (190, 0, 60), "top_rail_front": (-120, 0, 140)}.get(name)
        return (d is not None, d or (0, 0, 0), True)
    if st == 3:
        if name in _AV_PL or name in _AV_CP:
            return (True, (0, 0, 0), False)
        if is_dr and hw:
            return (True, (0, 90 if low else -90, 0), True)
        return (False, (0, 0, 0), False)
    if st == 4:
        if is_dr and dk == "1" and box_part:
            d = {"front": (-380, 0, 0), "bottom": (-230, 0, 0), "back": (170, 0, 0),
                 "side_L": (0, -150, 0), "side_R": (0, 150, 0)}[part]
            return (True, d, True)
        return (False, (0, 0, 0), False)
    if st == 5:
        if is_dr and dk == "1" and (box_part or clip):
            return (True, (0, 0, 150), True)
        if is_dr and dk == "1" and part.startswith("drawbar"):
            return (True, (0, 0, 0), False)
        return (False, (0, 0, 0), False)
    if st == 6:
        if name in _AV_PL or name in _AV_CP:
            return (True, (0, 0, 0), False)
        if is_dr and hw:
            return (True, (0, 0, 0), False)
        if is_dr and dk == "1" and (box_part or clip):
            return (True, (-300, 0, 110), True)
        return (False, (0, 0, 0), False)
    if st == 7:
        return (name == "drawer1_front", (0, 0, 0), True)
    if st == 8:
        if name in _AV_PL or name in _AV_CP:
            return (True, (0, 0, 0), False)
        if is_dr and (hw or part in ("side_L", "side_R", "back", "bottom")):
            return (True, (0, 0, 0), False)
        if is_dr and part == "front":
            return (True, (-170, 0, 0), True)
        return (False, (0, 0, 0), False)
    if st == 9:
        if name in _AV_PL or name in _AV_CP or name in ("benchtop_brackets", "link_bolts_to_main_run"):
            return (True, (0, 0, 0), name in ("benchtop_brackets", "link_bolts_to_main_run"))
        if is_dr and (box_part or hw):
            return (True, (0, 0, 0), False)
        if name == "Kb_kickboard":
            return (True, (-220, 0, 0), True)
        if name == "ref_BenchtopExt":
            return (True, (0, 0, 220), True)
        return (False, (0, 0, 0), False)
    return (True, (0, 0, 0), False)


def show(part, name, **kw):
    if AV_STEP:
        if name.startswith(("drawer", "side_", "carcass", "P1", "P2", "P3", "P4", "Kb", "top_rail", "benchtop_br")):
            _b = part.bounding_box()
            _BB[name] = (tuple(_b.min()), tuple(_b.max()))
        _v, _d, _n = _av_rule(name)
        if not _v:
            return
        if _d != (0, 0, 0):
            part = part.moved(Location.translation(*_d))
        if AV_STEP == 7:   # crop the front to a corner block so the pull profile fills the picture
            part = part & box(-1e5, 1e5, YC + 300.0, YC + 420.0, Z_TOP - 5.0 - 70.0, Z_TOP)
        kw["colour"] = _AV_NEW if _n else _AV_OLD
        _golf_show(part, name, **kw)
        return
    if DETAIL_X[1] > DETAIL_X[0]:
        if name in _DETAIL_CROP:
            part = part & box(DETAIL_X[0], DETAIL_X[1], -1000.0, 1000.0, DB_ZB[0] - 40.0, DB_ZB[0] + 45.0)
        elif name not in _DETAIL_KEEP:
            return
    if name in _BIN_MOVING and BIN_PULL:
        part = part.moved(Location.translation(0.0, -BIN_PULL, 0.0))
    if name == "wire_basket" and BASKET_PULL:   # basket is fixed to the bay sides; only it slides on its own runners
        part = part.moved(Location.translation(0.0, -BASKET_PULL, 0.0))
    if name.startswith("drawer") and name[6:7] in "1234" and "runner" not in name and name[7:8] == "_":
        _f = EXT_OPEN[int(name[6]) - 1]
        if _f:
            part = part.moved(Location.translation(-_f * EXT_TRAVEL, 0.0, 0.0))
    if _visible(name, kw.get("group")):
        if name.startswith("drawer1_") and "runner" not in name and 4 <= STAGE <= 7:
            part = part.moved(Location.translation(-PULL_OUT, 0.0, 0.0))
        _golf_show(part, name, **kw)


# ---- datum from bench.step placeholders ----
X_EDGE = 2440.885      # benchtop front edge (drawer-front side)
X_BACK = 3040.885      # back / right end of the benchtop, flush with main bench end (wall side)
REAR_SETBACK = 40.0    # carcass and plinth stop this far short of the wall: clears a skirting board that projects 20-25 mm
X_BACK_C = X_BACK - REAR_SETBACK   # rear face of the carcass
Y_A = -389.421         # free end of BenchtopExt
Y_B = 430.579          # joint with main benchtop
FRONT_BACK = 15.0      # the front of the unit is set this much further back from the benchtop edge (room for the 12 mm hem)
TOP_T = 26.0           # timber top thickness
HEM_T = 12.0           # hem under the front edge of the top only
Z_TOP = 128.602        # underside of benchtop: top surface 900 mm above the floor, minus the 26 mm timber top
Z_FLOOR = -745.398
Z_PLINTH_TOP = -620.398   # plinth frame 125 high: lifts the carcass so the bottom front (level with the doors) hangs 5 mm below it
KB_TOP = -630.398          # kickboard cover keeps the existing kickboard's height (115), so the 5 mm gap under the doors matches

T = 15.0               # carcass / plinth / panel ply (Bunnings STRUCTAply 15 mm)
FRONT_T = 15.0

# ---- carcass ----
FREE_OVERHANG = 15.0
X_CARC_FRONT = X_EDGE + 23.0 + FRONT_BACK   # 2478.885
Y_SIDE_A0 = Y_A + FREE_OVERHANG          # free-end side outer face
Y_SIDE_A1 = Y_SIDE_A0 + T
Y_SIDE_B1 = Y_B                          # back-end side outer face (flush with joint)
Y_SIDE_B0 = Y_SIDE_B1 - T
OPEN_W = Y_SIDE_B0 - Y_SIDE_A1           # 773 clear between sides
YC = (Y_SIDE_B0 + Y_SIDE_A1) / 2.0
X_BACKP0 = X_BACK_C - T
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
DOOR_FIX = 13.0   # existing doors: front face is 15 mm behind the benchtop edge (was 2 mm)
FRAME_FIX = 14.0  # top rail front face moves from y 450.6 to 464.6 (behind door backs)
KB_FIX = 38.0     # existing kickboard: front face 38 mm behind the door fronts
SHOW_DOOR = True
imp = import_step_file("/home/user/CAD/kitchen_bench_extension/bench.step")
KEEP = {"benchtop", "BenchtopExt", "framing", "Kickboard"}
rest = []
for p in imp.parts():
    n = p.name()
    if n == "KickboardExt":
        continue  # replaced by the plinth fascia below
    if n == "Kickboard":
        p = p.moved(Location.translation(0, KB_FIX, 0))   # corrected: recessed 38 mm behind door fronts
    if n == "framing":
        p = p.moved(Location.translation(0, FRAME_FIX, 0))  # corrected: rail sits behind the doors
    if n == "benchtop":
        p = p.moved(Location.translation(0, 0, 20.0))   # the real existing top is 899-900 mm; bench.step's placeholder is 880
    if n == "BenchtopExt":
        _bb = p.bounding_box()
        _x0, _y0, _z0 = _bb.min(); _x1, _y1, _z1 = _bb.max()
        p = box(_x0, _x1, _y0, _y1, Z_TOP, Z_TOP + TOP_T) + box(_x0, _x0 + HEM_T, _y0, _y1, Z_TOP - HEM_T, Z_TOP)
    if n in KEEP:
        show(p, "ref_" + n, group="Reference bench")
    else:
        rest.append(p)
# existing door (and its handle) replaced by the sliding door
REMOVED_REF = {"ref_door-left_2", "ref_handle-grip_2", "ref_handle-standoff_3", "ref_handle-standoff_4"}
FULL_REF = False   # True for the final export: every bench.step part is shown
if FULL_REF:
    seen = {}
    for p in rest:
        n = p.name()
        seen[n] = seen.get(n, 0) + 1
        _nm = "ref_" + n.replace(" ", "_") + ("" if seen[n] == 1 else f"_{seen[n]}")
        if _nm in REMOVED_REF:
            continue
        if n.startswith("door") or n.startswith("handle"):
            p = p.moved(Location.translation(0, DOOR_FIX, 0))
        show(p, _nm, group="Reference bench")

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
        cuts.append(cyl(add(S, -50.0, d), d, 50.0, 4.75))      # 9.5 mm pocket bore: from the shoulder out past the face; 50 mm puts the far end disc 8 mm clear of the face at 15 degrees, so the pocket opens fully
        cuts.append(cyl(S, d, 16.0 + 3.0, 1.9))                  # pilot to the end grain
        shaft = cyl(S, d, SCREW_L, 2.0)
        head = cyl(add(S, -3.0, d), d, 3.0, 4.0)
        screws.append(shaft + head)
    return fuse_list(cuts), screws


# ---------------- carcass ----------------
side_a = box(X_CARC_FRONT, X_BACK_C, Y_SIDE_A0, Y_SIDE_A1, Z_PLINTH_TOP, Z_TOP)
side_b = box(X_CARC_FRONT, X_BACK_C, Y_SIDE_B0, Y_SIDE_B1, Z_PLINTH_TOP, Z_TOP)
bottom = box(X_CARC_FRONT, X_BACKP0, Y_SIDE_A1, Y_SIDE_B0, Z_PLINTH_TOP, Z_BOT_TOP)
backp = box(X_BACKP0, X_BACK_C, Y_SIDE_A1, Y_SIDE_B0, Z_PLINTH_TOP, Z_TOP)   # full height: stands on the plinth rear rail, C3 butts its front face
STR_W = 60.0
str_front = box(X_CARC_FRONT, X_CARC_FRONT + STR_W, Y_SIDE_A1, Y_SIDE_B0, Z_TOP - T, Z_TOP)
str_rear = box(X_BACKP0 - STR_W, X_BACKP0, Y_SIDE_A1, Y_SIDE_B0, Z_TOP - T, Z_TOP)

# ---------------- plinth frame (structural) + kickboard (cover panel) ----------------
KB_SETBACK = 60.0      # kickboard face is this far behind the drawer-front face
FRONT_OVERHANG = 5.0   # bottom drawer front hangs 5 mm below the carcass base and ends level with the existing doors (DOOR_Z0 = -625.398)
KB_X0 = X_EDGE + 2.0 + FRONT_BACK + KB_SETBACK
KB_X1 = KB_X0 + T
RET_OUT = Y_SIDE_A0 + 6.0
ret_back_y1 = Y_SIDE_B1 - 2.0
kickboard = box(KB_X0, KB_X1, RET_OUT, 445.579 + KB_FIX, Z_FLOOR, KB_TOP)
rail_front = box(KB_X1, KB_X1 + T, RET_OUT + T, ret_back_y1 - T, Z_FLOOR, Z_PLINTH_TOP)
ret_free = box(KB_X1, X_BACKP0 + 8.0, RET_OUT, RET_OUT + T, Z_FLOOR, Z_PLINTH_TOP)
ret_joint = box(KB_X1, X_BACKP0 + 8.0, ret_back_y1 - T, ret_back_y1, Z_FLOOR, Z_PLINTH_TOP)
rail_rear = box(X_BACKP0 - T, X_BACKP0, RET_OUT + T, ret_back_y1 - T, Z_FLOOR, Z_PLINTH_TOP)   # P2: fully under C3, rear face level with C3's rear edge; side rails run 8 mm on under C4

# ---- carcass and plinth joints: 25 mm pocket screws at 15 degrees (30 in all), carcass hold-down screws ----
_ca, _sa = math.cos(A15), math.sin(A15)
_cs3, _ss3 = [], []
_xs3 = [2575.0, 2695.0, 2815.0, 2935.0]                       # C3: 4 per side, in its underside, clear of the plinth rails
for _y, _dy in ((Y_SIDE_A1, -1.0), (Y_SIDE_B0, 1.0)):
    _c, _s_ = pocket_set([(x, _y, Z_PLINTH_TOP + 9.0) for x in _xs3], (0.0, _dy * _ca, _sa))
    _cs3.append(_c); _ss3 += _s_
bottom = bottom - _cs3[0] - _cs3[1]
_cs4 = []
_zs4 = [Z_PLINTH_TOP + 70.0 + 140.0 * k for k in range(5)]     # C4: 5 per side, in its rear face
for _y, _dy in ((Y_SIDE_A1, -1.0), (Y_SIDE_B0, 1.0)):
    _c, _s_ = pocket_set([(X_BACK_C - 9.0, _y, z) for z in _zs4], (-_sa, _dy * _ca, 0.0))
    _cs4.append(_c); _ss3 += _s_
backp = backp - _cs4[0] - _cs4[1]
for _y, _dy in ((Y_SIDE_A1, -1.0), (Y_SIDE_B0, 1.0)):          # C9: 2 per end, in its underside
    _c, _s_ = pocket_set([(X_CARC_FRONT + dx, _y, Z_TOP - T + 9.0) for dx in (15.0, 45.0)], (0.0, _dy * _ca, _sa))
    str_front = str_front - _c; _ss3 += _s_
_ss_pl = []
_zpl = [Z_FLOOR + 30.0, Z_FLOOR + 85.0]
_xc5 = KB_X1 + T
for _y, _dy in ((RET_OUT + T, -1.0), (ret_back_y1 - T, 1.0)):   # C5, C6: 2 per end, in their inner faces
    _c, _s_ = pocket_set([(_xc5 - 9.0, _y, z) for z in _zpl], (-_sa, _dy * _ca, 0.0))
    rail_front = rail_front - _c; _ss_pl += _s_
    _x6 = X_BACKP0 - T
    _c, _s_ = pocket_set([(_x6 + 9.0, _y, z) for z in _zpl], (_sa, _dy * _ca, 0.0))
    rail_rear = rail_rear - _c; _ss_pl += _s_
_fx = []          # plinth-to-carcass fixing: pocket screws from inside the frame, up into the underside of C3 (P1, P2) and the bottom edges of the sides (P3, P4)
_fxc, _fxs = {}, []
_yfx = (-300.0, -100.0, 100.0, 300.0)
_c, _s_ = pocket_set([(_xc5 - 9.0, YC + y, Z_PLINTH_TOP) for y in _yfx], (-_sa, 0.0, _ca)); rail_front = rail_front - _c; _fx += _s_
_c, _s_ = pocket_set([(_x6 + 9.0, YC + y, Z_PLINTH_TOP) for y in _yfx], (_sa, 0.0, _ca)); rail_rear = rail_rear - _c; _fx += _s_
_xsr = (2600.0, 2800.0)
_E3 = [(x, RET_OUT + T - 9.0, Z_PLINTH_TOP) for x in _xsr]        # P3 inner face is +y; screw tilts toward it, exit 9 mm in from it, into the free-end side's bottom edge
_E4 = [(x, ret_back_y1 - T + 9.0, Z_PLINTH_TOP) for x in _xsr]
_c, _s_ = pocket_set(_E3, (0.0, -_sa, _ca)); ret_free = ret_free - _c; _fx += _s_
_c, _s_ = pocket_set(_E4, (0.0, _sa, _ca)); ret_joint = ret_joint - _c; _fx += _s_
_FP = {}   # fastener guide data for the picture steps: (point on the screw axis, receiving part, part carrying the screw head)
_P1, _P2, _P3, _P4 = "P1_front_rail", "P2_rear_rail", "P3_side_rail_free_end", "P4_side_rail_joint_end"
_FP["pl_rail_to_side"] = [((_xc5 - 9.0, RET_OUT + T, z), _P3, _P1) for z in _zpl] + [((_xc5 - 9.0, ret_back_y1 - T, z), _P4, _P1) for z in _zpl] \
    + [((_x6 + 9.0, RET_OUT + T, z), _P3, _P2) for z in _zpl] + [((_x6 + 9.0, ret_back_y1 - T, z), _P4, _P2) for z in _zpl]
_FP["plinth_to_carcass"] = [((_xc5 - 9.0, YC + y, Z_PLINTH_TOP), "carcass_bottom", _P1) for y in _yfx] + [((_x6 + 9.0, YC + y, Z_PLINTH_TOP), "carcass_bottom", _P2) for y in _yfx] \
    + [(e, "side_free_end", _P3) for e in _E3] + [(e, "side_joint_end", _P4) for e in _E4]
_FP["carcass"] = [((x, Y_SIDE_A1, Z_PLINTH_TOP + 9.0), "side_free_end", "carcass_bottom") for x in _xs3] + [((x, Y_SIDE_B0, Z_PLINTH_TOP + 9.0), "side_joint_end", "carcass_bottom") for x in _xs3] \
    + [((X_BACK_C - 9.0, Y_SIDE_A1, z), "side_free_end", "carcass_back") for z in _zs4] + [((X_BACK_C - 9.0, Y_SIDE_B0, z), "side_joint_end", "carcass_back") for z in _zs4] \
    + [((X_CARC_FRONT + dx, Y_SIDE_A1, Z_TOP - T + 9.0), "side_free_end", "top_rail_front") for dx in (15.0, 45.0)] + [((X_CARC_FRONT + dx, Y_SIDE_B0, Z_TOP - T + 9.0), "side_joint_end", "top_rail_front") for dx in (15.0, 45.0)]

grp = "Carcass"
show(side_a, "side_free_end", colour=COL_PLY, group=grp)
show(bottom, "carcass_bottom", colour=COL_PLY, group=grp)
show(backp, "carcass_back", colour=COL_PLY, group=grp)
show(str_front, "top_rail_front", colour=COL_PLY, group=grp)
grp = "Plinth"
show(kickboard, "Kb_kickboard", colour=(0.65, 0.65, 0.65), group=grp)
show(rail_front, "P1_front_rail", colour=(0.65, 0.65, 0.65), group=grp)
show(ret_free, "P3_side_rail_free_end", colour=(0.65, 0.65, 0.65), group=grp)
show(ret_joint, "P4_side_rail_joint_end", colour=(0.65, 0.65, 0.65), group=grp)
show(rail_rear, "P2_rear_rail", colour=(0.65, 0.65, 0.65), group=grp)
show(fuse_list(_ss_pl), "plinth_pocket_screws", colour=COL_STEEL, group=grp, solids=len(_ss_pl))
show(fuse_list(_ss3), "carcass_pocket_screws", colour=COL_STEEL, group="Carcass", solids=len(_ss3))
show(fuse_list(_fx), "plinth_fixing_screws", colour=COL_STEEL, group="Plinth", solids=len(_fx))

print("opening width", OPEN_W, "yc", YC, "inside depth", X_BACKP0 - X_CARC_FRONT)

# ======================= drawers =======================


FRONT_FACE_X = X_EDGE + 2.0 + FRONT_BACK
XF = FRONT_FACE_X + FRONT_T                 # back face of the drawer front
NL = 550.0                                  # Blum TANDEM 563H5500B runner / drawer side length
BOX_W = OPEN_W - 10.0                       # 763 -> inside = opening - 42 = 731
if DRAWER_SYS == "drawbar":
    BOX_W = OPEN_W - 32.0                   # side outer faces 16 mm from the walls: sides sit on the 15.2 mm flat of the drawbars
SIDE_IN = BOX_W / 2.0 - T                   # 365.5 from centre
GROOVE_D = 8.0
BOT_T = 15.0
GR0, GR1 = 12.75, 28.25                     # groove z band above side bottom edge (15 mm board underside at +13)

FRONT_H = [163.0, 163.0, 210.0, 210.0]     # two sizes: top pair, bottom pair
if DRAWER_SYS == "alto":
    FRONT_H = [133.0, 133.0, 240.0, 240.0]  # Alto 204 sets need fronts >= 225; Alto 86 sets need >= 105
elif DRAWER_SYS == "drawbar":
    FRONT_H = [205.0, 215.0, 313.0]         # 3 drawers; D1 stops 15 below the underside of the top (12 mm front hem + 3 mm) so it can open; D3 bottom level with the doors
GAP = 3.0
if DRAWER_SYS == "drawbar" and PULL in ("back_cove", "slot"):
    FRONT_H = [200.0, 200.0, 300.0]         # 20 mm air gaps above every front (fingers get behind the top lip)
    GAP = 20.0
if DRAWER_SYS == "drawbar" and PULL == "mitre":
    # the nose of each front's 45 degree mitre (R3) is 12.0 mm below its top edge. It must stay BELOW the bottom edge of the front above (with its R10 cove), otherwise
    # pulling the upper drawer would catch the nose of the one below. Clearance 2 mm, so the fronts overlap by 12 - 2 = 10 mm.
    MIT_NOSE_DROP, MIT_CLEAR = 12.0, 2.0
    GAP = -(MIT_NOSE_DROP - MIT_CLEAR)
    FRONT_H = [220.0, 220.0, 319.0]         # D1 top edge at 113.6 so its nose is 15 mm below the front hem
BOX_H = [130.0, 130.0, 165.0, 165.0]
N_DRAWERS = len(FRONT_H)
fr_bottom = [0.0] * N_DRAWERS
fr_bottom[-1] = Z_PLINTH_TOP - FRONT_OVERHANG   # bottom front hangs below the carcass base
for _i in range(N_DRAWERS - 2, -1, -1):
    fr_bottom[_i] = fr_bottom[_i + 1] + FRONT_H[_i + 1] + GAP
OB = [b + 11.0 for b in fr_bottom]
OB[-1] = Z_PLINTH_TOP + 17.0                  # bottom runner sits just above the carcass base          # runner "opening bottom" of each drawer


# ---- drawbar boxes: vertical layout. The drawbar front bracket hangs 31 mm below the drawbar top plate, so each box
# bottom sits >= 33 mm above its own front's bottom edge and >= 33 mm above the box below. ----
DB_L = 495.0                                  # box length (drawbar + bracket = 494.5)
RUN_DROP = 45.0     # the Alto runner (telescoping steel stack) hangs entirely BELOW the drawbar plate, about 45 mm (photographs)
RUN_CLR = 2.0
if DRAWER_SYS == "drawbar":
    BOX_H = [164.0, 164.0, 245.0]
    DB_ZB = [0.0] * N_DRAWERS
    if PULL == "mitre":
        # box sides stop where the mitre meets the back face of its front (MIT_L + 15 below the front's top edge), and there is 5 mm clear under each runner
        MIT_BASE_DROP, MIT_RUN_CLR = MIT_L + FRONT_T, 5.0
        BOX_H = [0.0] * N_DRAWERS
        DB_ZB[-1] = Z_BOT_TOP + RUN_DROP + MIT_RUN_CLR
        for _k in range(N_DRAWERS - 1, -1, -1):
            if _k < N_DRAWERS - 1:
                DB_ZB[_k] = max(fr_bottom[_k] + 33.0, DB_ZB[_k + 1] + BOX_H[_k + 1] + RUN_DROP + MIT_RUN_CLR)
            BOX_H[_k] = float(int(fr_bottom[_k] + FRONT_H[_k] - MIT_BASE_DROP - DB_ZB[_k]))
    else:
        DB_ZB[-1] = Z_BOT_TOP + RUN_DROP + RUN_CLR
        for _k in range(N_DRAWERS - 2, -1, -1):
            DB_ZB[_k] = max(fr_bottom[_k] + 33.0, DB_ZB[_k + 1] + BOX_H[_k + 1] + RUN_DROP + RUN_CLR)
    for _k in range(N_DRAWERS):
        assert DB_ZB[_k] + BOX_H[_k] <= fr_bottom[_k] + FRONT_H[_k] + (GAP - 2.0 if GAP > 10.0 else -1.0) + 0.01, ("box above its front", _k)
    assert DB_ZB[0] + BOX_H[0] <= Z_TOP - T - 3.0, "top box clashes with the front stretcher"
    print("drawbar layout: box bottoms", [round(v, 1) for v in DB_ZB], "heights", BOX_H)


# ---- Hafele Alto soft-close (732.25.602 family) envelope model, from the Hafele installation datasheet ----
# Datasheet: 37.5 mm from cabinet wall to the base edge (base width = ICW - 75 + 0.5), base length = runner - 5,
# back width = ICW - 89 + 0.5, 16 mm base/back, back height 70 (86 side) or 148 (164 side), min. depth 510.
# Side wall thickness, lip and runner section are assumed envelopes (no CAD file was available).
ALTO_L = 500.0
ALTO_HS = 86.0                                   # steel side height, all sets
ALTO_TOT = [86.0, 86.0, 204.0, 204.0]            # overall drawer height: 204 sets add gallery rails (round bars) above the 86 side
ALTO_T = 15.0


def _alto_zb():
    zb = [0.0] * N_DRAWERS
    zb[-1] = Z_BOT_TOP + 12.0
    for k in range(N_DRAWERS - 2, -1, -1):
        zb[k] = max(fr_bottom[k] + 30.0, zb[k + 1] + ALTO_TOT[k + 1] + 4.0 + 11.0)
    return zb


ALTO_ZB = _alto_zb() if DRAWER_SYS == "alto" else None


def alto_drawer(i):
    # Dimensions: datasheet labels (37.5 wall to base edge, 44.5 bracket hole line, 9 plate edge, 56 hole row) plus
    # runner footprint measured from the datasheet section (approx. 29 wide x 39 high, bottom 11 below the base).
    nm = f"drawer{i + 1}"
    hs = ALTO_HS
    tot = ALTO_TOT[i]
    zb = ALTO_ZB[i]
    f0, f1 = fr_bottom[i], fr_bottom[i] + FRONT_H[i]
    ya0, yb1 = Y_SIDE_A1, Y_SIDE_B0
    RW = 29.0                                                                          # runner width against the wall
    yin_l, yin_r = YC - (OPEN_W / 2.0 - 37.5 + 0.25), YC + (OPEN_W / 2.0 - 37.5 + 0.25)   # inner faces of the steel sides
    x0, x1 = XF, XF + ALTO_L
    front = box(FRONT_FACE_X, XF, YC - 401.0, YC + 401.0, f0, f1)
    sl = box(x0, x1, ya0 + RW, yin_l, zb, zb + hs)
    sr = box(x0, x1, yin_r, yb1 - RW, zb, zb + hs)
    lip_l = box(x0 + 2.0, x0 + ALTO_L - 3.0, yin_l, yin_l + 10.0, zb, zb + 2.0)
    lip_r = box(x0 + 2.0, x0 + ALTO_L - 3.0, yin_r - 10.0, yin_r, zb, zb + 2.0)
    sl = sl + lip_l
    sr = sr + lip_r
    bx1 = x0 + ALTO_L - 3.0
    bottom = box(x0 + 2.0, bx1, yin_l, yin_r, zb + 2.0, zb + 2.0 + ALTO_T)
    bw = OPEN_W - 89.0 + 0.5
    back = box(bx1 - ALTO_T, bx1, YC - bw / 2.0, YC + bw / 2.0, zb + 2.0 + ALTO_T, zb + tot)
    # front fixing brackets: 2 mm plate on the back of the front, hole line 44.5 from the wall, plate edge 9 beyond it
    bh = 59.0 if tot < 100 else 180.0
    brk_l = box(XF, XF + 2.0, yin_l, ya0 + 53.5, zb, zb + bh)
    brk_r = box(XF, XF + 2.0, yb1 - 53.5, yin_r, zb, zb + bh)
    rails = []
    if tot > 100:   # two 10 mm round gallery rails per side above the 86 mm side, top rail top at 204
        for zr in (zb + 125.0, zb + 199.0):
            for yy in (ya0 + 33.1, yb1 - 33.1):
                rails.append(cyl((XF + 2.0, yy, zr), (1.0, 0.0, 0.0), bx1 - XF - 2.0, 5.0))
    zc = (f0 + f1) / 2.0
    HL = 300.0
    grip = box(FRONT_FACE_X - 36.0, FRONT_FACE_X - 24.0, YC - HL / 2, YC + HL / 2, zc - 6.0, zc + 6.0)
    st = [cyl((FRONT_FACE_X, YC + s * 120.0, zc), (-1, 0, 0), 26.683, 5.0) for s in (-1, 1)]
    handle = grip + st[0] + st[1]
    # runner: 29 wide x 39 high against the cabinet wall, bottom 11 below the base underside, length 500
    rx0 = XF + 2.0
    zr0 = zb - 11.0
    run_l = box(rx0, rx0 + ALTO_L, ya0, ya0 + RW, zr0, zr0 + 39.0)
    run_r = box(rx0, rx0 + ALTO_L, yb1 - RW, yb1, zr0, zr0 + 39.0)
    g = f"Drawer {i + 1}"
    show(front, f"{nm}_front", colour=COL_FRONT, group=g)
    show(sl, f"{nm}_side_L", colour=(0.93, 0.93, 0.93), group=g)
    show(sr, f"{nm}_side_R", colour=(0.93, 0.93, 0.93), group=g)
    show(back, f"{nm}_back", colour=COL_PLY, group=g)
    show(bottom, f"{nm}_bottom", colour=COL_PLY, group=g)
    show(handle, f"{nm}_handle", colour=COL_HANDLE, group=g)
    show(brk_l + brk_r, f"{nm}_front_brackets", colour=COL_STEEL, group=g)
    if rails:
        show(fuse_list(rails), f"{nm}_gallery_rails", colour=(0.93, 0.93, 0.93), group=g)
    g = "Hardware - Hafele Alto 732.25.602"
    show(run_l, f"{nm}_runner_L", colour=COL_STEEL, group=g)
    show(run_r, f"{nm}_runner_R", colour=COL_STEEL, group=g)


_DB = {}


def _db_load():
    if _DB:
        return _DB
    base = "/home/user/CAD/kitchen_bench_extension/"
    for k, fn in (("L", "Left Runner Drawbar.step"), ("R", "Right Runner Drawbar.step")):
        ps = import_step_file(base + fn).parts()
        tube = max(ps, key=lambda q: list(q.bounding_box().size())[1])
        brk = min(ps, key=lambda q: list(q.bounding_box().size())[1])
        tb, bb = list(tube.bounding_box().min()), list(brk.bounding_box().min())
        tx = list(tube.bounding_box().max())
        _DB[k] = {"tube": tube, "brk": brk, "yf": bb[1], "yr": tx[1], "xmin": tb[0], "xmax": tx[0],
                  "cx": (tb[0] + tx[0]) / 2.0, "pt": tx[2] - 4.0}      # plate top = tube top minus the 4 mm rear tab
    _DB["clip"] = import_step_file(base + "Drawer Mounting Hardware - Snap Clip.step").parts()[0]
    return _DB


def _db_xf(k, zb):
    # STEP file frame -> world: rotate -90 deg about Z (file y = along the drawer, file x = across), front bracket face on XF,
    # drawbar outer edge 14 mm from the cabinet wall (file "R" goes on the low-Y wall, file "L" on the high-Y wall)
    d = _db_load()[k]
    tx = XF - d["yf"]
    ty = (Y_SIDE_B0 - 14.0 + d["xmin"]) if k == "L" else (Y_SIDE_A1 + 14.0 + d["xmax"])
    return tx, ty, zb - d["pt"]


def _db_place(part, k, zb):
    tx, ty, tz = _db_xf(k, zb)
    return part.moved(Location.about(Axis((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)), -90.0)).moved(Location.translation(tx, ty, tz))


def _db_pt(k, zb, xs, ys, zs):
    tx, ty, tz = _db_xf(k, zb)
    return (ys + tx, -xs + ty, zs + tz)


def drawbar_drawer(i):
    nm = f"drawer{i + 1}"
    zb = DB_ZB[i]                           # side bottom edge = top of the drawbar plates
    hb = BOX_H[i]
    f0, f1 = fr_bottom[i], fr_bottom[i] + FRONT_H[i]
    xr = XF + DB_L
    yl0, yr1 = YC - BOX_W / 2.0, YC + BOX_W / 2.0
    yl1, yr0 = yl0 + T, yr1 - T
    g0, g1 = zb + GR0, zb + GR1

    front = box(FRONT_FACE_X, XF, YC - 401.0, YC + 401.0, f0, f1)
    if BASE_SLOT == "front":
        front = front - box(XF - GROOVE_D, XF + 0.1, YC - SIDE_IN - GROOVE_D, YC + SIDE_IN + GROOVE_D, g0, g1)
    if PULL == "front_cove" and COVE_R > 0:   # concave quarter-round taken off the front-top corner, full width
        front = front - cyl((FRONT_FACE_X, YC - 405.0, f1), (0.0, 1.0, 0.0), 810.0, COVE_R)
    elif PULL == "back_cove" and COVE_R > 0:  # same cove on the BACK of the top edge: fingers hook behind the lip
        front = front - cyl((XF, YC - 405.0, f1), (0.0, 1.0, 0.0), 810.0, COVE_R)
    elif PULL == "groove":   # undercut finger slot: trapezoid pocket in the front face (dovetail), full width, 3 mm roundover on both edges
        _t = math.tan(math.radians(GRV_ANG))
        _pts = [(-0.5, -GRV_TOP), (0.0, -GRV_TOP), (GRV_D, -GRV_TOP + GRV_D * _t), (GRV_D, -GRV_TOP - GRV_OPEN - GRV_D * _t),
                (0.0, -GRV_TOP - GRV_OPEN), (-0.5, -GRV_TOP - GRV_OPEN)]

        def _edge_round(px, pz, sg):     # roundover cutter for the lip corner at (px, pz); lip above (sg = +1) or below (sg = -1)
            ang = math.radians(GRV_ANG)
            u1, u2 = (0.0, sg), (math.cos(ang), sg * math.sin(ang))
            q = math.acos(u1[0] * u2[0] + u1[1] * u2[1])
            d = GRV_RAD / math.tan(q / 2.0)
            bx, bz = u1[0] + u2[0], u1[1] + u2[1]
            bl = math.hypot(bx, bz)
            cx, cz = px + bx / bl * GRV_RAD / math.sin(q / 2.0), pz + bz / bl * GRV_RAD / math.sin(q / 2.0)
            t1 = (px + u1[0] * d, pz + u1[1] * d)
            t2 = (px + u2[0] * d, pz + u2[1] * d)
            a1, a2 = math.atan2(t1[1] - cz, t1[0] - cx), math.atan2(t2[1] - cz, t2[0] - cx)
            da = (a2 - a1 + math.pi) % (2.0 * math.pi) - math.pi
            arc = [(cx + GRV_RAD * math.cos(a1 + da * k / 16.0), cz + GRV_RAD * math.sin(a1 + da * k / 16.0)) for k in range(17)]
            return [(-0.5, pz - sg * 0.3), (-0.5, t1[1]), t1] + arc[1:-1] + [t2, (t2[0], t2[1] - sg * 0.3)]

        for _poly in (_pts, _edge_round(0.0, -GRV_TOP, 1), _edge_round(0.0, -GRV_TOP - GRV_OPEN, -1)):
            _pr = Sketch.polygon(_poly).extrude(GRV_LEN)
            _pr = _pr.moved(Location.rotation(90.0, 0.0, 0.0)).moved(Location.translation(FRONT_FACE_X, YC + GRV_LEN / 2.0, f1))
            front = front - _pr
    elif PULL in ("rebate", "mitre"):   # rebate: slot opened to the top edge, only the lower dovetail lip remains, 3 mm roundover on it. mitre: the same with a 45 degree undercut cut the full thickness of the front
        _ga, _gd = (GRV_ANG, GRV_D) if PULL == "rebate" else (MIT_ANG, FRONT_T + 1.0)
        _t = math.tan(math.radians(_ga))
        _ang = math.radians(_ga)
        _u1, _u2 = (0.0, -1.0), (math.cos(_ang), -math.sin(_ang))
        _q = math.acos(_u1[0] * _u2[0] + _u1[1] * _u2[1])
        _d = GRV_RAD / math.tan(_q / 2.0)
        _lc = MIT_L if PULL == "mitre" else REB_SPAN - _d       # corner depth: the radius tangent point is _d beyond the corner (3.84 mm for 14 deg, 7.24 mm for 45 deg)
        _pts = [(-0.5, 1.0), (_gd, 1.0), (_gd, -_lc - _gd * _t), (0.0, -_lc), (-0.5, -_lc)]
        _bx, _bz = _u1[0] + _u2[0], _u1[1] + _u2[1]
        _bl = math.hypot(_bx, _bz)
        _cx, _cz = _bx / _bl * GRV_RAD / math.sin(_q / 2.0), -_lc + _bz / _bl * GRV_RAD / math.sin(_q / 2.0)
        _t1 = (0.0, -_lc + _u1[1] * _d)
        _t2 = (_u2[0] * _d, -_lc + _u2[1] * _d)
        _a1, _a2 = math.atan2(_t1[1] - _cz, _t1[0] - _cx), math.atan2(_t2[1] - _cz, _t2[0] - _cx)
        _da = (_a2 - _a1 + math.pi) % (2.0 * math.pi) - math.pi
        _arc = [(_cx + GRV_RAD * math.cos(_a1 + _da * k / 16.0), _cz + GRV_RAD * math.sin(_a1 + _da * k / 16.0)) for k in range(17)]
        _rd = [(-0.5, -_lc + 0.3), (-0.5, _t1[1]), _t1] + _arc[1:-1] + [_t2, (_t2[0], _t2[1] + 0.3)]
        if PULL == "mitre":   # one cutter: everything above the 45 degree wall and the R3 nose, so no sliver is left behind
            _zc = -(_lc + _d) + MIT_BIT_UP          # roundover bit centre height: its arc starts tangent to the front face and crosses the mitre face at an edge
            _R, _Rf = GRV_RAD, MIT_FIL               # R3 roundover arc; R1 fillet (hand sanded) on the edge where it meets the mitre face
            _cc = -_lc - math.sqrt(2.0) * _Rf        # fillet centre lies on the line x + z = _cc (a fillet radius inside the mitre face)
            _qa = 2.0
            _qb = -2.0 * _R - 2.0 * (_cc - _zc)
            _qc = _R ** 2 + (_cc - _zc) ** 2 - (_R - _Rf) ** 2
            _fx = (-_qb - math.sqrt(_qb ** 2 - 4.0 * _qa * _qc)) / (2.0 * _qa)
            _F = (_fx, _cc - _fx)
            _ta = (_R + (_F[0] - _R) * _R / (_R - _Rf), _zc + (_F[1] - _zc) * _R / (_R - _Rf))   # fillet tangent point on the R3 arc
            _tl = (_F[0] + _Rf / math.sqrt(2.0), _F[1] + _Rf / math.sqrt(2.0))                   # and on the mitre face
            _aa = math.atan2(_ta[1] - _zc, _ta[0] - _R)
            _arc2 = [(_R + _R * math.cos(_aa + (math.pi - _aa) * k / 16.0), _zc + _R * math.sin(_aa + (math.pi - _aa) * k / 16.0)) for k in range(17)]
            _f1, _f2 = math.atan2(_tl[1] - _F[1], _tl[0] - _F[0]), math.atan2(_ta[1] - _F[1], _ta[0] - _F[0])
            _fd = (_f2 - _f1 + math.pi) % (2.0 * math.pi) - math.pi
            _fil = [(_F[0] + _Rf * math.cos(_f1 + _fd * k / 8.0), _F[1] + _Rf * math.sin(_f1 + _fd * k / 8.0)) for k in range(9)]
            _polys = ([(-0.5, 1.0), (_gd, 1.0), (_gd, -_lc - _gd * _t)] + _fil + _arc2[1:] + [(-0.5, _zc)],)
        else:
            _polys = (_pts, _rd)
        for _poly in _polys:
            _pr = Sketch.polygon(_poly).extrude(GRV_LEN)
            _pr = _pr.moved(Location.rotation(90.0, 0.0, 0.0)).moved(Location.translation(FRONT_FACE_X, YC + GRV_LEN / 2.0, f1))
            front = front - _pr
    elif PULL == "slot":   # finger-pull bit: board back face level with the cutter top, cut depth = bit radius - SLOT_K
        def _slot_d(x):    # depth below the top edge at distance x from the back face
            h = 21.0 - x
            for (h1, r1), (h2, r2) in zip(SLOT_BIT, SLOT_BIT[1:]):
                if h2 <= h <= h1:
                    return max(0.0, r2 + (r1 - r2) * (h - h2) / (h1 - h2) - SLOT_K)
            return 0.0
        cols = []
        dx = 0.25
        n = int(round(FRONT_T / dx))
        for i in range(n + 1):
            x0 = max(i * dx - dx / 2.0, -0.5)
            d = _slot_d(i * dx)
            if d > 0.0:
                cols.append(box(XF - (x0 + dx), XF - x0, YC - 405.0, YC + 405.0, f1 - d, f1 + 0.1))
        front = front - fuse_list(cols)
    if PULL == "mitre" and i < N_DRAWERS - 1:   # R10 cove on the front-bottom edge of D1 and D2: finger access from below
        front = front - cyl((FRONT_FACE_X, YC - 405.0, f0), (0.0, 1.0, 0.0), 810.0, MIT_COVE_R)
    sl = box(XF, xr, yl0, yl1, zb, zb + hb)
    sr = box(XF, xr, yr0, yr1, zb, zb + hb)
    sl = sl - box(XF - 0.1, xr + 0.1, yl1 - GROOVE_D, yl1 + 0.1, g0, g1)
    sr = sr - box(XF - 0.1, xr + 0.1, yr0 - 0.1, yr0 + GROOVE_D, g0, g1)
    if BASE_SLOT == "back":
        back = box(xr - T, xr, yl1, yr0, zb + BACK_Z0, zb + hb)
        back = back - box(xr - T - 0.1, xr - T + GROOVE_D, yl1 - 0.1, yr0 + 0.1, g0, g1)   # base groove in the back panel
    else:
        back = box(xr - T, xr, yl1, yr0, zb + GR1, zb + hb)
    if BASE_SLOT == "back":   # base butts the front, rear edge 0.5 short of the bottom of the back groove
        bottom = box(XF, xr - T + GROOVE_D - 0.5, YC - SIDE_IN - GROOVE_D + 0.25, YC + SIDE_IN + GROOVE_D - 0.25, zb + 13.0, zb + 13.0 + BOT_T)
    else:
        bottom = box(XF - GROOVE_D + 0.5, xr, YC - SIDE_IN - GROOVE_D + 0.25, YC + SIDE_IN + GROOVE_D - 0.25, zb + 13.0, zb + 13.0 + BOT_T)

    scr = []
    zs = [zb + 45.0, zb + 75.0] if hb < 200 else [zb + 60.0, zb + hb / 2.0, zb + hb - 60.0]
    cut_l, scr_l = pocket_set([(XF, yl0 + 9.0, z) for z in zs], (-math.cos(A15), +math.sin(A15), 0.0))
    cut_r, scr_r = pocket_set([(XF, yr1 - 9.0, z) for z in zs], (-math.cos(A15), -math.sin(A15), 0.0))
    sl = sl - cut_l
    sr = sr - cut_r
    scr += scr_l + scr_r
    zk = [zb + 45.0, zb + 75.0] if hb < 200 else [zb + 60.0, zb + hb / 2.0 + 10.0, zb + hb - 50.0]
    cut_bl, scr_bl = pocket_set([(xr - 9.0, yl1, z) for z in zk], (-math.sin(A15), -math.cos(A15), 0.0))
    cut_br, scr_br = pocket_set([(xr - 9.0, yr0, z) for z in zk], (-math.sin(A15), +math.cos(A15), 0.0))
    back = back - cut_bl - cut_br
    scr += scr_bl + scr_br

    zc = (f0 + f1) / 2.0
    HL = 300.0
    grip = box(FRONT_FACE_X - 36.0, FRONT_FACE_X - 24.0, YC - HL / 2, YC + HL / 2, zc - 6.0, zc + 6.0)
    st = [cyl((FRONT_FACE_X, YC + s * 120.0, zc), (-1, 0, 0), 26.683, 5.0) for s in (-1, 1)]
    handle = grip + st[0] + st[1]

    # ---- drawbars, snap clips / screws (real STEP geometry) ----
    D = _db_load()
    hw, fix = [], []
    side = {"R": sl, "L": sr}      # STEP file "R" is the low-Y (L) side of the box, file "L" the high-Y (R) side
    for k in ("R", "L"):
        d = D[k]
        sgn = 1.0 if k == "L" else -1.0       # which way is "inside" in the file's x
        w = "L" if k == "R" else "R"
        sd = side[k]
        pt, cx, yf, yr = d["pt"], d["cx"], d["yf"], d["yr"]
        tube = d["tube"]
        if DB_FIX == 1:
            clip_w = _db_place(D["clip"].moved(Location.translation(cx, yf + 23.5, pt - 6.25)), k, zb)
            sd = sd - clip_w                                            # the two 2.4 mm ears bite into the ply edge
            Pc = _db_pt(k, zb, cx, yf + 23.5 - 12.8, pt)
            sd = sd - cyl((Pc[0], Pc[1], zb), (0, 0, 1), 11.4, 1.75)    # clip screw pilot
            Pt = _db_pt(k, zb, cx + sgn * 3.9, yr - 13.0, pt)           # rear tab: notch in the inner bottom edge of the side
            if k == "R":
                sd = sd - box(Pt[0] - 5.0, Pt[0] + 5.0, Pt[1] - 3.6, yl1 + 0.1, zb - 0.1, zb + 4.6)
            else:
                sd = sd - box(Pt[0] - 5.0, Pt[0] + 5.0, yr0 - 0.1, Pt[1] + 3.6, zb - 0.1, zb + 4.6)
            zp = zb - 0.6
            fix.append(cyl((Pc[0], Pc[1], zp - 2.6), (0, 0, 1), 2.6, 3.5) + cyl((Pc[0], Pc[1], zp), (0, 0, 1), 12.0, 1.75))
            hw.append((f"{nm}_snap_clip_{w}", clip_w, (0.9, 0.5, 0.1)))
        else:
            xa, xb = sorted((cx + sgn * 0.3, cx + sgn * 7.5))
            tube = tube - box(xa, xb, yr - 17.0, yr - 8.0, pt, pt + 5.0)            # tab ground off flush
            sf = []
            for ys in (yf + 36.5, yr - 38.0):
                xs = cx + sgn * 4.1                                                    # centre of the 8 mm opening
                tube = tube - cyl((xs, ys, pt - 3.0), (0, 0, 1), 4.5, 2.1)
                sf.append(cyl((xs, ys, pt - 1.5 - 2.6), (0, 0, 1), 2.6, 3.5) + cyl((xs, ys, pt - 1.5), (0, 0, 1), 12.0, 1.75))
                P = _db_pt(k, zb, xs, ys, pt)
                sd = sd - cyl((P[0], P[1], zb), (0, 0, 1), 10.5, 1.75)
            fix.extend(_db_place(sc, k, zb) for sc in sf)
        if DB_FIX == 1:
            pass
        side[k] = sd
        hw.append((f"{nm}_drawbar_{w}", _db_place(tube, k, zb), COL_STEEL))
        hw.append((f"{nm}_drawbar_bracket_{w}", _db_place(d["brk"], k, zb), (0.23, 0.38, 0.71)))
    sl, sr = side["R"], side["L"]

    rx0 = XF + 2.0
    run_l = box(rx0, rx0 + 500.0, Y_SIDE_A1, Y_SIDE_A1 + 14.0, zb - RUN_DROP, zb)
    run_r = box(rx0, rx0 + 500.0, Y_SIDE_B0 - 14.0, Y_SIDE_B0, zb - RUN_DROP, zb)

    g = f"Drawer {i + 1}"
    show(front, f"{nm}_front", colour=COL_FRONT, group=g)
    show(sl, f"{nm}_side_L", colour=COL_PLY, group=g)
    show(sr, f"{nm}_side_R", colour=COL_PLY, group=g)
    show(back, f"{nm}_back", colour=COL_PLY, group=g)
    show(bottom, f"{nm}_bottom", colour=COL_BOARD, group=g)
    if HANDLES:
        show(handle, f"{nm}_handle", colour=COL_HANDLE, group=g)
    show(fuse_list(scr), f"{nm}_pocket_screws", colour=COL_STEEL, group=g, solids=len(scr))
    g = "Hardware - Hafele Alto drawbars"
    for n_, p_, c_ in hw:
        show(p_, n_, colour=c_, group=g)
    for n_, sc in enumerate(fix):
        show(sc, f"{nm}_fixing_screw_{n_ + 1}", colour=(0.3, 0.3, 0.33), group=g)
    g = "Hardware - Hafele Alto 732.25.602"
    show(run_l, f"{nm}_runner_L", colour=COL_STEEL, group=g)
    show(run_r, f"{nm}_runner_R", colour=COL_STEEL, group=g)


def drawer(i):
    if DRAWER_SYS == "drawbar":
        return drawbar_drawer(i)
    if DRAWER_SYS == "alto":
        return alto_drawer(i)
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
    zs = [zb + 45.0, zb + 75.0] if hb < 200 else [zb + 60.0, zb + hb / 2.0, zb + hb - 60.0]
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
    zk = [zb + 45.0, zb + 75.0] if hb < 200 else [zb + 60.0, zb + hb / 2.0 + 10.0, zb + hb - 50.0]
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
    for i in range(N_DRAWERS):
        drawer(i)
    print("OB", OB, "front bottoms", fr_bottom, "box w", BOX_W)


# ======================= fixings to the unit / benchtop =======================
def fixings():
    # 9 steel angle brackets (25 x 25 x 2, 40 long) under the benchtop: 3 per side, 3 on the back.
    # Their 2 mm legs sit in the drawer clearances, so nothing blocks the top drawer.
    BT, BW, BH = 2.0, 40.0, 25.0
    br = []
    for xc in (2575.0, 2735.0, 2895.0):
        x0, x1 = xc - BW / 2, xc + BW / 2
        br.append(box(x0, x1, Y_SIDE_A1, Y_SIDE_A1 + BT, Z_TOP - BH, Z_TOP) + box(x0, x1, Y_SIDE_A1, Y_SIDE_A1 + BH, Z_TOP - BT, Z_TOP))
        br.append(box(x0, x1, Y_SIDE_B0 - BT, Y_SIDE_B0, Z_TOP - BH, Z_TOP) + box(x0, x1, Y_SIDE_B0 - BH, Y_SIDE_B0, Z_TOP - BT, Z_TOP))
    for dy in (-250.0, 0.0, 250.0):
        y0, y1 = YC + dy - BW / 2, YC + dy + BW / 2
        br.append(box(X_BACKP0 - BT, X_BACKP0, y0, y1, Z_TOP - BH, Z_TOP) + box(X_BACKP0 - BH, X_BACKP0, y0, y1, Z_TOP - BT, Z_TOP))
    show(fuse_list(br), "benchtop_brackets", colour=COL_STEEL, group="Fixings", solids=len(br))
    # bracket screws: 2 per leg. Vertical legs: No.8 x 12 into the carcass; top legs: No.8 x 16 up into the benchtop
    bs = []
    for xc in (2575.0, 2735.0, 2895.0):
        for ox in (-10.0, 10.0):
            x = xc + ox
            bs.append(cyl((x, Y_SIDE_A1 + BT + 3.0, Z_TOP - 14.0), (0, -1, 0), 3.0, 4.0) + cyl((x, Y_SIDE_A1 + BT, Z_TOP - 14.0), (0, -1, 0), 12.0, 2.0))
            bs.append(cyl((x, Y_SIDE_B0 - BT - 3.0, Z_TOP - 14.0), (0, 1, 0), 3.0, 4.0) + cyl((x, Y_SIDE_B0 - BT, Z_TOP - 14.0), (0, 1, 0), 12.0, 2.0))
            bs.append(cyl((x, Y_SIDE_A1 + 15.0, Z_TOP - BT - 3.0), (0, 0, 1), 3.0, 4.0) + cyl((x, Y_SIDE_A1 + 15.0, Z_TOP - BT), (0, 0, 1), 16.0, 2.0))
            bs.append(cyl((x, Y_SIDE_B0 - 15.0, Z_TOP - BT - 3.0), (0, 0, 1), 3.0, 4.0) + cyl((x, Y_SIDE_B0 - 15.0, Z_TOP - BT), (0, 0, 1), 16.0, 2.0))
    for dy in (-250.0, 0.0, 250.0):
        for oy in (-10.0, 10.0):
            y = YC + dy + oy
            bs.append(cyl((X_BACKP0 - BT - 3.0, y, Z_TOP - 14.0), (1, 0, 0), 3.0, 4.0) + cyl((X_BACKP0 - BT, y, Z_TOP - 14.0), (1, 0, 0), 12.0, 2.0))
            bs.append(cyl((X_BACKP0 - 15.0, y, Z_TOP - BT - 3.0), (0, 0, 1), 3.0, 4.0) + cyl((X_BACKP0 - 15.0, y, Z_TOP - BT), (0, 0, 1), 16.0, 2.0))
    show(fuse_list(bs), "bracket_screws", colour=COL_STEEL, group="Fixings", solids=len(bs))
    # four No.8 x 25 screws from inside the plinth, through the front rail into the kickboard (non-structural cover)
    ks = [cyl((KB_X1 + T + 3.0, YC + dy, Z_FLOOR + 57.5), (-1, 0, 0), 3.0, 4.0) + cyl((KB_X1 + T, YC + dy, Z_FLOOR + 57.5), (-1, 0, 0), 25.0, 2.0)
          for dy in (-300.0, -100.0, 100.0, 300.0)]
    show(fuse_list(ks), "kickboard_screws", colour=COL_STEEL, group="Plinth", solids=len(ks))
    # two M6 x 65 link bolts from the joint-end side into the main run's front framing rail
    bolts = []
    holes = []
    for xb in (2935.0, 2975.0):   # behind the full-height door's parked position (door edge x 2912.9)
        z = 104.5
        holes.append(box(xb - 3.25, xb + 3.25, Y_SIDE_B0 - 1.0, Y_SIDE_B0 + T + 1.0, z - 3.25, Z_TOP + 1.0))   # slot open to the top edge: a round hole would leave only 1.9 mm of ply above it
        bolts.append(cyl((xb, Y_SIDE_B0 - 5.0, z), (0, 1, 0), 5.0, 4.0) + cyl((xb, Y_SIDE_B0, z), (0, 1, 0), 50.0 + FRAME_FIX, 3.0))
    show(fuse_list(bolts), "link_bolts_to_main_run", colour=COL_STEEL, group="Fixings", solids=len(bolts))
    return fuse_list(holes)


_link_holes = fixings()
show(side_b - _link_holes, "side_joint_end", colour=COL_PLY, group="Carcass")


# ======================= sliding door over the corner cupboard =======================
# Door closes the 311 mm gap beside the bin drawer, slides right BEHIND the bench extension and parks with its
# leading edge flush with the extension's front plane (x 2442.9). A push latch + magnet holds it there; pushing it
# in releases the latch, which pops the door ~20 mm back out so the edge can be gripped.
DOOR_SLIDE = 0.0           # 0 closed, 452 parked behind the extension, 432 popped out 20 mm
RP1 = 1990.885             # outer face of the bin drawer's right side panel
SD_X0 = RP1
SD_W = 470.0               # 450 mm opening + 20 mm tucked behind the extension when closed
DY0 = 445.579              # same plane as the existing doors
DY1 = DY0 + 15.0
DX0 = SD_X0 + DOOR_SLIDE
DX1 = DX0 + SD_W
DZ0, DZ1 = -625.398, 104.602  # full height, same as the other doors
TRACK_X0, TRACK_X1 = 2005.0, 2930.0   # track hangs under the framing rail (clear of the sink rim)


def sliding_door():
    door = box(DX0, DX1, DY0, DY1, DZ0, DZ1)
    fx, fz = DX0 + 40.0, -100.0                                                              # routed finger pull
    door = door - box(fx - 15, fx + 15, DY0 - 0.1, DY0 + 6.0, fz - 35, fz + 35)
    door = door - cyl((fx, DY0 - 0.1, fz + 35), (0, 1, 0), 6.1, 15.0) - cyl((fx, DY0 - 0.1, fz - 35), (0, 1, 0), 6.1, 15.0)
    show(door, "sliding_door", colour=COL_FRONT, group="Sliding door")

    # C-channel track screwed to the underside of the framing rail (z 69.6), opening toward the front
    track = box(TRACK_X0, TRACK_X1, 467.579, 481.579, 55.6, 69.6)
    track = track - box(TRACK_X0 - 1, TRACK_X1 + 1, 466.0, 477.579, 59.0, 66.0)
    show(track, "door_top_track", colour=COL_STEEL, group="Sliding door")

    # hangers: 2 mm plate on the door's back face (in the 3 mm gap to the rail) + arm running in the track
    hangers = []
    for hx in (DX0 + 70.0, DX0 + 400.0):
        hangers.append(box(hx - 15, hx + 15, DY1, DY1 + 2.0, 50.0, 69.0) + box(hx - 15, hx + 15, DY1, 474.579, 60.0, 65.0))
    show(fuse_list(hangers), "door_hangers", colour=COL_STEEL, group="Sliding door", solids=len(hangers))

    latch = box(2861.0, 2891.0, 468.579, 472.579, 60.5, 64.5)                               # push latch + magnet in the track end
    show(latch, "door_push_latch", colour=(0.8, 0.2, 0.2), group="Sliding door")


if SHOW_DOOR:
    sliding_door()


# ======================= push-to-open bin drawer in the bay beside the extension =======================
# The existing left door (ref_door-left_2 + handle) is removed. The 773 mm bay gets two fixed side panels,
# a base, a push-to-open bin drawer and a fixed filler panel above it, all in the existing doors' plane.
BAY_X0, BAY_X1 = 1667.885, X_EDGE            # bay between door-right and the extension's front plane
RP1 = 1990.885                                # outer face of the bin drawer's right side panel (sliding door starts here)
DF_Y0 = 445.579                               # existing door fronts (15 mm behind the benchtop edge)
DF_Y1 = DF_Y0 + 19.0
BAY_Y1 = 1026.0                               # side panels / base stop short of the cabinet back (y 1030)
DOOR_Z0, DOOR_Z1 = -625.398, 104.602
B_SIDE_L = box(BAY_X0, BAY_X0 + T, DF_Y1, BAY_Y1, Z_PLINTH_TOP, Z_TOP - 41.0)
B_SIDE_R = box(RP1 - T, RP1, DF_Y1, BAY_Y1, Z_PLINTH_TOP, Z_TOP - 41.0)
B_BASE = box(BAY_X0 + T, RP1 - T, DF_Y1, BAY_Y1, Z_PLINTH_TOP, Z_PLINTH_TOP + 16.0)   # existing base (not built; kept for reference)
show(B_SIDE_L, "bay_side_L", colour=COL_PLY, group="Bay bin drawer")
show(B_SIDE_R, "bay_side_R", colour=COL_PLY, group="Bay bin drawer")
show(B_BASE, "bay_base", colour=(0.6, 0.6, 0.6), group="Existing joinery (assumed)")

B_OPEN = (RP1 - T) - (BAY_X0 + T)              # 426 between the side panels
B_BOXW = B_OPEN - 10.0                        # 731 outer -> 699 inside (opening - 42)
BX0 = (BAY_X0 + RP1) / 2.0 - B_BOXW / 2.0
BX1 = BX0 + B_BOXW
FRONT_X0, FRONT_X1 = BAY_X0 + 4.0, RP1 - 4.0        # 450 wide, 4 mm gaps like the existing doors
BF_H = 730.0                                  # full door height
BF0 = DOOR_Z0
BF1 = BF0 + BF_H
BZB = BF0 + 22.0                              # box side bottom edge (runner rule as the unit's drawers)
BHB = 350.0                                   # low box sides: top at z -250, below the fixed basket runners
BNL = 550.0
BYP = DF_Y1                                   # front edge of the bay panels (fixed hardware is set from here)
BY0 = DF_Y0 + FRONT_T                         # back face of the 15 mm bin drawer front
BY1 = BY0 + BNL
b_front = box(FRONT_X0, FRONT_X1, DF_Y0, BY0, BF0, BF1)
b_front = b_front - box(BX0 + T - GROOVE_D, BX1 - T + GROOVE_D, BY0 - GROOVE_D, BY0 + 0.1, BZB + GR0, BZB + GR1)
b_sl = box(BX0, BX0 + T, BY0, BY1, BZB, BZB + BHB) - box(BX0 + T - GROOVE_D, BX0 + T + 0.1, BY0 - 0.1, BY1 + 0.1, BZB + GR0, BZB + GR1)
b_sr = box(BX1 - T, BX1, BY0, BY1, BZB, BZB + BHB) - box(BX1 - T - 0.1, BX1 - T + GROOVE_D, BY0 - 0.1, BY1 + 0.1, BZB + GR0, BZB + GR1)
b_back = box(BX0 + T, BX1 - T, BY1 - T, BY1, BZB + GR1, BZB + BHB)
b_bot = box(BX0 + T - GROOVE_D + 0.25, BX1 - T + GROOVE_D - 0.25, BY0 - GROOVE_D + 0.5, BY1, BZB + 13.0, BZB + 13.0 + BOT_T)
show(b_front, "bin_drawer_front", colour=COL_FRONT, group="Bay bin drawer")
show(b_sl, "bin_drawer_side_L", colour=COL_PLY, group="Bay bin drawer")
show(b_sr, "bin_drawer_side_R", colour=COL_PLY, group="Bay bin drawer")
show(b_back, "bin_drawer_back", colour=COL_PLY, group="Bay bin drawer")
show(b_bot, "bin_drawer_bottom", colour=COL_BOARD, group="Bay bin drawer")

# two bins stand on the drawer base, one behind the other, taller than the box sides
bins = []
bw = B_BOXW - 2 * T - 12.0
bx0 = BX0 + T + 6.0
zb0 = BZB + 13.0 + BOT_T
for k in (0, 1):
    by0 = BY0 + 10.0 + k * 261.0
    outer = box(bx0, bx0 + bw, by0, by0 + 255.0, zb0, zb0 + 360.0)
    inner = box(bx0 + 3.0, bx0 + bw - 3.0, by0 + 3.0, by0 + 252.0, zb0 + 3.0, zb0 + 361.0)
    show(outer - inner, f"bin_{k + 1}", colour=(0.25, 0.35, 0.3), group="Bay bin drawer")

# Blum TANDEM 563H5500B envelopes (same simplified model as the unit's drawers) + TIP-ON adapter block
rz0 = BZB - 12.0                              # runner flange top meets the box side bottom
ry0 = BYP + 3.0
rl = box(BAY_X0 + T, BAY_X0 + T + 1.5, ry0, ry0 + NL, rz0, rz0 + 40.0) + box(BAY_X0 + T, BAY_X0 + T + 21.0, ry0, ry0 + NL, rz0, rz0 + 12.0)
rr = box(RP1 - T - 1.5, RP1 - T, ry0, ry0 + NL, rz0, rz0 + 40.0) + box(RP1 - T - 21.0, RP1 - T, ry0, ry0 + NL, rz0, rz0 + 12.0)
show(rl, "bin_drawer_runner_L", colour=COL_STEEL, group="Hardware - Blum TANDEM 563H5500B")
show(rr, "bin_drawer_runner_R", colour=COL_STEEL, group="Hardware - Blum TANDEM 563H5500B")
tip = box((BX0 + BX1) / 2.0 - 30.0, (BX0 + BX1) / 2.0 + 30.0, BY1 + 2.0, BY1 + 22.0, BZB + 30.0, BZB + 60.0)
show(tip, "bin_drawer_tipon_envelope", colour=COL_STEEL, group="Hardware - Blum TANDEM 563H5500B")

# internal wire basket on its own runners above the bins (cleaning products, bin bags)
BK_Z0, BK_Z1 = -205.0, -75.0                          # basket sits 10 mm above bin tops (z -215.4)
bk_x0, bk_x1 = BAY_X0 + T + 13.0, RP1 - T - 13.0       # between runners fixed to the bay side panels
bk_y0, bk_y1 = BYP + 30.0, BYP + 450.0
sub_l = box(BAY_X0 + T, BAY_X0 + T + 13.0, BYP + 20.0, BYP + 470.0, BK_Z0 - 10.0, BK_Z0 + 30.0)
sub_r = box(RP1 - T - 13.0, RP1 - T, BYP + 20.0, BYP + 470.0, BK_Z0 - 10.0, BK_Z0 + 30.0)
show(sub_l, "basket_runner_L", colour=COL_STEEL, group="Hardware - Blum TANDEM 563H5500B")
show(sub_r, "basket_runner_R", colour=COL_STEEL, group="Hardware - Blum TANDEM 563H5500B")
rods = []
w = 5.0                                               # 5 mm square bars (wire modelled as square section)
nx = 7
xs = [bk_x0 + i * (bk_x1 - bk_x0 - w) / (nx - 1) for i in range(nx)]
ys = [bk_y0 + j * (bk_y1 - bk_y0 - w) / 7 for j in range(8)]
for x in xs:                                          # bottom bars along y
    rods.append(box(x, x + w, bk_y0, bk_y1, BK_Z0, BK_Z0 + w))
for y in ys:                                          # bottom cross bars
    rods.append(box(bk_x0, bk_x1, y, y + w, BK_Z0, BK_Z0 + w))
zt = BK_Z1 - w                                        # top perimeter
rods.append(box(bk_x0, bk_x1, bk_y0, bk_y0 + w, zt, BK_Z1))
rods.append(box(bk_x0, bk_x1, bk_y1 - w, bk_y1, zt, BK_Z1))
rods.append(box(bk_x0, bk_x0 + w, bk_y0, bk_y1, zt, BK_Z1))
rods.append(box(bk_x1 - w, bk_x1, bk_y0, bk_y1, zt, BK_Z1))
for xx in (bk_x0, bk_x1 - w):                         # side uprights
    for yy in (bk_y0, (bk_y0 + bk_y1) / 2.0 - w / 2, bk_y1 - w):
        rods.append(box(xx, xx + w, yy, yy + w, BK_Z0, BK_Z1))
xm = (bk_x0 + bk_x1) / 2.0 - w / 2                    # front / back uprights
for yy in (bk_y0, bk_y1 - w):
    rods.append(box(xm, xm + w, yy, yy + w, BK_Z0, BK_Z1))
show(fuse_list(rods), "wire_basket", colour=(0.8, 0.8, 0.82), group="Bay bin drawer")


# ---- dashed assembly (fastener) lines for the picture steps ----
def _tree_fuse(lst):
    while len(lst) > 1:
        lst = [lst[k] + lst[k + 1] if k + 1 < len(lst) else lst[k] for k in range(0, len(lst), 2)]
    return lst[0]


def _dashes(a, b, r=1.5, on=14.0, off=10.0):
    d = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    L = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
    out, t = [], 0.0
    if L < 6.0:
        return out
    while t < L - 1.0:
        out.append(cyl(add(a, t, d if False else (d[0] / L, d[1] / L, d[2] / L)), d, min(on, L - t), r))
        t += on + off
    return out


def _av_lines(pairs):
    """pairs: list of (a, b) world points; one dashed line each."""
    segs = []
    for a, b in pairs:
        segs += _dashes(a, b)
    if segs:
        _golf_show(_tree_fuse(segs), "av_assembly_lines", colour=(0.1, 0.1, 0.1), group="Guides", solids=len(segs))


def _off(n):
    return _av_rule(n)[1]


def _sub(p, o):
    return (p[0] + o[0], p[1] + o[1], p[2] + o[2])


def _fp_pairs(key):
    out = []
    for pt, recv, mover in _FP[key]:
        out.append((_sub(pt, _off(mover)), _sub(pt, _off(recv))))
    return out


def _ctr(n):
    lo, hi = _BB[n]
    return ((lo[0] + hi[0]) / 2.0, (lo[1] + hi[1]) / 2.0, (lo[2] + hi[2]) / 2.0)


def _av_guides():
    st = AV_STEP
    pr = []
    if st == 1:
        pr = _fp_pairs("pl_rail_to_side")
    elif st == 2:
        pr = _fp_pairs("plinth_to_carcass") + _fp_pairs("carcass")
    elif st == 3:       # runners go onto the carcass walls: lines at the front and rear runner fixing positions
        for k in "123":
            for w in "LR":
                c = _ctr("drawer%s_runner_%s" % (k, w))
                o = _off("drawer%s_runner_%s" % (k, w))
                for dx in (-170.0, 170.0):
                    P = (c[0] + dx, c[1], c[2])
                    pr.append((_sub(P, o), P))
    elif st == 4:
        lo = {n: _BB["drawer1_" + n] for n in ("front", "side_L", "side_R", "back", "bottom")}
        zb = (lo["side_L"][0][2] + lo["side_L"][1][2]) / 2.0
        hh = lo["side_L"][1][2] - lo["side_L"][0][2]
        for sd in ("side_L", "side_R"):
            ys = (lo[sd][0][1] + lo[sd][1][1]) / 2.0
            for f in (0.3, 0.7):
                z = lo[sd][0][2] + hh * f
                for nb, x in (("front", lo["front"][1][0] - 0.0), ("back", lo["back"][0][0] + 7.5)):
                    P = (x, ys, z)
                    pr.append((_sub(P, _off("drawer1_" + nb)), _sub(P, _off("drawer1_" + sd))))
        bc = _ctr("drawer1_bottom")
        for dy in (-250.0, 250.0):
            P = (bc[0], bc[1] + dy, bc[2])
            pr.append((_sub(P, _off("drawer1_bottom")), P))
    elif st == 5:
        for w in "LR":
            c = _ctr("drawer1_snap_clip_" + w)
            P = (c[0], c[1], c[2] - 7.0)
            pr.append((_sub(P, (0, 0, 150)), P))
            db = _BB["drawer1_drawbar_" + w] if "drawer1_drawbar_" + w in _BB else None
            if db:
                T_ = ((db[1][0] - 14.0), c[1], c[2] - 7.0)
                pr.append((_sub(T_, (0, 0, 150)), T_))
    elif st == 6:
        for w in "LR":
            c = _ctr("drawer1_snap_clip_" + w)
            pr.append((_sub(c, (-300, 0, 110)), c))
    elif st == 8:
        for k in "123":
            for w in "LR":
                c = _ctr("drawer%s_drawbar_bracket_%s" % (k, w))
                o = _off("drawer%s_front" % k)
                pr.append((_sub(c, o), c))
    elif st == 9:
        for dy in (-300.0, -100.0, 100.0, 300.0):
            P = (KB_X1 + T, YC + dy, Z_FLOOR + 57.5)
            pr.append((_sub(P, (-220, 0, 0)), P))
        for xb in (2935.0, 2975.0):
            P = (xb, Y_SIDE_B0 - 5.0, 104.5)
            pr.append(((P[0], P[1] - 110.0, P[2]), P))
        for xc in (2575.0, 2735.0, 2895.0):
            for ox in (-10.0, 10.0):
                for ys in (Y_SIDE_A1 + 15.0, Y_SIDE_B0 - 15.0):
                    P = (xc + ox, ys, Z_TOP - 2.0)
                    pr.append((_sub(P, (0, 0, 220)), P))
    _av_lines(pr)


if AV_STEP:
    _av_guides()
