#!/usr/bin/env python3
"""Generate a minimal placeholder resume PDF without external dependencies."""

from pathlib import Path


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf(lines):
    objects = []

    def add_object(content: str) -> int:
        objects.append(content)
        return len(objects)

    font_obj = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    stream_parts = ["BT"]
    y = 750
    for size, text in lines:
        stream_parts.append(f"/F1 {size} Tf")
        stream_parts.append(f"50 {y} Td")
        stream_parts.append(f"({escape_pdf_text(text)}) Tj")
        stream_parts.append("0 0 Td")
        y -= size + 8
    stream_parts.append("ET")
    stream = "\n".join(stream_parts).encode("latin-1", errors="replace")

    content_obj = add_object(
        f"<< /Length {len(stream)} >>\nstream\n{stream.decode('latin-1')}\nendstream"
    )

    page_obj = add_object(
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        f"/Contents {content_obj} 0 R /Resources << /Font << /F1 {font_obj} 0 R >> >> >>"
    )

    pages_obj = add_object(f"<< /Type /Pages /Kids [{page_obj} 0 R] /Count 1 >>")
    catalog_obj = add_object(f"<< /Type /Catalog /Pages {pages_obj} 0 R >>")

    pdf = ["%PDF-1.4\n"]
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len("".join(pdf).encode("latin-1", errors="replace")))
        pdf.append(f"{index} 0 obj\n{obj}\nendobj\n")

    xref_offset = len("".join(pdf).encode("latin-1", errors="replace"))
    pdf.append(f"xref\n0 {len(objects) + 1}\n")
    pdf.append("0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.append(f"{offset:010d} 00000 n \n")
    pdf.append(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_obj} 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    )
    return "".join(pdf).encode("latin-1", errors="replace")


LINES = [
    (18, "Madeleine Schmidlin"),
    (12, "Staff Scientist, Melt Process Development"),
    (10, "linkedin.com/in/madeleineschmidlin"),
    (11, "PLACEHOLDER RESUME - replace with final version"),
    (14, "Experience"),
    (10, "Staff Scientist, Melt Process Development - Corning (2025-Present)"),
    (10, "Sr. Process Engineer - Corning (2022-2025)"),
    (10, "Process Engineer - Corning (2019-2022)"),
    (10, "Process Engineer Intern - Corning Inc. (2018)"),
    (10, "R&D Intern - W.R. Grace, Columbia MD (2017)"),
    (10, "REU - University of Notre Dame (2016)"),
    (14, "Education"),
    (10, "M.Eng., Materials Science and Engineering - Cornell (2021-2023)"),
    (10, "B.S., Chemical Engineering - University of Oregon (2015-2019)"),
]

output = Path(__file__).resolve().parent.parent / "src" / "assets" / "resume.pdf"
output.write_bytes(build_pdf(LINES))
print(f"Resume written to {output}")
