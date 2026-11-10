D = "/home/user/CAD/kitchen_bench_extension/"
clip = import_step_file(D + "Drawer Mounting Hardware - Snap Clip.step").parts()[0]
L = import_step_file(D + "Left Runner Drawbar.step").parts()
def slabs(p, axis, lo, hi, n, tag):
    for i in range(n):
        a = lo + (hi - lo) * i / n; b = lo + (hi - lo) * (i + 1) / n
        mid = (a + b) / 2
        if axis == 2: cut = Part.cuboid(1000, 1000, b - a).moved(Location.translation(0, 0, mid))
        elif axis == 0: cut = Part.cuboid(b - a, 1000, 1000).moved(Location.translation(mid, 0, 0))
        else: cut = Part.cuboid(1000, b - a, 1000).moved(Location.translation(0, mid, 0))
        try:
            s = p & cut
            bb = s.bounding_box()
            print(tag, "ax", axis, round(a, 2), round(b, 2), [round(v, 2) for v in bb.min()], [round(v, 2) for v in bb.max()], round(s.volume(), 1))
        except Exception as e:
            print(tag, axis, round(a, 2), "empty/err", str(e)[:40])
slabs(clip, 2, -5.95, 8.65, 14, "clipZ")
for f in clip.faces().of_kind(SurfaceKind.Cylinder):
    print("clip cyl", f.id(), round(f.radius(), 2), [round(v, 2) for v in f.axis().origin()] if hasattr(f.axis(), "origin") else f.axis(), f.axis())
L0 = L[0]
slabs(L0, 2, -64.76, -33.76, 10, "L0Z")
for f in L0.faces().of_kind(SurfaceKind.Cylinder):
    print("L0 cyl", f.id(), round(f.radius(), 2), f.axis())
show(clip, "clip")
