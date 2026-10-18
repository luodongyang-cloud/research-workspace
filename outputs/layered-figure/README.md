# Layered 2TG1C1S schematic

- [High-resolution PNG](2TG1C1S_layered.png)
- [Editable SVG](2TG1C1S_layered.svg)
- [Vector PDF](2TG1C1S_layered.pdf)
- [Generation script](generate_layered_figure.py)
- [Caption and design assumptions](design-notes.md)

The diagram uses editable vector shapes and text. The PDF contains no raster images. PNG dimensions: 3240 × 2160 pixels. Functional layers are conceptual, not a physical 3D stack. All traces and score marks are schematic rather than measured.

## Reproduce

Requires Python 3 and CairoSVG for PDF/PNG export.

```sh
python -m pip install cairosvg
python generate_layered_figure.py
```

SVG units map to a 183 × 122 mm landscape page. Perspective is intentionally used to express functional layers per the author brief. SVG text is live; fonts are DejaVu Sans with Arial/sans-serif fallbacks. The main labels and panel letters use a larger hierarchy than ordinary text; the audit explicitly permits text up to 9 pt.

Download using GitHub’s **Download raw file** button.
