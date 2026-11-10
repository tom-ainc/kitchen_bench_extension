D = "/home/user/CAD/kitchen_bench_extension/"
for fn, tag in [("Left Runner Drawbar.step", "L"), ("Right Runner Drawbar.step", "R"), ("Drawer Mounting Hardware - Snap Clip.step", "C")]:
    ps = import_step_file(D + fn).parts()
    for i, p in enumerate(ps):
        show(p, f"{tag}{i}")
        print(tag, i, p.bbox() if hasattr(p, "bbox") else "")
