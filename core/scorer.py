import re
import config
from core.ats import check_ats_compliance
from core.matcher import match_role_to_resume
from core.sections import detect_missing_sections

def score_structure(resume_data):
    """
    Score resume structure and formatting (0-100)
    Checks: section completeness, page count, organization
    """
    score = 0
    evidence = []
    
    sections = resume_data.get('sections', {})
    page_count = resume_data.get('page_count', 1)
    
    # Section completeness (60 points)
    required_sections = ['education', 'experience', 'projects', 'skills']
    present_count = sum(1 for sec in required_sections if sec in sections and sections[sec].strip())
    score += (present_count / len(required_sections)) * 60
    
    if present_count < len(required_sections):
        missing = [s for s in required_sections if s not in sections or not sections[s].strip()]
        evidence.append(f"Missing sections: {', '.join(missing)}")
    
    # Page count (20 points) - ideal is 1-2 pages
    if page_count == 1 or page_count == 2:
        score += 20
        evidence.append(f"Good resume length: {page_count} page(s)")
    elif page_count == 3:
        score += 10
        evidence.append(f"Resume is slightly long: {page_count} pages")
    else:
        evidence.append(f"Resume length issue: {page_count} pages")
    
    # Optional sections bonus (20 points)
    optional_sections = ['achievements', 'certifications', 'summary']
    optional_count = sum(1 for sec in optional_sections if sec in sections and sections[sec].strip())
    score += (optional_count / len(optional_sections)) * 20
    
    return min(100, score), evidence

def score_grammar(resume_data):
    """
    Score grammar and clarity (0-100)
    Checks: action verbs, passive voice, bullet structure
    """
    score = 100
    evidence = []
    
    full_text = resume_data.get('full_text', '').lower()
    sections = resume_data.get('sections', {})
    
    # Check for action verbs (40 points)
    action_verb_count = sum(1 for verb in config.ACTION_VERBS if verb in full_text)
    if action_verb_count >= 10:
        evidence.append(f"Good use of action verbs ({action_verb_count} found)")
    elif action_verb_count >= 5:
        score -= 20
        evidence.append(f"Limited action verbs ({action_verb_count} found)")
    else:
        score -= 40
        evidence.append(f"Very few action verbs ({action_verb_count} found)")
    
    # Check for passive voice (30 points penalty)
    passive_count = 0
    for pattern in config.PASSIVE_PATTERNS:
        passive_count += len(re.findall(pattern, full_text))
    
    if passive_count > 5:
        score -= 30
        evidence.append(f"Excessive passive voice detected ({passive_count} instances)")
    elif passive_count > 2:
        score -= 15
        evidence.append(f"Some passive voice detected ({passive_count} instances)")
    
    # Check for quantifiable achievements (30 points)
    numbers = re.findall(r'\d+[%+]?', full_text)
    if len(numbers) >= 5:
        evidence.append(f"Good use of metrics ({len(numbers)} numbers found)")
    elif len(numbers) >= 2:
        score -= 15
        evidence.append(f"Limited metrics ({len(numbers)} numbers found)")
    else:
        score -= 30
        evidence.append("Very few quantifiable achievements")
    
    return max(0, score), evidence

def score_ats_compliance(resume_data):
    """Score ATS compliance (0-100)"""
    ats_result = check_ats_compliance(resume_data)
    return ats_result['score'], ats_result['checks']['issues']

def score_skill_match(resume_data, target_role=None, jd_text=None):
    """
    Score skill match to target role or JD (0-100)
    Uses semantic similarity and keyword coverage
    """
    match_result = match_role_to_resume(resume_data, target_role, jd_text)
    
    # Combine semantic similarity (60%) and keyword coverage (40%)
    similarity = match_result['semantic_similarity']
    coverage = match_result['keyword_coverage']
    
    score = (similarity * 0.6 + coverage * 0.4) * 100
    
    evidence = [
        f"Semantic similarity: {similarity:.2f}",
        f"Keyword coverage: {coverage:.2%}",
        f"Skills matched: {len(match_result['matched_skills'])}"
    ]
    
    if match_result['skill_gaps']:
        evidence.append(f"Missing skills: {', '.join(match_result['skill_gaps'][:5])}")
    
    return score, evidence, match_result['skill_gaps']

