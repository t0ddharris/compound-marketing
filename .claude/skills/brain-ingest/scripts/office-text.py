#!/usr/bin/env python3
"""Print the text of a .pptx or .docx file, any size, using only the standard library.

Usage: python3 office-text.py FILE [FILE ...]

Slides come out in order with their speaker notes. Images, charts, and
layout are skipped; only text is extracted.
"""
import re
import sys
import zipfile
from html import unescape

PARA = re.compile(r"<(?:a|w):p[ >].*?</(?:a|w):p>", re.S)
RUN = re.compile(r"<(?:a|w):t(?: [^>]*)?>(.*?)</(?:a|w):t>", re.S)


def paragraphs(xml):
    for p in PARA.findall(xml):
        text = unescape("".join(RUN.findall(p))).strip()
        if text:
            yield text


def numbered(z, pattern):
    hits = [(int(m.group(1)), n) for n in z.namelist() if (m := re.fullmatch(pattern, n))]
    return dict(sorted(hits))


def pptx(z):
    slides = numbered(z, r"ppt/slides/slide(\d+)\.xml")
    notes = {}
    # Notes files aren't numbered to match slides; follow each slide's relationship to its notes.
    names = set(z.namelist())
    for i in slides:
        rels = f"ppt/slides/_rels/slide{i}.xml.rels"
        m = rels in names and re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', z.read(rels).decode("utf8", "replace"))
        if m:
            notes[i] = "ppt/notesSlides/" + m.group(1)
    for i, slide in slides.items():
        print(f"## Slide {i}")
        print("\n".join(paragraphs(z.read(slide).decode("utf8", "replace"))))
        if i in notes:
            text = "\n".join(paragraphs(z.read(notes[i]).decode("utf8", "replace")))
            if text:
                print(f"\nNotes:\n{text}")
        print()


def docx(z):
    print("\n\n".join(paragraphs(z.read("word/document.xml").decode("utf8", "replace"))))


for path in sys.argv[1:] or sys.exit(__doc__):
    print(f"# {path}\n")
    try:
        with zipfile.ZipFile(path) as z:
            {"pptx": pptx, "docx": docx}[path.rsplit(".", 1)[-1].lower()](z)
    except (KeyError, zipfile.BadZipFile) as e:
        print(f"Could not read {path}: {e!r}", file=sys.stderr)
