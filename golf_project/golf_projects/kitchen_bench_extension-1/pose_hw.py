D = "/home/user/CAD/kitchen_bench_extension/"
TY = -338.0   # world y of clip rear end
TZ = -33.762  # plate top = tube top
clip = import_step_file(D + "Drawer Mounting Hardware - Snap Clip.step").parts()[0]
L = import_step_file(D + "Left Runner Drawbar.step").parts()
show(L[0].with_colour((0.23, 0.38, 0.71, 0.55)), "bracket")
show(L[1].with_colour((0.65, 0.65, 0.65, 0.55)), "drawbar")
c = clip.moved(Location.translation(-128.9047, TY, TZ - 6.25))
show(c.with_colour((0.9, 0.5, 0.1)), "clip")
