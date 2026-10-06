#!/usr/bin/env python3
"""Draw sketches/workflow.svg: a closer look at the day-to-day workflow.

One canvas, 1460x640, beat by beat, like the picture (see draw_picture.py):
each beat is a <g class="fragment">, and its motion hangs off a trigger,
<set class="on-reveal" begin="indefinite">, fired by js/smil.js.

  0  analyst A, an empty input_files/ inbox
  1  datom_init_repo(): the git repo (code) and the data store appear
  2  A drops two files in and syncs: both new; parquet to storage, a commit to git
  3  analyst B: datom_clone() brings the code, not the data
  4  B syncs next month's extract: unchanged (skipped), changed (v2), new (v1)
  5  a reader reads lb at version 1 from storage alone

Run from the repo root:  python tools/draw_workflow.py
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "sketches" / "workflow.svg"

W, H = 1460, 640
INK, HATCH, BLUE, ORANGE, PAPER = "#3A3834", "#8C877D", "#2F6690", "#C8692E", "#F5F1E8"
PEN = (f'fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" '
       f'stroke-linejoin="round" filter="url(#wf-wob)"')


# ---------------------------------------------------------------- primitives
def beat(n, body):
    return f'<g class="fragment" data-fragment-index="{n}">{body}</g>'

def trigger(n):
    return (f'<rect width="0" height="0"><set id="wf-t{n}" class="on-reveal" '
            f'attributeName="x" to="0" begin="indefinite" dur="0.01s"/></rect>')

def at(n, s):
    return f"wf-t{n}.begin+{s:g}s"

def html(x, y, w, h, inner, cls, style=""):
    return (f'<foreignObject x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" style="{style}">{inner}</div>'
            f'</foreignObject>')

def tag(x, y, text, w=220, color=None, left=True, size=None):
    style = ("justify-content: flex-start;" if left else "") + (f" color: {color};" if color else "") + (f" font-size: {size}px; letter-spacing: 0.12em;" if size else "")
    return html(x, y - 12, w, 24, text, "sc-tag", style)

def name(x, y, text, w=260):
    return html(x, y - 12, w, 24, text, "sc-name", f"justify-content: flex-start; color: {INK};")

def cmd(x, y, text, w=340):
    return html(x, y, w, 34, text, "sc-cmd")

def note(x, y, text, w=300, h=60):
    return html(x, y, w, h, text, "sc-note")

def frame(x0, y0, x1, y1, ident):
    return (f'<rect id="{ident}" x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="18" fill="{PAPER}"/>'
            f'<use href="#{ident}" transform="translate(2 2)" opacity="0.4"/>')

def person(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="12"/>'
            f'<path d="M{cx-21} {cy+36} C {cx-19} {cy+17}, {cx+19} {cy+17}, {cx+21} {cy+36}"/>'
            f'<path d="M{cx+14} {cy+36} H{cx+50} M{cx+18} {cy+36} L{cx+24} {cy+14} '
            f'H{cx+48} L{cx+44} {cy+36}" stroke-width="2.5"/>')

def doc(x, y):
    """A small file: a text file in an inbox, or a metadata file in git."""
    return (f'<path d="M{x} {y-16} H{x+18} L{x+26} {y-8} V{y+16} H{x} Z" fill="{PAPER}" stroke-width="2.4"/>'
            f'<path d="M{x+18} {y-16} V{y-8} H{x+26}" stroke-width="1.8"/>'
            f'<path d="M{x+5} {y-2} H{x+20} M{x+5} {y+5} H{x+20} M{x+5} {y+11} H{x+14}" stroke-width="1.5"/>')

def parquet(x, y):
    """A parquet file, as on the data-as-code slide."""
    return (f'<rect x="{x}" y="{y-16}" width="28" height="34" rx="3" fill="{PAPER}" stroke="none"/>'
            f'<rect x="{x}" y="{y-16}" width="28" height="9" fill="url(#wf-hatch)" stroke="none"/>'
            f'<rect x="{x}" y="{y-16}" width="28" height="34" rx="3" stroke-width="2.4"/>'
            f'<path d="M{x} {y-7} H{x+28} M{x+9.3} {y-7} V{y+18} M{x+18.6} {y-7} V{y+18}" stroke-width="1.6"/>')

def pill(x, y, text, w=44):
    return (f'<rect x="{x}" y="{y-13}" width="{w}" height="26" rx="13" fill="{PAPER}" stroke-width="2.2"/>'
            + html(x, y - 12, w, 24, text, "sc-name", f"color: {INK}; font-size: 15px;"))

def table_card(x, y):
    w, h = 78, 56
    return (f'<g transform="translate({x} {y})">'
            f'<rect width="{w}" height="{h}" rx="6" fill="{PAPER}" stroke="none"/>'
            f'<path d="M6 0 H{w-6} Q{w} 0 {w} 6 V14 H0 V6 Q0 0 6 0 Z" fill="url(#wf-hatch)" stroke="none"/>'
            f'<rect width="{w}" height="{h}" rx="6"/><path d="M0 14 H{w}" stroke-width="2"/>'
            f'<path d="M26 14 V{h}" stroke-width="1.6"/>'
            f'<path d="M7 26 H19 M7 36 H19 M7 46 H19 M32 26 H{w-8} M32 36 H{w-8} M32 46 H{w-20}" stroke-width="1.6"/></g>')


# ---------------------------------------------------------------- motion
def pulse(d, begin, dur=1.2, r=5.5):
    return (f'<circle r="{r}" fill="{ORANGE}" opacity="0">'
            f'<animateMotion path="{d}" begin="{begin}" dur="{dur}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.25 1"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.88;1" '
            f'begin="{begin}" dur="{dur}s" fill="freeze"/></circle>')

def arrive(body, begin, dy=-30):
    return (f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{begin}" dur="0.45s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" '
            f'begin="{begin}" dur="0.7s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines="0.22 0.61 0.36 1"/>{body}</g>')

def fade(body, begin):
    return (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin}" '
            f'dur="0.45s" fill="freeze"/>{body}</g>')

def path(p0, p1, bend=0.0):
    """A gentle S-curve from p0 to p1."""
    (x0, y0), (x1, y1) = p0, p1
    mx = (x1 - x0) * 0.5
    return f"M{x0} {y0} C {x0+mx} {y0+bend}, {x1-mx} {y1-bend}, {x1} {y1}"


# ---------------------------------------------------------------- the scene
A = (40, 40, 440, 280)          # analyst A's clone
B = (40, 360, 440, 600)         # analyst B's clone
GIT = (600, 40, 960, 280)       # the git repo: code
STORE = (600, 360, 960, 600)    # the data store: values
READER = (1150, 470)

A_FILES = {"dm": 120, "lb": 175}                 # y of each file in A's inbox
B_FILES = {"dm": 440, "lb": 495, "ae": 550}       # y of each file in B's inbox
FILE_X, STATUS_X = 190, 318
GIT_ROWS = {"dm": 90, "lb": 145, "ae": 200}      # y of each table in git
STORE_ROWS = [("dm/7a3b&#8230;.parquet", 398), ("lb/72d3&#8230;.parquet", 442),
              ("lb/b27e&#8230;.parquet", 486), ("ae/1e4a&#8230;.parquet", 530)]


def scene():
    out = []

    # 0: analyst A and an empty inbox
    a = frame(*A, "wf-a") + person(95, 95)
    out.append(f'<g {PEN}>{a}</g>')
    out.append(tag(60, 262, "analyst a"))
    out.append(tag(FILE_X, 70, "input_files/", w=200, color=HATCH))

    # 1: datom_init_repo(): git (code) and storage (data) appear
    b1 = trigger(1)
    b1 += arrive(f'<g {PEN}>{frame(*GIT, "wf-git")}'
                 f'<path d="M906 66 V100 M906 90 C 906 80, 926 80, 926 72" stroke-width="2.4"/>'
                 f'<circle cx="906" cy="64" r="4.5" fill="{PAPER}" stroke-width="2.2"/>'
                 f'<circle cx="906" cy="104" r="4.5" fill="{PAPER}" stroke-width="2.2"/>'
                 f'<circle cx="926" cy="68" r="4.5" fill="{PAPER}" stroke-width="2.2"/></g>'
                 + tag(620, 262, "git · the code") , at(1, 0.1))
    b1 += arrive(f'<g {PEN}>{frame(*STORE, "wf-store")}</g>' + tag(620, 582, "storage · the data"), at(1, 0.4))
    b1 += fade(cmd(450, 2, "datom_init_repo()"), at(1, 0.2))
    out.append(beat(1, b1))

    # 2: A drops dm and lb in and syncs; both new
    b2 = trigger(2)
    for i, (t, y) in enumerate(A_FILES.items()):
        b2 += arrive(f'<g {PEN}>{doc(FILE_X, y)}</g>' + name(FILE_X + 34, y, f"{t}.csv", 120), at(2, 0.1 * i))
        b2 += fade(tag(STATUS_X, y, "new", 110, size=13), at(2, 1.0))
        s = 0.9 + 0.35 * i
        sy = STORE_ROWS[i][1]
        b2 += pulse(path((FILE_X + 30, y), (622, sy), 40), at(2, s))
        b2 += pulse(path((FILE_X + 30, y), (622, GIT_ROWS[t]), -10), at(2, s), r=4)
        b2 += arrive(f'<g {PEN}>{parquet(622, sy)}</g>' + name(662, sy, STORE_ROWS[i][0]), at(2, s + 1.1), dy=-14)
        b2 += arrive(f'<g {PEN}>{doc(622, GIT_ROWS[t])}{pill(700, GIT_ROWS[t], "v1")}</g>'
                     + name(658, GIT_ROWS[t], t, 40), at(2, s + 1.1), dy=-14)
    b2 += fade(cmd(455, 150, "datom_sync()", 200), at(2, 0.6))
    out.append(beat(2, b2))

    # 3: analyst B clones: the code comes down, the data stays put
    b3 = trigger(3)
    b3 += arrive(f'<g {PEN}>{frame(*B, "wf-b")}{person(95, 415)}</g>' + tag(60, 582, "analyst b"), at(3, 0))
    b3 += pulse(path((600, 230), (440, 420), 0), at(3, 0.6))
    b3 += fade(cmd(455, 262, "datom_clone()", 200), at(3, 0.3))
    b3 += fade(note(455, 300, "brings the code,<br/>not the data", 160), at(3, 1.6))
    out.append(beat(3, b3))

    # 4: B syncs next month's extract: unchanged, changed, new
    b4 = trigger(4)
    b4 += fade(tag(FILE_X, 390, "input_files/", w=200, color=HATCH), at(4, 0))
    for i, (t, y) in enumerate(B_FILES.items()):
        b4 += arrive(f'<g {PEN}>{doc(FILE_X, y)}</g>' + name(FILE_X + 34, y, f"{t}.csv", 120), at(4, 0.1 * i))
    b4 += fade(tag(STATUS_X, B_FILES["dm"], "unchanged", 110, color=HATCH, size=13), at(4, 1.0))
    b4 += fade(tag(STATUS_X, B_FILES["lb"], "changed", 110, size=13), at(4, 1.0))
    b4 += fade(tag(STATUS_X, B_FILES["ae"], "new", 110, size=13), at(4, 1.0))
    for t, row, s in (("lb", 2, 1.2), ("ae", 3, 1.55)):
        y, sy = B_FILES[t], STORE_ROWS[row][1]
        b4 += pulse(path((FILE_X + 30, y), (622, sy), 0), at(4, s))
        b4 += pulse(path((FILE_X + 30, y), (622, GIT_ROWS[t]), 30), at(4, s), r=4)
        b4 += arrive(f'<g {PEN}>{parquet(622, sy)}</g>' + name(662, sy, STORE_ROWS[row][0]), at(4, s + 1.1), dy=-14)
    b4 += arrive(f'<g {PEN}>{pill(752, GIT_ROWS["lb"], "v2")}</g>', at(4, 2.3), dy=-14)
    b4 += arrive(f'<g {PEN}>{doc(622, GIT_ROWS["ae"])}{pill(700, GIT_ROWS["ae"], "v1")}</g>'
                 + name(658, GIT_ROWS["ae"], "ae", 40), at(4, 2.65), dy=-14)
    b4 += fade(cmd(455, 470, "datom_sync()", 200), at(4, 0.6))
    out.append(beat(4, b4))

    # 5: a reader reads lb, version 1, from storage alone
    b5 = trigger(5)
    rx, ry = READER
    b5 += arrive(f'<g {PEN}>{person(rx, ry - 18)}{table_card(rx + 70, ry - 30)}</g>'
                 + tag(rx - 30, ry + 50, "reader", 160), at(5, 0))
    b5 += pulse(path((960, STORE_ROWS[1][1]), (rx + 70, ry), -20), at(5, 0.7))
    b5 += fade(cmd(1000, 330, 'datom_read(conn, "lb",<br/>&#160;&#160;version = v1)', 330), at(5, 0.3))
    b5 += fade(note(1000, 560, "storage alone:<br/>no git, no PAT", 220), at(5, 1.6))
    out.append(beat(5, b5))

    return "".join(out)


def main():
    svg = (f'<svg class="scene" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
           f'style="overflow: visible" role="img" aria-label="The datom workflow, beat by beat: '
           f'an analyst sets up a git repo for the code and a store for the data; syncs two new files; '
           f'a second analyst clones the code and syncs next month&apos;s extract, where one file is unchanged '
           f'and skipped, one changed and one new; a reader reads version 1 from storage alone">'
           f'<defs><filter id="wf-wob" x="-10%" y="-10%" width="120%" height="120%">'
           f'<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="29" result="noise"/>'
           f'<feDisplacementMap in="SourceGraphic" in2="noise" scale="4" xChannelSelector="R" yChannelSelector="G"/>'
           f'</filter><pattern id="wf-hatch" width="9" height="9" patternUnits="userSpaceOnUse" '
           f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="9" stroke="{HATCH}" stroke-width="1.4"/>'
           f'</pattern></defs>{scene()}</svg>\n')
    OUT.write_text(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
