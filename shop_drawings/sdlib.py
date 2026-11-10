# Small 2D drafting helpers on top of matplotlib. Paper is A4 landscape (297 x 210); drawing units are A3-grid millimetres (420 x 297), scaled to fit.
import matplotlib
import matplotlib.text
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, Arc

INK = "#111111"
GREY = "#8a8a8a"
LIGHT = "#d9d9d9"
PLY = "#f3e6cf"
STEEL = "#c9d3dc"
RED = "#b3261e"

PW, PH = 420.0, 297.0


class Sheet:
    def __init__(self, pdf, number, title, sub=""):
        self.pdf = pdf
        self.number, self.title, self.sub = number, title, sub
        self.fig = plt.figure(figsize=(297.0 / 25.4, 210.0 / 25.4))   # A4 landscape; drawing coordinates stay on the 420 x 297 grid (scaled 0.707)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, PW); self.ax.set_ylim(0, PH)
        self.ax.set_aspect("equal"); self.ax.axis("off")
        self._wrap_text()
        self.frame()

    def _wrap_text(self):
        """A4: every label is at least 5 pt; a line that would run past the frame is wrapped onto more lines instead of shrunk."""
        import textwrap
        ax = self.ax
        t0, a0 = ax.text, ax.annotate
        MINFS = 5.0
        CW = 0.3528 * 0.56 / 0.707            # grid mm per character per point of font size

        def prep(x, fs, t, ha):
            fs = max(fs, MINFS)
            t = str(t)
            if ha in ("left", "right") and "\n" not in t:
                room = (PW - 10 - x) if ha == "left" else (x - 10)
                n = int(room / (fs * CW)) if room > 5 else 0
                if n > 12 and len(t) > n:
                    t = "\n".join(textwrap.wrap(t, n))
            return fs, t

        def text(x, y, t, *a_, **kw):
            fs = kw.pop("fontsize", 6)
            if kw.get("zorder") == 6 and "bbox" not in kw:
                kw["bbox"] = dict(fc="white", ec="none", pad=0.4, alpha=0.9)
            if kw.get("rotation", 0):
                kw["fontsize"] = max(fs, MINFS)
            else:
                kw["fontsize"], t = prep(x, fs, t, kw.get("ha", "left"))
            return t0(x, y, t, *a_, **kw)

        def annotate(t, xy=None, xytext=None, **kw):
            fs = kw.pop("fontsize", 6)
            kw["fontsize"], t = prep(xytext[0] if xytext else xy[0], fs, t, kw.get("ha", "left"))
            kw.setdefault("bbox", dict(fc="white", ec="none", pad=0.6, alpha=0.9))
            return a0(t, xy=xy, xytext=xytext, **kw)
        ax.text, ax.annotate = text, annotate

    def frame(self):
        a = self.ax
        a.add_patch(Rectangle((8, 8), PW - 16, PH - 16, fill=False, lw=1.0, ec=INK))
        a.add_patch(Rectangle((PW - 8 - 150, 8), 150, 34, fill=False, lw=0.8, ec=INK))
        a.plot([PW - 158, PW - 8], [26, 26], lw=0.5, c=INK)
        a.plot([PW - 58, PW - 58], [8, 26], lw=0.5, c=INK)
        a.text(PW - 154, 36, "KITCHEN BENCH EXTENSION  -  EXTENSION UNIT", fontsize=7.5, weight="bold", va="center")
        a.text(PW - 154, 30.3, self.title, fontsize=7, va="center")
        import textwrap as _t
        sub = "\n".join(_t.wrap(self.sub or "All dimensions in mm", 52))
        a.text(PW - 154, 21.0, sub, fontsize=5.5, va="center", color="#333", linespacing=1.0)
        a.text(PW - 154, 11.5, "15 mm ply unless noted. Do not scale: dimensions govern.", fontsize=5, va="center", color="#333")
        a.text(PW - 54, 21.5, "SHEET", fontsize=5, va="center", color="#333")
        a.text(PW - 54, 13.0, str(self.number), fontsize=13, weight="bold", va="center")
        a.text(PW - 30, 21.5, "DATE", fontsize=5, va="center", color="#333")
        a.text(PW - 30, 14.5, "2026-11-07", fontsize=6, va="center")

    def _declutter(self, rounds=40, cap=14.0):
        """Nudge overlapping labels apart by at most `cap` grid mm (leader texts first), along the axis that needs the smaller move."""
        import itertools
        fig = self.fig
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        inv = self.ax.transData.inverted()
        texts = [t for t in self.ax.texts if t.get_text().strip()]
        home = {id(t): t.get_position() for t in texts}
        for _ in range(rounds):
            moved = False
            boxes = [matplotlib.text.Text.get_window_extent(t, r) for t in texts]
            for (i, a), (j, b) in itertools.combinations(enumerate(texts), 2):
                ba, bb = boxes[i], boxes[j]
                ix = min(ba.x1, bb.x1) - max(ba.x0, bb.x0)
                iy = min(ba.y1, bb.y1) - max(ba.y0, bb.y0)
                if ix <= 0.5 or iy <= 0.5:
                    continue
                A = matplotlib.text.Annotation
                if isinstance(a, A) and not isinstance(b, A):
                    mover, bm, bo = a, ba, bb
                else:
                    mover, bm, bo = b, bb, ba
                if mover.get_rotation() == 0 and ix < iy + 6:
                    dx = (ix + 2.0) * (1 if (bm.x0 + bm.x1) >= (bo.x0 + bo.x1) else -1); dy = 0.0
                else:
                    dx = 0.0; dy = (iy + 2.0) * (1 if (bm.y0 + bm.y1) >= (bo.y0 + bo.y1) else -1)
                x0, y0 = self.ax.transData.transform(mover.get_position())
                nx, ny = inv.transform((x0 + dx, y0 + dy))
                hx, hy = home[id(mover)]
                if abs(nx - hx) > cap or abs(ny - hy) > cap:
                    continue
                mover.set_position((nx, ny))
                moved = True
                boxes[texts.index(mover)] = matplotlib.text.Text.get_window_extent(mover, r)
            if not moved:
                break

    def save(self):
        self._declutter()
        self.pdf.savefig(self.fig)
        plt.close(self.fig)

    def png(self, path, dpi=100):
        self.fig.savefig(path, dpi=dpi)


