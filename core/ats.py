import re
import config

def check_ats_compliance(resume_data):
    """
    Check ATS (Applicant Tracking System) compliance
    Returns dict with compliance checks and score
    """
    checks = {
        'has_text_layer': True,  # PDF parsing succeeded
        'is_parsable': True,
        'standard_headers_present': [],
        'fonts_ok': True,  # Assume OK if parsed successfully
        'contact_info_complete': {},
        'issues': []
    }
    
    sections = resume_data.get('sections', {})
    contact = resume_data.get('contact', {})
    
    # Check for standard section headers
    standard_sections = ['education', 'experience', 'projects', 'skills']
    for section in standard_sections:
        if section in sections and sections[section].strip():
            checks['standard_headers_present'].append(section.title())
    
    # Check contact information completeness
    checks['contact_info_complete'] = {
        'email': contact.get('email') is not None,
        'phone': contact.get('phone') is not None,
        'linkedin': contact.get('linkedin') is not None,
        'github': contact.get('github') is not None
    }
    
    # Identify issues
    if len(checks['standard_headers_present']) < 3:
        checks['issues'].append('Missing standard section headers')
    
    if not checks['contact_info_complete']['email']:
        checks['issues'].append('Email address not found')
    
    if not checks['contact_info_complete']['phone']:
        checks['issues'].append('Phone number not found')
    
    # Calculate ATS score (0-100)
    score = 0
    score += len(checks['standard_headers_present']) * 15  # Max 60 for 4 sections
    score += sum(checks['contact_info_complete'].values()) * 10  # Max 40 for 4 contact fields
    
    return {
        'score': min(100, score),
        'checks': checks
    }
