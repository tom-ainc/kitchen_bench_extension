# Alto drawbar fixing options, one runner side (left), in the drawbar STEP file's own coordinates (mm).
# OPTION 1: snap clip under the base at the front + Ø10 blind hole over the rear tab.
# OPTION 2: rear tab cut off, two screws from below through the drawbar top plate.
OPTION = 1
D = "/home/user/CAD/kitchen_bench_extension/"
BASE_T = 15.0
PLATE_TOP = -33.762          # top of the drawbar plate = underside of the base
PLATE_BOT = -35.262          # underside of the drawbar plate (1.5 mm steel)
CLIP_X, CLIP_Y = -128.9047, -338.0   # clip centre line, and its rear end against the bracket back wall
SLOT_X = -124.8              # centre of the 8 mm opening in the underside of the drawbar
TAB_X, TAB_Y = -125.0, 120.4

def bx(x0, x1, y0, y1, z0, z1):
    return Part.cuboid(x1 - x0, y1 - y0, z1 - z0).moved(Location.translation((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))

def cy(x, y, z0, z1, r):
    return Part.cylinder(r, z1 - z0).moved(Location.translation(x, y, (z0 + z1) / 2))

clip = import_step_file(D + "Drawer Mounting Hardware - Snap Clip.step").parts()[0]
L = import_step_file(D + "Left Runner Drawbar.step").parts()
bracket, drawbar = L[0], L[1]

base = bx(-136.5, -90.0, -361.0, 134.0, PLATE_TOP, PLATE_TOP + BASE_T)
STEEL = (0.62, 0.64, 0.68)
screws = []

if OPTION == 1:
    clip_p = clip.moved(Location.translation(CLIP_X, CLIP_Y, PLATE_TOP - 6.25))
    cy_clip = CLIP_Y - 12.8
    base = base - clip_p                                   # the two 2.4 mm ears bite into the ply
    base = base - cy(CLIP_X, cy_clip, PLATE_TOP, PLATE_TOP + 11.4, 1.75)    # screw pilot
    base = base - cy(TAB_X, TAB_Y, PLATE_TOP, PLATE_TOP + 6.0, 5.0)         # Ø10 x 6 hole over the rear tab
    zb = PLATE_TOP - 0.6                                   # underside of the clip plate
    screws.append(cy(CLIP_X, cy_clip, zb - 2.6, zb, 3.5) + cy(CLIP_X, cy_clip, zb, zb + 12.0, 1.75))
    show(clip_p.with_colour((0.9, 0.5, 0.1)), "snap_clip", group="Fixing option 1: snap clip")
else:
    drawbar = drawbar - bx(-128.6, -121.4, 116.0, 125.0, PLATE_TOP + 0.05, PLATE_TOP + 5.0)   # tab ground off flush
    for yy in (-325.0, 95.0):
        drawbar = drawbar - cy(SLOT_X, yy, PLATE_BOT - 0.5, PLATE_TOP + 0.5, 2.1)
        base = base - cy(SLOT_X, yy, PLATE_TOP, PLATE_TOP + 10.5, 1.75)
        screws.append(cy(SLOT_X, yy, PLATE_BOT - 2.6, PLATE_BOT, 3.5) + cy(SLOT_X, yy, PLATE_BOT, PLATE_BOT + 12.0, 1.75))

grp = "Fixing option %d" % OPTION
show(base.with_colour((0.82, 0.68, 0.46)), "base_15mm_ply", group=grp)
show(drawbar.with_colour(STEEL), "drawbar_L", group=grp)
show(bracket.with_colour((0.23, 0.38, 0.71)), "front_bracket_L", group=grp)
for i, s in enumerate(screws):
    show(s.with_colour((0.3, 0.3, 0.33)), "screw_%d" % (i + 1), group=grp)
