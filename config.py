import os

# Scoring weights for each component
WEIGHTS = {
    'structure': 0.15,
    'grammar': 0.15,
    'ats': 0.20,
    'skill_match': 0.25,
    'projects': 0.20,
    'education': 0.05
}

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = f'sqlite:///{os.path.join(BASE_DIR, "autocv.db")}'

# Model configuration
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
SPACY_MODEL = 'en_core_web_sm'

# Upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Skills taxonomy path
SKILLS_TAXONOMY_PATH = os.path.join(BASE_DIR, 'data', 'skills_taxonomy.json')

# Action verbs for grammar scoring
ACTION_VERBS = [
    'developed', 'built', 'created', 'designed', 'implemented', 'engineered',
    'deployed', 'optimized', 'achieved', 'led', 'managed', 'coordinated',
    'analyzed', 'researched', 'improved', 'automated', 'integrated', 'launched',
    'established', 'streamlined', 'collaborated', 'spearheaded', 'architected'
]

# Passive voice patterns to detect
PASSIVE_PATTERNS = [
    r'\bwas\s+\w+ed\b',
    r'\bwere\s+\w+ed\b',
    r'\bbeen\s+\w+ed\b',
    r'\bworked\s+on\b',
    r'\bhelped\s+with\b',
    r'\binvolved\s+in\b'
]

# Standard resume sections
STANDARD_SECTIONS = [
    'education', 'experience', 'projects', 'skills', 'achievements',
    'certifications', 'summary', 'objective'
]


