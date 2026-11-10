from sdlib import *


def part_label(V, u, v, t, size=6.5):
    V.txt(u, v, t, size=size, weight="bold", c="#6b5a3c")


def sheet4(pdf, png=None):
    sh = Sheet(pdf, 4, "CARCASS PARTS C1 TO C4", "Scale 1:8. Dimensions in mm. All 15 mm ply")
    s = 0.11
    # ---- C1 (free-end side) viewed from outside; C2 viewed from inside the unit. Front edge at the left. u = depth, v = height.
    for k, (ox, name, sub) in enumerate(((22, "C1 SIDE, FREE END", "1 off. Seen from outside"), (100, "C2 SIDE, JOINT END", "1 off. Seen from inside the unit"))):
        V = View(sh, ox, 172, s)
        V.rect(0, 0, 522, 749, fc=PLY, lw=0.8)
        V.title(0, 779 + (150 if k else 0), name, sub)
        V.dim_h(0, 522, 0, -9, "522")
        V.dim_v(0, 749, 0, -9, "749")
        V.txt(261, 374, "FRONT EDGE ON THE LEFT", size=4.6, c=GREY)
        V.txt(0, -50, "front", size=4.5, ha="left", c=GREY)
        if k == 1:
            for u in (456.1, 496.1):
                V.rect(u - 3.25, 721.65, u + 3.25, 749, fc="white", lw=0.6)
            V.dim_h(0, 456.1, 743.9, 7, "456.1")
            V.dim_h(456.1, 496.1, 743.9, 16, "40")
            V.dim_v(721.65, 749, 522, 8, "27.4")
            V.leader(496.1, 743.9, -3, -22, "2 slots 6.5 wide open to the top edge (M6 link bolts)", ha="right")
    # ---- C3 bottom, plan: u = width (775), v = depth (522), front at the bottom
    V = View(sh, 185, 172, s)
    V.rect(0, 0, 775, 507, fc=PLY, lw=0.8)
    V.title(0, 600, "C3 BOTTOM", "1 off. Plan, front edge at the bottom")
    V.dim_h(0, 775, 0, -9, "775"); V.dim_v(0, 507, 0, -9, "507")
    V.txt(388, 254, "NO MACHINING", size=5, c=GREY)
    # ---- C4 back, elevation from inside: u = width (775), v = height (725)
    V = View(sh, 290, 172, s)
    V.rect(0, 0, 775, 749, fc=PLY, lw=0.8)
    V.title(0, 779, "C4 BACK", "1 off. Seen from inside")
    V.dim_h(0, 775, 0, -9, "775"); V.dim_v(0, 749, 0, -9, "749")
    V.txt(388, 374, "NO MACHINING", size=5, c=GREY)
    # ---- C9 front top rail
    V = View(sh, 290, 132, s)
    V.rect(0, 0, 775, 60, fc=PLY, lw=0.8)
    V.title(0, 90, "C9 TOP RAIL, FRONT", "1 off. Between the sides at the top; 2 pocket holes at each end")
    V.dim_h(0, 775, 0, -9, "775"); V.dim_v(0, 60, 0, -9, "60")
    for u in (20, 755):
        for v in (18, 42):
            V.circ(u, v, 4.0, fc="white", lw=0.5)
    # ---- assembly sketch
    A = View(sh, 25, 40, 0.07)
    A.txt(0, 0, "", size=1)
    notes = [
        "ASSEMBLY",
        "Sides C1, C2 stand on the plinth. C3 goes between them, its bottom edge flush with the bottom edges of the sides and its front edge flush with the side fronts.",
        "C4 is full height, between the sides, standing on the ends of the plinth side rails, its rear face flush with the side rear edges; C3 butts its front face. C9 goes between the sides at the top front.",
        "Glue every joint and pocket-screw (25 mm) from C3 (4 per side, in its underside), C4 (5 per side, in its rear face) and C9 (2 per end, in its underside) into the faces of the sides. Check square (within 1 mm).",
        "Overall carcass: 805 wide x 522 deep x 749 high, 775 clear between the sides, inside depth 507, inside height above C3 734. The top of the carcass is 874 above the floor.",
        "The benchtop (existing) sits on the sides and back; 9 angle brackets 25 x 25 x 2 x 40 long fix it (see sheet 3). Two M6 x 65 bolts through C2 link the unit to the main run.",
    ]
    for i, t in enumerate(notes):
        sh.ax.text(25, 98 - i * 5.2, t, fontsize=6.2 if i == 0 else 5.4, weight="bold" if i == 0 else "normal", va="center")
    if png:
        sh.png(png)
    sh.save()


