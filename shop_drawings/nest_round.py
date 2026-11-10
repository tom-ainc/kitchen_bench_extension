"""Cutting layout where every cut made at the store (panel saw) lands on a multiple of 100 mm.
Parts are grouped into rough BLANKS whose sizes are multiples of 100 (stack of parts + home kerfs, rounded up);
blanks are packed in strips: stage 1 = rip strips across the sheet, stage 2 = cross-cut blanks off each strip.
The user trims each blank to the final parts at home.  Run directly to print a summary."""
import itertools
import math
import random

SW, SH, K = 2400.0, 1200.0, 3.0   # sheet length (grain), width, home saw kerf
R = 100.0


def up(v):
    return math.ceil(v / R - 1e-9) * R


def part_list():
    P = []

    def add(lbl, w, h, q=1, rot=False):
        for i in range(q):
            P.append(dict(n=lbl if q == 1 else "%s%d" % (lbl, i + 1), w=w, h=h, rot=rot))
    add("C1", 749, 522); add("C2", 749, 522); add("C3", 775, 507); add("C4", 775, 749); add("C9", 775, 60)
    add("P1", 767, 125); add("P2", 767, 125); add("P3", 461, 125); add("P4", 461, 125); add("Kb", 852, 115, rot=False)
    add("D1F", 802, 212.7, rot=False); add("D2F", 802, 212.7, rot=False); add("D3F", 802, 326.3, rot=False); add("TS", 802, 32.3, rot=False)
    add("D1sL", 495, 153); add("D1sR", 495, 153); add("D2sL", 495, 153); add("D2sR", 495, 153)
    add("D3sL", 495, 231); add("D3sR", 495, 231)
    add("D1bk", 713, 148); add("D2bk", 713, 148); add("D3bk", 713, 226)
    for n in ("D1", "D2", "D3"):
        add(n + "base", 728.5, 487.5)
    return P


def make_block(parts, axis, flip, exact=False):
    """parts: list of part dicts (oriented as w along the sheet length unless flipped). axis 0 = stack along length (x), 1 = along width (y).
    returns block dict with rough size (multiples of 100) and parts placed inside it."""
    placed = []
    x = y = 0.0
    bw = bh = 0.0
    for p, rotated in parts:
        w, h = (p["h"], p["w"]) if rotated else (p["w"], p["h"])
        placed.append((p["n"], x, y, w, h, rotated))
        if axis == 0:
            x += w + K
            bw = x - K
            bh = max(bh, h)
        else:
            y += h + K
            bh = y - K
            bw = max(bw, w)
    locked = any(not p["rot"] for p, _ in parts)
    return dict(w=(bw if exact else up(bw)), h=(bh if exact else up(bh)), exact_w=bw, exact_h=bh, parts=placed, locked=locked, exact=exact,
                names=[p["n"] for p, _ in parts])


def pack_strips(blocks, rng, max_sheets=2):
    """blocks: list of dicts (w along length, h across). returns sheets (list of strips) or None if more than 2 sheets needed."""
    items = []
    for b in blocks:
        opts = [(b["w"], b["h"], False)]
        if not b["locked"] and b["w"] != b["h"]:
            opts.append((b["h"], b["w"], True))
        items.append((b, opts))
    rng.shuffle(items)
    # choose orientation: prefer the one with the longer side along the sheet length
    chosen = []
    for b, opts in items:
        o = max(opts, key=lambda t: t[0]) if rng.random() < 0.7 else rng.choice(opts)
        if o[1] > SH or o[0] > SW:
            o = [t for t in opts if t[1] <= SH and t[0] <= SW]
            if not o:
                return None
            o = o[0]
        chosen.append((b, o))
    chosen.sort(key=lambda t: (-t[1][1], -t[1][0]))
    sheets = [[]]
    for b, (w, h, rot) in chosen:
        placed = False
        for sheet in sheets:
            # try an existing strip with enough height and length
            for strip in sheet:
                if h <= strip["h"] and strip["used"] + w <= SW:
                    strip["blocks"].append((b, w, h, rot)); strip["used"] += w; placed = True; break
            if placed:
                break
            ysum = sum(s["h"] for s in sheet)
            if ysum + h <= SH:
                sheet.append(dict(h=h, used=w, blocks=[(b, w, h, rot)])); placed = True; break
        if not placed:
            if len(sheets) >= max_sheets:
                return None
            sheets.append([dict(h=h, used=w, blocks=[(b, w, h, rot)])])
    return sheets


def waste(sheets):
    return sum(SW * SH - sum(s["h"] * s["used"] for s in sh) for sh in sheets)


def search(seed=11, iters=60000, max_sheets=2, pexact=0.0, tol=60, pm=0.35, maxn=(2, 3, 4)):
    rng = random.Random(seed)
    parts = part_list()
    best = None
    names = [p["n"] for p in parts]
    byname = {p["n"]: p for p in parts}
    for it in range(iters):
        # random partition into blocks: shuffle, then merge neighbours of similar size
        order = parts[:]
        rng.shuffle(order)
        blocks = []
        used = set()
        for p in order:
            if p["n"] in used:
                continue
            members = [p]
            used.add(p["n"])
            for q in order:
                if q["n"] in used or rng.random() > pm:
                    continue
                # only merge parts with similar cross dimension, to share rounding
                if abs(q["h"] - p["h"]) <= tol or abs(q["w"] - p["w"]) <= tol:
                    members.append(q); used.add(q["n"])
                    if len(members) >= rng.choice(maxn):
                        break
            # orient and stack
            if len(members) == 1:
                rot = rng.random() < 0.0
                blocks.append(make_block([(p, False)], 0, False, exact=rng.random() < pexact))
            else:
                ax = rng.choice((0, 1))
                # keep long sides aligned: stack along the short side of the first part
                ms = []
                for m in members:
                    ms.append((m, False))
                ex = rng.random() < pexact
                blocks.append(make_block(ms, 1, False, ex) if ax else make_block(ms, 0, False, ex))
        sheets = pack_strips(blocks, rng, max_sheets)
        if sheets is None:
            continue
        inner = sum(len(b["parts"]) - 1 for b in blocks)      # extra cuts at home to separate stacked parts
        nonround = sum(1 for sh in sheets for st in sh if st['h'] % R) + sum(1 for sh in sheets for st in sh for (bb, w, h, r) in st['blocks'] if w % R)
        third = sum(st['h'] * st['used'] for st in sheets[2]) if len(sheets) > 2 else 0
        score = (len(sheets), nonround, third, inner, waste(sheets))
        if best is None or score < best[0]:
            best = (score, sheets, blocks)
    return best


if __name__ == "__main__":
    b = search(iters=40000, max_sheets=3, tol=150, pm=0.5, maxn=(2, 3, 4))
    print(b[0] if b else None)
    import json
    out = []
    for sh in b[1]:
        out.append([dict(h=st["h"], used=st["used"], blocks=[dict(w=w, h=h, rot=rot, parts=bb["parts"], names=bb["names"]) for (bb, w, h, rot) in st["blocks"]]) for st in sh])
    json.dump(out, open("round_layout.json", "w"))
