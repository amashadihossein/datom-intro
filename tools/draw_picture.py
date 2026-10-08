#!/usr/bin/env python3
"""Draw sketches/picture.svg: the central picture, built up beat by beat.

One canvas, 1500x750, drawn 1:1 into the slide's camera. Each beat is a
<g class="fragment" data-fragment-index="N">, so reveal.js builds the scene one
click at a time. Labels are HTML inside <foreignObject>, so they share the
drawing's coordinates and move with the camera.

One-shot motion (cards arriving, pulses travelling) starts when its beat is
shown: each beat holds a trigger, <set class="on-reveal" begin="indefinite">,
which js/smil.js fires; that beat's animations begin relative to it.

Conventions as in the README: pencil strokes, wobble filter, 45-degree hatch,
orange only on things that move.

Run from the repo root:  python tools/draw_picture.py
"""
import math, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "sketches" / "picture.svg"

W, H = 1500, 750
INK, HATCH, BLUE, ORANGE, PAPER = "#3A3834", "#8C877D", "#2F6690", "#C8692E", "#F5F1E8"
CW, CH = 96, 68          # a table or set card
OFF = (18, -16)          # each newer version sits up and to the right
PEN = (f'fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" '
       f'stroke-linejoin="round" filter="url(#pg-wob)"')
BLUE_PEN = (f'fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-linecap="round" '
            f'stroke-linejoin="round" filter="url(#pg-wob)"')


# ---------------------------------------------------------------- primitives
def g(body, attrs=""):
    return f"<g {attrs}>{body}</g>" if attrs else f"<g>{body}</g>"

def beat(n, body, cls="fragment", style=""):
    st = f' style="{style}"' if style else ""
    return f'<g class="{cls}" data-fragment-index="{n}"{st}>{body}</g>'

def trigger(n):
    return (f'<rect width="0" height="0"><set id="pg-t{n}" class="on-reveal" '
            f'attributeName="x" to="0" begin="indefinite" dur="0.01s"/></rect>')

def at(n, s):
    """A begin time s seconds after beat n's trigger (n=0 means slide start)."""
    return f"{0.4 + s:g}s" if n == 0 else f"pg-t{n}.begin+{s:g}s"

def html(x, y, w, h, inner, cls, frag="", style=""):
    fc = f' class="{frag}"' if frag else ""
    return (f'<foreignObject x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"{fc}>'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" style="{style}">{inner}</div>'
            f'</foreignObject>')

def tag(cx, cy, text, w=200):
    return html(cx - w / 2, cy - 12, w, 24, text, "sc-tag")

def name(cx, cy, text, w=200):
    return html(cx - w / 2, cy - 12, w, 24, text, "sc-name")

def note(x, y, text, w=260, h=34, frag="", style=""):
    return html(x, y, w, h, text, "sc-note", frag, style)


# ---------------------------------------------------------------- drawings
def table_card(x, y):
    w, h = CW, CH
    return (f'<g transform="translate({x} {y})">'
            f'<rect width="{w}" height="{h}" rx="6" fill="{PAPER}" stroke="none"/>'
            f'<path d="M6 0 H{w-6} Q{w} 0 {w} 6 V16 H0 V6 Q0 0 6 0 Z" fill="url(#pg-hatch)" stroke="none"/>'
            f'<rect width="{w}" height="{h}" rx="6"/>'
            f'<path d="M0 16 H{w}" stroke-width="2"/>'
            f'<path d="M30 16 V{h}" stroke-width="1.6"/>'
            f'<path d="M8 30 H22 M8 42 H22 M8 54 H22 M38 30 H{w-10} M38 42 H{w-10} M38 54 H{w-26}" stroke-width="1.6"/>'
            f'</g>')

def set_card(x, y):
    w, h = CW, CH
    edge = f"M16 0 H{w-6} Q{w} 0 {w} 6 V{h-6} Q{w} {h} {w-6} {h} H16 L0 {h-16} V16 Z"
    dots = "".join(f'<circle cx="34" cy="{yy}" r="2.8" fill="{INK}" stroke="none"/>' for yy in (20, 34, 48))
    return (f'<g transform="translate({x} {y})">'
            f'<path d="{edge}" fill="{PAPER}" stroke="none"/>'
            f'<path d="M{w-30} 0 H{w-6} Q{w} 0 {w} 6 V{h-6} Q{w} {h} {w-6} {h} H{w-30} Z" fill="url(#pg-hatch)" stroke="none"/>'
            f'<path d="{edge}"/><circle cx="14" cy="{h/2}" r="4.5" stroke-width="2"/>{dots}'
            f'<path d="M42 20 H{w-36} M42 34 H{w-36} M42 48 H{w-44}" stroke-width="1.8"/>'
            f'</g>')

