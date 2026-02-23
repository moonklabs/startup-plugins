"""HwpxBuilder — programmatic HWPX document construction.

HWPX is a ZIP archive with XML files following the Hangul Markup Language (HML) spec.

Structure:
  mimetype
  META-INF/container.xml
  Contents/content.hpf      — manifest
  Contents/header.xml       — styles, fonts, char/para properties
  Contents/section0.xml     — body content (paragraphs, tables)
  Contents/masterPage.xml   — page master (headers/footers)
  Contents/settings.xml     — document settings

Units:
  Length: 1/100 mm  (e.g. A4 width = 21000)
  Font size: 1/100 pt  (e.g. 10pt = 1000)
  Line spacing: 1/100 %  (e.g. 160% = 16000)
"""

import zipfile
from pathlib import Path
from lxml import etree

# HML namespaces
NS_HP = "http://www.hancom.co.kr/hwpml/2011/paragraph"
NS_HH = "http://www.hancom.co.kr/hwpml/2011/head"
NS_HS = "http://www.hancom.co.kr/hwpml/2011/section"
NS_HPF = "http://www.hancom.co.kr/schema/2011/content"

# Korean government document standard defaults
DEFAULT_FONT = "함초롬바탕"
DEFAULT_FONT_SIZE = 1000       # 10pt
HEADING1_SIZE = 2200           # 22pt
HEADING2_SIZE = 1600           # 16pt
HEADING3_SIZE = 1300           # 13pt
LINE_SPACING = 16000           # 160%


