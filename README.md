# AutoCV - AI-Powered Resume Scoring System

AutoCV is a Flask-based web application that analyzes student resumes using NLP and machine learning to provide detailed scores, actionable feedback, and bullet point improvements.

## Features

- **Comprehensive Scoring**: Analyzes resumes across 6 dimensions with 0-100 scores
- **AI-Powered Matching**: Uses sentence-transformers for intelligent skill matching
- **Actionable Feedback**: Prioritized suggestions for improvement
- **Bullet Rewrites**: Example improvements for weak descriptions
- **ATS Compliance**: Checks resume parse-ability for Applicant Tracking Systems
- **Role-Aware**: Tailored scoring when target role or job description provided
- **REST API**: Full API for integration with other systems

## Tech Stack

- **Backend**: Python 3.11, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **NLP**: spaCy, sentence-transformers (all-MiniLM-L6-v2)
- **Parsing**: PyMuPDF (PDF), python-docx (DOCX)
- **Frontend**: Jinja2 templates with Tailwind CSS

## Installation

### Prerequisites

- Python 3.11+
- pip

### Setup

1. **Clone or download the project**

2. **Create virtual environment**
```bash
python3.11 -m venv venv   # On Windows: python -m venv venvwin
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

5. **Run the application** (database auto-initializes on first run)
```bash
python app.py
```

6. **Access the application**
Open browser and go to: `http://127.0.0.1:5000`

## Usage

### Web Interface

1. Navigate to `http://127.0.0.1:5000`
2. Upload your resume (PDF or DOCX)
3. Optionally enter target role and/or job description
4. Click "Analyze Resume"
5. View your detailed report with scores and feedback

### API Usage

**Score Resume (POST /api/score-resume)**

```bash
curl -X POST http://127.0.0.1:5000/api/score-resume \
  -F "file=@resume.pdf" \
  -F "target_role=SDE Intern" \
  -F "jd_text=Looking for Python developer with Flask experience..."
```

**Get Report (GET /api/report/<report_id>)**

```bash
curl http://127.0.0.1:5000/api/report/550e8400-e29b-41d4-a716-446655440000
```

## Scoring System

Overall score is computed using weighted sub-scores:

- **Structure & Formatting** (15%): Section completeness, page count
- **Grammar & Clarity** (15%): Action verbs, metrics, passive voice
- **ATS Compliance** (20%): Parse-ability, standard headers, contact info
- **Skill Match** (25%): Semantic similarity to role/JD
- **Projects & Impact** (20%): Number of projects, technical depth, metrics
- **Education & Achievements** (5%): Degree, GPA, certifications

## Project Structure

```
autocv/
├── app.py                    # Flask application entry point
├── config.py                 # Configuration and constants
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .github/
│   └── copilot-instructions.md  # AI coding agent guidelines
├── database/
│   ├── models.py            # SQLAlchemy models
│   └── db.py                # Database initialization
├── core/
│   ├── parser.py            # PDF/DOCX parsing
│   ├── sections.py          # Section detection
│   ├── skills.py            # Skill extraction
│   ├── matcher.py           # JD/role matching
│   ├── scorer.py            # Scoring logic
│   ├── feedback.py          # Feedback generation
│   └── ats.py               # ATS compliance checks
├── data/
│   └── skills_taxonomy.json # Tech skills database
├── templates/
│   ├── base.html            # Base template
│   ├── upload.html          # Upload form
│   └── report.html          # Report display
├── static/
│   └── (CSS/JS assets)
├── uploads/                 # Temporary file storage
└── tests/
    ├── test_parser.py
    └── test_scorer.py
```

## Performance

- Average processing time: 3-5 seconds per resume
- Supports 1-5 page resumes
- Handles PDF and DOCX formats
- Local processing, no external API calls

## Future Enhancements

- Multi-language support
- LinkedIn/GitHub import
- Batch processing dashboard for T&P cells
- Role-specific rubrics (SDE, Data, Cybersecurity)
- Export to PDF reports

## License

MIT License

## Author

Built with Flask + AI for student career success
## Example API Response

```json
{
  "report_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-10-29T22:30:00Z",
  "filename": "john_doe_resume.pdf",
  "overall_score": 78.5,
  "sub_scores": {
    "structure_formatting": 85.0,
    "grammar_clarity": 75.0,
    "ats_compliance": 90.0,
    "skill_match": 72.0,
    "projects_impact": 68.0,
    "education_achievements": 82.0
  },
  "feedback": {
    "high_priority": [
      "Add quantifiable metrics to project descriptions (e.g., 'improved performance by 40%')",
      "Add relevant skills for better role match: GraphQL, System Design, Docker"
    ],
    "medium_priority": [
      "Replace passive phrases with strong action verbs (Developed, Built, Implemented)"
    ],
    "low_priority": []
  },
  "bullet_rewrites": [
    {
      "original": "Made a face detection system",
      "suggested": "Developed real-time face detection system using OpenCV and Python, achieving 92% accuracy on test dataset of 5,000+ images"
    }
  ],
  "evidence": {
    "missing_sections": {},
    "skill_gaps": ["Docker", "Kubernetes", "System Design"],
    "weak_bullets": ["Worked on college website"],
    "ats_issues": []
  },
  "target_role": "SDE Intern"
}
```

## Quick Start Commands

**Setup**

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Run**

```bash
python app.py
```

**Test API**

```bash
curl -X POST http://127.0.0.1:5000/api/score-resume -F "file=@resume.pdf"
```