def version(base, k):
    return (base[0] + OFF[0] * k, base[1] + OFF[1] * k)

def person(cx, cy, laptop=False):
    s = (f'<circle cx="{cx}" cy="{cy}" r="12"/>'
         f'<path d="M{cx-21} {cy+36} C {cx-19} {cy+17}, {cx+19} {cy+17}, {cx+21} {cy+36}"/>')
    if laptop:
        s += (f'<path d="M{cx+14} {cy+36} H{cx+50} M{cx+18} {cy+36} L{cx+24} {cy+14} '
              f'H{cx+48} L{cx+44} {cy+36}" stroke-width="2.5"/>')
    return s

def cylinder(cx, cy):
    rx, ry, hh = 32, 9, 52
    top = cy - hh / 2
    side = f"M{cx-rx} {top} V{top+hh} A{rx} {ry} 0 0 0 {cx+rx} {top+hh} V{top}"
    return (f'<path d="{side} Z" fill="url(#pg-hatch)" stroke="none"/>'
            f'<ellipse cx="{cx}" cy="{top}" rx="{rx}" ry="{ry}" fill="{PAPER}"/>'
            f'<path d="{side}"/>'
            f'<path d="M{cx-rx} {top+hh/2} A{rx} {ry} 0 0 0 {cx+rx} {top+hh/2}" stroke-width="1.6"/>')

def frame(x0, y0, x1, y1, ident):
    return (f'<rect id="{ident}" x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="18"/>'
            f'<use href="#{ident}" transform="translate(2 2)" opacity="0.4"/>')

def dashboard(cx, cy):
    x0, y0 = cx - 58, cy - 38
    bars = "".join(
        f'<rect x="{x0+bx}" y="{y0+66-bh}" width="16" height="{bh}" fill="url(#pg-hatch)" stroke-width="2"/>'
        for bx, bh in ((16, 24), (40, 40), (64, 16)))
    return (f'<rect x="{x0}" y="{y0}" width="116" height="76" rx="7" fill="{PAPER}"/>{bars}'
            f'<path d="M{cx} {cy+38} V{cy+56} M{cx-28} {cy+56} H{cx+28}"/>')

def curve(p0, c1, c2, p1):
    return f"M{p0[0]} {p0[1]} C {c1[0]} {c1[1]}, {c2[0]} {c2[1]}, {p1[0]} {p1[1]}"

def arrow(p0, c1, c2, p1, width=3, pencil=False):
    d = curve(p0, c1, c2, p1)
    dx, dy = p1[0] - c2[0], p1[1] - c2[1]
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    hx, hy = [], []
    for sgn in (1, -1):
        a = math.radians(26) * sgn
        rx, ry = ux * math.cos(a) - uy * math.sin(a), ux * math.sin(a) + uy * math.cos(a)
        hx.append(p1[0] - 13 * rx); hy.append(p1[1] - 13 * ry)
    head = f"M{hx[0]:.1f} {hy[0]:.1f} L{p1[0]} {p1[1]} L{hx[1]:.1f} {hy[1]:.1f}"
    sw = f' stroke-width="{width}"' if width != 3 else ""
    return f'<path d="{d}"{sw}/><path d="{head}"{sw}/>', d

def rev(p0, c1, c2, p1):
    return curve(p1, c2, c1, p0)

def pin(p0, c1, c2, p1):
    d = curve(p0, c1, c2, p1)
    return (f'<path d="{d}" stroke-width="1.8"/>'
            f'<circle cx="{p1[0]}" cy="{p1[1]}" r="5" fill="{INK}" stroke="none"/>'), d


# ---------------------------------------------------------------- motion
def pulse(d, begin, dur=1.3):
    return (f'<circle r="5.5" fill="{ORANGE}" opacity="0">'
            f'<animateMotion path="{d}" begin="{begin}" dur="{dur}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.25 1"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.88;1" '
            f'begin="{begin}" dur="{dur}s" fill="freeze"/></circle>')

def arrive(body, begin, dy=-46):
    return (f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{begin}" dur="0.45s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" '
            f'begin="{begin}" dur="0.85s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines="0.22 0.61 0.36 1"/>{body}</g>')

