from fpdf import FPDF


def add_section(pdf: FPDF, title: str):
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def add_paragraph(pdf: FPDF, text: str):
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, text)
    pdf.ln(2)


def add_bullets(pdf: FPDF, items):
    pdf.set_font("Helvetica", size=12)
    pdf.set_x(pdf.l_margin)
    for item in items:
        pdf.multi_cell(pdf.w - 2 * pdf.l_margin, 8, f"- {item}")
    pdf.ln(2)


def build_pdf(path: str = "project_overview.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "AutoCV - Project Overview", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    add_section(pdf, "Purpose")
    add_paragraph(pdf, "Accept resumes (PDF/DOCX), parse, score against target roles, and return a report with prioritized feedback.")

    add_section(pdf, "Tech Stack")
    add_bullets(
        pdf,
        [
            "Backend: Flask 3.x, SQLAlchemy/SQLite (Postgres-ready), Gunicorn for prod",
            "Parsing: PyMuPDF (fitz) for PDF, python-docx for DOCX",
            "NLP/Scoring: spaCy en_core_web_sm, sentence-transformers, custom scoring logic",
            "Frontend: Jinja templates with Tailwind-like utility classes",
            "Config: config.py + .env (SECRET_KEY), python-dotenv",
        ],
    )

    add_section(pdf, "Flow")
    add_bullets(
        pdf,
        [
            "Upload: Flask receives resume at /upload and saves to uploads/",
            "Parse: core/parser.py uses fitz for PDF or python-docx for DOCX; cleans text/sections",
            "Skills/Sections: core/skills.py loads data/skills_taxonomy.json; core/sections.py maps sections",
            "Score: core/scorer.py and core/matcher.py compute sub-scores and overall score",
            "Feedback: core/feedback.py and core/ats.py produce High/Medium/Low priorities and bullet rewrites",
            "Persist: SQLAlchemy saves report/feedback (SQLite by default)",
            "Render: /report/<id> uses templates/report.html to display scores and feedback",
        ],
    )

    add_section(pdf, "Run Locally")
    add_paragraph(
        pdf,
        "python -m venv .venv\n"
        "source .venv/bin/activate\n"
        "pip install --upgrade pip setuptools wheel\n"
        "pip install -r requirements.txt\n"
        "echo 'SECRET_KEY=replace-me' > .env\n"
        "python app.py  # http://127.0.0.1:5000",
    )

    add_section(pdf, "Deployment Notes")
    add_paragraph(
        pdf,
        "Use Python 3.11.x (PyMuPDF wheels). Start: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT.\n"
        "Set SECRET_KEY and DATABASE_URL in env; default is SQLite.",
    )

    pdf.output(path)
    print(f"Wrote {path}")


if __name__ == "__main__":
    build_pdf()
