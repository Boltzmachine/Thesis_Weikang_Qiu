# -*- coding: utf-8 -*-
"""Two card figures for the 'What Brain Signals Look Like' preliminary slide.

  eeg_format.svg   channels x time  (EEG / MEG / ECoG)
  fmri_format.svg  voxels   x time  (fMRI)

Both are drawn on a 408 x 228 pt canvas = the figure area inside a deck card.
"""
import math

W, H = 408.0, 272.0
SMALL, BIG = 13.0, 15.0          # in-figure label sizes (points on the slide)
BLUE, NAVY, ORANGE = "#4472C4", "#00356B", "#C2650B"
BODY, MUTED, HAIR = "#333F4F", "#7A8595", "#D9DEE7"
BLUE_TINT, ORANGE_TINT = "#EAF1FB", "#FBEFE3"
FONT = "Calibri, 'Helvetica Neue', Helvetica, Arial, sans-serif"


def head(s, W, H):
    s.insert(0, f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*3:.0f}" height="{H*3:.0f}" '
                f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="{FONT}">'
                f'<rect width="{W}" height="{H}" fill="#F5F8FC"/>')
    s.append('</svg>')
    return "\n".join(s)


def arrow(x1, y1, x2, y2, col, w=1.6, head_len=6.0, head_w=4.6):
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head_len * math.cos(a), y2 - head_len * math.sin(a)
    px, py = -math.sin(a) * head_w / 2, math.cos(a) * head_w / 2
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M {x2:.1f} {y2:.1f} L {bx+px:.1f} {by+py:.1f} L {bx-px:.1f} {by-py:.1f} Z" fill="{col}"/>')


def txt(x, y, t, size=9.5, col=BODY, anchor="start", bold=False, extra=""):
    b = ' font-weight="bold"' if bold else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" '
            f'text-anchor="{anchor}"{b}{extra}>{t}</text>')


