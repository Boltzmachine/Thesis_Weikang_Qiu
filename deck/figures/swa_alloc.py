# -*- coding: utf-8 -*-
SP = '/private/tmp/claude-501/-Users-qiuweikang-Library-CloudStorage-OneDrive-YaleUniversity-Thesis-Weikang-Qiu/e08798ff-aa47-4714-8b6f-ed338ba0070b/scratchpad'
W, H = 450.0, 320.0
BLUE, GREEN, GREY, BODY, HAIR = "#4472C4", "#1F8A44", "#9AA3AE", "#333F4F", "#D9DEE7"
NAVY = "#00356B"

# five nested bands of p = (1-B)(1-C); darkest = smallest p = most protected
BANDS = [(0.45, "#E8EEF6"), (0.25, "#BCD2E6"), (0.12, "#7FA6CE"), (0.05, "#2C5E93"), (0.00, NAVY)]

s = []; A = s.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*3:.0f}" height="{H*3:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" '
  f'font-family="Calibri, \'PingFang SC\', \'Helvetica Neue\', sans-serif">')
A(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

# ───────────────────── Panel A · head-level priority map ─────────────────────
ax, ay, aw = 44.0, 58.0, 148.0
A(f'<text x="6" y="24" font-size="12.5" font-weight="bold" fill="{NAVY}">哪些头会被保护</text>')
A(f'<text x="6" y="42" font-size="9.5" fill="{BODY}">颜色 = 优先级 p　·　深色 = 保留</text>')

def P(c, b):                      # plot coords → svg
    return ax + c*aw, ay + aw - b*aw

for k, col in BANDS:
    if k <= 0:
        d = f'M {ax:.2f} {ay:.2f} L {ax+aw:.2f} {ay:.2f} L {ax+aw:.2f} {ay+aw:.2f} Z'   # degenerate; skip
        continue
    pts = []
    steps = 90
    for t in range(steps+1):
        c = (1-k) * t/steps
        b = 1 - k/(1-c)
        pts.append(P(c, b))
    x1, y1 = P(1, 0); x2, y2 = P(1, 1); x3, y3 = P(0, 1)
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    d += f" L {x1:.2f} {y1:.2f} L {x2:.2f} {y2:.2f} L {x3:.2f} {y3:.2f} Z"
    if col == BANDS[0][1]:
        A(f'<rect x="{ax}" y="{ay}" width="{aw}" height="{aw}" fill="#F6F8FB"/>')
    A(f'<path d="{d}" fill="{col}"/>')
A(f'<rect x="{ax}" y="{ay}" width="{aw}" height="{aw}" fill="none" stroke="{HAIR}" stroke-width="0.8"/>')

A(f'<text x="{ax+aw/2:.1f}" y="{ay+aw+15:.1f}" font-size="9.5" fill="{BODY}" text-anchor="middle">Core 分数  →</text>')
A(f'<text x="{ax-12:.1f}" y="{ay+aw/2:.1f}" font-size="9.5" fill="{BODY}" text-anchor="middle" '
  f'transform="rotate(-90 {ax-12:.1f} {ay+aw/2:.1f})">Bridge 分数  →</text>')

def dot(c, b, col, label, dx, dy, anchor="start"):
    x, y = P(c, b)
    A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/>')
    A(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" font-size="9.5" font-weight="bold" fill="{col}" text-anchor="{anchor}" '
      f'stroke="#FFFFFF" stroke-width="2.8" paint-order="stroke">{label}</text>')

dot(0.15, 0.87, GREEN, "Bridge 头", 8, 3.4)
dot(0.88, 0.14, BLUE,  "Core 头", -8, 3.4, "end")
dot(0.17, 0.32, GREY,  "普通头", 8, 3.4)

A(f'<text x="{ax+aw-5:.1f}" y="{ay+14:.1f}" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="end">保护带</text>')
A(f'<text x="{ax+5:.1f}" y="{ay+aw-7:.1f}" font-size="9" fill="{BODY}">两者都低 → 先剪</text>')

# discrete legend
lw = aw/5
for i, (k, col) in enumerate(BANDS[:-1] + [(0.0, NAVY)]):
    x = ax + (4-i)*lw
    A(f'<rect x="{x:.2f}" y="{ay+aw+24:.1f}" width="{lw:.2f}" height="7" fill="{col}" stroke="{HAIR}" stroke-width="0.4"/>')
A(f'<text x="{ax:.1f}" y="{ay+aw+43:.1f}" font-size="9" fill="{BODY}">保留</text>')
A(f'<text x="{ax+aw:.1f}" y="{ay+aw+43:.1f}" font-size="9" fill="{BODY}" text-anchor="end">剪掉</text>')
A(f'<text x="6" y="{ay+aw+63:.1f}" font-size="10.5" font-weight="bold" fill="{GREEN}">任一角色突出 → 这个头就被保护</text>')

# ───────────────────── Panel B · layer-level budget ─────────────────────
bx = 236.0
A(f'<line x1="{bx-16:.0f}" y1="14" x2="{bx-16:.0f}" y2="{H-12:.0f}" stroke="{HAIR}" stroke-width="0.8"/>')
A(f'<text x="{bx}" y="24" font-size="12.5" font-weight="bold" fill="{NAVY}">每层剪掉多少</text>')
A(f'<text x="{bx}" y="42" font-size="9.5" fill="{BODY}">结构越重要的层，剪得越少</text>')

pbar  = [0.29, 0.36, 0.52, 0.62, 0.43, 0.70, 0.64, 0.44]          # mean = 0.500
heads = [[0.10,0.22,0.35,0.28,0.44,0.35],[0.20,0.30,0.42,0.33,0.48,0.43],
         [0.40,0.50,0.55,0.48,0.62,0.57],[0.52,0.60,0.66,0.58,0.72,0.64],
         [0.30,0.38,0.46,0.40,0.55,0.49],[0.62,0.68,0.74,0.70,0.78,0.68],
         [0.55,0.62,0.70,0.64,0.72,0.61],[0.32,0.40,0.48,0.42,0.54,0.48]]

def band_col(p):
    for k, col in BANDS[:-1]:
        if p > k: return col
    return NAVY
def band_col2(p):
    if p > 0.45: return BANDS[0][1]
    if p > 0.25: return BANDS[1][1]
    if p > 0.12: return BANDS[2][1]
    if p > 0.05: return BANDS[3][1]
    return NAVY

row_h, top = 22.5, 70.0
hx, bar_x, bar_w, target = bx + 18, bx + 86, 104.0, 0.5
A(f'<text x="{hx-2:.0f}" y="{top-7:.0f}" font-size="8.5" fill="{GREY}">层内各头 p</text>')
A(f'<text x="{bar_x:.0f}" y="{top-7:.0f}" font-size="8.5" fill="{GREY}">该层稀疏度</text>')

for k, pv in enumerate(pbar):
    yc = top + k*row_h + row_h/2
    A(f'<text x="{bx:.0f}" y="{yc+3.2:.1f}" font-size="9" fill="{GREY}">L{k+1}</text>')
    for m, hp in enumerate(heads[k]):
        A(f'<circle cx="{hx + m*10.6:.1f}" cy="{yc:.1f}" r="3.7" fill="{band_col2(hp)}" stroke="{HAIR}" stroke-width="0.5"/>')
    A(f'<rect x="{bar_x:.1f}" y="{yc-6:.1f}" width="{bar_w:.1f}" height="12" fill="#F1F3F7"/>')
    A(f'<rect x="{bar_x:.1f}" y="{yc-6:.1f}" width="{pv*bar_w:.1f}" height="12" fill="{NAVY if pv>=target else "#9FBFDC"}"/>')
    A(f'<text x="{bar_x+bar_w+5:.1f}" y="{yc+3.2:.1f}" font-size="8.5" fill="{BODY}">{pv:.2f}</text>')

tx = bar_x + target*bar_w
A(f'<line x1="{tx:.1f}" y1="{top-2:.1f}" x2="{tx:.1f}" y2="{top+len(pbar)*row_h+5:.1f}" stroke="{GREEN}" '
  f'stroke-width="1.3" stroke-dasharray="3.5 2.5"/>')
A(f'<text x="{tx:.1f}" y="{top+len(pbar)*row_h+18:.1f}" font-size="9" font-weight="bold" fill="{GREEN}" '
  f'text-anchor="middle">目标 0.5</text>')
A(f'<text x="{bx}" y="{top+len(pbar)*row_h+40:.1f}" font-size="10.5" font-weight="bold" fill="{GREEN}">重标定后：全局平均正好 = 目标</text>')
A('</svg>')

open(f'{SP}/swa_alloc.svg','w').write("\n".join(s))
print("ok")
