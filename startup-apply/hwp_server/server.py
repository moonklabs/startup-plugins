#!/usr/bin/env python3
"""hwp-generator MCP server — HWPX document generator for Korean business plans.

Install dependencies:
    pip install mcp lxml

Run (stdio transport):
    python server.py

MCP tools exposed:
  create_document      — start a new empty document (returns doc_id)
  add_heading          — insert a heading paragraph
  add_paragraph        — insert a body text paragraph
  add_table            — insert a table
  set_page_setup       — configure page size and margins
  fill_template        — fill {{placeholders}} in an existing .hwpx template
  convert_hwp_to_hwpx  — convert legacy .hwp → .hwpx via Java subprocess
  export_file          — save accumulated document to .hwpx file
  get_document_info    — list active documents and their paragraph counts
"""

import json
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from builder import HwpxBuilder

mcp = FastMCP("hwp-generator")

# In-memory document store: doc_id → HwpxBuilder instance
_docs: dict[str, HwpxBuilder] = {}


def _get_doc(doc_id: str) -> HwpxBuilder:
    if doc_id not in _docs:
        raise ValueError(f"Document '{doc_id}' not found. Call create_document first.")
    return _docs[doc_id]


# ------------------------------------------------------------------ #
# Tools                                                               #
# ------------------------------------------------------------------ #

@mcp.tool()
def create_document(title: str = "") -> dict[str, Any]:
    """Create a new empty HWPX document and return its doc_id.

    Args:
        title: Optional document title (used as the first heading if provided).

    Returns:
        {"doc_id": str, "message": str}
    """
    doc_id = str(uuid.uuid4())[:8]
    builder = HwpxBuilder()
    _docs[doc_id] = builder
    if title:
        builder.add_heading(title, level=1)
    return {"doc_id": doc_id, "message": f"Document '{doc_id}' created."}


@mcp.tool()
def add_heading(doc_id: str, text: str, level: int = 1) -> dict[str, Any]:
    """Insert a heading paragraph into the document.

    Args:
        doc_id: Document ID returned by create_document.
        text:   Heading text.
        level:  Heading level 1 (22pt), 2 (16pt), or 3 (13pt). Default 1.

    Returns:
        {"ok": True, "paragraphs": int}
    """
    builder = _get_doc(doc_id)
    if level not in (1, 2, 3):
        raise ValueError("level must be 1, 2, or 3")
    builder.add_heading(text, level=level)
    return {"ok": True, "paragraphs": len(builder._body)}


@mcp.tool()
def add_paragraph(
    doc_id: str,
    text: str,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    font_size_pt: int = 10,
) -> dict[str, Any]:
    """Insert a body text paragraph.

    Args:
        doc_id:       Document ID.
        text:         Paragraph text.
        bold:         Bold formatting.
        italic:       Italic formatting.
        underline:    Underline formatting.
        font_size_pt: Font size in points (default 10).

    Returns:
        {"ok": True, "paragraphs": int}
    """
    builder = _get_doc(doc_id)
    builder.add_paragraph(
        text, bold=bold, italic=italic, underline=underline, font_size_pt=font_size_pt
    )
    return {"ok": True, "paragraphs": len(builder._body)}


@mcp.tool()
def add_table(
    doc_id: str,
    data: list,
    col_widths_mm: list | None = None,
) -> dict[str, Any]:
    """Insert a table into the document.

    Args:
        doc_id:        Document ID.
        data:          2-D list of strings: [[row1col1, row1col2], [row2col1, ...]].
                       First row is treated as the header row.
        col_widths_mm: Optional list of column widths in mm. Defaults to equal widths.

    Returns:
        {"ok": True, "paragraphs": int}
    """
    builder = _get_doc(doc_id)
    builder.add_table(data, col_widths_mm=col_widths_mm)
    return {"ok": True, "paragraphs": len(builder._body)}


@mcp.tool()
def set_page_setup(
    doc_id: str,
    width_mm: float = 210,
    height_mm: float = 297,
    margin_top_mm: float = 30,
    margin_bottom_mm: float = 30,
    margin_left_mm: float = 30,
    margin_right_mm: float = 30,
) -> dict[str, Any]:
    """Configure page size and margins.

    Defaults are Korean government standard (A4, 30mm margins).
    Call before adding content for best results.

    Args:
        doc_id:           Document ID.
        width_mm:         Page width in mm (default 210 = A4).
        height_mm:        Page height in mm (default 297 = A4).
        margin_top_mm:    Top margin in mm (default 30).
        margin_bottom_mm: Bottom margin in mm (default 30).
        margin_left_mm:   Left margin in mm (default 30).
        margin_right_mm:  Right margin in mm (default 30).

    Returns:
        {"ok": True, "page": dict}
    """
    builder = _get_doc(doc_id)
    builder.set_page_setup(
        width_mm=width_mm, height_mm=height_mm,
        margin_top_mm=margin_top_mm, margin_bottom_mm=margin_bottom_mm,
        margin_left_mm=margin_left_mm, margin_right_mm=margin_right_mm,
    )
    return {"ok": True, "page": builder._page}


