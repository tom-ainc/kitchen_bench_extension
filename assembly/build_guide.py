"""Build assembly_guide.pdf and ASSEMBLY_GUIDE.md from content.py. Run: python3 -I build_guide.py"""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C  # noqa: E402

PW, PH = 210.0, 297.0           # A4 portrait, mm
ML, MR, MT, MB = 18.0, 18.0, 20.0, 18.0
TW = PW - ML - MR
INK, GREY, ACC = "#1b1b1b", "#666666", "#8a5a14"
PT = 25.4 / 72.0                # mm per point


class Doc:
    def __init__(self, pdf):
        self.pdf = pdf
        self.n = 0
        self.fig = self.ax = None
        self.y = 0.0
        self.new_page()

    def new_page(self):
        if self.fig is not None:
            self.close()
        self.n += 1
        self.fig = plt.figure(figsize=(PW / 25.4, PH / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, PW)
        self.ax.set_ylim(PH, 0)       # y grows downward
        self.ax.axis("off")
        self.ax.plot([ML, PW - MR], [PH - MB + 3, PH - MB + 3], lw=0.4, c=INK)
        self.ax.text(ML, PH - MB + 7, "Kitchen bench extension: assembly guide", fontsize=6, c=GREY, va="center")
        self.ax.text(PW - MR, PH - MB + 7, f"Page {self.n}", fontsize=6, c=GREY, va="center", ha="right")
        self.y = MT

    def close(self):
        self.pdf.savefig(self.fig)
        plt.close(self.fig)
        self.fig = None

    def room(self, h):
        if self.y + h > PH - MB:
            self.new_page()

    def text(self, x, s, size, weight="normal", color=INK, ha="left"):
        self.ax.text(x, self.y, s, fontsize=size, weight=weight, color=color, va="top", ha=ha)

    def lines(self, s, size, width_mm, x, weight="normal", lead=1.45, color=INK):
        cw = size * PT * 0.52               # average character width in mm
        cols = max(10, int(width_mm / cw))
        out = []
        for para in s.split("\n"):
            out += textwrap.wrap(para, cols) or [""]
        return out

    def para(self, s, size=8.6, x=None, width=None, weight="normal", color=INK, gap=2.0):
        x = ML if x is None else x
        width = TW if width is None else width
        ls = self.lines(s, size, width, x)
        lh = size * PT * 1.45
        for l in ls:
            self.room(lh)
            self.text(x, l, size, weight, color)
            self.y += lh
        self.y += gap

    def h1(self, s):
        self.room(18)
        self.y += 3
        self.text(ML, s, 12, "bold", ACC)
        self.y += 6.2
        self.ax.plot([ML, PW - MR], [self.y, self.y], lw=0.5, c=ACC)
        self.y += 2.8

    def h2(self, s):
        self.room(12)
        self.text(ML, s, 9.2, "bold")
        self.y += 5.2

    def bullets(self, items, size=8.6):
        for it in items:
            ls = self.lines(it, size, TW - 6, ML + 6)
            lh = size * PT * 1.45
            self.room(lh * len(ls) + 1)
            self.text(ML + 1.5, "•", size)
            for l in ls:
                self.text(ML + 6, l, size)
                self.y += lh
            self.y += 1.0
        self.y += 1.0

    def steps(self, items, size=8.6):
        for i, it in enumerate(items, 1):
            ls = self.lines(it, size, TW - 8, ML + 8)
            lh = size * PT * 1.45
            self.room(lh * len(ls) + 1)
            self.text(ML + 0.5, f"{i}.", size, "bold")
            for l in ls:
                self.text(ML + 8, l, size)
                self.y += lh
            self.y += 1.4
        self.y += 1.0

    def table(self, head, rows, widths, size=7.8):
        tot = sum(widths)
        widths = [w * TW / tot for w in widths]
        xs = [ML]
        for w in widths:
            xs.append(xs[-1] + w)
        lh = size * PT * 1.4

        def row(cells, bold=False):
            wrapped = [self.lines(c, size, widths[j] - 3, xs[j]) for j, c in enumerate(cells)]
            h = lh * max(len(w) for w in wrapped) + 2.2
            self.room(h + 1)
            for j, w in enumerate(wrapped):
                yy = self.y + 1.0
                for l in w:
                    self.ax.text(xs[j] + 1.5, yy, l, fontsize=size, weight="bold" if bold else "normal", va="top")
                    yy += lh
            self.y += h
            self.ax.plot([ML, xs[-1]], [self.y, self.y], lw=0.7 if bold else 0.25, c=INK)

        self.room(12)
        self.ax.plot([ML, xs[-1]], [self.y, self.y], lw=0.7, c=INK)
        row(head, True)
        for r in rows:
            row(r)
        self.y += 3.0

    def note(self, label, s, size=8.2):
        ls = self.lines(s, size, TW - 8, ML + 4)
        lh = size * PT * 1.45
        h = lh * len(ls) + 9
        self.room(h + 2)
        self.ax.add_patch(Rectangle((ML, self.y), TW, h, fc="#f6efe0", ec=ACC, lw=0.6))
        self.ax.text(ML + 3, self.y + 2.2, label, fontsize=7.4, weight="bold", color=ACC, va="top")
        yy = self.y + 6.4
        for l in ls:
            self.ax.text(ML + 3, yy, l, fontsize=size, va="top")
            yy += lh
        self.y += h + 3

    def img(self, path, caption, width=150.0):
        im = mpimg.imread(os.path.join(HERE, path))
        h = width * im.shape[0] / im.shape[1]
        self.room(h + 9)
        x = ML + (TW - width) / 2
        self.ax.imshow(im, extent=(x, x + width, self.y + h, self.y), aspect="auto", zorder=1)
        self.ax.set_xlim(0, PW)
        self.ax.set_ylim(PH, 0)
        self.y += h + 1.5
        self.ax.text(PW / 2, self.y, caption, fontsize=7, color=GREY, va="top", ha="center", style="italic")
        self.y += 6.5


import steps_content as SC  # noqa: E402


def draw_cover(d):
    d.y += 10
    d.text(ML, C.TITLE, 17, "bold")
    d.y += 10
    d.para(C.SUBTITLE, 9.4, color=GREY, gap=6)
    d.img("img/s_final.png", "The finished unit (benchtop extension, three drawers, kickboard)", width=170)
    d.y += 4
    d.h2("How to read the pictures")
    d.bullets(["Solid parts are the ones you add in that step. See-through parts are already built.",
               "Parts are shown pulled apart along the direction they move in. Nothing is drawn to a scale you can measure: use the dimensions in the text boxes and the shop drawings.",
               "Part references (C1 to C4, C9, P1 to P4, Kb, D1 to D3) are those on sheet 1 of the shop drawings. Dimensions are in millimetres.",
               "The written guide that follows the pictures has the full routing, drilling and checking details, and the open points."])
    d.note("BEFORE YOU START", "Not yet proven by building. Make and test the mitre and the cove on an offcut (step 7), and build drawer 1 (step 6) first, before you cut the pulls on all the fronts. "
           "Measure your own plywood and the real Alto parts against the model (written guide, section 2).")


def draw_step(d, st):
    d.new_page()
    ax = d.ax
    # step number badge
    ax.add_patch(Rectangle((ML, MT - 4), 20, 20, fc=INK, ec=INK))
    ax.text(ML + 10, MT + 6, str(st["n"]), fontsize=26, weight="bold", color="white", ha="center", va="center")
    ax.text(ML + 26, MT + 6, st["title"], fontsize=15, weight="bold", va="center")
    d.y = MT + 22
    imgs = st["images"]
    if len(imgs) == 1:
        d.img(imgs[0][0], imgs[0][1], width=TW) if imgs[0][1] else d.img(imgs[0][0], "", width=TW)
        d.y -= 4
    else:
        w = (TW - 4 * (len(imgs) - 1)) / len(imgs) if len(imgs) > 2 else (TW - 6) / 2
        top = d.y
        hmax = 0
        for i, (p, cap) in enumerate(imgs):
            im = mpimg.imread(os.path.join(HERE, p))
            h = w * im.shape[0] / im.shape[1]
            x = ML + i * (w + (6 if len(imgs) == 2 else 4))
            if len(imgs) == 3 or (st["n"] == 9 and i == 1):
                pass
            ax.imshow(im, extent=(x, x + w, top + h, top), aspect="auto", zorder=1)
            ax.text(x + w / 2, top + h + 1.5, cap, fontsize=7, color=GREY, va="top", ha="center", style="italic")
            hmax = max(hmax, h)
        ax.set_xlim(0, PW)
        ax.set_ylim(PH, 0)
        d.y = top + hmax + 8
    # parts column (left) and instructions (right)
    y0 = d.y
    ax.text(ML, y0, "PARTS", fontsize=7.5, weight="bold", color=ACC, va="top")
    yy = y0 + 5.5
    for q, t in st["parts"]:
        ax.add_patch(Rectangle((ML, yy - 1), 62, 7.6, fc="#f6efe0", ec=ACC, lw=0.5))
        ax.text(ML + 2, yy + 2.8, q, fontsize=11, weight="bold", va="center")
        for k, l in enumerate(d.lines(t, 7.4, 46, ML + 14)[:2]):
            ax.text(ML + 13, yy + 1.6 + k * 3.0, l, fontsize=7.2, va="center")
        yy += 9.2
    if "heights" in st:
        ax.text(ML, yy + 1, "DRAWBAR PLATE TOP ABOVE C3", fontsize=6.8, weight="bold", color=ACC, va="top")
        yy += 5.5
        for j, (k, v) in enumerate(st["heights"]):
            ax.text(ML + 2 + j * 20, yy + 3, f"{k}  {v}", fontsize=8.5, weight="bold", va="center")
        yy += 8
    ax.text(ML + 70, y0, "DO", fontsize=7.5, weight="bold", color=ACC, va="top")
    ty = y0 + 5.5
    for i, t in enumerate(st["do"], 1):
        ls = d.lines(t, 8.2, TW - 70 - 6, ML + 76)
        ax.text(ML + 70, ty, f"{i}.", fontsize=8.2, weight="bold", va="top")
        for l in ls:
            ax.text(ML + 76, ty, l, fontsize=8.2, va="top")
            ty += 8.2 * PT * 1.45
        ty += 1.6
    y1 = max(yy, ty) + 2
    for label, key in (("CHECK", "check"), ("WARNING", "warn")):
        if key in st:
            ls = d.lines(st[key], 8.0, TW - 28, ML + 24)
            h = 8.0 * PT * 1.45 * len(ls) + 4
            ax.add_patch(Rectangle((ML, y1), TW, h, fc="#f6efe0" if key == "check" else "#fbe4df", ec=ACC if key == "check" else "#b03a2e", lw=0.6))
            ax.text(ML + 3, y1 + h / 2, label, fontsize=7.4, weight="bold", color=ACC if key == "check" else "#b03a2e", va="center")
            for k, l in enumerate(ls):
                ax.text(ML + 24, y1 + 2 + k * 8.0 * PT * 1.45, l, fontsize=8.0, va="top")
            y1 += h + 2


def build_pdf(path):
    with PdfPages(path) as pdf:
        d = Doc(pdf)
        draw_cover(d)
        for st in SC.STEPS:
            draw_step(d, st)
        d.new_page()
        d.y += 6
        d.text(ML, "WRITTEN GUIDE: DETAILS, DIMENSIONS AND CHECKS", 14, "bold")
        d.y += 9
        d.para(C.SUBTITLE, 9.2, color=GREY, gap=3.5)
        for i, b in enumerate(C.B):
            k = b[0]
            if k == "h1":
                if i + 1 < len(C.B) and C.B[i + 1][0] == "img":
                    d.room(140)       # keep a heading with the picture that follows it
                d.h1(b[1])
            elif k == "h2":
                d.h2(b[1])
            elif k == "p":
                d.para(b[1])
            elif k == "steps":
                d.steps(b[1])
            elif k == "bul":
                d.bullets(b[1])
            elif k == "table":
                d.table(b[1], b[2], b[3])
            elif k == "img":
                d.img(b[1], b[2])
            elif k == "note":
                d.note(b[1], b[2])
        d.close()


def build_md(path):
    o = [f"# {C.TITLE.title()}", "", f"_{C.SUBTITLE}_", "", "![The finished unit](img/s_final.png)", "",
         "Solid parts are added in that step; see-through parts are already built. Dashed lines show where each fastener goes.", ""]
    for st in SC.STEPS:
        o += [f"## Step {st['n']}: {st['title']}", ""]
        o += [f"![{c or st['title']}]({p})" for p, c in st["images"]] + [""]
        o += ["**Parts:** " + "; ".join(f"{q} {t}" for q, t in st["parts"]), ""]
        if "heights" in st:
            o += ["**Drawbar plate top above C3:** " + ", ".join(f"{k} {v}" for k, v in st["heights"]), ""]
        o += [f"{i}. {t}" for i, t in enumerate(st["do"], 1)] + [""]
        if "check" in st:
            o += [f"> **Check.** {st['check']}", ""]
        if "warn" in st:
            o += [f"> **Warning.** {st['warn']}", ""]
    o += ["---", "", "# Written guide: details, dimensions and checks", ""]
    for b in C.B:
        k = b[0]
        if k == "h1":
            o += [f"## {b[1]}", ""]
        elif k == "h2":
            o += [f"### {b[1]}", ""]
        elif k == "p":
            o += [b[1], ""]
        elif k == "steps":
            o += [f"{i}. {s}" for i, s in enumerate(b[1], 1)] + [""]
        elif k == "bul":
            o += [f"- {s}" for s in b[1]] + [""]
        elif k == "table":
            o += ["| " + " | ".join(b[1]) + " |", "|" + "---|" * len(b[1])]
            o += ["| " + " | ".join(r) + " |" for r in b[2]] + [""]
        elif k == "img":
            o += [f"![{b[2]}]({b[1]})", f"*{b[2]}*", ""]
        elif k == "note":
            o += [f"> **{b[1]}.** {b[2]}", ""]
    open(path, "w").write("\n".join(o))


if __name__ == "__main__":
    build_pdf(os.path.join(HERE, "extension_unit_assembly_guide.pdf"))
    build_md(os.path.join(HERE, "ASSEMBLY_GUIDE.md"))
    print("wrote guide")
