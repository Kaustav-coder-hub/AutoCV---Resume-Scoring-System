import json
import re
import spacy
import config

# Load spaCy model
try:
    nlp = spacy.load(config.SPACY_MODEL)
except:
    print(f"Warning: spaCy model {config.SPACY_MODEL} not found. Run: python -m spacy download {config.SPACY_MODEL}")
    nlp = None

def load_taxonomy():
    """Load skills taxonomy from JSON file"""
    try:
        with open(config.SKILLS_TAXONOMY_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: skills_taxonomy.json not found, using default taxonomy")
        return get_default_taxonomy()

def get_default_taxonomy():
    """Return default skills taxonomy if file not found"""
    return {
        "languages": ["Python", "Java", "JavaScript", "C++", "C", "Go", "Rust", "TypeScript"],
        "frameworks": ["Flask", "Django", "React", "Node.js", "Express", "Spring Boot", "FastAPI"],
        "ml_ai": ["PyTorch", "TensorFlow", "scikit-learn", "OpenCV", "Keras", "Hugging Face"],
        "databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Firebase"],
        "cloud": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Heroku", "Vercel"],
        "tools": ["Git", "GitHub", "Linux", "CI/CD", "Jenkins", "VS Code"],
        "security": ["Kali Linux", "penetration testing", "OWASP", "cybersecurity"]
    }

def extract_skills(text, taxonomy=None):
    """
    Extract technical skills from text using taxonomy and NLP
    Returns list of matched skills with categories
    """
    if taxonomy is None:
        taxonomy = load_taxonomy()
    
    found_skills = {}
    text_lower = text.lower()
    
    # Search for each skill in taxonomy
    for category, skills in taxonomy.items():
        found_skills[category] = []
        
        for skill in skills:
            # Case-insensitive search with word boundaries
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills[category].append(skill)
    
    # Use spaCy for additional entity extraction if available
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG']:
                # Check if it's a tech term
                if any(ent.text.lower() in skill.lower() for category in taxonomy.values() for skill in category):
                    continue  # Already captured
    
    # Flatten and return unique skills
    all_skills = []
    for category, skills in found_skills.items():
        for skill in skills:
            all_skills.append({'skill': skill, 'category': category})
    
    return all_skills
