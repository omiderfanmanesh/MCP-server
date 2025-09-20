import csv
import os
import re
import zipfile
from io import TextIOBase
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET


def xlsx_first_sheet_to_csv(xlsx_path: str, csv_path: str) -> None:
    if not os.path.exists(xlsx_path):
        raise FileNotFoundError(f"XLSX not found: {xlsx_path}")
    with zipfile.ZipFile(xlsx_path) as zf:
        # Find first worksheet path from workbook relationships if available
        sheet_path = _find_first_sheet_path(zf)
        if sheet_path is None:
            # fallback to common default
            sheet_path = "xl/worksheets/sheet1.xml"
        shared_strings = _parse_shared_strings(zf)
        with zf.open(sheet_path) as sheet_file, open(csv_path, "w", newline="", encoding="utf-8") as out_csv:
            writer = csv.writer(out_csv)
            for row in _iter_rows(sheet_file, shared_strings):
                writer.writerow(row)


def _find_first_sheet_path(zf: zipfile.ZipFile) -> Optional[str]:
    try:
        wb_xml = zf.read("xl/workbook.xml")
        tree = ET.fromstring(wb_xml)
        ns = {
            "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
            "x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        }
        sheets = tree.findall(".//x:sheets/x:sheet", ns)
        if not sheets:
            return None
        first_sheet = sheets[0]
        r_id = first_sheet.attrib.get(f"{{{ns['r']}}}id")
        if not r_id:
            return None
        rels_xml = zf.read("xl/_rels/workbook.xml.rels")
        rels = ET.fromstring(rels_xml)
        for rel in rels.findall(".//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
            if rel.attrib.get("Id") == r_id:
                target = rel.attrib.get("Target")
                if target:
                    if not target.startswith("xl/"):
                        target = "xl/" + target
                    return target
        return None
    except KeyError:
        return None


def _parse_shared_strings(zf: zipfile.ZipFile) -> List[str]:
    try:
        ss_xml = zf.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    tree = ET.fromstring(ss_xml)
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    strings: List[str] = []
    for si in tree.findall(".//x:si", ns):
        # A shared string may have multiple <t> segments
        texts: List[str] = []
        for t in si.findall(".//x:t", ns):
            texts.append(t.text or "")
        strings.append("".join(texts))
    return strings


_col_re = re.compile(r"([A-Z]+)(\d+)")


def _col_to_index(col_letters: str) -> int:
    # A -> 0, B -> 1, ... Z -> 25, AA -> 26, ...
    idx = 0
    for ch in col_letters:
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def _iter_rows(sheet_file, shared_strings: List[str]):
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    tree = ET.parse(sheet_file)
    root = tree.getroot()
    for row in root.findall(".//x:sheetData/x:row", ns):
        cells = []  # dynamic; we will resize as needed
        for c in row.findall("x:c", ns):
            r = c.attrib.get("r", "A1")
            m = _col_re.match(r)
            col_letters = m.group(1) if m else "A"
            idx = _col_to_index(col_letters)
            # ensure cells list long enough
            if idx >= len(cells):
                cells.extend([""] * (idx - len(cells) + 1))
            t = c.attrib.get("t")  # type
            v_el = c.find("x:v", ns)
            if v_el is None or v_el.text is None:
                value = ""
            else:
                raw = v_el.text
                if t == "s":  # shared string
                    try:
                        value = shared_strings[int(raw)]
                    except (ValueError, IndexError):
                        value = raw
                else:
                    value = raw
            cells[idx] = value
        # Trim trailing empties
        while cells and cells[-1] == "":
            cells.pop()
        yield cells

