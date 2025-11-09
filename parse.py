import requests

import os
from markdownify import markdownify as md
import camelot


def extract_text_from_pdf_path(pdf_path: str) -> str:
    """Extract text from a local PDF file."""
    tables = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")

    if not tables:
        print("No tables found in the PDF.")
        return ""

    markdown_tables = []
    for table in tables:
        df = table.df  # pandas DataFrame
        markdown = df.to_markdown(index=False)
        markdown_tables.append(markdown)

    return "\n\n".join(markdown_tables)


def extract_text_from_pdf_url(pdf_url: str) -> str:
    """Download PDF from URL and extract text."""
    response = requests.get(pdf_url)
    response.raise_for_status()

    temp_pdf = "temp_download.pdf"
    with open(temp_pdf, "wb") as f:
        f.write(response.content)

    text = extract_text_from_pdf_path(temp_pdf)
    os.remove(temp_pdf)  # Clean up temp file
    return text


def parse_url(url: str) -> str:
    if url.lower().endswith(".pdf"):
        return extract_text_from_pdf_url(url)
    else:
        response = requests.get(url)
        html_content = response.text
        return md(html_content)


if __name__ == "__main__":
    # test_url = "https://app.food2050.ch/de/v2/zfv/zhdk,toni-areal/mensa-molki/mittagsverpflegung/menu/weekly"
    test_url = "http://www.lunch-5.ch/uploads/menuplan.pdf"
    markdown = parse_url(test_url)
    print(markdown)