def spark(cx, cy, begin, r1=44):
    return (f'<circle cx="{cx}" cy="{cy}" r="6" fill="none" stroke="{ORANGE}" stroke-width="2.5" opacity="0">'
            f'<animate attributeName="r" values="6;{r1}" begin="{begin}" dur="1.2s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="0.9;0" begin="{begin}" dur="1.2s" fill="freeze"/></circle>')


# ---------------------------------------------------------------- the scene
def study(dy, name, ident):
    """Geometry for one study row; dy shifts the whole row."""
    s = dict(dy=dy, name=name, ident=ident)
    s["edc"] = (90, 182 + dy)
    s["frame"] = (170, 60 + dy, 720, 300 + dy)
    s["lb"] = (245, 150 + dy)
    s["adlb"] = (535, 150 + dy)
    s["dev"] = (440, 100 + dy)
    s["dev2"] = (482, 100 + dy)
    s["edc_link"] = ((126, 184 + dy), (165, 176 + dy), (200, 192 + dy), (241, 186 + dy))
    s["derive"] = ((343, 198 + dy), (400, 210 + dy), (470, 210 + dy), (531, 198 + dy))
    # where a pin lands on each adlb version (a strip that stays visible)
    s["pin_v2"] = (628, 194 + dy)
    s["pin_v3"] = (650, 170 + dy)
    return s

S1 = study(0, "STUDY_001", "pg-f1")
S2 = study(380, "STUDY_002", "pg-f2")
POOL = dict(frame=(900, 300, 1440, 510), set=(950, 370), out=(1230, 370), dev=(1137, 336))
DASH = (1240, 610)
STAT = (850, 112)

def study_static(s, versions_lb, versions_adlb, with_dev=True):
    """Draw a study as it stands, no motion (used for study 2's first appearance)."""
    body = frame(*s["frame"], s["ident"]) + cylinder(*s["edc"])
    a, _ = arrow(*s["edc_link"])
    body += a
    if with_dev:
        d, _ = arrow(*s["derive"])
        body += d + person(*s["dev"])
    for k in range(versions_lb):
        body += table_card(*version(s["lb"], k))
    for k in range(versions_adlb):
        body += table_card(*version(s["adlb"], k))
    labels = (html(182, s["frame"][1] + 6, 200, 24, s["name"], "sc-tag sc-left")
              + tag(s["edc"][0], s["edc"][1] + 50, "EDC", 120)
              + name(s["lb"][0] + CW / 2, s["lb"][1] + CH + 16, "lb", 100)
              + name(s["adlb"][0] + CW / 2, s["adlb"][1] + CH + 16, "adlb", 100))
    if with_dev:
        labels += tag(s["dev"][0], s["dev"][1] + 136, "programmer", 160)
    return g(body, PEN) + labels


parts = []

# -- beat 0 (on arrival): one study, one extract -----------------------------
s = S1
_, d_edc1 = arrow(*s["edc_link"])
b0 = g(frame(*s["frame"], s["ident"]) + cylinder(*s["edc"]) + arrow(*s["edc_link"])[0], PEN)
b0 += arrive(g(table_card(*s["lb"]), PEN), at(0, 0.9))
b0 += pulse(d_edc1, at(0, 0.2), 1.1)
b0 += (html(182, s["frame"][1] + 6, 200, 24, s["name"], "sc-tag sc-left")
       + tag(s["edc"][0], s["edc"][1] + 50, "EDC", 120)
       + name(s["lb"][0] + CW / 2, s["lb"][1] + CH + 16, "lb", 100))
b0 += beat(1, note(560, 14, "one datom project", 220), cls="fragment fade-out")
b0 += beat(1, g(f'<path d="M640 44 C 650 52, 662 56, 668 62"/>'
                f'<path d="M660 60 L669 63 L668 53"/>',
                BLUE_PEN), cls="fragment fade-out")
parts.append(b0)

# -- beat 1: a programmer derives liver labs ----------------------------------
a1, d_der1 = arrow(*s["derive"])
b1 = trigger(1) + g(a1 + person(*s["dev"]), PEN)
b1 += arrive(g(table_card(*s["adlb"]), PEN), at(1, 1.0))
b1 += pulse(d_der1, at(1, 0.15), 1.1)
b1 += (name(s["adlb"][0] + CW / 2, s["adlb"][1] + CH + 16, "adlb", 100)
       + beat(6, tag(s["dev"][0], s["dev"][1] + 136, "programmer", 160), cls="fragment fade-out"))
parts.append(beat(1, b1))