def score_projects(resume_data):
    """
    Score projects and impact (0-100)
    Checks: number of projects, technical depth, measurable outcomes
    """
    score = 0
    evidence = []
    
    sections = resume_data.get('sections', {})
    projects_text = sections.get('projects', '')
    
    if not projects_text:
        return 0, ["No projects section found"]
    
    # Count project indicators (bullet points, project names)
    project_count = len(re.findall(r'(?:^|\n)[\-\•\*]', projects_text))
    project_count = max(project_count, len(re.findall(r'\bproject\b', projects_text.lower())))
    
    # Number of projects (40 points)
    if project_count >= 3:
        score += 40
        evidence.append(f"Good number of projects: {project_count}")
    elif project_count >= 2:
        score += 30
        evidence.append(f"Adequate projects: {project_count}")
    else:
        score += 15
        evidence.append(f"Limited projects: {project_count}")
    
    # Technical depth - check for technology mentions (30 points)
    tech_mentions = len(re.findall(r'\b(?:Python|Java|React|Flask|Django|ML|AI|database|API)\b', 
                                   projects_text, re.IGNORECASE))
    if tech_mentions >= 5:
        score += 30
        evidence.append(f"Strong technical depth ({tech_mentions} tech mentions)")
    elif tech_mentions >= 3:
        score += 20
    else:
        score += 10
        evidence.append("Limited technical details")
    
    # Measurable outcomes (30 points)
    metrics = re.findall(r'\d+[%+]?', projects_text)
    if len(metrics) >= 3:
        score += 30
        evidence.append(f"Projects show measurable impact ({len(metrics)} metrics)")
    elif len(metrics) >= 1:
        score += 15
    else:
        score += 5
        evidence.append("Projects lack measurable outcomes")
    
    return min(100, score), evidence

def score_education(resume_data):
    """
    Score education and achievements (0-100)
    Checks: degree completion, GPA, certifications, awards
    """
    score = 0
    evidence = []
    
    sections = resume_data.get('sections', {})
    education_text = sections.get('education', '')
    achievements_text = sections.get('achievements', '')
    certifications_text = sections.get('certifications', '')
    
    if not education_text:
        return 0, ["No education section found"]
    
    # Check for degree (50 points)
    degree_keywords = ['b.tech', 'btech', 'bachelor', 'b.e', 'b.sc', 'master', 'm.tech', 'mtech']
    if any(kw in education_text.lower() for kw in degree_keywords):
        score += 50
        evidence.append("Degree information present")
    else:
        score += 20
        evidence.append("Degree information unclear")
    
    # Check for GPA/percentage (20 points)
    gpa_pattern = r'(?:\d\.\d+|\d{2,3}(?:\.\d+)?%)'
    if re.search(gpa_pattern, education_text):
        score += 20
        evidence.append("Academic performance mentioned")
    
    # Certifications (15 points)
    if certifications_text and len(certifications_text) > 20:
        score += 15
        evidence.append("Certifications listed")
    
    # Achievements/Awards (15 points)
    if achievements_text and len(achievements_text) > 20:
        score += 15
        evidence.append("Achievements/awards mentioned")
    
    return min(100, score), evidence

def compute_overall_score(sub_scores, weights=None):
    """
    Compute weighted overall score from sub-scores
    """
    if weights is None:
        weights = config.WEIGHTS
    
    overall = (
        sub_scores['structure_formatting'] * weights['structure'] +
        sub_scores['grammar_clarity'] * weights['grammar'] +
        sub_scores['ats_compliance'] * weights['ats'] +
        sub_scores['skill_match'] * weights['skill_match'] +
        sub_scores['projects_impact'] * weights['projects'] +
        sub_scores['education_achievements'] * weights['education']
    )
    
    return round(overall, 1)

def score_resume(resume_data, target_role=None, jd_text=None):
    """
    Main function to score resume across all dimensions
    Returns complete scoring report
    """
    # Compute all sub-scores
    structure_score, structure_evidence = score_structure(resume_data)
    grammar_score, grammar_evidence = score_grammar(resume_data)
    ats_score, ats_evidence = score_ats_compliance(resume_data)
    skill_score, skill_evidence, skill_gaps = score_skill_match(resume_data, target_role, jd_text)
    projects_score, projects_evidence = score_projects(resume_data)
    education_score, education_evidence = score_education(resume_data)
    
    sub_scores = {
        'structure_formatting': round(structure_score, 1),
        'grammar_clarity': round(grammar_score, 1),
        'ats_compliance': round(ats_score, 1),
        'skill_match': round(skill_score, 1),
        'projects_impact': round(projects_score, 1),
        'education_achievements': round(education_score, 1)
    }
    
    overall_score = compute_overall_score(sub_scores)
    
    # Compile evidence
    evidence = {
        'structure': structure_evidence,
        'grammar': grammar_evidence,
        'ats': ats_evidence,
        'skills': skill_evidence,
        'projects': projects_evidence,
        'education': education_evidence,
        'skill_gaps': skill_gaps,
        'missing_sections': detect_missing_sections(resume_data.get('sections', {}))
    }
    
    return {
        'overall_score': overall_score,
        'sub_scores': sub_scores,
        'evidence': evidence
    }
