D = "/home/user/CAD/kitchen_bench_extension/"
clip = import_step_file(D + "Drawer Mounting Hardware - Snap Clip.step").parts()[0]
L0 = import_step_file(D + "Left Runner Drawbar.step").parts()[0]
CX = -128.9047
best = []
for tz in range(-47, -33, 1):
    row = []
    for ty in range(-362, -336, 3):
        # clip plate top local z=6.25 -> world tz
        c = clip.moved(Location.translation(CX, ty, tz - 6.25))
        try:
            v = (c & L0).volume()
        except Exception:
            v = 0.0
        row.append(round(v, 1))
        best.append((v, tz, ty))
    print("tz", tz, row)
print("ty:", list(range(-362, -336, 3)))
show(clip, "clip")
