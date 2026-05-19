"""Build the SPARK one-pager PDF (external-pitch tone, single page)."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

OUTPUT = "../assets/SPARK-methodology.pdf"

ACCENT = HexColor("#1E3A8A")   # deep blue
TEXT   = HexColor("#1F2937")   # near-black
MUTED  = HexColor("#6B7280")   # warm grey

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=0.6 * inch,
    rightMargin=0.6 * inch,
    topMargin=0.5 * inch,
    bottomMargin=0.5 * inch,
    title="SPARK — A Methodology for AI-Augmented Decision-Making",
    author="DrRon",
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title", parent=styles["Title"],
    fontName="Helvetica-Bold", fontSize=34, leading=38,
    textColor=ACCENT, alignment=TA_LEFT, spaceAfter=0,
)
subhead_style = ParagraphStyle(
    "Subhead", parent=styles["Normal"],
    fontName="Helvetica", fontSize=12, leading=14,
    textColor=TEXT, alignment=TA_LEFT, spaceAfter=2,
)
tagline_style = ParagraphStyle(
    "Tagline", parent=styles["Normal"],
    fontName="Helvetica-Oblique", fontSize=10, leading=12,
    textColor=MUTED, alignment=TA_LEFT, spaceAfter=8,
)
lead_style = ParagraphStyle(
    "Lead", parent=styles["Normal"],
    fontName="Helvetica", fontSize=10, leading=13.5,
    textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=10,
)
stage_letter_style = ParagraphStyle(
    "StageLetter", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=22, leading=24,
    textColor=ACCENT, alignment=TA_CENTER,
)
stage_name_style = ParagraphStyle(
    "StageName", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=11, leading=13.5,
    textColor=TEXT, alignment=TA_LEFT, spaceAfter=2,
)
stage_body_style = ParagraphStyle(
    "StageBody", parent=styles["Normal"],
    fontName="Helvetica", fontSize=9.25, leading=12,
    textColor=TEXT, alignment=TA_LEFT,
)
section_header_style = ParagraphStyle(
    "Section", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=10.5, leading=13,
    textColor=ACCENT, alignment=TA_LEFT, spaceAfter=4,
)
bullet_style = ParagraphStyle(
    "Bullet", parent=styles["Normal"],
    fontName="Helvetica", fontSize=9.25, leading=12,
    textColor=TEXT, alignment=TA_LEFT,
    leftIndent=10, bulletIndent=0,
)
footer_style = ParagraphStyle(
    "Footer", parent=styles["Normal"],
    fontName="Helvetica-Oblique", fontSize=8, leading=10,
    textColor=MUTED, alignment=TA_CENTER,
)

story = []

# Header block
story.append(Paragraph("SPARK", title_style))
story.append(Paragraph("A methodology for AI-augmented decision-making", subhead_style))
story.append(Paragraph("Speculate &nbsp;·&nbsp; Plan &nbsp;·&nbsp; Assess &nbsp;·&nbsp; Rank &nbsp;·&nbsp; Kickoff", tagline_style))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=2, spaceAfter=10))

# Lead paragraph
lead = (
    "Most teams collapse the journey from possibility to execution into a blur of meetings "
    "and gut calls. SPARK separates the work into five distinct stages, each matched to a "
    "specific mode of thinking and a specific kind of AI assistance. The result is a deliberate, "
    "defensible path from open-ended question to committed build — without losing the ambition "
    "of the original brief."
)
story.append(Paragraph(lead, lead_style))

# Five stages
stages = [
    ("S", "Speculate",
     "Diverge widely. Generate possibilities without filtering, judging, or scoping. "
     "<b>AI's role:</b> expand the option space using context from connected tools — past projects, "
     "market signals, prior decisions — and surface adjacent ideas the team would not reach on its own."),
    ("P", "Plan",
     "Sketch the shape of each promising candidate. Just enough detail to understand its scope, "
     "dependencies, and resource demands. <b>AI's role:</b> draft lightweight specifications, locate "
     "analogous prior work, and identify likely risks before they cost anything."),
    ("A", "Assess",
     "Confront each candidate with reality: budget, capacity, calendar, technical readiness, "
     "strategic fit. <b>AI's role:</b> pull live data from connected systems, surface conflicts, and "
     "flag the missing information that would otherwise emerge late."),
    ("R", "Rank",
     "Order the candidates. Force the trade-offs out into the open. <b>AI's role:</b> model alternative "
     "weightings, surface the cost of each choice, and draft the rationale so the decision can be "
     "defended later."),
    ("K", "Kickoff",
     "Commit. Move the top candidate(s) into build mode with owners, milestones, and a working "
     "feedback loop. <b>AI's role:</b> scaffold the work plan, set up tracking, and schedule follow-ups "
     "across connected systems so momentum doesn't depend on memory."),
]

rows = []
for letter_, name, body in stages:
    rows.append([
        Paragraph(letter_, stage_letter_style),
        [Paragraph(name, stage_name_style), Paragraph(body, stage_body_style)],
    ])

stage_table = Table(rows, colWidths=[0.55 * inch, 6.75 * inch])
stage_table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LINEBELOW", (0, 0), (-1, -2), 0.25, MUTED),
]))
story.append(stage_table)
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=2, spaceAfter=8))

# Why SPARK works
story.append(Paragraph("Why SPARK works", section_header_style))
why_points = [
    "Each stage names a distinct mode of thinking, so teams know what is being asked of them.",
    "AI's contribution differs by stage; the methodology tells you which kind of help to invoke.",
    "Connected tools turn AI from a generic brainstormer into a context-aware partner.",
    "Ranking is treated as a commitment, not a vote — feasibility wins arguments, not enthusiasm.",
]
for p in why_points:
    story.append(Paragraph(p, bullet_style, bulletText="•"))

story.append(Spacer(1, 10))
story.append(Paragraph(
    "SPARK · An AI-augmented methodology for moving from possibility to practice",
    footer_style,
))

doc.build(story)
print(f"Wrote {OUTPUT}")