class HwpxBuilder:
    """Builds an HWPX document incrementally.

    Usage:
        builder = HwpxBuilder()
        builder.set_page_setup(margin_top_mm=30, margin_bottom_mm=30)
        builder.add_heading("제목", level=1)
        builder.add_paragraph("본문 내용입니다.")
        builder.add_table([["항목", "내용"], ["팀", "개발팀"]])
        builder.build("/tmp/output.hwpx")
    """

    def __init__(self):
        self._fonts: list[dict] = []
        self._char_prs: list[dict] = []
        self._para_prs: list[dict] = []
        self._styles: list[dict] = []
        self._body: list = []          # lxml Elements (hp:p or hp:tbl)
        self._page = {
            "width": 21000,            # A4
            "height": 29700,
            "margin_top": 3000,
            "margin_bottom": 3000,
            "margin_left": 3000,
            "margin_right": 3000,
        }
        self._setup_defaults()

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def set_page_setup(
        self,
        width_mm: float = 210,
        height_mm: float = 297,
        margin_top_mm: float = 30,
        margin_bottom_mm: float = 30,
        margin_left_mm: float = 30,
        margin_right_mm: float = 30,
    ) -> None:
        """Set page dimensions and margins (mm → internal 1/100 mm units)."""
        self._page = {
            "width": int(width_mm * 100),
            "height": int(height_mm * 100),
            "margin_top": int(margin_top_mm * 100),
            "margin_bottom": int(margin_bottom_mm * 100),
            "margin_left": int(margin_left_mm * 100),
            "margin_right": int(margin_right_mm * 100),
        }

    def add_heading(self, text: str, level: int = 1) -> None:
        """Append a heading paragraph.

        level 1 → 22pt bold, margin-after 200 (2mm)
        level 2 → 16pt bold, margin-after 150
        level 3 → 13pt bold, margin-after 100
        """
        sizes = {1: HEADING1_SIZE, 2: HEADING2_SIZE, 3: HEADING3_SIZE}
        after = {1: 200, 2: 150, 3: 100}
        size = sizes.get(level, HEADING3_SIZE)
        cpr_id = self._get_or_create_char_pr(height=size, bold=True)
        ppr_id = self._get_or_create_para_pr(margin_next=after.get(level, 100))
        self._body.append(self._make_p(text, cpr_id, ppr_id))

    def add_paragraph(
        self,
        text: str,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        font_size_pt: int = 10,
    ) -> None:
        """Append a body text paragraph."""
        height = font_size_pt * 100
        cpr_id = self._get_or_create_char_pr(
            height=height, bold=bold, italic=italic, underline=underline
        )
        ppr_id = self._get_or_create_para_pr()
        self._body.append(self._make_p(text, cpr_id, ppr_id))

    def add_table(
        self,
        data: list,
        col_widths_mm: list | None = None,
    ) -> None:
        """Append a table.

        Args:
            data: List of rows; each row is a list of cell text strings.
            col_widths_mm: Optional column widths in mm. Defaults to equal widths summing to 160mm.
        """
        if not data:
            return
        HP = NS_HP
        num_cols = max(len(row) for row in data)
        if col_widths_mm is None:
            equal = 160 / num_cols
            col_widths_mm = [equal] * num_cols
        col_widths = [int(w * 100) for w in col_widths_mm]

        tbl = etree.Element(f"{{{HP}}}tbl")
        tbl.set("id", str(len(self._body)))
        tbl.set("width", str(sum(col_widths)))
        tbl.set("height", "0")
        tbl.set("cellSpacing", "0")
        tbl.set("borderFillIDRef", "0")
        tbl.set("noAdjust", "false")

        for row_data in data:
            tr = etree.SubElement(tbl, f"{{{HP}}}tr")
            tr.set("height", "600")
            tr.set("cantSplit", "false")
            tr.set("repeatHeader", "false")
            for ci, cell_text in enumerate(row_data):
                tc = etree.SubElement(tr, f"{{{HP}}}tc")
                tc.set("name", "")
                tc.set("header", "false")
                tc.set("hasMargin", "false")
                tc.set("protect", "false")
                tc.set("editable", "false")
                tc.set("dirty", "false")
                tc.set("borderFillIDRef", "0")

                sz = etree.SubElement(tc, f"{{{HP}}}tcSz")
                w = col_widths[ci] if ci < len(col_widths) else col_widths[-1]
                sz.set("width", str(w))
                sz.set("height", "600")

                tc.append(self._make_p(cell_text, 0, 0))

        self._body.append(tbl)

    def fill_template(self, template_path: str, replacements: dict) -> "HwpxBuilder":
        """Load an HWPX template and replace {{key}} placeholders.

        Returns a new HwpxBuilder whose body is taken from the filled template.
        Useful when a base .hwpx template already has the correct layout.
        """
        import re

        filled = HwpxBuilder.__new__(HwpxBuilder)
        filled._fonts = []
        filled._char_prs = []
        filled._para_prs = []
        filled._styles = []
        filled._body = []
        filled._page = dict(self._page)

        with zipfile.ZipFile(template_path, "r") as zf:
            section_xml = zf.read("Contents/section0.xml")

        # Text-level replacement (operates on raw XML bytes for simplicity)
        text = section_xml.decode("utf-8")
        for key, value in replacements.items():
            text = text.replace("{{" + key + "}}", str(value))
            text = re.sub(r"\{\{" + re.escape(key) + r"\}\}", str(value), text)

        # Re-parse replaced section and copy paragraphs
        root = etree.fromstring(text.encode("utf-8"))
        HP = NS_HP
        for child in root:
            tag = etree.QName(child).localname
            if tag in ("p", "tbl"):
                filled._body.append(child)

        return filled

    def build(self, output_path: str) -> None:
        """Write the HWPX ZIP archive to *output_path*."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(str(path), "w", zipfile.ZIP_DEFLATED) as zf:
            # mimetype — must be uncompressed per ODF convention
            mi = zipfile.ZipInfo("mimetype")
            mi.compress_type = zipfile.ZIP_STORED
            zf.writestr(mi, "application/hwp+zip")

            zf.writestr("META-INF/container.xml", self._container_xml())
            zf.writestr("Contents/content.hpf", self._hpf_xml())
            zf.writestr("Contents/header.xml", self._header_xml())
            zf.writestr("Contents/section0.xml", self._section_xml())
            zf.writestr("Contents/masterPage.xml", self._master_page_xml())
            zf.writestr("Contents/settings.xml", self._settings_xml())

    # ------------------------------------------------------------------ #
    # Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    def _setup_defaults(self) -> None:
        self._fonts.append({"id": 0, "face": DEFAULT_FONT, "type": "TTFFONT"})
        self._char_prs.append(
            {"id": 0, "height": DEFAULT_FONT_SIZE, "bold": False,
             "italic": False, "underline": False, "fontRef": 0}
        )
        self._para_prs.append(
            {"id": 0, "lineSpace": LINE_SPACING, "lineSpaceType": "LEADING",
             "marginLeft": 0, "marginRight": 0, "indent": 0,
             "marginPrev": 0, "marginNext": 0}
        )
        self._styles.append(
            {"id": 0, "type": "PARA", "name": "바탕글", "engName": "Normal",
             "paraPrIDRef": 0, "charPrIDRef": 0, "nextStyleIDRef": 0}
        )

    def _get_or_create_font(self, face: str) -> int:
        for f in self._fonts:
            if f["face"] == face:
                return f["id"]
        fid = len(self._fonts)
        self._fonts.append({"id": fid, "face": face, "type": "TTFFONT"})
        return fid

    def _get_or_create_char_pr(
        self,
        height: int = DEFAULT_FONT_SIZE,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        font_face: str = DEFAULT_FONT,
    ) -> int:
        fref = self._get_or_create_font(font_face)
        for cp in self._char_prs:
            if (cp["height"] == height and cp["bold"] == bold
                    and cp["italic"] == italic and cp["underline"] == underline
                    and cp["fontRef"] == fref):
                return cp["id"]
        cid = len(self._char_prs)
        self._char_prs.append(
            {"id": cid, "height": height, "bold": bold,
             "italic": italic, "underline": underline, "fontRef": fref}
        )
        return cid

    def _get_or_create_para_pr(
        self,
        line_space: int = LINE_SPACING,
        margin_left: int = 0,
        margin_right: int = 0,
        indent: int = 0,
        margin_prev: int = 0,
        margin_next: int = 0,
    ) -> int:
        for pp in self._para_prs:
            if (pp["lineSpace"] == line_space
                    and pp["marginLeft"] == margin_left
                    and pp["marginRight"] == margin_right
                    and pp["indent"] == indent
                    and pp["marginPrev"] == margin_prev
                    and pp["marginNext"] == margin_next):
                return pp["id"]
        pid = len(self._para_prs)
        self._para_prs.append(
            {"id": pid, "lineSpace": line_space, "lineSpaceType": "LEADING",
             "marginLeft": margin_left, "marginRight": margin_right,
             "indent": indent, "marginPrev": margin_prev, "marginNext": margin_next}
        )
        return pid

    def _make_p(self, text: str, cpr_id: int, ppr_id: int):
        HP = NS_HP
        p = etree.Element(f"{{{HP}}}p")
        pPr = etree.SubElement(p, f"{{{HP}}}pPr")
        pPr.set("paraPrIDRef", str(ppr_id))
        pPr.set("styleIDRef", "0")
        if text:
            run = etree.SubElement(p, f"{{{HP}}}run")
            run.set("charPrIDRef", str(cpr_id))
            t = etree.SubElement(run, f"{{{HP}}}t")
            t.text = text
        return p

    # ------------------------------------------------------------------ #
    # XML serialisers                                                      #
    # ------------------------------------------------------------------ #

    def _container_xml(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
            '  <rootfiles>\n'
            '    <rootfile full-path="Contents/content.hpf"'
            ' media-type="application/hwp+zip"/>\n'
            '  </rootfiles>\n'
            '</container>'
        )

    def _hpf_xml(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<hpf:package xmlns:hpf="http://www.hancom.co.kr/schema/2011/content"'
            ' version="1.2">\n'
            '  <hpf:manifest>\n'
            '    <hpf:item id="header" href="header.xml" media-type="application/xml"/>\n'
            '    <hpf:item id="section0" href="section0.xml" media-type="application/xml"/>\n'
            '    <hpf:item id="masterPage" href="masterPage.xml" media-type="application/xml"/>\n'
            '    <hpf:item id="settings" href="settings.xml" media-type="application/xml"/>\n'
            '  </hpf:manifest>\n'
            '  <hpf:metadata>\n'
            '    <hpf:Title/><hpf:Subject/><hpf:Creator/><hpf:Description/>\n'
            '  </hpf:metadata>\n'
            '  <hpf:spine>\n'
            '    <hpf:itemref idref="section0"/>\n'
            '  </hpf:spine>\n'
            '</hpf:package>'
        )

    def _header_xml(self) -> bytes:
        HH = NS_HH
        head = etree.Element(f"{{{HH}}}head", nsmap={"hh": HH})

        etree.SubElement(head, f"{{{HH}}}docOption")
        etree.SubElement(head, f"{{{HH}}}trackChangeConfig")

        # charPrList
        cpl = etree.SubElement(head, f"{{{HH}}}charPrList")
        for cp in self._char_prs:
            el = etree.SubElement(cpl, f"{{{HH}}}charPr")
            el.set("id", str(cp["id"]))
            el.set("height", str(cp["height"]))
            el.set("textColor", "0")
            el.set("shadeColor", "16777215")
            el.set("bold", "true" if cp["bold"] else "false")
            el.set("italic", "true" if cp["italic"] else "false")
            el.set("underlineType", "UNDERLINE" if cp["underline"] else "NONE")
            el.set("strikeOutType", "NONE")
            el.set("outlineType", "NONE")
            el.set("fontRef", str(cp["fontRef"]))
            el.set("langFontRef", str(cp["fontRef"]))
            el.set("hanjFontRef", str(cp["fontRef"]))
            el.set("symbFontRef", str(cp["fontRef"]))

        # paraPrList
        ppl = etree.SubElement(head, f"{{{HH}}}paraPrList")
        for pp in self._para_prs:
            el = etree.SubElement(ppl, f"{{{HH}}}paraPr")
            el.set("id", str(pp["id"]))
            el.set("tabRef", "0")
            el.set("numbering", "false")
            el.set("lineSpace", str(pp["lineSpace"]))
            el.set("lineSpaceType", pp["lineSpaceType"])
            im = etree.SubElement(el, f"{{{HH}}}indentMargin")
            im.set("marginLeft", str(pp["marginLeft"]))
            im.set("marginRight", str(pp["marginRight"]))
            im.set("indent", str(pp["indent"]))
            im.set("marginPrev", str(pp["marginPrev"]))
            im.set("marginNext", str(pp["marginNext"]))

        # styleList
        sl = etree.SubElement(head, f"{{{HH}}}styleList")
        for s in self._styles:
            el = etree.SubElement(sl, f"{{{HH}}}style")
            el.set("id", str(s["id"]))
            el.set("type", s["type"])
            el.set("name", s["name"])
            el.set("engName", s["engName"])
            el.set("paraPrIDRef", str(s["paraPrIDRef"]))
            el.set("charPrIDRef", str(s["charPrIDRef"]))
            el.set("nextStyleIDRef", str(s["nextStyleIDRef"]))
            el.set("langID", "1042")

        etree.SubElement(head, f"{{{HH}}}memoList")
        etree.SubElement(head, f"{{{HH}}}trackChangeList")

        # fontList
        fl = etree.SubElement(head, f"{{{HH}}}fontList")
        for f in self._fonts:
            el = etree.SubElement(fl, f"{{{HH}}}font")
            el.set("id", str(f["id"]))
            el.set("face", f["face"])
            el.set("type", f["type"])
            el.set("isEmbedded", "false")

        return etree.tostring(head, xml_declaration=True, encoding="UTF-8", pretty_print=True)

    def _section_xml(self) -> bytes:
        HS = NS_HS
        HP = NS_HP
        sec = etree.Element(f"{{{HS}}}sec", nsmap={"hs": HS, "hp": HP})

        # Page layout
        secPr = etree.SubElement(sec, f"{{{HS}}}secPr")
        p = self._page
        pageSz = etree.SubElement(secPr, f"{{{HS}}}pageSz")
        pageSz.set("width", str(p["width"]))
        pageSz.set("height", str(p["height"]))
        pageSz.set("landscape", "false")

        pageMar = etree.SubElement(secPr, f"{{{HS}}}pageMar")
        pageMar.set("top", str(p["margin_top"]))
        pageMar.set("bottom", str(p["margin_bottom"]))
        pageMar.set("left", str(p["margin_left"]))
        pageMar.set("right", str(p["margin_right"]))
        pageMar.set("header", "850")
        pageMar.set("footer", "850")
        pageMar.set("gutter", "0")

        for elem in self._body:
            sec.append(elem)

        return etree.tostring(sec, xml_declaration=True, encoding="UTF-8", pretty_print=True)

    def _master_page_xml(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<masterPages xmlns="http://www.hancom.co.kr/hwpml/2011/masterPage"/>'
        )

    def _settings_xml(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<settings xmlns="http://www.hancom.co.kr/hwpml/2011/settings"/>'
        )
