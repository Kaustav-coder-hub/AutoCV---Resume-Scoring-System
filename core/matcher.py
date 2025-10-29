from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import config

# Load sentence transformer model (lazy loading)
_model = None

def get_model():
    """Lazy load sentence transformer model"""
    global _model
    if _model is None:
        print(f"Loading embedding model: {config.EMBEDDING_MODEL}")
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model

def compute_similarity(resume_text, jd_text):
    """
    Compute semantic similarity between resume and job description
    Returns similarity score between 0 and 1
    """
    if not jd_text or not resume_text:
        return 0.0
    
    model = get_model()
    
    # Generate embeddings
    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([jd_text])
    
    # Compute cosine similarity
    similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
    
    return float(similarity)

def keyword_coverage(resume_skills, jd_skills):
    """
    Calculate percentage of JD skills present in resume
    Returns coverage ratio between 0 and 1
    """
    if not jd_skills:
        return 1.0  # No specific requirements
    
    resume_skills_lower = {skill.lower() for skill in resume_skills}
    jd_skills_lower = {skill.lower() for skill in jd_skills}
    
    matched = resume_skills_lower.intersection(jd_skills_lower)
    coverage = len(matched) / len(jd_skills_lower) if jd_skills_lower else 0.0
    
    return coverage

def extract_jd_skills(jd_text, taxonomy):
    """Extract skills from job description using taxonomy"""
    from core.skills import extract_skills
    skills = extract_skills(jd_text, taxonomy)
    return [s['skill'] for s in skills]

def match_role_to_resume(resume_data, target_role=None, jd_text=None):
    """
    Match resume to target role or job description
    Returns dict with similarity score and skill gaps
    """
    from core.skills import load_taxonomy, extract_skills
    
    taxonomy = load_taxonomy()
    resume_text = resume_data.get('full_text', '')
    resume_skills_data = extract_skills(resume_text, taxonomy)
    resume_skills = [s['skill'] for s in resume_skills_data]
    
    result = {
        'semantic_similarity': 0.0,
        'keyword_coverage': 0.0,
        'skill_gaps': [],
        'matched_skills': resume_skills
    }
    
    # If JD provided, use it
    if jd_text:
        result['semantic_similarity'] = compute_similarity(resume_text, jd_text)
        jd_skills = extract_jd_skills(jd_text, taxonomy)
        result['keyword_coverage'] = keyword_coverage(resume_skills, jd_skills)
        result['skill_gaps'] = list(set(jd_skills) - set(resume_skills))
    
    # If only role provided, use role-specific keywords
    elif target_role:
        role_keywords = get_role_keywords(target_role)
        result['semantic_similarity'] = compute_similarity(resume_text, ' '.join(role_keywords))
        result['keyword_coverage'] = keyword_coverage(resume_skills, role_keywords)
        result['skill_gaps'] = list(set(role_keywords) - set(resume_skills))
    
    return result

def get_role_keywords(role):
    """Get expected skills for common roles"""
    role_mappings = {
        'sde intern': ['Python', 'Java', 'C++', 'DSA', 'Git', 'OOP', 'algorithms'],
        'data analyst': ['Python', 'SQL', 'Excel', 'Tableau', 'Power BI', 'statistics'],
        'ml engineer': ['Python', 'PyTorch', 'TensorFlow', 'scikit-learn', 'ML', 'deep learning'],
        'frontend': ['JavaScript', 'React', 'HTML', 'CSS', 'TypeScript', 'UI/UX'],
        'backend': ['Python', 'Java', 'Node.js', 'SQL', 'API', 'Docker'],
        'full stack': ['React', 'Node.js', 'Python', 'SQL', 'Git', 'REST API'],
        'cybersecurity': ['Kali Linux', 'penetration testing', 'OWASP', 'networking', 'security']
    }
    
    role_lower = role.lower()
    for key, keywords in role_mappings.items():
        if key in role_lower:
            return keywords
    
    return []  # No specific role keywords