class View:
    """Model coordinates (u, v) in mm -> paper at scale s, origin (ox, oy)."""

    def __init__(self, sheet, ox, oy, s):
        self.sh, self.ax, self.ox, self.oy, self.s = sheet, sheet.ax, ox, oy, s

    def P(self, u, v):
        return (self.ox + self.s * u, self.oy + self.s * v)

    def rect(self, u0, v0, u1, v1, fc="none", ec=INK, lw=0.6, hatch=None, ls="-", z=2):
        x0, y0 = self.P(min(u0, u1), min(v0, v1))
        w, h = abs(u1 - u0) * self.s, abs(v1 - v0) * self.s
        r = Rectangle((x0, y0), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z)
        if hatch:
            r.set_hatch(hatch)
        self.ax.add_patch(r)

    def poly(self, pts, fc="none", ec=INK, lw=0.6, ls="-", z=2, closed=True):
        self.ax.add_patch(Polygon([self.P(*p) for p in pts], closed=closed, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))

    def line(self, u0, v0, u1, v1, lw=0.5, ls="-", c=INK, z=3):
        a, b = self.P(u0, v0), self.P(u1, v1)
        self.ax.plot([a[0], b[0]], [a[1], b[1]], lw=lw, ls=ls, c=c, zorder=z, solid_capstyle="butt")

    def center_h(self, u0, u1, v):
        self.line(u0, v, u1, v, lw=0.3, ls=(0, (8, 2, 1, 2)), c=GREY)

    def center_v(self, v0, v1, u):
        self.line(u, v0, u, v1, lw=0.3, ls=(0, (8, 2, 1, 2)), c=GREY)

    def circ(self, u, v, r, fc="none", ec=INK, lw=0.5, z=3):
        x, y = self.P(u, v)
        self.ax.add_patch(Circle((x, y), r * self.s, fc=fc, ec=ec, lw=lw, zorder=z))

    def txt(self, u, v, t, size=5.5, ha="center", va="center", rot=0, c=INK, weight="normal", bg=False):
        x, y = self.P(u, v)
        kw = dict(bbox=dict(fc="white", ec="none", pad=0.4)) if bg else {}
        self.ax.text(x, y, t, fontsize=size, ha=ha, va=va, rotation=rot, color=c, weight=weight, zorder=6, **kw)

    def ptxt(self, du, dv, u, v, t, **kw):   # text offset in paper mm from a model point
        x, y = self.P(u, v)
        self.ax.text(x + du, y + dv, t, zorder=6, **{**dict(fontsize=5.5, ha="center", va="center"), **kw})

    def _arrow(self, p0, p1):
        self.ax.annotate("", xy=p1, xytext=p0, zorder=5,
                         arrowprops=dict(arrowstyle="<|-|>", lw=0.35, color=INK, mutation_scale=3.5, shrinkA=0, shrinkB=0))

    def dim_h(self, u0, u1, v, off, t=None, size=5.5, ext=2.0, inside=False):
        """Horizontal dimension: dimension line at paper offset `off` (mm) above (+) or below (-) model v."""
        t = t if t is not None else fmt(abs(u1 - u0))
        x0, y = self.P(u0, v); x1, _ = self.P(u1, v)
        yd = y + off
        sg = 1 if off >= 0 else -1
        self.ax.plot([x0, x0], [y + sg * 0.8, yd + sg * ext], lw=0.3, c=INK, zorder=4)
        self.ax.plot([x1, x1], [y + sg * 0.8, yd + sg * ext], lw=0.3, c=INK, zorder=4)
        self._arrow((x0, yd), (x1, yd))
        self.ax.text((x0 + x1) / 2, yd + sg * 1.5, t, fontsize=size, ha="center", va="bottom" if sg > 0 else "top", zorder=6)

    def dim_v(self, v0, v1, u, off, t=None, size=5.5, ext=2.0):
        t = t if t is not None else fmt(abs(v1 - v0))
        x, y0 = self.P(u, v0); _, y1 = self.P(u, v1)
        xd = x + off
        sg = 1 if off >= 0 else -1
        self.ax.plot([x + sg * 0.8, xd + sg * ext], [y0, y0], lw=0.3, c=INK, zorder=4)
        self.ax.plot([x + sg * 0.8, xd + sg * ext], [y1, y1], lw=0.3, c=INK, zorder=4)
        self._arrow((xd, y0), (xd, y1))
        self.ax.text(xd - sg * 1.2, (y0 + y1) / 2, t, fontsize=size, ha="right" if sg > 0 else "left", va="center",
                     rotation=90, zorder=6, rotation_mode="anchor")

    def chain_v(self, vals, u, off, labels=None, size=5.2, ext=2.0):
        """Continuous vertical dimension chain through the model heights `vals` (ascending), line at paper offset `off`."""
        x, _ = self.P(u, vals[0])
        xd = x + off
        sg = 1 if off >= 0 else -1
        ys = [self.P(u, v)[1] for v in vals]
        for y in ys:
            self.ax.plot([x + sg * 0.8, xd + sg * ext], [y, y], lw=0.3, c=INK, zorder=4)
        for i in range(len(vals) - 1):
            self._arrow((xd, ys[i]), (xd, ys[i + 1]))
            t = labels[i] if labels else fmt(vals[i + 1] - vals[i])
            if not t:
                continue
            seg = abs(ys[i + 1] - ys[i])
            ym = (ys[i] + ys[i + 1]) / 2
            if seg >= 7:
                self.ax.text(xd - sg * 1.2, ym, t, fontsize=size, ha="right" if sg > 0 else "left", va="center", rotation=90,
                             rotation_mode="anchor", zorder=6)
            else:
                self.ax.text(xd + sg * 1.6, ym, t, fontsize=size - 0.4, ha="left" if sg > 0 else "right", va="center", zorder=6)

    def leader(self, u, v, du, dv, t, size=5.2, ha="left"):
        x, y = self.P(u, v)
        self.ax.annotate(t, xy=(x, y), xytext=(x + du, y + dv), fontsize=size, ha=ha, va="center", zorder=6,
                         arrowprops=dict(arrowstyle="-|>", lw=0.35, color=INK, mutation_scale=3.5))

    def title(self, u, v, t, scale):
        x, y = self.P(u, v)
        self.ax.text(x, y + 4.0, t, fontsize=7.5, weight="bold", ha="left", va="center")
        self.ax.text(x, y - 0.2, scale, fontsize=5.5, ha="left", va="center", color="#333")

    def note(self, u, v, lines, size=5.2, lead=3.6):
        x, y = self.P(u, v)
        for i, l in enumerate(lines):
            self.ax.text(x, y - i * lead, l, fontsize=size, ha="left", va="top", zorder=6)


def fmt(x):
    r = round(x, 2)
    return ("%d" % r) if abs(r - round(r)) < 1e-9 else ("%g" % r)


def stack(ax, x, y, items, fs=5.4, width=100, gap=1.2, lead=None, weight="normal", indent=0.0):
    """Draw wrapped paragraphs one under another (top at y, going down). Returns the y below the last line."""
    import textwrap
    lead = lead or fs * 0.3528 * 1.55 / 0.707
    for t in items:
        for k, ln in enumerate(textwrap.wrap(t, width)):
            ax.text(x + (indent if k else 0), y, ln, fontsize=fs, va="top", weight=weight)
            y -= lead
        y -= gap
    return y