# -- beat 2: next month's extract; nothing is overwritten ---------------------
b2 = trigger(2)
b2 += pulse(d_edc1, at(2, 0.1), 1.1)
b2 += arrive(g(table_card(*version(s["lb"], 1)), PEN), at(2, 0.8))
b2 += pulse(d_der1, at(2, 1.5), 1.1)
b2 += arrive(g(table_card(*version(s["adlb"], 1)), PEN), at(2, 2.3))
b2 += beat(2, note(176, 248, "v1 is still here", 200)
           + g('<path d="M210 252 C 214 238, 226 228, 240 221"/><path d="M229 220 L241 220 L236 231"/>',
               BLUE_PEN), cls="fragment fade-in-then-out")
parts.append(beat(2, b2))

# -- beat 3: readers just read --------------------------------------------------
a3, d_read = arrow((652, 152), (712, 132), (770, 124), (812, 128))
b3 = trigger(3) + g(a3 + person(*STAT, laptop=True), PEN)
b3 += pulse(d_read, at(3, 0.2), 1.1)
b3 += tag(STAT[0] + 10, STAT[1] + 58, "statistician", 180)
parts.append(beat(3, b3))

# -- beat 4: same therapy, a second study (camera pulls back) -----------------
s2 = S2
_, d_edc2 = arrow(*s2["edc_link"])
_, d_der2 = arrow(*s2["derive"])
b4 = trigger(4) + study_static(s2, 2, 2)
b4 += pulse(d_edc2, at(4, 1.4), 1.1) + pulse(d_der2, at(4, 2.2), 1.1)
parts.append(beat(4, b4, style="transition-delay: 0.9s"))

# -- beat 5: one set pools both, at exact versions -----------------------------
P = POOL
setv1, outv1 = P["set"], P["out"]
pin1, _ = pin((950, 392), (860, 380), (720, 214), S1["pin_v2"])
pin2, _ = pin((950, 410), (860, 430), (720, 560), S2["pin_v2"])
a5, d_pool = arrow((1048, 404), (1110, 418), (1170, 418), (1226, 404))
a5d, d_dash = arrow((1040, 442), (1052, 560), (1100, 612), (1176, 612))
b5 = trigger(5)
b5 += g(frame(*P["frame"], "pg-f3") + a5 + person(*P["dev"]) + a5d + dashboard(*DASH), PEN)
b5 += beat(7, g(pin1 + pin2, PEN), cls="fragment semi-fade-out")
b5 += arrive(g(set_card(*setv1), PEN), at(5, 0.2))
# pulses travel from the studies into the set, so run the pin paths backwards
b5 += pulse(rev((950, 392), (860, 380), (720, 214), S1["pin_v2"]), at(5, 0.9), 1.1)
b5 += pulse(rev((950, 410), (860, 430), (720, 560), S2["pin_v2"]), at(5, 0.9), 1.1)
b5 += pulse(d_pool, at(5, 2.0), 1.0)
b5 += arrive(g(table_card(*outv1), PEN), at(5, 2.8))
b5 += pulse(d_dash, at(5, 3.6), 1.0)
b5 += (html(912, 306, 200, 24, "LIVER_POOL", "sc-tag sc-left")
       + name(setv1[0] + CW / 2, setv1[1] + CH + 16, "set", 100)
       + name(outv1[0] + CW / 2, outv1[1] + CH + 16, "liver_pool", 160)
       + tag(P["dev"][0], 454, "programmer", 160)
       + tag(DASH[0], DASH[1] + 74, "program dashboard", 240))
b5 += beat(7, html(DASH[0] - 52, DASH[1] - 34, 104, 22, "set v1", "sc-screen"), cls="fragment fade-out")
b5 += beat(5, note(742, 372, "the set pins<br/>exact versions", 160, 64), cls="fragment fade-in-then-out")
parts.append(beat(5, b5))

# -- beat 6: months go by; nothing pinned moves --------------------------------
b6 = trigger(6) + g(person(*S1["dev2"]), PEN) + tag(S1["dev"][0], S1["dev"][1] + 136, "two programmers", 220)
for i, st in enumerate((S1, S2)):
    _, de = arrow(*st["edc_link"])
    _, dd = arrow(*st["derive"])
    t0 = 0.2 + 0.5 * i
    b6 += pulse(de, at(6, t0), 1.1)
    b6 += arrive(g(table_card(*version(st["lb"], 2)), PEN), at(6, t0 + 0.7))
    b6 += pulse(dd, at(6, t0 + 1.3), 1.1)
    b6 += arrive(g(table_card(*version(st["adlb"], 2)), PEN), at(6, t0 + 2.1))
