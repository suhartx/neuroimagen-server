from pathlib import Path


def _escape_pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_minimal_pdf(destination: Path, title: str, lines: list[str]) -> None:
    safe_title = _escape_pdf_text(title)
    text_lines = [safe_title, *[_escape_pdf_text(line) for line in lines]]

    commands = ["BT", "/F1 16 Tf", "72 760 Td"]
    for index, line in enumerate(text_lines):
        if index == 0:
            commands.append(f"({line}) Tj")
        else:
            commands.append("0 -22 Td")
            commands.append(f"({line}) Tj")
    commands.append("ET")
    stream = "\n".join(commands).encode("latin-1", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Length {len(stream)} >>stream\n".encode("latin-1") + stream + b"\nendstream",
    ]

    chunks = [b"%PDF-1.4\n"]
    offsets = [0]
    current_offset = len(chunks[0])

    for index, obj in enumerate(objects, start=1):
        offsets.append(current_offset)
        chunk = f"{index} 0 obj\n".encode("latin-1") + obj + b"\nendobj\n"
        chunks.append(chunk)
        current_offset += len(chunk)

    xref_offset = current_offset
    xref_lines = [b"xref\n", f"0 {len(objects) + 1}\n".encode("latin-1"), b"0000000000 65535 f \n"]
    for offset in offsets[1:]:
        xref_lines.append(f"{offset:010d} 00000 n \n".encode("latin-1"))

    trailer = (
        f"trailer<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode("latin-1")
        + b"startxref\n"
        + f"{xref_offset}\n".encode("latin-1")
        + b"%%EOF\n"
    )
    pdf = b"".join(chunks + xref_lines + [trailer])
    destination.write_bytes(pdf)
