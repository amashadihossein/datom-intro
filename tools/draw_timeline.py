"""Draw sketches/timeline.svg: where datom comes from, and where a standard can go.

It starts with a question, which leads into daapr.
Upper track, data as code (daapr): 2020 daapr, the R/Pharma 2021 talk, years of
use across studies, the posit::conf 2025 talk. It carries on.
Lower track, a standard for storage (datom): it branches off in 2025, when the
second realization came, and runs to R/Pharma 2026, today.
From today, a fan: what a storage standard with line of sight can enable. None of
it ships today; the last ray is the audience's own build.

Beats (data-fragment-index):
  0  the year axis, the question, the daapr track
  1  the R/Pharma talk, years of use, the posit::conf talk: realization one, it delivered
  2  realization two, and the branch: datom, a standard for storage, to R/Pharma 2026, today
  3  the fan from today, one ray after another

Run: python tools/draw_timeline.py   (edit this file, not the SVG)
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "sketches" / "timeline.svg"

W, H = 1500, 540
INK, HATCH, BLUE, PAPER, PAPER_ALT = "#3A3834", "#8C877D", "#2F6690", "#F5F1E8", "#EDE7DA"
# user-space filter region: a filter on a flat line's zero-height box would render nothing
PEN = (f'fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" '
       f'stroke-linejoin="round" filter="url(#tl-wob)"')
BLUE_PEN = (f'fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-linecap="round" '
            f'stroke-linejoin="round" filter="url(#tl-wob)"')

UP, LO, AXIS = 140, 330, 450      # y of the daapr track, the datom track, the year axis
X0, X1 = 2020.3, 2026.8           # daapr starts; today (R/Pharma, October 2026)
QX = 62                           # the question, before daapr


def X(year):
    return 140 + (year - 2020) * 138


def beat(n, body, delay=None):
    st = f' style="transition-delay: {delay:.2f}s"' if delay else ""
    return f'<g class="fragment" data-fragment-index="{n}"{st}>{body}</g>'

def html(x, y, w, h, inner, cls, style=""):
    return (f'<foreignObject x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" style="{style}">{inner}</div>'
            f'</foreignObject>')

def tag(cx, y, text, w=260, size=None):
    st = f"font-size: {size}px; letter-spacing: 0.12em;" if size else ""
    return html(cx - w / 2, y - 12, w, 24, text, "sc-tag", st)

def name(cx, y, text, w=220):
    return html(cx - w / 2, y - 14, w, 28, text, "sc-name", f"color: {INK}; font-size: 20px;")

def note(x, y, text, w=320, h=40):
    return html(x, y, w, h, text, "sc-note")

def dot(x, y, filled=False):
    fill = INK if filled else PAPER
    return f'<circle cx="{x:.1f}" cy="{y}" r="9" fill="{fill}" stroke-width="3"/>'


# the fan: (angle in degrees from today, label). Longest labels sit where the rays are shortest.
FAN_R = 205
FAN = [(-44, "diffs without fetching"),
       (-27, "self-describing data"),
       (-10, "access from lineage"),
       (7,   "managed migration"),
       (24,  "reads by policy"),
       (41,  None)]                   # the open ray: your build


def build():
    # 0: the axis, the question, the daapr track
    ticks = "".join(f'<path d="M{X(y):.1f} {AXIS - 7} V{AXIS + 7}" stroke-width="2.4"/>' for y in range(2020, 2027))
    axis = (f'<path d="M{X(2020) - 20:.1f} {AXIS} H{X(2026.95):.1f}" stroke="{HATCH}" stroke-width="2.4"/>'
            + ticks.replace('stroke-width', f'stroke="{HATCH}" stroke-width'))
    years = "".join(tag(X(y), AXIS + 32, str(y), 80) for y in range(2020, 2027))
    end = X(2026.95)
    track = (f'<path d="M{X(X0):.1f} {UP} H{end:.1f}"/>'
             f'<path d="M{end - 12:.1f} {UP - 8} L{end:.1f} {UP} L{end - 12:.1f} {UP + 8}"/>'
             f'<path d="M{QX + 22} {UP} H{X(X0) - 12:.1f}" stroke-dasharray="2 9"/>'
             f'<circle cx="{QX}" cy="{UP}" r="20" fill="{PAPER}" stroke-width="2.4" stroke-dasharray="4 6"/>')
    qmark = html(QX - 20, UP - 22, 40, 44, "?", "sc-name",
                 f"color: {BLUE}; font: 600 30px/1 'Caveat', cursive;")
    question = note(QX - 26, UP + 34, "why can&#8217;t data collaboration<br/>be as smooth as<br/>code collaboration?", 340, 96)
    b0 = (f'<g {PEN}>{axis}{track}{dot(X(X0), UP, True)}</g>' + years + qmark + question
          + name(X(X0) + 40, UP - 62, "daapr", 160)
          + tag(X(X0) + 40, UP - 36, "data as code, in R", 240, 13)
          + tag(end + 66, UP, "carries on", 110, 12))

    # 1: shared at R/Pharma, used across studies for years, shared again at posit::conf
    r21, pc25 = X(2021.85), X(2025.7)
    band = (f'<rect x="{X(2022):.1f}" y="{UP + 14}" width="{X(2025.45) - X(2022):.1f}" height="22" rx="4" '
            f'fill="url(#tl-hatch)" stroke-width="2.2"/>')
    b1 = (f'<g {PEN}>{dot(r21, UP)}{dot(pc25, UP)}{band}</g>'
          + name(r21 + 20, UP - 62, "R/Pharma", 160) + tag(r21 + 20, UP - 36, "the first talk", 200, 13)
          + name(pc25 - 10, UP - 62, "posit::conf", 180) + tag(pc25 - 10, UP - 36, "talk by Clara Amorosi", 240, 13)
          + tag((X(2022) + X(2025.45)) / 2, UP + 58, "years of use, across studies", 360, 13)
          + note(560, UP - 86, "&#9312; it delivered", 220))

    # 2: realization two, and the branch: datom, a standard for storage, to today
    bx, dx, today = X(2025.4), X(2025.75), X(X1)
    branch = (f'<path d="M{bx:.1f} {UP} C {bx + 40:.1f} {UP}, {dx - 50:.1f} {LO}, {dx:.1f} {LO} H{today:.1f}"/>')
    b2 = (f'<g {PEN}>{branch}{dot(dx, LO, True)}{dot(today, LO)}'
          f'<circle cx="{today:.1f}" cy="{LO}" r="17" stroke-width="2" stroke-dasharray="3 6"/></g>'
          + note(548, LO - 62, "&#9313; storage is written for machines:<br/>what more could it do for us?", 340, 70)
          + name(dx - 16, LO + 40, "datom", 160) + tag(dx - 16, LO + 66, "a standard for storage", 280, 13)
          + name(today - 34, LO - 46, "R/Pharma", 160) + note(today - 30, LO + 28, "today", 120))

    # 3: the fan from today: what a standard with line of sight can enable
    r_out = 400
    a0, a1 = math.radians(-51), math.radians(46)
    beam = (f'<path d="M{today:.1f} {LO} L{today + r_out * math.cos(a0):.1f} {LO + r_out * math.sin(a0):.1f} '
            f'A{r_out} {r_out} 0 0 1 {today + r_out * math.cos(a1):.1f} {LO + r_out * math.sin(a1):.1f} Z" '
            f'fill="url(#tl-beam)" stroke="none"/>')
    edges = "".join(f'<path d="M{today + 26 * math.cos(a):.1f} {LO + 26 * math.sin(a):.1f} '
                    f'L{today + 200 * math.cos(a):.1f} {LO + 200 * math.sin(a):.1f}" '
                    f'stroke="{HATCH}" stroke-width="2" stroke-dasharray="2 8"/>' for a in (a0, a1))
    rays = []
    for i, (deg, label) in enumerate(FAN):
        a = math.radians(deg)
        ex, ey = today + FAN_R * math.cos(a), LO + FAN_R * math.sin(a)
        color = BLUE if label is None else INK
        pen = PEN.replace(f'stroke="{INK}" stroke-width="3"', f'stroke="{color}" stroke-width="2.6"')
        line = (f'<g {pen}>'
                f'<path d="M{today + 26 * math.cos(a):.1f} {LO + 26 * math.sin(a):.1f} L{ex - 9 * math.cos(a):.1f} {ey - 9 * math.sin(a):.1f}" stroke-dasharray="3 8"/>'
                f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="8" fill="{PAPER}" stroke-dasharray="3 4"/></g>')
        if label is None:
            text = note(ex + 14, ey - 20, "your build", 160)
        else:
            text = html(ex + 16, ey - 14, 1500 - ex - 16, 28, label, "sc-name",
                        f"color: {INK}; font-size: 19px; justify-content: flex-start;")
        rays.append(beat(3, line + text, 0.15 + 0.22 * i))
    behind = beat(3, beam + f'<g {PEN}>{edges}</g>')   # drawn first, under the tracks
    b3 = ("".join(rays)
          + beat(3, tag(1318, LO + 192, "ahead &#183; designed, or open to build", 360, 12), 1.5))

    return (f'<svg class="scene" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
            f'style="overflow: visible" role="img" aria-label="A timeline. It starts with a question: why '
            f'can&#8217;t data collaboration be as smooth as code collaboration? Data as code: daapr from 2020, '
            f'an R/Pharma talk in 2021, years of use across studies, a posit::conf talk in 2025. In 2025 a '
            f'second track branches off: datom, a standard for storage, running to R/Pharma 2026, today. From '
            f'today, rays fan out to what a storage standard can enable: self-describing data, diffs without '
            f'fetching, managed migration, access from lineage, reads by policy, and your build.">\n'
            f'  <defs>\n'
            f'    <filter id="tl-wob" filterUnits="userSpaceOnUse" x="-20" y="-20" width="{W + 40}" height="{H + 40}">\n'
            f'      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="41" result="noise"/>\n'
            f'      <feDisplacementMap in="SourceGraphic" in2="noise" scale="4" xChannelSelector="R" yChannelSelector="G"/>\n'
            f'    </filter>\n'
            f'    <pattern id="tl-hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">\n'
            f'      <line x1="0" y1="0" x2="0" y2="9" stroke="{HATCH}" stroke-width="1.4"/>\n'
            f'    </pattern>\n'
            f'    <radialGradient id="tl-beam" gradientUnits="userSpaceOnUse" cx="{X(X1):.1f}" cy="{LO}" r="{r_out}">\n'
            f'      <stop offset="0" stop-color="#E8E0CF" stop-opacity="1"/>\n'
            f'      <stop offset="0.75" stop-color="{PAPER_ALT}" stop-opacity="0.9"/>\n'
            f'      <stop offset="1" stop-color="{PAPER_ALT}" stop-opacity="0"/>\n'
            f'    </radialGradient>\n'
            f'  </defs>\n'
            f'  <!-- generated by tools/draw_timeline.py: edit that, not this -->\n'
            f'  {behind}\n  {b0}\n  {beat(1, b1)}\n  {beat(2, b2)}\n  {b3}\n'
            f'</svg>\n')


if __name__ == "__main__":
    OUT.write_text(build())
    print(f"wrote {OUT}")
