#!/usr/bin/env python3
"""Regenerate the owner-directed Galactica.com lockup. Requires fonttools[woff]."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT=Path(__file__).resolve().parents[1]
font=instantiateVariableFont(TTFont(ROOT/'assets/fonts/red-hat-display-latin-variable.woff2'),{'wght':700},inplace=False)
glyphs=font.getGlyphSet();cmap=font.getBestCmap();x=0;paths=[]
for word in ('Galactica','com'):
    if word=='com':
        dot=f'<circle cx="{x+105}" cy="735" r="85" fill="#F7931A"/>'
        x+=270
    for char in word:
        name=cmap[ord(char)];pen=SVGPathPen(glyphs)
        glyphs[name].draw(TransformPen(pen,(1,0,0,-1,x,820)))
        paths.append(f'<path d="{pen.getCommands()}"/>')
        x+=font['hmtx'][name][0]
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x} 1020" fill="currentColor" role="img" aria-label="Galactica.com">'+''.join(paths)+dot+'</svg>\n'
(ROOT/'assets/galactica.svg').write_text(svg)
print('Generated outlined Galactica.com lockup with a bold orange dot.')
