#!/usr/bin/env python3
"""
Excalidraw file generator.

Takes a JSON diagram spec on stdin (or as a file argument) and outputs
a valid .excalidraw file that is fully editable in Excalidraw.

The spec format is minimal — just describe shapes, text, and arrows.
This script handles: random IDs, seeds, versionNonces, bidirectional
bindings, text dimension estimation, and all required boilerplate fields.
"""

import json
import sys
import random
import string
import math
from typing import Any, Optional

# --- ID Generation (nanoid-style, matches what Excalidraw actually uses) ---

NANOID_ALPHABET = string.ascii_letters + string.digits + "_-"
NANOID_LENGTH = 21


def nanoid() -> str:
    return "".join(random.choices(NANOID_ALPHABET, k=NANOID_LENGTH))


def random_seed() -> int:
    return random.randint(1, 2**31 - 1)


def random_version_nonce() -> int:
    return random.randint(1, 2**31 - 1)


# --- Text Dimension Estimation ---

CHAR_WIDTH_MULTIPLIERS = {
    1: 0.6,   # Virgil (hand-drawn)
    2: 0.55,  # Helvetica
    3: 0.6,   # Monospace (Cascadia)
    5: 0.55,  # Excalifont
}


def estimate_text_dimensions(text: str, font_size: int, font_family: int) -> tuple[int, int]:
    multiplier = CHAR_WIDTH_MULTIPLIERS.get(font_family, 0.6)
    lines = text.split("\n")
    max_line_len = max(len(line) for line in lines)
    width = math.ceil(max_line_len * font_size * multiplier) + 10
    height = math.ceil(len(lines) * font_size * 1.25)
    return width, height


# --- Dark Background Detection (BT.709 luminance) ---

def is_dark_background(hex_color: str) -> bool:
    if hex_color == "transparent" or not hex_color.startswith("#"):
        return False
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance < 128


