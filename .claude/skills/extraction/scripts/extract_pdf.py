#!/usr/bin/env python3
"""
PDF Extraction Script for MDAA (Modular Discovery & Analysis Agent)

Converts PDF documents to clean Markdown text with table extraction.
Designed for financial/legal documents like SEC filings and merger agreements.

Usage:
    python extract_pdf.py input.pdf [--output output.md] [--tables-only] [--pages 1-10]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
    from pypdf.errors import PdfStreamError, PdfReadError
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def validate_pdf(pdf_path: Path) -> tuple[bool, str]:
    """Validate that a file is a readable PDF. Returns (is_valid, error_message)."""
    try:
        # Check magic bytes first
        with open(pdf_path, "rb") as f:
            header = f.read(8)
            if not header.startswith(b"%PDF"):
                return False, f"Invalid PDF header (got: {header[:20]!r})"

        # Try to open with pypdf
        reader = PdfReader(str(pdf_path))
        _ = len(reader.pages)  # Force reading page count
        return True, ""
    except (PdfStreamError, PdfReadError) as e:
        return False, f"Corrupted or invalid PDF: {e}"
    except Exception as e:
        return False, f"Failed to read PDF: {e}"


def extract_text_pypdf(pdf_path: Path, page_range: Optional[tuple] = None) -> str:
    """Extract text using pypdf (fast, basic extraction)."""
    reader = PdfReader(str(pdf_path))
    text_parts = []

    total_pages = len(reader.pages)
    start_page = 0
    end_page = total_pages

    if page_range:
        start_page = max(0, page_range[0] - 1)  # Convert to 0-indexed
        end_page = min(total_pages, page_range[1])

    for i in range(start_page, end_page):
        page = reader.pages[i]
        page_text = page.extract_text()
        if page_text:
            text_parts.append(f"\n\n--- Page {i + 1} ---\n\n")
            text_parts.append(page_text)

    return "".join(text_parts)


def extract_tables_pdfplumber(pdf_path: Path, page_range: Optional[tuple] = None) -> list:
    """Extract tables using pdfplumber."""
    if pdfplumber is None:
        return []

    tables = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        total_pages = len(pdf.pages)
        start_page = 0
        end_page = total_pages

        if page_range:
            start_page = max(0, page_range[0] - 1)
            end_page = min(total_pages, page_range[1])

        for i in range(start_page, end_page):
            page = pdf.pages[i]
            page_tables = page.extract_tables()

            for j, table in enumerate(page_tables):
                if table and len(table) > 1:  # Has header + at least one row
                    tables.append({
                        "page": i + 1,
                        "table_index": j + 1,
                        "data": table
                    })

    return tables


def table_to_markdown(table_data: list) -> str:
    """Convert a table to Markdown format."""
    if not table_data or len(table_data) < 1:
        return ""

    # Clean cells
    def clean_cell(cell):
        if cell is None:
            return ""
        return str(cell).replace("\n", " ").strip()

    header = [clean_cell(cell) for cell in table_data[0]]
    rows = [[clean_cell(cell) for cell in row] for row in table_data[1:]]

    # Build markdown table
    md_parts = []
    md_parts.append("| " + " | ".join(header) + " |")
    md_parts.append("|" + "|".join(["---"] * len(header)) + "|")

    for row in rows:
        # Ensure row has same number of columns as header
        while len(row) < len(header):
            row.append("")
        md_parts.append("| " + " | ".join(row[:len(header)]) + " |")

    return "\n".join(md_parts)


def format_markdown_output(
    filename: str,
    source_url: str,
    total_pages: int,
    text_content: str,
    tables: list
) -> str:
    """Format the complete markdown output."""

    output_parts = [
        f"# Document: {filename}",
        "",
        "## Metadata",
        f"- **Source URL**: {source_url}",
        f"- **Pages**: {total_pages}",
        f"- **Extracted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## Content",
        "",
        text_content,
    ]

    if tables:
        output_parts.extend([
            "",
            "---",
            "",
            "## Tables",
            "",
        ])

        for table_info in tables:
            output_parts.append(f"### Table {table_info['table_index']} (Page {table_info['page']})")
            output_parts.append("")
            output_parts.append(table_to_markdown(table_info['data']))
            output_parts.append("")

    return "\n".join(output_parts)


def parse_page_range(page_str: str) -> Optional[tuple]:
    """Parse page range string like '1-10' into tuple."""
    if not page_str:
        return None

    if "-" in page_str:
        parts = page_str.split("-")
        return (int(parts[0]), int(parts[1]))
    else:
        page = int(page_str)
        return (page, page)


def main():
    parser = argparse.ArgumentParser(
        description="Extract content from PDF documents to Markdown"
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("--output", "-o", help="Output Markdown file path")
    parser.add_argument("--tables-only", action="store_true",
                        help="Extract only tables (skip text)")
    parser.add_argument("--pages", help="Page range to extract (e.g., '1-10')")
    parser.add_argument("--source-url", default="local file",
                        help="Original source URL for metadata")
    parser.add_argument("--json-tables", action="store_true",
                        help="Also output tables as JSON")

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    if not input_path.suffix.lower() == ".pdf":
        print(f"Warning: File may not be a PDF: {input_path}")

    # Validate PDF before processing
    is_valid, error_msg = validate_pdf(input_path)
    if not is_valid:
        print(f"Error: {error_msg}")
        sys.exit(1)

    # Warn if --tables-only but pdfplumber not available
    if args.tables_only and pdfplumber is None:
        print("Error: --tables-only requires pdfplumber. Install with: pip install pdfplumber")
        sys.exit(1)

    # Print pdfplumber status
    if pdfplumber is None:
        print("Note: pdfplumber not installed. Table extraction disabled.")

    # Parse page range
    page_range = parse_page_range(args.pages) if args.pages else None

    # Get total pages
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)

    print(f"Processing: {input_path.name} ({total_pages} pages)")

    # Extract text
    text_content = ""
    if not args.tables_only:
        print("Extracting text...")
        text_content = extract_text_pypdf(input_path, page_range)
        print(f"  Extracted {len(text_content):,} characters")

    # Extract tables
    tables = []
    if pdfplumber:
        print("Extracting tables...")
        tables = extract_tables_pdfplumber(input_path, page_range)
        print(f"  Found {len(tables)} tables")

    # Format output
    markdown_output = format_markdown_output(
        filename=input_path.name,
        source_url=args.source_url,
        total_pages=total_pages,
        text_content=text_content,
        tables=tables
    )

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".md")

    # Create parent directories if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write markdown output
    output_path.write_text(markdown_output, encoding="utf-8")
    print(f"Output saved to: {output_path}")

    # Optionally write JSON tables
    if args.json_tables and tables:
        json_path = input_path.with_suffix("_tables.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(tables, f, indent=2)
        print(f"Tables JSON saved to: {json_path}")

    # Print summary
    print("\n--- Extraction Summary ---")
    print(f"  File: {input_path.name}")
    print(f"  Pages: {total_pages}")
    print(f"  Text length: {len(text_content):,} chars")
    print(f"  Tables found: {len(tables)}")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