# ───────────────────────────── EEG · channels × time ─────────────────────────────
def eeg():
    s = []
    A = s.append

    # ---- top-view head with electrodes -------------------------------------
    hx, hy, r = 52.0, 112.0, 42.0
    A(f'<path d="M {hx-7:.1f} {hy-r+2:.1f} L {hx:.1f} {hy-r-11:.1f} L {hx+7:.1f} {hy-r+2:.1f} Z" '
      f'fill="{BLUE_TINT}" stroke="{BLUE}" stroke-width="2" stroke-linejoin="round"/>')
    for sx in (-1, 1):
        A(f'<ellipse cx="{hx+sx*(r+3):.1f}" cy="{hy-4:.1f}" rx="5" ry="9" fill="{BLUE_TINT}" '
          f'stroke="{BLUE}" stroke-width="2"/>')
    A(f'<circle cx="{hx}" cy="{hy}" r="{r}" fill="{BLUE_TINT}" stroke="{BLUE}" stroke-width="2.2"/>')

    dots = [(0.0, 0.0)]
    for k in range(6):
        ang = math.pi / 2 + k * math.pi / 3
        dots.append((0.5 * math.cos(ang), 0.5 * math.sin(ang)))
    for k in range(10):
        ang = math.pi / 2 + k * 2 * math.pi / 10
        dots.append((0.84 * math.cos(ang), 0.84 * math.sin(ang)))
    # highlight three electrodes on the side the traces come out of
    picks = []
    hi = sorted((i for i, (u, v) in enumerate(dots) if u < 0.72),
                key=lambda i: (-dots[i][0], dots[i][1]))[:3]
    for i, (u, v) in enumerate(dots):
        cx, cy = hx + u * r, hy - v * r
        if i in hi:
            picks.append((cx, cy))
            A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.4" fill="{NAVY}" stroke="#FFFFFF" stroke-width="1.4"/>')
        else:
            A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.4" fill="#FFFFFF" stroke="{BLUE}" stroke-width="1.4"/>')
    A(txt(hx, hy + r + 26, '64 electrodes', SMALL, BODY, "middle"))

    # ---- traces -------------------------------------------------------------
    x0, x1 = 172.0, 396.0
    rows = [("ch 1", 46.0), ("ch 2", 88.0), ("ch 3", 130.0), (None, 162.0), ("ch 64", 194.0)]
    picks.sort(key=lambda p: p[1])

    def wave(seed, y, amp=14.0):
        pts = []
        n = 260
        for i in range(n + 1):
            t = i / n
            x = x0 + t * (x1 - x0)
            v = (math.sin(2 * math.pi * (3.1 + seed * 0.7) * t + seed) * 0.55
                 + math.sin(2 * math.pi * (7.3 + seed) * t + seed * 2.1) * 0.3
                 + math.sin(2 * math.pi * (17.0 + seed * 3) * t + seed * 0.6) * 0.13
                 + math.sin(2 * math.pi * (41.0 + seed * 5) * t + seed * 1.7) * 0.06)
            pts.append((x, y - v * amp))
        return pts

    lead = 0
    for i, (lab, y) in enumerate(rows):
        if lab is None:                                # the "more channels" gap
            for k in range(3):
                A(f'<circle cx="{x0 - 26:.1f}" cy="{y - 8 + k*8:.1f}" r="1.3" fill="{MUTED}"/>')
            continue
        col = NAVY if i < 3 else "#8FA8C8"
        pts = wave(i + 1, y)
        d = "M " + " L ".join(f"{px:.2f} {py:.2f}" for px, py in pts)
        A(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.3" stroke-linejoin="round"/>')
        A(txt(x0 - 14, y + 4.6, lab, SMALL, BODY, "end"))
        if i < 3:                                      # leader from its electrode
            ex, ey = picks[lead]; lead += 1
            A(f'<path d="M {ex+5:.1f} {ey:.1f} C {ex+34:.1f} {ey:.1f} {x0-92:.1f} {y:.1f} {x0-58:.1f} {y:.1f}" '
              f'fill="none" stroke="{BLUE}" stroke-width="0.9" stroke-dasharray="3 3"/>')

    # one sample = one number
    sx, sy = wave(2, 88.0)[200]
    A(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3.6" fill="{ORANGE}" stroke="#FFFFFF" stroke-width="1.2"/>')
    A(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{sx:.1f}" y2="28" stroke="{ORANGE}" stroke-width="0.9" '
      f'stroke-dasharray="3 3"/>')
    A(txt(sx - 8, 24, 'one number: µV at one instant', SMALL, ORANGE, "end"))

    # ---- time axis ----------------------------------------------------------
    ay = 222.0
    A(arrow(x0, ay, x1 + 6, ay, MUTED, 1.3))
    for k in range(4):
        tx = x0 + k * (x1 - x0) / 3
        A(f'<line x1="{tx:.1f}" y1="{ay-3.5:.1f}" x2="{tx:.1f}" y2="{ay+3.5:.1f}" stroke="{MUTED}" stroke-width="1.3"/>')
        A(txt(tx, ay + 19, f'{k} s', 12, MUTED, "middle"))
    A(txt((x0 + x1) / 2, 264, '1 000 samples per second', BIG, NAVY, "middle", True))
    return head(s, W, H)


# ───────────────────────────── fMRI · voxels × time ──────────────────────────────
def slice_path(cx, cy, w, h):
    """One axial brain outline: a slightly pinched ellipse."""
    a, b = w / 2, h / 2
    p = []
    n = 72
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        rr = (1 + 0.05 * math.cos(2 * t) - 0.10 * math.cos(t)
              - 0.09 * math.exp(-((math.sin(t / 2)) ** 2) * 90)
              - 0.07 * math.exp(-((math.cos(t / 2)) ** 2) * 90))
        p.append((cx + a * rr * math.sin(t), cy - b * rr * math.cos(t)))
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in p) + " Z"


def volume(A, cx, cy, w, h, grid=False, hi_voxel=None):
    """A stack of axial slices = one fMRI volume."""
    for k in (3, 2, 1, 0):
        off = k * 5.0
        fill = ORANGE_TINT if k == 0 else "#FDF6EE"
        A(f'<path d="{slice_path(cx - off*0.6, cy + off, w, h)}" fill="{fill}" stroke="{ORANGE}" '
          f'stroke-width="{1.7 if k == 0 else 0.9}" stroke-linejoin="round" opacity="{1 if k == 0 else 0.6}"/>')
    out = (cx, cy)
    if grid:
        cid = f"clip{int(cx)}"
        A(f'<clipPath id="{cid}"><path d="{slice_path(cx, cy, w, h)}"/></clipPath>')
        A(f'<g clip-path="url(#{cid})">')
        A(f'<g stroke="{ORANGE}" stroke-width="0.5" opacity="0.5">')
        step = 7.0
        gx0, gy0 = cx - w / 2 - step, cy - h / 2 - step
        for i in range(int(w / step) + 3):
            A(f'<line x1="{gx0+i*step:.1f}" y1="{gy0:.1f}" x2="{gx0+i*step:.1f}" y2="{gy0+h+2*step:.1f}"/>')
        for j in range(int(h / step) + 3):
            A(f'<line x1="{gx0:.1f}" y1="{gy0+j*step:.1f}" x2="{gx0+w+2*step:.1f}" y2="{gy0+j*step:.1f}"/>')
        A('</g></g>')
        if hi_voxel:
            i, j = hi_voxel
            vx, vy = gx0 + i * step, gy0 + j * step
            A(f'<rect x="{vx:.1f}" y="{vy:.1f}" width="{step}" height="{step}" fill="{ORANGE}"/>')
            out = (vx + step / 2, vy + step / 2)
    # interhemispheric fissure + ventricles, so a slice reads as a brain
    A(f'<line x1="{cx:.1f}" y1="{cy-h/2+5:.1f}" x2="{cx:.1f}" y2="{cy+h/2-4:.1f}" stroke="{ORANGE}" '
      f'stroke-width="1.2" opacity="0.8"/>')
    if not grid:                                   # a few sulci, so it reads as a brain
        for sx in (-1, 1):
            for k, (dy, ln) in enumerate(((-18, 0.52), (-4, 0.66), (10, 0.60), (22, 0.40))):
                x1 = cx + sx * 4
                x2 = cx + sx * (4 + ln * (w / 2 - 8))
                A(f'<path d="M {x1:.1f} {cy+dy:.1f} C {(x1+x2)/2:.1f} {cy+dy-4:.1f} '
                  f'{(x1+x2)/2:.1f} {cy+dy+4:.1f} {x2:.1f} {cy+dy+1:.1f}" fill="none" '
                  f'stroke="{ORANGE}" stroke-width="0.9" opacity="0.45"/>')
    return out


def fmri():
    s = []
    A = s.append
    cxs = [72.0, 204.0, 336.0]
    cy, vw, vh = 108.0, 96.0, 78.0

    A(txt(204, 24, '≈ 200 000 voxels per volume', BIG, NAVY, "middle", True))

    vx, vy = volume(A, cxs[0], cy, vw, vh, grid=True, hi_voxel=(4, 7))
    volume(A, cxs[1], cy, vw, vh)
    volume(A, cxs[2], cy, vw, vh)
    for a, b in ((0, 1), (1, 2)):
        A(arrow(cxs[a] + vw / 2 + 3, cy + 6, cxs[b] - vw / 2 - 3, cy + 6, MUTED, 1.4))

    A(f'<line x1="{vx:.1f}" y1="{vy:.1f}" x2="34" y2="52" stroke="{ORANGE}" '
      f'stroke-width="1" stroke-dasharray="3 3"/>')
    A(txt(24, 48, '1 voxel ≈ 2×2×2 mm', SMALL, ORANGE))

    # ---- time axis: one volume per TR ---------------------------------------
    ay = 192.0
    A(arrow(24, ay, 390, ay, MUTED, 1.3))
    for k, cx in enumerate(cxs):
        A(f'<line x1="{cx:.1f}" y1="{cy+vh/2+20:.1f}" x2="{cx:.1f}" y2="{ay-4:.1f}" stroke="{HAIR}" stroke-width="1"/>')
        A(f'<line x1="{cx:.1f}" y1="{ay-3.5:.1f}" x2="{cx:.1f}" y2="{ay+3.5:.1f}" stroke="{MUTED}" stroke-width="1.3"/>')
        A(txt(cx, ay + 18, ['0 s', '1.5 s', '3 s'][k], 12, MUTED, "middle"))
    A(txt(392, ay - 8, 'time', 12, MUTED, "end"))

    # BOLD course of the highlighted voxel, sampled once per volume
    by, amp = 240.0, 9.0
    pts = []
    for i in range(241):
        t = i / 240
        x = 24 + t * 366
        v = (math.sin(2 * math.pi * 0.9 * t + 0.6) * 0.7 + math.sin(2 * math.pi * 1.7 * t + 2.2) * 0.3)
        pts.append((x, by - v * amp))
    A('<path d="M ' + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) +
      f'" fill="none" stroke="{ORANGE}" stroke-width="1.5"/>')
    for cx in cxs:
        i = int(round((cx - 24) / 366 * 240))
        A(f'<circle cx="{pts[i][0]:.1f}" cy="{pts[i][1]:.1f}" r="3.6" fill="{ORANGE}" stroke="#FFFFFF" stroke-width="1.2"/>')
    A(txt(390, 229, 'one number: BOLD in that voxel', SMALL, ORANGE, "end"))
    A(txt(204, 266, 'one volume every 1.5 seconds', BIG, NAVY, "middle", True))
    return head(s, W, H)


import sys, os
out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
open(os.path.join(out, 'eeg_format.svg'), 'w').write(eeg())
open(os.path.join(out, 'fmri_format.svg'), 'w').write(fmri())
print('wrote eeg_format.svg / fmri_format.svg to', out)
