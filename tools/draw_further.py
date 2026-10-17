"""Draw sketches/further.svg: the "Beyond faster and cheaper" scene.

Left, faster and cheaper: a set box with a castle on its lid, the same castle
built beside it, and a stopwatch whose hand sweeps. Right, further: two sets
built as two towers, then a bridge between them that uses both sets' bricks and
that no box ever showed.

Beats (data-fragment-index):
  1  the box, the castle it shows, and the stopwatch
  2  two sets, two towers: set A hatched, set B plain
  3  the bridge: each set's deck reaches halfway; one brick on top spans the gap

Run: python tools/draw_further.py   (edit this file, not the SVG)
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "sketches" / "further.svg"

W, H = 1500, 600
INK, HATCH, BLUE, ORANGE, PAPER = "#3A3834", "#8C877D", "#2F6690", "#C8692E", "#F5F1E8"
PEN = (f'fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" '
       f'stroke-linejoin="round" filter="url(#fu-wob)"')

# isometric brick grid, scaled from the baseplate's brick (39.8 / 23 / 55.2)
S = 0.8
U, V, BH = 39.8 * S, 23 * S, 55.2 * S
SRX, SRY, SH = 16.9 * S, 9.8 * S, 9.7 * S


# ---------------------------------------------------------------- primitives
def beat(n, body):
    return f'<g class="fragment" data-fragment-index="{n}">{body}</g>'

def trigger(n):
    return (f'<rect width="0" height="0"><set id="fu-t{n}" class="on-reveal" '
            f'attributeName="x" to="0" begin="indefinite" dur="0.01s"/></rect>')

def at(n, s):
    return f"fu-t{n}.begin+{s:g}s"

def html(x, y, w, h, inner, cls, style=""):
    return (f'<foreignObject x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{cls}" style="{style}">{inner}</div>'
            f'</foreignObject>')

def tag(x, y, text, w=320, left=True, color=None):
    style = ("justify-content: flex-start;" if left else "") + (f" color: {color};" if color else "")
    return html(x, y - 12, w, 24, text, "sc-tag", style)

def note(x, y, text, w=320, h=40, center=False):
    return html(x, y, w, h, text, "sc-note", "text-align: center;" if center else "")

def pts(*ps):
    return " ".join(f"{x:.1f} {y:.1f}" for x, y in ps)


class Iso:
    """An isometric grid anchored at (ox, oy): grid x runs down-right, y down-left, z up."""
    def __init__(self, ox, oy):
        self.ox, self.oy = ox, oy

    def p(self, gx, gy, z):
        return (self.ox + (gx - gy) * U, self.oy + (gx + gy) * V - z * BH)

    def brick(self, gx, gy, z, w, d, hatch=False, h=1, studs=True):
        p = self.p
        z1 = z + h
        a, b = p(gx, gy, z1), p(gx + w, gy, z1)
        c, e = p(gx + w, gy + d, z1), p(gx, gy + d, z1)
        b0, c0, e0 = p(gx + w, gy, z), p(gx + w, gy + d, z), p(gx, gy + d, z)
        out = [f'<path d="M{pts(a, b, b0, c0, e0, e)} Z" fill="{PAPER}" stroke="none"/>']
        if hatch:
            out.append(f'<path d="M{pts(e, c, c0, e0)} Z" fill="url(#fu-hatch)" stroke="none"/>')
            out.append(f'<path d="M{pts(c, b, b0, c0)} Z" fill="url(#fu-hatch)" stroke="none" opacity="0.55"/>')
        out.append(f'<path d="M{pts(a, b, b0, c0, e0, e)} Z"/>')
        out.append(f'<path d="M{pts(e, c, b)} M{pts(c, c0)}"/>')
        if studs:
            for i in range(w):
                for j in range(d):
                    cx, cy = p(gx + i + 0.5, gy + j + 0.5, z1)
                    top = cy - SH
                    out.append(f'<path d="M{cx - SRX:.1f} {top:.1f} L{cx - SRX:.1f} {cy:.1f} '
                               f'A{SRX:.1f} {SRY:.1f} 0 0 0 {cx + SRX:.1f} {cy:.1f} L{cx + SRX:.1f} {top:.1f}" '
                               f'fill="{PAPER}" stroke-width="2.2"/>')
                    out.append(f'<ellipse cx="{cx:.1f}" cy="{top:.1f}" rx="{SRX:.1f}" ry="{SRY:.1f}" '
                               f'fill="{PAPER}" stroke-width="2.2"/>')
        return "".join(out)


# ---------------------------------------------------------------- the castle
# (gx, gy, z, w, d): two towers, a wall between them, and crenels; back to front
CASTLE = [
    (0, 0, 0, 2, 2), (2, 1, 0, 3, 1), (5, 0, 0, 2, 2),
    (0, 0, 1, 2, 2), (2, 1, 1, 3, 1), (5, 0, 1, 2, 2),
    (0, 0, 2, 2, 2), (2, 1, 2, 1, 1), (4, 1, 2, 1, 1), (5, 0, 2, 2, 2),
]

def castle(iso):
    order = sorted(CASTLE, key=lambda b: (b[2], b[0] + b[1]))
    return "".join(iso.brick(*b) for b in order)

def castle_front(x, y, s):
    """The castle as the box lid shows it: a flat front view, s pixels per stud."""
    t = s * 1.1                       # one brick's height on the lid
    w, h = 7 * s, 3 * t
    # towers are three bricks tall; the wall between them two, with a crenel at each end
    sil = [(x, y + h), (x, y), (x + 3 * s, y), (x + 3 * s, y + t),
           (x + 4 * s, y + t), (x + 4 * s, y), (x + w, y), (x + w, y + h)]
    door = (f'M{x + 3 * s:.1f} {y + h:.1f} L{x + 3 * s:.1f} {y + h - 0.55 * t:.1f} '
            f'Q{x + 3.5 * s:.1f} {y + h - 1.05 * t:.1f} {x + 4 * s:.1f} {y + h - 0.55 * t:.1f} L{x + 4 * s:.1f} {y + h:.1f}')
    rows = (f'M{x:.1f} {y + t:.1f} L{x + 3 * s:.1f} {y + t:.1f} M{x + 4 * s:.1f} {y + t:.1f} L{x + w:.1f} {y + t:.1f} '
            f'M{x:.1f} {y + 2 * t:.1f} L{x + w:.1f} {y + 2 * t:.1f} '
            f'M{x + 2 * s:.1f} {y:.1f} L{x + 2 * s:.1f} {y + h:.1f} M{x + 5 * s:.1f} {y:.1f} L{x + 5 * s:.1f} {y + h:.1f}')
    return (f'<path d="M{pts(*sil)} Z" fill="{PAPER}"/>'
            f'<path d="{door}" stroke-width="2.2"/>'
            f'<path d="{rows}" stroke-width="1.8"/>'
            f'<path d="M{x - 10:.1f} {y + h:.1f} L{x + w + 10:.1f} {y + h:.1f}" stroke-width="2.2"/>')

def set_box(x, y, w, h):
    """A set box, face on, with the castle on its lid."""
    return (f'<rect id="fu-box" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{PAPER}"/>'
            f'<use href="#fu-box" transform="translate(2 2)" opacity="0.4"/>'
            f'<path d="M{x + w} {y + 12} L{x + w + 26} {y - 8} L{x + w + 26} {y + h - 20} L{x + w} {y + h}" fill="url(#fu-hatch)"/>'
            f'<path d="M{x + 12} {y} L{x + 38} {y - 20} L{x + w + 26} {y - 20} L{x + w + 26} {y - 8}" />'
            f'<rect x="{x + 16}" y="{y + 16}" width="{w - 32}" height="{h - 32}" rx="6" stroke-width="2" stroke-dasharray="2 7"/>'
            + castle_front(x + (w - 7 * 22) / 2, y + 70, 22))

def stopwatch(cx, cy, r):
    hand = (f'<g><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 9}" stroke="{ORANGE}" stroke-width="3.2"/>'
            f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" '
            f'begin="{at(1, 0.6)}" dur="1.6s" repeatCount="indefinite"/></g>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}"/>'
            f'<path d="M{cx - 7} {cy - r - 12} L{cx + 7} {cy - r - 12} M{cx} {cy - r - 12} L{cx} {cy - r}" />'
            f'<path d="M{cx + r * 0.72:.1f} {cy - r * 0.72:.1f} L{cx + r * 0.9:.1f} {cy - r * 0.9:.1f}" />'
            f'<path d="M{cx} {cy - r + 4} L{cx} {cy - r + 9} M{cx + r - 4} {cy} L{cx + r - 9} {cy} '
            f'M{cx} {cy + r - 4} L{cx} {cy + r - 9} M{cx - r + 4} {cy} L{cx - r + 9} {cy}" stroke-width="2"/>'
            + hand + f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{INK}" stroke="none"/>')


# ---------------------------------------------------------------- the bridge
def bridge_towers(iso):
    out = []
    for z in range(3):
        out.append(iso.brick(0, 0, z, 2, 2, hatch=True))
    for z in range(3):
        out.append(iso.brick(6, 0, z, 2, 2))
    return "".join(out)

def bridge_deck(iso):
    # each set reaches halfway; one brick on top clutches both halves and closes the gap
    deck = iso.brick(0, 0, 3, 4, 2, hatch=True) + iso.brick(4, 0, 3, 4, 2)
    top = iso.brick(2, 0, 4, 4, 2)
    drop = (f'<g opacity="0" transform="translate(0 -70)">{top}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{at(3, 0.9)}" dur="0.3s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 -70" to="0 0" '
            f'begin="{at(3, 0.9)}" dur="0.8s" calcMode="spline" keySplines="0.3 0 0.4 1" fill="freeze"/></g>')
    return deck + drop


# ---------------------------------------------------------------- the scene
def build():
    # no wobble filter here: a filter on a zero-width box renders nothing
    divider = (f'<path d="M770 70 L770 560" fill="none" stroke="{HATCH}" stroke-width="2.4" '
               f'stroke-dasharray="4 10" stroke-linecap="round"/>')

    left_iso = Iso(475, 300)
    b1 = (trigger(1) + divider
          + f'<g {PEN}>{set_box(60, 250, 240, 210)}{castle(left_iso)}{stopwatch(705, 150, 32)}</g>'
          + tag(60, 40, "faster and cheaper")
          + html(50, 476, 260, 26, "the set", "sc-tag", "")
          + note(350, 505, "the same castle, sooner", 400, center=True))

    right_iso = Iso(1035, 290)
    b2 = (trigger(2)
          + f'<g {PEN}>{bridge_towers(right_iso)}</g>'
          + tag(830, 40, "further")
          + html(right_iso.p(1, 1, 0)[0] - 90, right_iso.p(2, 2, 0)[1] + 14, 180, 26, "set a", "sc-tag", "")
          + html(right_iso.p(7, 1, 0)[0] - 90, right_iso.p(8, 2, 0)[1] + 14, 180, 26, "set b", "sc-tag", ""))

    b3 = (trigger(3)
          + f'<g {PEN}>{bridge_deck(right_iso)}</g>'
          + note(980, 520, "no box had this", 300, center=True))

    return (f'<svg class="scene" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
            f'style="overflow: visible" role="img" aria-label="Left: a set box showing a castle, the same '
            f'castle built beside it, and a stopwatch. Right: two towers from two different sets, joined by a '
            f'bridge built from both sets&apos; bricks.">\n'
            f'  <defs>\n'
            f'    <filter id="fu-wob" x="-10%" y="-10%" width="120%" height="120%">\n'
            f'      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="29" result="noise"/>\n'
            f'      <feDisplacementMap in="SourceGraphic" in2="noise" scale="4" xChannelSelector="R" yChannelSelector="G"/>\n'
            f'    </filter>\n'
            f'    <pattern id="fu-hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">\n'
            f'      <line x1="0" y1="0" x2="0" y2="9" stroke="{HATCH}" stroke-width="1.4"/>\n'
            f'    </pattern>\n'
            f'  </defs>\n'
            f'  <!-- generated by tools/draw_further.py: edit that, not this -->\n'
                        f'  {beat(1, b1)}\n  {beat(2, b2)}\n  {beat(3, b3)}\n'
            f'</svg>\n')


if __name__ == "__main__":
    OUT.write_text(build())
    print(f"wrote {OUT}")