def sheet5(pdf, png=None):
    sh = Sheet(pdf, 5, "PLINTH P1 TO P4 AND KICKBOARD Kb", "Scale 1:5. Dimensions in mm. All 15 mm ply")
    s = 0.2
    # plan: u = w (joint end at left), v = d (front at bottom)
    P = View(sh, 25, 80, s)
    ox = 60.0
    def U(w): return w + ox
    P.rect(U(-53), 77, U(799), 92, fc=LIGHT, lw=0.7)                  # Kb
    P.rect(U(17), 92, U(782), 107, fc=PLY, lw=0.7)                      # P1
    P.rect(U(17), 530, U(782), 545, fc=PLY, lw=0.7)                    # P2
    P.rect(U(2), 92, U(17), 553, fc=PLY, lw=0.7)                       # P4 joint end
    P.rect(U(782), 92, U(797), 553, fc=PLY, lw=0.7)                    # P3 free end
    P.rect(U(2), 593, U(17), 596, fc=PLY, lw=0.7) if False else None
    # carcass above, outline
    P.rect(U(0), 38, U(805), 560, ls=(0, (6, 3)), lw=0.4, ec=GREY, z=1)
    P.txt(U(400), 330, "CARCASS ABOVE (DASHED)", size=5, c=GREY)
    P.txt(U(400), 85, "Kb", size=6, weight="bold"); P.txt(U(400), 100, "P1", size=6, weight="bold"); P.txt(U(400), 538, "P2", size=6, weight="bold")
    P.txt(U(9.5), 335, "P4", size=6, weight="bold", rot=90); P.txt(U(789.5), 335, "P3", size=6, weight="bold", rot=90)
    P.dim_h(U(-53), U(799), 77, -9, "852 (Kb)")
    P.dim_h(U(2), U(797), 553, 9, "795 outer frame")
    P.dim_h(U(17), U(782), 553, 17, "767 (P1, P2)")
    P.dim_v(92, 553, U(-60), -2, "461 (P3, P4)")
    P.dim_v(17, 77, U(-53), -10, "60")
    P.dim_v(62, 77, U(-53), -10, "15") if False else None
    P.dim_h(U(-53), U(2), 77, 5, "53")
    P.dim_v(38, 92, U(805), 8, "54")
    P.leader(U(102.5), 84.5, 0, -24, "4 x No.8 x 25 screws\nthrough P1 into Kb", ha="left")
    for w in (102.5, 302.5, 502.5, 702.5):
        P.circ(U(w), 99.5, 1.8, fc="white", lw=0.5, z=6)
    P.title(U(-53), 700, "PLINTH FRAME P1 TO P4 AND KICKBOARD Kb, PLAN", "SCALE 1:5")
    # strips on the right
    R = View(sh, 235, 232, 0.15)
    items = [("P1", 767, "FRONT RAIL, 1 off"), ("P2", 767, "REAR RAIL, 1 off"), ("P3, P4", 461, "SIDE RAILS, 2 off"), ("Kb", 852, "KICKBOARD COVER, 1 off")]
    y = 0.0
    for i, (n, L, nm) in enumerate(items):
        v0 = -i * 215.0
        hh = 115 if n == "Kb" else 125
        R.rect(0, v0, L, v0 + hh, fc=PLY if n != "Kb" else LIGHT, lw=0.7)
        R.txt(L / 2, v0 + 57, n, size=7, weight="bold", c="#6b5a3c")
        R.dim_h(0, L, v0, -4.5 if False else -7, "%d" % L)
        R.dim_v(v0, v0 + hh, 0, -6, "%d" % hh)
        R.txt(0, v0 + 128, nm, size=5.5, ha="left", weight="bold")
        if n in ("P1", "Kb"):
            xs = [85.5, 285.5, 485.5, 685.5] if n == "P1" else [155.5, 355.5, 555.5, 755.5]
            for x in xs:
                R.circ(x, v0 + 57.5, 2.0, fc="white", lw=0.5)
            R.dim_h(0, xs[0], v0 + 57.5, 0, "%g" % xs[0]) if False else None
            R.txt(L / 2, v0 + 80, "screws at %s, 57.5 up" % (", ".join("%g" % q for q in xs)), size=4.4, c=GREY)
    notes = ["Plinth: glue P1 and P2 between the two side rails P3 and P4 and pocket-screw them (25 mm, 2 per end at 30 and 85 above the floor, in the inner faces of P1 and P2); check square.",
             "It stands on the floor and carries the carcass. Kb is a cover only: screw on from inside through P1.",
             "Kb runs 53 past the joint end to meet the main run's kickboard; its face is 60 behind the drawer fronts.",
             "P2 sits fully under C3 (d 530 to 545), its rear face level with C3's rear edge; P3 and P4 run 8 mm on under C4 (d to 553).",
             "Carcass to plinth: with the carcass upside down, set the frame on it and pocket-screw from inside the frame, up into C3 (P1: 4 at 100 and 300 either side of the centre line, P2: 4 likewise) and into the bottom edges of the sides (P3, P4: 2 each, 159 and 359 back from the front edge of the benchtop)."]
    sh.ax.text(255, 236 + 0, "", fontsize=1)
    import textwrap
    yy_ = 80.0
    for t in notes:
        for k_, ln in enumerate(textwrap.wrap(t, 105)):
            sh.ax.text(235, yy_, ("" if k_ == 0 else "   ") + ln, fontsize=5.2, va="center")
            yy_ -= 3.6
        yy_ -= 1.2
    if png:
        sh.png(png)
    sh.save()
