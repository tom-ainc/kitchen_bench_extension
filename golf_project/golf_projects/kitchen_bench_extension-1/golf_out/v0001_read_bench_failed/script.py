imp = import_step_file("/home/user/CAD/kitchen_bench_extension/bench.step")
for p in imp.parts():
    bb = p.bounding_box()
    print(p.name(), [round(v,1) for v in bb.min()], [round(v,1) for v in bb.max()], round(p.volume()))
    show(p, p.name() or "part")
