# A standard for where clinical data lives — R/Pharma 2026

Quarto reveal.js deck, built as a small codebase.

```
_quarto.yml        deck config (1600x900, self-contained output)
index.qmd          includes slides/*.qmd in order
slides/NN-*.qmd    one file per slide (content + speaker notes)
sketches/*.svg     one pencil-sketch drawing per file, inlined into slides
theme/paper.scss   all styling: palette, type, sketch labels
js/smil.js         starts each slide's SVG motion when the slide is shown
tools/shoot.py     screenshots slides mid-animation, for checking the look
```

Render: `quarto render` → `_output/index.html` (open in a browser; `s` for speaker view).
Live edit: `quarto preview`.

Every push re-renders the deck in CI; the self-contained HTML is attached to the run as the `deck` artifact.

The deck evolves between venues. Tag the commit you present (`git tag rpharma-2026`) so that version can always be rebuilt exactly.

Sketch conventions: ~3px round-capped strokes in `#3A3834`, no fill; wobble via
`feTurbulence` + `feDisplacementMap`; shading via a 45° hatch `<pattern>`; key outlines
redrawn 2px offset at 40% opacity; orange `#C8692E` only on things that move; labels are
HTML over the SVG, never `<text>`. Each SVG prefixes its ids (`cv-`, `lh-`, …) because
inlined SVGs share one document.
