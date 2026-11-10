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
seen = {}
for p in imp.parts():
    n = p.name()
    if n == "KickboardExt":
        continue  # replaced by the plinth fascia below
    seen[n] = seen.get(n, 0) + 1
    nm = n.replace(" ", "_") + ("" if seen[n] == 1 else f"_{seen[n]}")
    show(p, "ref_" + nm, group="Reference bench")

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
show(side_b, "side_joint_end", colour=COL_PLY, group=grp)
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
