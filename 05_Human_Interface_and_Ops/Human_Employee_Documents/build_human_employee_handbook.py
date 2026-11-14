"""Render the controlled human handbook Markdown into a Word document."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

SOURCE = Path(__file__).with_name("HUMAN_EMPLOYEE_HANDBOOK.md")
OUTPUT = Path(__file__).with_name("Triton_AI_Corp_Human_Employee_Handbook.docx")


def set_font(run, name: str, size: float, color: RGBColor, bold: bool = False) -> None:
    """Apply portable font settings to a run."""
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.bold = bold


def configure_document(document: Document) -> None:
    """Apply the compact-reference-guide design tokens."""
    section = document.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = section.bottom_margin = Inches(1)
    section.left_margin = section.right_margin = Inches(1)
    section.header_distance = section.footer_distance = Inches(0.492)

    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.25

    for name, size, color, before, after in (
        ("Heading 1", 16, RGBColor(46, 116, 181), 18, 10),
        ("Heading 2", 13, RGBColor(46, 116, 181), 14, 7),
    ):
        style = styles[name]
        style.font.name = "Calibri"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
        style.font.size = Pt(size)
        style.font.color.rgb = color
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    if "Handbook Subtitle" not in styles:
        subtitle = styles.add_style("Handbook Subtitle", WD_STYLE_TYPE.PARAGRAPH)
        subtitle.font.name = "Calibri"
        subtitle._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
        subtitle._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
        subtitle.font.size = Pt(12)
        subtitle.font.color.rgb = RGBColor(89, 89, 89)
        subtitle.paragraph_format.space_after = Pt(18)

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_font(header.add_run("TRITON AI CORP | HUMAN EMPLOYEE HANDBOOK"), "Calibri", 8, RGBColor(89, 89, 89))
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_font(footer.add_run("Controlled human-facing guide"), "Calibri", 8, RGBColor(89, 89, 89))


def add_bullet(document: Document, text: str) -> None:
    """Add a real numbered-list paragraph using Word's bullet style."""
    paragraph = document.add_paragraph(style="List Bullet")
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.paragraph_format.line_spacing = 1.25
    paragraph.add_run(text)


def add_numbered(document: Document, text: str) -> None:
    """Add a real numbered-list paragraph using Word's numbering style."""
    paragraph = document.add_paragraph(style="List Number")
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.paragraph_format.line_spacing = 1.25
    paragraph.add_run(text)


def build() -> None:
    """Create one human-readable handbook from the canonical Markdown source."""
    document = Document()
    configure_document(document)
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    first_heading = True

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            title = document.add_paragraph()
            title.paragraph_format.space_before = Pt(12)
            title.paragraph_format.space_after = Pt(3)
            set_font(title.add_run(stripped[2:]), "Calibri", 24, RGBColor(11, 37, 69), True)
            subtitle = document.add_paragraph("Human-facing guide for the hybrid operating system", style="Handbook Subtitle")
            continue
        if stripped.startswith("## "):
            if not first_heading:
                document.add_paragraph().paragraph_format.space_after = Pt(2)
            document.add_paragraph(stripped[3:], style="Heading 1")
            first_heading = False
            continue
        if stripped.startswith("- "):
            add_bullet(document, stripped[2:].strip("`"))
            continue
        if len(stripped) > 3 and stripped[0].isdigit() and stripped[1:3] == ". ":
            add_numbered(document, stripped[3:])
            continue
        document.add_paragraph(stripped)

    document.core_properties.title = "Triton AI Corp Human Employee Handbook"
    document.core_properties.subject = "Human-facing operating guide"
    document.core_properties.author = "Triton AI Corp"
    document.save(OUTPUT)


if __name__ == "__main__":
    build()
