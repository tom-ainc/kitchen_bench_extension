imp = import_step_file("/home/user/CAD/kitchen_bench_extension/bench.step")
ps = imp.parts()
print(len(ps), imp.warnings())
for i, p in enumerate(ps):
    bb = p.bounding_box()
    print(i, p.name(), [round(v,1) for v in bb.min()], [round(v,1) for v in bb.max()], round(p.volume()))
    show(p, f"{i}_{p.name()}")
