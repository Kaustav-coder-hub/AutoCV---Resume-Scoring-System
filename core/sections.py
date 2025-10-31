import re
import config

def normalize_sections(sections):
    """
    Normalize and validate resume sections
    Returns dict with standardized section names
    """
    normalized = {}
    
    # Map variations to standard names
    section_mapping = {
        'education': ['education', 'academic', 'qualification'],
        'experience': ['experience', 'employment', 'work', 'work history'],
        'projects': ['projects', 'project', 'portfolio'],
        'skills': ['skills', 'technical skills', 'competencies'],
        'achievements': ['achievements', 'accomplishments', 'awards'],
        'certifications': ['certifications', 'certificates', 'licenses'],
        'summary': ['summary', 'profile', 'objective', 'about']
    }
    
    for standard_name, variations in section_mapping.items():
        for section_key in sections.keys():
            if section_key.lower() in variations:
                normalized[standard_name] = sections[section_key]
                break
    
    return normalized

def detect_missing_sections(sections):
    """
    Identify which standard sections are missing
    Returns list of missing section names
    """
    present_sections = set(sections.keys())
    required_sections = {'education', 'experience', 'projects', 'skills'}
    optional_sections = {'achievements', 'certifications', 'summary'}
    
    missing_required = required_sections - present_sections
    missing_optional = optional_sections - present_sections
    
    return {
        'missing_required': list(missing_required),
        'missing_optional': list(missing_optional)
    }

def count_bullets(section_text):
    """Count bullet points in a section"""
    bullet_patterns = [r'^\s*[\-\•\*]', r'^\s*\d+\.']
    lines = section_text.split('\n')
    count = 0
    
    for line in lines:
        for pattern in bullet_patterns:
            if re.match(pattern, line.strip()):
                count += 1
                break
    
    return count