b6 += beat(6, note(736, 196, "the set still pins v2", 240)
           + g('<path d="M742 214 C 712 210, 676 204, 642 198"/><path d="M652 192 L641 198 L651 205"/>',
               BLUE_PEN), cls="fragment fade-in-then-out")
b6 += beat(6, note(872, 636, "the dashboard hasn't moved", 280)
           + g('<path d="M1144 654 C 1156 652, 1166 648, 1176 642"/><path d="M1165 637 L1177 642 L1167 649"/>',
               BLUE_PEN), cls="fragment fade-in-then-out")
parts.append(beat(6, b6))

# -- beat 7: release; one write moves the set, code and all --------------------
setv2, outv2 = version(setv1, 1), version(outv1, 1)
p1b = ((968, 376), (870, 362), (740, 186), S1["pin_v3"])
p2b = ((968, 394), (870, 414), (740, 540), S2["pin_v3"])
pin1b, _ = pin(*p1b)
pin2b, _ = pin(*p2b)
b7 = trigger(7)
b7 += pulse(rev(*p1b), at(7, 0.2), 1.1) + pulse(rev(*p2b), at(7, 0.2), 1.1)
b7 += arrive(g(pin1b + pin2b, PEN), at(7, 0.9), dy=0)
b7 += arrive(g(set_card(*setv2), PEN), at(7, 0.9))
b7 += pulse(d_pool, at(7, 1.8), 1.0)
b7 += arrive(g(table_card(*outv2), PEN), at(7, 2.6))
b7 += pulse(d_dash, at(7, 3.3), 1.0)
b7 += arrive(html(DASH[0] - 52, DASH[1] - 34, 104, 22, "set v2", "sc-screen"), at(7, 4.2), dy=0)
b7 += spark(DASH[0], DASH[1], at(7, 4.2), 70)
b7 += beat(7, note(752, 528, "set + code,<br/>one commit", 160, 64)
           + g('<path d="M868 540 C 900 520, 930 470, 956 432"/><path d="M944 436 L957 431 L956 444"/>',
               BLUE_PEN), cls="fragment fade-in-then-out")
parts.append(beat(7, b7))

# -- beat 8: the same six months, in folders ------------------------------------
files = [
    (200, 128, -7, "lb_jan.sas7bdat"), (214, 166, 5, "lb_feb.sas7bdat"), (196, 204, -3, "lb_feb_RERUN.sas7bdat"),
    (500, 124, 4, "adlb_final.sas7bdat"), (522, 162, -6, "adlb_final_v2"), (506, 200, 3, "adlb_v2_USE_THIS"),
    (204, 512, -4, "lb_002_mar.sas7bdat"), (500, 506, 5, "adlb_002_final"), (520, 546, -2, "adlb_002 (copy)"),
    (496, 586, 6, "adlb_002_final_JM"), (950, 360, -5, "liver_pool_v3_JM.xlsx"), (1150, 398, 4, "pool_OLD_do_not_use"),
    (1000, 440, -3, "pool_with_002_feb?"), (1220, 448, 6, "liver_pool_FINAL"), (1150, 596, -4, "dashboard_data_latest(2).csv"),
]
b8 = f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}" opacity="0.86"/>'
for x, y, r, fname in files:
    b8 += html(x, y - 12, 280, 58, f"<span>{fname}</span>", "sc-file", style=f"transform: rotate({r}deg)")
for x, y in ((182, 140), (436, 236), (800, 300), (800, 470), (1090, 540), (760, 120)):
    b8 += html(x, y, 40, 50, "?", "sc-q")
b8 += note(880, 236, "which copy fed which?", 300) + note(800, 70, "which one did you use?", 280)
parts.append(beat(8, b8))

defs = (f'<defs>'
        f'<filter id="pg-wob" x="-5%" y="-5%" width="110%" height="110%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="5" result="noise"/>'
        f'<feDisplacementMap in="SourceGraphic" in2="noise" scale="4" xChannelSelector="R" yChannelSelector="G"/>'
        f'</filter>'
        f'<pattern id="pg-hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<line x1="0" y1="0" x2="0" y2="9" stroke="{HATCH}" stroke-width="1.4"/></pattern>'
        f'</defs>')

svg = (f'<svg class="scene" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
       f'aria-label="Two clinical studies and a pooled liver-safety set, versioned over six months">'
       f'{defs}{"".join(parts)}</svg>\n')
OUT.write_text(svg)
print(f"wrote {OUT} ({len(svg)/1024:.0f} KB)")