# --- Fractional Index Generation ---
# Excalidraw uses @excalidraw/fractional-indexing with base-62 digits:
#   0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
# Integer encoding: head char sets total length:
#   'a' → 2 chars (a0..az = 62 values)
#   'b' → 3 chars (b00..bzz = 3844 values)
# Fractional parts must NOT end with '0' (the zero digit).

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def generate_indices(count: int, prefix: str = "") -> list[str]:
    """Generate `count` valid Excalidraw fractional indices in order."""
    indices = []
    for i in range(count):
        if i < 62:
            indices.append(f"a{BASE62[i]}")
        elif i < 62 + 3844:
            n = i - 62
            d1 = BASE62[n // 62]
            d2 = BASE62[n % 62]
            indices.append(f"b{d1}{d2}")
        else:
            n = i - 62 - 3844
            d1 = BASE62[n // (62 * 62)]
            d2 = BASE62[(n // 62) % 62]
            d3 = BASE62[n % 62]
            indices.append(f"c{d1}{d2}{d3}")
    return indices


# --- Element Factory ---

def make_base_element(elem_type: str, overrides: dict) -> dict:
    element = {
        "type": elem_type,
        "version": 2,
        "versionNonce": random_version_nonce(),
        "index": "a0",
        "isDeleted": False,
        "id": nanoid(),
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "x": 0,
        "y": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "width": 100,
        "height": 50,
        "seed": random_seed(),
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "boundElements": [],
        "updated": 1714400000000,
        "link": None,
        "locked": False,
    }
    element.update(overrides)
    return element


def make_rectangle(spec: dict) -> dict:
    overrides = {
        "x": spec.get("x", 0),
        "y": spec.get("y", 0),
        "width": spec.get("width", 280),
        "height": spec.get("height", 56),
        "strokeColor": spec.get("strokeColor", "#1F2937"),
        "backgroundColor": spec.get("backgroundColor", "transparent"),
        "strokeWidth": spec.get("strokeWidth", 2),
        "roundness": spec.get("roundness", None),
        "boundElements": [],
    }
    return make_base_element("rectangle", overrides)


def make_diamond(spec: dict) -> dict:
    print("WARNING: Diamond shapes have unreliable arrow bindings in raw "
          "Excalidraw JSON. Consider using a rectangle with "
          "roundness:{type:3} instead.", file=sys.stderr)
    overrides = {
        "x": spec.get("x", 0),
        "y": spec.get("y", 0),
        "width": spec.get("width", 320),
        "height": spec.get("height", 180),
        "strokeColor": spec.get("strokeColor", "#1F2937"),
        "backgroundColor": spec.get("backgroundColor", "transparent"),
        "strokeWidth": spec.get("strokeWidth", 2),
        "roundness": spec.get("roundness", None),
        "boundElements": [],
    }
    return make_base_element("diamond", overrides)


def make_ellipse(spec: dict) -> dict:
    overrides = {
        "x": spec.get("x", 0),
        "y": spec.get("y", 0),
        "width": spec.get("width", 200),
        "height": spec.get("height", 100),
        "strokeColor": spec.get("strokeColor", "#1F2937"),
        "backgroundColor": spec.get("backgroundColor", "transparent"),
        "strokeWidth": spec.get("strokeWidth", 2),
        "roundness": spec.get("roundness", {"type": 2}),
        "boundElements": [],
    }
    return make_base_element("ellipse", overrides)


def make_text(spec: dict, container_id: Optional[str] = None) -> dict:
    text = spec.get("text", "")
    font_size = spec.get("fontSize", 20)
    font_family = spec.get("fontFamily", 3)
    width, height = estimate_text_dimensions(text, font_size, font_family)

    if spec.get("width"):
        width = spec["width"]
    if spec.get("height"):
        height = spec["height"]

    overrides = {
        "x": spec.get("x", 0),
        "y": spec.get("y", 0),
        "width": width,
        "height": height,
        "strokeColor": spec.get("strokeColor", "#1F2937"),
        "backgroundColor": "transparent",
        "strokeWidth": 1,
        "text": text,
        "fontSize": font_size,
        "fontFamily": font_family,
        "textAlign": spec.get("textAlign", "center" if container_id else "left"),
        "verticalAlign": spec.get("verticalAlign", "middle" if container_id else "top"),
        "containerId": container_id,
        "originalText": text,
        "autoResize": True,
        "lineHeight": 1.25,
        "boundElements": [],
    }
    return make_base_element("text", overrides)


def arrow_bounding_box(points: list) -> tuple[float, float]:
    """Width/height must equal the max absolute point values across ALL points."""
    if len(points) < 2:
        return 0, 0
    w = max(abs(p[0]) for p in points)
    h = max(abs(p[1]) for p in points)
    return w, h


def make_arrow(spec: dict) -> dict:
    points = spec.get("points", [[0, 0], [0, 68]])
    w, h = arrow_bounding_box(points)
    elbowed = spec.get("elbowed", False)
    overrides = {
        "x": spec.get("x", 0),
        "y": spec.get("y", 0),
        "width": w,
        "height": h,
        "strokeColor": spec.get("strokeColor", "#1F2937"),
        "strokeWidth": spec.get("strokeWidth", 1.5),
        "points": points,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": spec.get("startArrowhead", None),
        "endArrowhead": spec.get("endArrowhead", "arrow"),
        "elbowed": elbowed,
        "boundElements": [],
    }
    if elbowed:
        overrides["roughness"] = 0
        overrides["roundness"] = None
    return make_base_element("arrow", overrides)


def make_line(spec: dict) -> dict:
    points = spec.get("points", [[0, 0], [80, 0]])
    overrides = {
        "x": spec.get("x", 0),
        "y": spec.get("y", 0),
        "width": abs(points[-1][0] - points[0][0]) if len(points) > 1 else 0,
        "height": abs(points[-1][1] - points[0][1]) if len(points) > 1 else 0,
        "strokeColor": spec.get("strokeColor", "#6B7280"),
        "strokeWidth": spec.get("strokeWidth", 1),
        "strokeStyle": spec.get("strokeStyle", "dashed"),
        "points": points,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": None,
        "boundElements": [],
    }
    return make_base_element("line", overrides)


def make_frame(spec: dict) -> dict:
    overrides = {
        "x": spec.get("x", 0),
        "y": spec.get("y", 0),
        "width": spec.get("width", 600),
        "height": spec.get("height", 400),
        "strokeColor": "#bbb",
        "backgroundColor": "transparent",
        "strokeWidth": 1,
        "name": spec.get("name", None),
        "boundElements": [],
    }
    return make_base_element("frame", overrides)


# --- Validation ---

def validate_elements(elements: list[dict]) -> None:
    """Pre-flight checks that catch silent Excalidraw rendering bugs."""
    errors = []
    by_id: dict[str, dict] = {}
    ids_seen: set[str] = set()

    for elem in elements:
        eid = elem["id"]
        if eid in ids_seen:
            errors.append(f"Duplicate ID: {eid}")
        ids_seen.add(eid)
        by_id[eid] = elem

    for elem in elements:
        eid = elem["id"]
        etype = elem["type"]

        # Check text ↔ container bidirectional binding
        if etype == "text" and elem.get("containerId"):
            cid = elem["containerId"]
            container = by_id.get(cid)
            if not container:
                errors.append(f"Text {eid} references containerId {cid} which doesn't exist")
            elif not any(b["id"] == eid and b["type"] == "text" for b in container.get("boundElements", [])):
                errors.append(f"Text {eid} has containerId {cid} but container lacks matching boundElements entry")

        # Check shape boundElements text refs resolve
        for bound in elem.get("boundElements", []):
            if bound["type"] == "text":
                text_elem = by_id.get(bound["id"])
                if not text_elem:
                    errors.append(f"Element {eid} references bound text {bound['id']} which doesn't exist")
                elif text_elem.get("containerId") != eid:
                    errors.append(f"Element {eid} has bound text {bound['id']} but text's containerId is {text_elem.get('containerId')}")

        # Check arrow bindings are bidirectional
        if etype == "arrow":
            for binding_key in ("startBinding", "endBinding"):
                binding = elem.get(binding_key)
                if binding and binding.get("elementId"):
                    target = by_id.get(binding["elementId"])
                    if not target:
                        errors.append(f"Arrow {eid} {binding_key} references {binding['elementId']} which doesn't exist")
                    elif not any(b["id"] == eid and b["type"] == "arrow" for b in target.get("boundElements", [])):
                        errors.append(f"Arrow {eid} binds to {binding['elementId']} but target lacks matching boundElements entry")

            # Check arrow bbox matches points
            points = elem.get("points", [])
            if len(points) >= 2:
                expected_w = max(abs(p[0]) for p in points)
                expected_h = max(abs(p[1]) for p in points)
                if abs(elem.get("width", 0) - expected_w) > 1:
                    errors.append(f"Arrow {eid} width {elem['width']} doesn't match points (expected {expected_w})")
                if abs(elem.get("height", 0) - expected_h) > 1:
                    errors.append(f"Arrow {eid} height {elem['height']} doesn't match points (expected {expected_h})")

            # Multi-point arrows must use elbow mode
            if len(points) > 2:
                if not elem.get("elbowed"):
                    errors.append(f"Arrow {eid} has {len(points)} points but elbowed != true")
                if elem.get("roundness") is not None:
                    errors.append(f"Arrow {eid} has multi-point path but roundness != null")

            # Geometric check: arrow endpoints near bound shape edges
            for binding_key, pt_idx in [("startBinding", 0), ("endBinding", -1)]:
                binding = elem.get(binding_key)
                if not binding or not binding.get("elementId"):
                    continue
                target = by_id.get(binding["elementId"])
                if not target or target["type"] == "text":
                    continue
                px = elem["x"] + points[pt_idx][0]
                py = elem["y"] + points[pt_idx][1]
                tx, ty = target["x"], target["y"]
                tw, th = target["width"], target["height"]
                dist_to_edges = [
                    abs(py - ty) if tx <= px <= tx + tw else float("inf"),       # top
                    abs(py - (ty + th)) if tx <= px <= tx + tw else float("inf"), # bottom
                    abs(px - tx) if ty <= py <= ty + th else float("inf"),        # left
                    abs(px - (tx + tw)) if ty <= py <= ty + th else float("inf"), # right
                ]
                if min(dist_to_edges) > 15:
                    errors.append(f"Arrow {eid} {binding_key} point ({px:.0f},{py:.0f}) is {min(dist_to_edges):.0f}px from nearest edge of {binding['elementId']}")

    if errors:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        raise ValueError(f"Diagram has {len(errors)} validation error(s)")


# --- Diagram Builder ---

def build_diagram(spec: dict) -> dict:
    """
    Build a complete .excalidraw file from a diagram spec.

    Spec format:
    {
        "viewBackgroundColor": "#FAFAF7",  // optional
        "nodes": [
            {
                "ref": "step1",            // reference ID for arrows
                "type": "rectangle",       // rectangle, diamond, ellipse
                "label": "Do the thing",   // text inside the shape
                "x": 160, "y": 60,
                "width": 280, "height": 56,
                "strokeColor": "#1F2937",  // optional overrides
                "backgroundColor": "transparent",
                "fontSize": 20,
                "fontFamily": 3
            }
        ],
        "arrows": [
            {
                "from": "step1",           // ref of source node
                "to": "step2",             // ref of target node
                "label": "yes",            // optional label on arrow
                "strokeColor": "#1F2937",
                "elbowed": false,
                "points": [[0,0],[0,68]]   // optional manual points override
            }
        ],
        "annotations": [
            {
                "text": "This is important",
                "attachTo": "step1",       // ref of node to annotate
                "position": "right"        // right (default), left, above, below
            }
        ],
        "freeText": [
            {
                "text": "Title",
                "x": 100, "y": 20,
                "fontSize": 24,
                "textAlign": "left"
            }
        ]
    }
    """
    nodes = spec.get("nodes", [])
    arrows_spec = spec.get("arrows", [])
    annotations = spec.get("annotations", [])
    free_text = spec.get("freeText", [])

    elements = []
    ref_to_element: dict[str, dict] = {}
    ref_to_text: dict[str, dict] = {}

    # --- Build nodes ---
    for node_spec in nodes:
        node_type = node_spec.get("type", "rectangle")
        ref = node_spec.get("ref", nanoid())

        if node_type == "rectangle":
            shape = make_rectangle(node_spec)
        elif node_type == "diamond":
            shape = make_diamond(node_spec)
        elif node_type == "ellipse":
            shape = make_ellipse(node_spec)
        elif node_type == "frame":
            shape = make_frame(node_spec)
        else:
            shape = make_rectangle(node_spec)

        ref_to_element[ref] = shape
        elements.append(shape)

        # Create label text if specified
        label = node_spec.get("label")
        if label and node_type != "frame":
            font_size = node_spec.get("fontSize", 20)
            font_family = node_spec.get("fontFamily", 3)
            bg = node_spec.get("backgroundColor", "transparent")
            fill_style = node_spec.get("fillStyle", "solid")

            text_color = node_spec.get("labelColor", node_spec.get("strokeColor", "#1F2937"))
            if is_dark_background(bg) and fill_style == "solid":
                text_color = "#ffffff"

            _, text_height = estimate_text_dimensions(label, font_size, font_family)
            text_spec = {
                "text": label,
                "fontSize": font_size,
                "fontFamily": font_family,
                "strokeColor": text_color,
                "x": shape["x"] + 10,
                "y": shape["y"] + (shape["height"] - text_height) / 2,
                "width": shape["width"] - 20,
                "height": text_height,
            }
            text_elem = make_text(text_spec, container_id=shape["id"])
            ref_to_text[ref] = text_elem

            # Bidirectional binding
            shape["boundElements"].append({"id": text_elem["id"], "type": "text"})
            elements.append(text_elem)

    # --- Pre-compute edge stagger positions ---
    def detect_edges(fe: dict, te: dict) -> tuple[str, str]:
        """Determine which edges two shapes connect through."""
        fcx = fe["x"] + fe["width"] / 2
        tcx = te["x"] + te["width"] / 2
        d_x = tcx - fcx
        d_y = (te["y"] + te["height"] / 2) - (fe["y"] + fe["height"] / 2)
        fb = fe["y"] + fe["height"]
        fr = fe["x"] + fe["width"]
        tb = te["y"] + te["height"]
        tr = te["x"] + te["width"]
        vg = max(0, te["y"] - fb, fe["y"] - tb)
        hg = max(0, te["x"] - fr, fe["x"] - tr)
        if vg > 0 and vg >= hg:
            vert = True
        elif hg > 0 and hg > vg:
            vert = False
        else:
            vert = abs(d_y) > abs(d_x)
        if vert:
            return ("bottom", "top") if d_y > 0 else ("top", "bottom")
        return ("right", "left") if d_x > 0 else ("left", "right")

    edge_counts: dict[str, int] = {}  # "ref:edge" -> count
    for arrow_spec in arrows_spec:
        from_ref = arrow_spec.get("from")
        to_ref = arrow_spec.get("to")
        from_elem = ref_to_element.get(from_ref)
        to_elem = ref_to_element.get(to_ref)
        if not from_elem or not to_elem:
            continue
        from_edge, to_edge = detect_edges(from_elem, to_elem)
        for key in (f"{from_ref}:{from_edge}", f"{to_ref}:{to_edge}"):
            edge_counts[key] = edge_counts.get(key, 0) + 1

    def compute_fixedpoint_along(source: dict, target: dict, edge: str) -> float:
        """Compute a fixedPoint value that aligns the arrow with the target's center."""
        if edge in ("top", "bottom"):
            target_cx = target["x"] + target["width"] / 2
            fp = (target_cx - source["x"]) / source["width"]
        else:
            target_cy = target["y"] + target["height"] / 2
            fp = (target_cy - source["y"]) / source["height"]
        return max(0.05, min(0.95, fp))

    # --- Build arrows ---
    for arrow_spec in arrows_spec:
        from_ref = arrow_spec.get("from")
        to_ref = arrow_spec.get("to")
        from_elem = ref_to_element.get(from_ref)
        to_elem = ref_to_element.get(to_ref)

        if not from_elem or not to_elem:
            continue

        from_cx = from_elem["x"] + from_elem["width"] / 2
        from_cy = from_elem["y"] + from_elem["height"] / 2
        to_cx = to_elem["x"] + to_elem["width"] / 2
        to_cy = to_elem["y"] + to_elem["height"] / 2
        dx = to_cx - from_cx
        dy = to_cy - from_cy

        from_bottom = from_elem["y"] + from_elem["height"]
        from_right = from_elem["x"] + from_elem["width"]
        to_bottom = to_elem["y"] + to_elem["height"]
        to_right = to_elem["x"] + to_elem["width"]

        # Prefer vertical when shapes don't overlap vertically
        v_gap = max(0, to_elem["y"] - from_bottom, from_elem["y"] - to_bottom)
        h_gap = max(0, to_elem["x"] - from_right, from_elem["x"] - to_right)

        if v_gap > 0 and v_gap >= h_gap:
            use_vertical = True
        elif h_gap > 0 and h_gap > v_gap:
            use_vertical = False
        else:
            use_vertical = abs(dy) > abs(dx)

        if use_vertical:
            if dy > 0:
                from_edge, to_edge = "bottom", "top"
            else:
                from_edge, to_edge = "top", "bottom"
        else:
            if dx > 0:
                from_edge, to_edge = "right", "left"
            else:
                from_edge, to_edge = "left", "right"

        from_count = edge_counts.get(f"{from_ref}:{from_edge}", 1)
        to_count = edge_counts.get(f"{to_ref}:{to_edge}", 1)

        if from_count > 1:
            from_fp_along = compute_fixedpoint_along(from_elem, to_elem, from_edge)
        else:
            from_fp_along = 0.5

        if to_count > 1:
            to_fp_along = compute_fixedpoint_along(to_elem, from_elem, to_edge)
        else:
            to_fp_along = 0.5

        fp_map = {
            "top":    lambda t: [t, 0],
            "bottom": lambda t: [t, 1],
            "left":   lambda t: [0, t],
            "right":  lambda t: [1, t],
        }
        start_fp = fp_map[from_edge](from_fp_along)
        end_fp = fp_map[to_edge](to_fp_along)

        # Calculate actual pixel positions from fixedPoints
        start_x = from_elem["x"] + start_fp[0] * from_elem["width"]
        start_y = from_elem["y"] + start_fp[1] * from_elem["height"]
        end_x = to_elem["x"] + end_fp[0] * to_elem["width"]
        end_y = to_elem["y"] + end_fp[1] * to_elem["height"]

        points = arrow_spec.get("points", [[0, 0], [end_x - start_x, end_y - start_y]])

        a_spec = {
            "x": start_x,
            "y": start_y,
            "points": points,
            "strokeColor": arrow_spec.get("strokeColor", "#1F2937"),
            "strokeWidth": arrow_spec.get("strokeWidth", 1.5),
            "endArrowhead": arrow_spec.get("endArrowhead", "arrow"),
            "startArrowhead": arrow_spec.get("startArrowhead", None),
            "elbowed": arrow_spec.get("elbowed", False),
        }
        arrow = make_arrow(a_spec)

        # Bindings with fixedPoint
        arrow["startBinding"] = {
            "elementId": from_elem["id"],
            "focus": 0,
            "gap": 1,
            "fixedPoint": start_fp,
        }
        arrow["endBinding"] = {
            "elementId": to_elem["id"],
            "focus": 0,
            "gap": 1,
            "fixedPoint": end_fp,
        }

        from_elem["boundElements"].append({"id": arrow["id"], "type": "arrow"})
        to_elem["boundElements"].append({"id": arrow["id"], "type": "arrow"})

        elements.append(arrow)

        # Arrow label (positioned at midpoint of longest segment for multi-point arrows)
        arrow_label = arrow_spec.get("label")
        if arrow_label:
            if len(points) <= 2:
                mid_x = start_x + points[-1][0] / 2
                mid_y = start_y + points[-1][1] / 2
            else:
                longest_idx, longest_len = 1, 0
                for seg_i in range(1, len(points)):
                    seg_len = abs(points[seg_i][0] - points[seg_i-1][0]) + abs(points[seg_i][1] - points[seg_i-1][1])
                    if seg_len > longest_len:
                        longest_len = seg_len
                        longest_idx = seg_i
                p0, p1 = points[longest_idx - 1], points[longest_idx]
                mid_x = start_x + (p0[0] + p1[0]) / 2
                mid_y = start_y + (p0[1] + p1[1]) / 2
            label_spec = {
                "text": arrow_label,
                "x": mid_x + 8,
                "y": mid_y - 10,
                "fontSize": 14,
                "fontFamily": 3,
                "strokeColor": "#6B7280",
                "backgroundColor": "#ffffff",
                "fillStyle": "solid",
                "textAlign": "left",
                "verticalAlign": "top",
            }
            label_elem = make_text(label_spec)
            elements.append(label_elem)

    # --- Build annotations ---
    for ann_spec in annotations:
        attach_ref = ann_spec.get("attachTo")
        attach_elem = ref_to_element.get(attach_ref)
        if not attach_elem:
            continue

        position = ann_spec.get("position", "right")
        font_size = ann_spec.get("fontSize", 14)
        text = ann_spec.get("text", "")

        text_width, text_height = estimate_text_dimensions(text, font_size, 3)

        if position == "right":
            tx = attach_elem["x"] + attach_elem["width"] + 70
            ty = attach_elem["y"] + (attach_elem["height"] - text_height) / 2
            line_start_x = attach_elem["x"] + attach_elem["width"]
            line_start_y = attach_elem["y"] + attach_elem["height"] / 2
            line_points = [[0, 0], [50, 0]]
        elif position == "left":
            tx = attach_elem["x"] - text_width - 70
            ty = attach_elem["y"] + (attach_elem["height"] - text_height) / 2
            line_start_x = attach_elem["x"]
            line_start_y = attach_elem["y"] + attach_elem["height"] / 2
            line_points = [[0, 0], [-50, 0]]
        elif position == "above":
            tx = attach_elem["x"]
            ty = attach_elem["y"] - text_height - 30
            line_start_x = attach_elem["x"] + attach_elem["width"] / 2
            line_start_y = attach_elem["y"]
            line_points = [[0, 0], [0, -20]]
        else:  # below
            tx = attach_elem["x"]
            ty = attach_elem["y"] + attach_elem["height"] + 30
            line_start_x = attach_elem["x"] + attach_elem["width"] / 2
            line_start_y = attach_elem["y"] + attach_elem["height"]
            line_points = [[0, 0], [0, 20]]

        ann_text_spec = {
            "text": text,
            "x": tx,
            "y": ty,
            "fontSize": font_size,
            "fontFamily": 3,
            "strokeColor": ann_spec.get("strokeColor", "#6B7280"),
            "textAlign": "left",
            "verticalAlign": "top",
            "width": text_width,
            "height": text_height,
        }
        ann_text = make_text(ann_text_spec)
        elements.append(ann_text)

        # Leader line
        line_spec = {
            "x": line_start_x,
            "y": line_start_y,
            "points": line_points,
            "strokeColor": "#6B7280",
            "strokeStyle": "dashed",
            "strokeWidth": 1,
        }
        leader = make_line(line_spec)
        elements.append(leader)

    # --- Compute diagram bounding box from nodes ---
    if ref_to_element:
        bbox_left = min(e["x"] for e in ref_to_element.values())
        bbox_right = max(e["x"] + e["width"] for e in ref_to_element.values())
        bbox_top = min(e["y"] for e in ref_to_element.values())
        bbox_bottom = max(e["y"] + e["height"] for e in ref_to_element.values())
        bbox_center_x = (bbox_left + bbox_right) / 2
    else:
        bbox_left = bbox_right = bbox_top = bbox_bottom = bbox_center_x = 0

    # --- Build free text (two-pass for alignment) ---
    ft_entries = []
    for ft_spec in free_text:
        align = ft_spec.pop("align", None)
        text_elem = make_text(ft_spec)
        ft_entries.append((align, text_elem))

    # Compute shared left-align x from widest left-aligned label
    left_widths = [elem["width"] for a, elem in ft_entries if a == "left"]
    left_align_x = bbox_left - max(left_widths) - 20 if left_widths else 0

    for align, text_elem in ft_entries:
        if align == "center":
            text_elem["x"] = bbox_center_x - text_elem["width"] / 2
        elif align == "left":
            text_elem["x"] = left_align_x
        elements.append(text_elem)

    # --- Assign indices ---
    indices = generate_indices(len(elements))
    for i, elem in enumerate(elements):
        elem["index"] = indices[i]

    # --- Validation pass ---
    validate_elements(elements)

    # --- Build file wrapper ---
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": spec.get("viewBackgroundColor", "#ffffff"),
            "gridSize": None,
            "gridStep": 5,
            "gridModeEnabled": False,
        },
        "files": {},
    }


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            spec = json.load(f)
    else:
        spec = json.load(sys.stdin)

    result = build_diagram(spec)
    print(json.dumps(result, indent="\t"))


if __name__ == "__main__":
    main()
