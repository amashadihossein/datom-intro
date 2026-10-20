"""Draw sketches/timeline.svg: where datom comes from, on two tracks.

Upper track, data as code (daapr): 2020 daapr, the R/Pharma 2021 talk, years of
use across studies, the posit::conf 2025 talk. It carries on.
Lower track, a standard for storage (datom): it branches off in 2025, when the
second realization came, and runs to R/Pharma 2026, today.

Beats (data-fragment-index):
  0  the year axis, the daapr track, and where it started
  1  the R/Pharma talk, years of use, the posit::conf talk: realization one, it delivered
  2  realization two: if storage serves machines, what more could it do? (the questions)
  3  the branch: datom, a standard for storage, to R/Pharma 2026, today

Run: python tools/draw_timeline.py   (edit this file, not the SVG)
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "sketches" / "timeline.svg"

W, H = 1500, 560
INK, HATCH, BLUE, PAPER = "#3A3834", "#8C877D", "#2F6690", "#F5F1E8"
# user-space filter region: a filter on a flat line's zero-height box would render nothing
PEN = (f'fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" '
       f'stroke-linejoin="round" filter="url(#tl-wob)"')
BLUE_PEN = (f'fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-linecap="round" '
            f'stroke-linejoin="round" filter="url(#tl-wob)"')

UP, LO, AXIS = 190, 380, 500      # y of the daapr track, the datom track, the year axis
X0, X1 = 2020.3, 2026.8           # daapr starts; today (R/Pharma, October 2026)


def X(year):
    return 100 + (year - 2020) * 195


def beat(n, body):
    return f'<g class="fragment" data-fragment-index="{n}">{body}</g>'

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


def build():
    # 0: the axis, the daapr track, where it started
    ticks = "".join(f'<path d="M{X(y):.1f} {AXIS - 7} V{AXIS + 7}" stroke-width="2.4"/>' for y in range(2020, 2027))
    axis = (f'<path d="M{X(2020) - 20:.1f} {AXIS} H{X(2026.95):.1f}" stroke="{HATCH}" stroke-width="2.4"/>'
            + ticks.replace('stroke-width', f'stroke="{HATCH}" stroke-width'))
    years = "".join(tag(X(y), AXIS + 32, str(y), 80) for y in range(2020, 2027))
    track = (f'<path d="M{X(X0):.1f} {UP} H{X(2026.95):.1f}"/>'
             f'<path d="M{X(2026.95) - 12:.1f} {UP - 8} L{X(2026.95):.1f} {UP} L{X(2026.95) - 12:.1f} {UP + 8}"/>')
    b0 = (f'<g {PEN}>{axis}{track}{dot(X(X0), UP, True)}</g>' + years
          + name(X(X0) + 60, UP - 62, "daapr", 160)
          + tag(X(X0) + 60, UP - 36, "data as code, in R", 240, 13)
          + tag(X(2026.6), UP - 24, "carries on", 160, 12))

    # 1: shared at R/Pharma, used across studies for years, shared again at posit::conf
    r21, pc25 = X(2021.85), X(2025.7)
    band = (f'<rect x="{X(2022):.1f}" y="{UP + 14}" width="{X(2025.45) - X(2022):.1f}" height="22" rx="4" '
            f'fill="url(#tl-hatch)" stroke-width="2.2"/>')
    b1 = (f'<g {PEN}>{dot(r21, UP)}{dot(pc25, UP)}{band}</g>'
          + name(r21, UP - 62, "R/Pharma", 160) + tag(r21, UP - 36, "the first talk", 200, 13)
          + name(pc25 - 10, UP - 62, "posit::conf", 180) + tag(pc25 - 10, UP - 36, "talk by Clara Amorosi", 240, 13)
          + tag((X(2022) + X(2025.45)) / 2, UP + 58, "years of use, across studies", 360, 13)
          + note(640, UP - 86, "&#9312; it delivered", 220))

    # 2: the second realization, as questions
    qs = ("if storage is written for machines,<br/>what more could it do for us?<br/>"
          "&#183; plan for migration?<br/>&#183; manage access?<br/>"
          "&#183; diff versions without fetching?<br/>&#183; carry its own data dictionary?")
    b2 = (note(640, UP + 84, "&#9313; " + qs, 430, 190)
          + f'<g {BLUE_PEN}><path d="M1010 {UP + 112} C 1060 {UP + 100}, 1110 {UP + 60}, 1140 {UP + 14}"/>'
            f'<path d="M1128 {UP + 22} L1141 {UP + 12} L1143 {UP + 28}"/></g>')

    # 3: the branch: datom, a standard for storage, to today
    bx, dx, today = X(2025.4), X(2025.75), X(X1)
    branch = (f'<path d="M{bx:.1f} {UP} C {bx + 40:.1f} {UP}, {dx - 50:.1f} {LO}, {dx:.1f} {LO} H{today:.1f}"/>')
    b3 = (f'<g {PEN}>{branch}{dot(dx, LO, True)}{dot(today, LO)}'
          f'<circle cx="{today:.1f}" cy="{LO}" r="17" stroke-width="2" stroke-dasharray="3 6"/></g>'
          + name(dx, LO + 40, "datom", 160) + tag(dx, LO + 66, "a standard for storage", 280, 13)
          + name(today - 4, LO - 46, "R/Pharma", 160) + note(today - 52, LO + 30, "today", 120))

    return (f'<svg class="scene" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
            f'style="overflow: visible" role="img" aria-label="A timeline on two tracks. Data as code: daapr '
            f'from 2020, an R/Pharma talk in 2021, years of use across studies, a posit::conf talk in 2025. '
            f'In 2025 a second track branches off: datom, a standard for storage, running to R/Pharma 2026, today.">\n'
            f'  <defs>\n'
            f'    <filter id="tl-wob" filterUnits="userSpaceOnUse" x="-20" y="-20" width="{W + 40}" height="{H + 40}">\n'
            f'      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="41" result="noise"/>\n'
            f'      <feDisplacementMap in="SourceGraphic" in2="noise" scale="4" xChannelSelector="R" yChannelSelector="G"/>\n'
            f'    </filter>\n'
            f'    <pattern id="tl-hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">\n'
            f'      <line x1="0" y1="0" x2="0" y2="9" stroke="{HATCH}" stroke-width="1.4"/>\n'
            f'    </pattern>\n'
            f'  </defs>\n'
            f'  <!-- generated by tools/draw_timeline.py: edit that, not this -->\n'
            f'  {b0}\n  {beat(1, b1)}\n  {beat(2, b2)}\n  {beat(3, b3)}\n'
            f'</svg>\n')


if __name__ == "__main__":
    OUT.write_text(build())
    print(f"wrote {OUT}")
