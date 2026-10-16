"""Shared draw.io helpers for the Presentation 1 figures: add shapes, then save() writes .drawio and exports PNG."""
import os
import subprocess
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DRAWIO_PATHS = [r"C:\Program Files\draw.io\draw.io.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Programs\draw.io\draw.io.exe")]
FONT = "Segoe UI"

cells = []
_id = [1]


def nid():
    _id[0] += 1
    return f"c{_id[0]}"


def add(value, style, x, y, w, h):
    i = nid()
    cells.append(
        f'<mxCell id="{i}" value="{escape(value, {chr(34): "&quot;"})}" style="{style}" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
    )
    return i


def text(value, x, y, w, h, size=14, bold=False, align="center", color="#222222"):
    style = (f"text;html=1;whiteSpace=wrap;align={align};verticalAlign=middle;fontColor={color};"
             f"fontSize={size};fontFamily={FONT};{'fontStyle=1;' if bold else ''}")
    return add(value, style, x, y, w, h)


def box(label, x, y, w, h, fill="#FFFFFF", stroke="#999999", where="top", sw=1, dashed=False, size=15):
    style = (f"rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={sw};"
             f"verticalAlign={where};align=left;spacingLeft=10;spacingTop=4;spacingBottom=4;fontStyle=1;"
             f"fontSize={size};fontFamily={FONT};fontColor=#222222;{'dashed=1;' if dashed else ''}")
    return add(label, style, x, y, w, h)


def card(label, x, y, w, h):
    style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;"
             f"fontSize=14;fontFamily={FONT};fontColor=#222222;")
    return add(label, style, x, y, w, h)


LABEL = {}


def icon(path, label, x, y, size=64, lw=180, pos="below", lh=54):
    """Add an icon and its label; LABEL[icon id] = label id, so an edge can start below the label."""
    i = add("", "image;aspect=fixed;html=1;points=[];image=img/lib/azure2/" + path + ".svg;", x, y, size, size)
    if pos == "below":
        LABEL[i] = text(label, x + size / 2 - lw / 2, y + size + 4, lw, lh)
    elif pos == "above":
        LABEL[i] = text(label, x + size / 2 - lw / 2, y - 58, lw, 54)
    elif pos == "right":
        LABEL[i] = text(label, x + size + 8, y, lw, size, align="left")
    return i


def edge(src, dst, label="", exit=None, entry=None, dashed=False, points=None, color="#333333", at=0):
    """at: label position along the edge, -1 = source end, 0 = middle, 1 = target end."""
    i = nid()
    style = (f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;strokeWidth=2;"
             f"strokeColor={color};fontSize=13;fontFamily={FONT};fontColor=#C00000;fontStyle=1;"
             f"labelBackgroundColor=#FFFFFF;{'dashed=1;' if dashed else ''}")
    if exit:
        style += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
    if entry:
        style += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    pts = ""
    if points:
        pts = '<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + "</Array>"
    cells.append(
        f'<mxCell id="{i}" value="{escape(label)}" style="{style}" edge="1" parent="1" source="{src}" target="{dst}">'
        f'<mxGeometry relative="1" x="{at}" as="geometry">{pts}</mxGeometry></mxCell>'
    )


def save(name, width=1280, height=720):
    """Write <name>.drawio, export <name>.png (scale 2) when draw.io desktop is installed, then start a fresh canvas."""
    out = os.path.join(HERE, name + ".drawio")
    png = os.path.join(HERE, name + ".png")
    xml = (
        f'<mxfile host="drawio_lib.py"><diagram name="{name}" id="{name}">'
        f'<mxGraphModel dx="{width}" dy="{height}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" '
        f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" '
        f'background="#FFFFFF" math="0" shadow="0">'
        '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>"
    )
    with open(out, "w", encoding="utf-8") as f:
        f.write(xml)
    print("wrote", out)
    drawio = next((p for p in DRAWIO_PATHS if os.path.exists(p)), None)
    if drawio:
        subprocess.run([drawio, "-x", "-f", "png", "-s", "2", "-o", png, out], check=True)
        print("wrote", png)
    cells.clear()
    LABEL.clear()
