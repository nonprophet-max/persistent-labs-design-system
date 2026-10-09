#!/usr/bin/env python3
"""Extract the owner's Pi vector artwork. Optional dependency: PyMuPDF.

Normal site/skill builds use the checked-in SVGs and do not need PyMuPDF.
The drawing selections refer to the recorded, single-page source PDF.
"""
from pathlib import Path
import hashlib
import json
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/pi/brand-identity.pdf'
OUT = ROOT / 'assets/pi'
SOURCE_SHA256 = 'f7ad60d71d1fecf9433996562ede36d6e02b64ffa73b434f41e92028e58623bf'


def extract():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256, 'New source PDF: review drawing selections before extraction.'
    document = pymupdf.open(SOURCE)
    assert len(document) == 1
    drawings = document[0].get_drawings()
    selections = {
        'mark': list(range(143, 145)),
        'horizontal': list(range(123, 141)),
        'vertical': list(range(67, 85)),
        'logotype': list(range(147, 163)),
        'horizontal-dark': list(range(2, 20)),
        'horizontal-reversed': list(range(165, 182)),
    }
    assets = []
    for name, indices in selections.items():
        shapes = [drawings[i] for i in indices]
        bounds = pymupdf.Rect(shapes[0]['rect'])
        for shape in shapes[1:]:
            bounds |= shape['rect']
        def point(p):
            return f'{p.x-bounds.x0:.4f} {p.y-bounds.y0:.4f}'
        paths = []
        for shape in shapes:
            assert shape['type'] == 'f' and shape['fill_opacity'] == 1
            commands = []
            previous = None
            for item in shape['items']:
                kind = item[0]
                if kind == 're':
                    r, orientation = item[1:]
                    points = [r.tl, r.tr, r.br, r.bl] if orientation == 1 else [r.bl, r.br, r.tr, r.tl]
                    commands.append('M' + point(points[0]) + ''.join('L' + point(p) for p in points[1:]) + 'Z')
                    previous = None
                elif kind in ('l', 'c'):
                    if previous != item[1]:
                        commands.append('M' + point(item[1]))
                    commands.append(('L' if kind == 'l' else 'C') + ' '.join(point(p) for p in item[2:]))
                    previous = item[-1]
                else:
                    raise ValueError(f'Unsupported PDF path item: {kind}')
            color = '#' + ''.join(f'{round(v*255):02X}' for v in shape['fill'])
            rule = 'evenodd' if shape['even_odd'] else 'nonzero'
            paths.append(f'<path fill="{color}" fill-rule="{rule}" d="{" ".join(commands)}"/>')
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {bounds.width:.4f} {bounds.height:.4f}" role="img" aria-label="Private Inference {name.replace("-", " ")}">\n' + '\n'.join(paths) + '\n</svg>\n'
        (OUT / f'{name}.svg').write_text(svg)
        assets.append({'file': f'{name}.svg', 'drawing_indices': indices,
                       'source_bounds': list(bounds), 'sha256': hashlib.sha256(svg.encode()).hexdigest()})
    # Preserve the established asset URL while replacing the superseded concept.
    (ROOT / 'assets/privateinference.svg').write_bytes((OUT / 'mark.svg').read_bytes())
    provenance = {
        'source': 'Pi Brand Identity(upd).pdf', 'page': 1, 'owner_designation_date': '2026-10-09',
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'method': 'Extracted original filled vector paths; translated to tight viewBoxes, with source RGB colors rounded to 8-bit sRGB. No retyping, redrawing, or placeholder taglines.',
        'assets': assets,
    }
    (OUT / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(f'Extracted {len(assets)} Pi vector assets and recorded source provenance.')


if __name__ == '__main__':
    extract()
