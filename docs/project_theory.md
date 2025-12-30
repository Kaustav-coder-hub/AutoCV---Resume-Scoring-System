# AutoCV – Project Theory (Practical Brief for Teammates)

AutoCV is a web-based resume scoring and feedback system. A user uploads a PDF or DOCX resume, optionally provides a target role, and the system analyzes the content to produce a score plus prioritized feedback showing how well the resume fits the role and what to improve.

## High-Level Goal

Convert a resume into a machine-readable form, compare it against a target role, compute a balanced score, and provide clear, actionable feedback.

## Tech Stack (What and Why)

- **Backend:** Flask (Python) for HTTP routes, form handling, file upload, and server-side templates. Lightweight and easy to integrate with NLP/ML code.
- **Database:** SQLite with SQLAlchemy to store reports (scores, feedback, metadata). SQLAlchemy keeps schema and queries simple; can be swapped to Postgres by changing the DB URL.
- **Parsing:** PyMuPDF (fitz) for PDFs and `python-docx` for DOCX to extract clean text from binary files.
- **NLP & Scoring:** spaCy for tokens/entities; Sentence-Transformers for embeddings (semantic similarity); custom rules for skills coverage, section presence, ATS checks, and final scoring.
- **Frontend:** Jinja2 templates with utility (Tailwind-style) classes for fast styling of upload and report pages.
- **Config & Secrets:** `config.py` for paths and limits; `.env` for `SECRET_KEY`, DB URL, and other secrets via `python-dotenv` to avoid hardcoding.

## End-to-End Flow

1. **Landing & Upload**

   - What: User visits `/`, uploads a resume (PDF/DOCX), and can enter a target role.
   - How: `app.py` renders `upload.html`; POST `/upload` saves the file to `uploads/` and captures role text and metadata.
   - Why: We need the binary resume plus role context before parsing and scoring.

2. **Parsing (File → Text)**

   - What: Convert the uploaded file to plain text and clean it.
   - How: `core/parser.py` picks fitz for PDFs or `python-docx` for DOCX; extracts text per page/paragraph; removes extra newlines and spaces.
   - Why: All downstream NLP and scoring operate on text, not binary files; better parsing leads to better scoring.

3. **Sections & Skills Extraction**

   - What: Split resume text into logical sections (Summary, Experience, Education, Skills, Projects) and detect skills (e.g., Python, SQL, ML).
   - How: `core/sections.py` uses heading heuristics (“EXPERIENCE”, “EDUCATION”, etc.) to chunk text; `core/skills.py` loads `data/skills_taxonomy.json` and matches tokens/phrases to known skills; spaCy entities (ORG, DATE) can help identify experience lines.
   - Why: Structured content makes it easy to detect missing sections and compute skills coverage.

4. **Match to Target Role & Score**

   - What: Compare resume content to the target role and compute scores.
   - How (two parts):
     - **Keyword/Skills Coverage:** `core/matcher.py` derives required/preferred skills from the role/JD, then overlaps them with extracted resume skills to find matches and missing must-haves.
     - **Semantic Similarity:** Sentence-Transformers embeddings for resume text vs. role/JD text; cosine similarity captures meaning beyond exact words.
   - Final Score: `core/scorer.py` combines coverage, semantic similarity, and structure/ATS signals into sub-scores and an overall score (0–100). Balancing keywords and semantics reduces false negatives and irrelevant matches.

5. **Feedback Generation (High / Medium / Low)**

   - What: Actionable feedback grouped by priority, plus suggested bullet rewrites.
   - How: `core/feedback.py` and `core/ats.py` apply rules: missing required skills, absent sections, bullets lacking metrics, ATS formatting issues. Priority reflects impact/urgency.
   - Why: Users need specific steps, not just a numeric score.

6. **Persist the Report**

   - What: Store score, sub-scores, extracted skills/sections, feedback, and timestamp.
   - How: SQLAlchemy models in `database/models.py`; SQLite path from `config.py`. Switching to Postgres is just a DB URL change.
   - Why: Enables `/report/<id>` retrieval, history, and future analytics.

7. **Render the Report**

   - What: Show a clean HTML report with overall score, priority feedback, skills match, and section status.
   - How: Flask route `/report/<id>` fetches from DB; `templates/report.html` renders score cards and color-coded badges (High=red, Medium=yellow, Low=green).
   - Why: Human-friendly visualization so users immediately see strengths, gaps, and next steps.

8. **Optional API Access**
   - What: JSON endpoints (e.g., `/api/report/<id>`) for report data.
   - How: Flask routes serialize stored report objects.
   - Why: Supports integrations and alternate frontends.

## How to Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "SECRET_KEY=replace-me" > .env  # set your secret key
python app.py  # visit http://127.0.0.1:5000
```

- Use Python 3.11.x so PyMuPDF installs from wheels.
- Uploaded files are saved in `uploads/`.

## Deployment Notes

- Command: `gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT`
- Env vars: `SECRET_KEY` (required), `DATABASE_URL` (optional; defaults to SQLite). Prefer Postgres in production for durability.
- Reasoning: Gunicorn is production-grade; env vars keep secrets and deployment-specific config out of code.

## Where to Extend Next

- Scoring: Adjust weights or add role-specific configs in `core/scorer.py` and the skills taxonomy JSON.
- Database: Swap SQLite to Postgres by changing the SQLAlchemy URL in `config.py` or via environment variable.
- Authentication/multi-user: Add users table and gate report access per user.
- UI: Refine `templates/*.html`; utility-class styling makes iteration fast.