@mcp.tool()
def fill_template(
    template_path: str,
    replacements: dict,
    output_path: str,
) -> dict[str, Any]:
    """Fill {{placeholder}} fields in an existing .hwpx template and save.

    Does not require a pre-created doc_id — reads the template directly.

    Args:
        template_path: Absolute path to the source .hwpx template file.
        replacements:  Dict mapping placeholder names to replacement text,
                       e.g. {"company_name": "주식회사 예시", "year": "2026"}.
        output_path:   Absolute path for the filled output .hwpx file.

    Returns:
        {"ok": True, "output_path": str, "replaced_count": int}
    """
    import re
    import zipfile
    from pathlib import Path

    src = Path(template_path)
    if not src.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    dst = Path(output_path)
    dst.parent.mkdir(parents=True, exist_ok=True)

    replaced_count = 0
    with zipfile.ZipFile(str(src), "r") as zin, zipfile.ZipFile(str(dst), "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith(".xml"):
                text = data.decode("utf-8")
                for key, value in replacements.items():
                    pattern = "{{" + key + "}}"
                    count = text.count(pattern)
                    if count:
                        text = text.replace(pattern, str(value))
                        replaced_count += count
                data = text.encode("utf-8")
            if item.filename == "mimetype":
                mi = zipfile.ZipInfo("mimetype")
                mi.compress_type = zipfile.ZIP_STORED
                zout.writestr(mi, data)
            else:
                zout.writestr(item, data)

    return {"ok": True, "output_path": str(dst), "replaced_count": replaced_count}


@mcp.tool()
def convert_hwp_to_hwpx(
    hwp_path: str,
    output_path: str,
    jar_path: str = "",
) -> dict[str, Any]:
    """Convert a legacy .hwp file to .hwpx using the hwp2hwpx Java library.

    Requires Java (JRE 11+) and the hwp2hwpx-all.jar (github.com/neolord0/hwp2hwpx).

    Args:
        hwp_path:    Absolute path to the source .hwp file.
        output_path: Absolute path for the output .hwpx file.
        jar_path:    Path to hwp2hwpx-all.jar. If empty, looks in the same
                     directory as this script and in PATH.

    Returns:
        {"ok": True, "output_path": str} on success.
        {"ok": False, "error": str} if Java or JAR is unavailable.
    """
    hwp = Path(hwp_path)
    if not hwp.exists():
        return {"ok": False, "error": f"HWP file not found: {hwp_path}"}

    # Locate JAR
    jar = Path(jar_path) if jar_path else None
    if jar is None or not jar.exists():
        candidates = [
            Path(__file__).parent / "hwp2hwpx-all.jar",
            Path(__file__).parent / "lib" / "hwp2hwpx-all.jar",
        ]
        for c in candidates:
            if c.exists():
                jar = c
                break
    if jar is None or not jar.exists():
        return {
            "ok": False,
            "error": (
                "hwp2hwpx-all.jar not found. "
                "Download from https://github.com/neolord0/hwp2hwpx/releases "
                f"and place it at {Path(__file__).parent / 'hwp2hwpx-all.jar'}"
            ),
        }

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            ["java", "-jar", str(jar), str(hwp), str(out)],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except FileNotFoundError:
        return {"ok": False, "error": "Java not found. Install JRE 11+ and ensure 'java' is in PATH."}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Conversion timed out (>60s)."}

    if result.returncode != 0:
        return {"ok": False, "error": result.stderr or result.stdout}

    return {"ok": True, "output_path": str(out)}


@mcp.tool()
def export_file(doc_id: str, output_path: str) -> dict[str, Any]:
    """Save the document to an .hwpx file.

    Args:
        doc_id:      Document ID returned by create_document.
        output_path: Absolute path for the output .hwpx file.
                     Directories are created automatically.

    Returns:
        {"ok": True, "output_path": str, "paragraphs": int}
    """
    builder = _get_doc(doc_id)
    out = Path(output_path)
    builder.build(str(out))
    return {
        "ok": True,
        "output_path": str(out.resolve()),
        "paragraphs": len(builder._body),
    }


@mcp.tool()
def get_document_info(doc_id: str = "") -> dict[str, Any]:
    """List active documents or get details about a specific document.

    Args:
        doc_id: If provided, return details for that document only.
                If empty, list all active document IDs.

    Returns:
        {"documents": [...]} or {"doc_id": str, "paragraphs": int, "page": dict}
    """
    if doc_id:
        builder = _get_doc(doc_id)
        return {
            "doc_id": doc_id,
            "paragraphs": len(builder._body),
            "page": builder._page,
            "char_styles": len(builder._char_prs),
            "para_styles": len(builder._para_prs),
        }
    return {
        "documents": [
            {"doc_id": did, "paragraphs": len(b._body)}
            for did, b in _docs.items()
        ]
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
