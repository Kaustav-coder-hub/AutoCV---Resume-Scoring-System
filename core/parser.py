import fitz  # PyMuPDF
from docx import Document
import re

def parse_pdf(file_path):
    """
    Parse PDF resume and extract structured information
    Returns dict with sections, contact info, and links
    """
    try:
        doc = fitz.open(file_path)
        full_text = ""
        
        # Extract text from all pages
        for page in doc:
            full_text += page.get_text()
        
        # Get page count BEFORE closing
        page_count = len(doc)
        
        doc.close()
        
        # Extract contact information
        contact = extract_contact_info(full_text)
        
        # Extract links
        links = extract_links(full_text)
        
        # Parse into sections
        sections = parse_sections(full_text)
        
        return {
            'full_text': full_text,
            'sections': sections,
            'contact': contact,
            'links': links,
            'page_count': page_count
        }
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")

def parse_docx(file_path):
    """
    Parse DOCX resume and extract structured information
    Returns dict with sections, contact info, and links
    """
    try:
        doc = Document(file_path)
        full_text = ""
        
        # Extract text from paragraphs
        for para in doc.paragraphs:
            full_text += para.text + "\n"
        
        # Extract contact information
        contact = extract_contact_info(full_text)
        
        # Extract links
        links = extract_links(full_text)
        
        # Parse into sections
        sections = parse_sections(full_text)
        
        # Estimate page count (rough approximation)
        page_count = max(1, len(full_text) // 3000)
        
        return {
            'full_text': full_text,
            'sections': sections,
            'contact': contact,
            'links': links,
            'page_count': page_count
        }
    except Exception as e:
        raise Exception(f"Error parsing DOCX: {str(e)}")

def extract_contact_info(text):
    """Extract email, phone, and other contact information"""
    contact = {
        'email': None,
        'phone': None,
        'linkedin': None,
        'github': None
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact['email'] = email_match.group()
    
    # Phone pattern (Indian and international)
    phone_pattern = r'\+?[\d\s\-\(\)]{10,}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact['phone'] = phone_match.group().strip()
    
    # LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
    linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_match:
        contact['linkedin'] = linkedin_match.group()
    
    # GitHub
    github_pattern = r'github\.com/[\w\-]+'
    github_match = re.search(github_pattern, text, re.IGNORECASE)
    if github_match:
        contact['github'] = github_match.group()
    
    return contact

def extract_links(text):
    """Extract all URLs from text"""
    url_pattern = r'https?://[^\s]+'
    links = re.findall(url_pattern, text)
    return links

def parse_sections(text):
    """
    Parse text into resume sections based on common headers
    Returns dict of section_name: content
    """
    sections = {}
    
    # Common section headers (case insensitive)
    section_patterns = {
        'education': r'(?i)(education|academic|qualification)',
        'experience': r'(?i)(experience|employment|work history)',
        'projects': r'(?i)(projects?|portfolio)',
        'skills': r'(?i)(skills?|technical skills?|competencies)',
        'achievements': r'(?i)(achievements?|accomplishments?|awards?)',
        'certifications': r'(?i)(certifications?|certificates?)',
        'summary': r'(?i)(summary|profile|objective|about)'
    }
    
    lines = text.split('\n')
    current_section = 'other'
    sections[current_section] = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line is a section header
        matched = False
        for section_name, pattern in section_patterns.items():
            if re.match(pattern, line):
                current_section = section_name
                sections[current_section] = []
                matched = True
                break
        
        if not matched:
            sections[current_section].append(line)
    
    # Join lines within each section
    for section in sections:
        sections[section] = '\n'.join(sections[section])
    
    return sections
