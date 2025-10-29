import random

def generate_feedback(scoring_result, resume_data):
    """
    Generate prioritized, actionable feedback based on scores
    Returns dict with high/medium/low priority suggestions
    """
    sub_scores = scoring_result['sub_scores']
    evidence = scoring_result['evidence']
    
    high_priority = []
    medium_priority = []
    low_priority = []
    
    # Structure feedback (score < 70)
    if sub_scores['structure_formatting'] < 70:
        missing = evidence.get('missing_sections', {})
        if missing.get('missing_required'):
            high_priority.append(f"Add missing critical sections: {', '.join(missing['missing_required'])}")
        if missing.get('missing_optional'):
            medium_priority.append(f"Consider adding: {', '.join(missing['missing_optional'])}")
    
    # Grammar feedback (score < 70)
    if sub_scores['grammar_clarity'] < 70:
        high_priority.append("Replace passive phrases with strong action verbs (Developed, Built, Implemented, Achieved)")
        if 'Limited metrics' in str(evidence.get('grammar', [])):
            high_priority.append("Add quantifiable metrics to demonstrate impact (e.g., 'improved performance by 40%', 'reduced load time by 2s')")
    
    # ATS feedback (score < 80)
    if sub_scores['ats_compliance'] < 80:
        ats_issues = evidence.get('ats', [])
        for issue in ats_issues:
            medium_priority.append(f"ATS Issue: {issue}")
    
    # Skill match feedback (score < 75)
    if sub_scores['skill_match'] < 75:
        skill_gaps = evidence.get('skill_gaps', [])
        if skill_gaps:
            gap_list = ', '.join(skill_gaps[:5])
            high_priority.append(f"Add relevant skills for better role match: {gap_list}")
        else:
            medium_priority.append("Highlight more technical skills and tools you've used")
    
    # Projects feedback (score < 70)
    if sub_scores['projects_impact'] < 70:
        if 'Limited projects' in str(evidence.get('projects', [])):
            high_priority.append("Add 2-3 substantial projects showcasing different skills")
        if 'lack measurable outcomes' in str(evidence.get('projects', [])):
            high_priority.append("Quantify project impact with metrics (users served, performance gains, time saved)")
        if 'Limited technical' in str(evidence.get('projects', [])):
            medium_priority.append("Include specific technologies, frameworks, and tools used in each project")
    
    # Education feedback (score < 60)
    if sub_scores['education_achievements'] < 60:
        low_priority.append("Consider adding GPA, relevant coursework, or academic achievements")
        if 'certifications' not in resume_data.get('sections', {}):
            low_priority.append("Add relevant certifications to strengthen your profile")
    
    # General recommendations
    if scoring_result['overall_score'] < 75:
        medium_priority.append("Ensure consistent formatting, font sizes, and bullet point styles throughout")
    
    return {
        'high_priority': high_priority[:4],  # Limit to top 4
        'medium_priority': medium_priority[:4],
        'low_priority': low_priority[:3]
    }

def generate_bullet_rewrites(resume_data):
    """
    Generate example bullet rewrites for weak descriptions
    Returns list of before/after examples
    """
    rewrites = []
    sections = resume_data.get('sections', {})
    
    # Pattern to detect weak bullets
    weak_patterns = [
        r'worked on',
        r'helped with',
        r'involved in',
        r'made a',
        r'did',
        r'created a'
    ]
    
    # Check projects section
    projects_text = sections.get('projects', '')
    if projects_text:
        lines = projects_text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if not line or len(line) < 20:
                continue
            
            # Check if line contains weak phrases
            is_weak = any(pattern in line.lower() for pattern in weak_patterns)
            
            if is_weak:
                rewritten = rewrite_bullet(line)
                if rewritten != line:
                    rewrites.append({
                        'original': line[:100],  # Truncate if too long
                        'suggested': rewritten
                    })
            
            if len(rewrites) >= 3:  # Limit to 3 examples
                break
    
    # If no weak bullets found, provide generic examples
    if not rewrites:
        rewrites = [
            {
                'original': 'Made a website for college fest',
                'suggested': 'Developed responsive fest registration portal using React and Flask, handling 1,200+ registrations and reducing manual data entry by 80%'
            },
            {
                'original': 'Worked on machine learning project',
                'suggested': 'Built image classification model using PyTorch and ResNet-18, achieving 92% accuracy on 5,000+ test images'
            }
        ]
    
    return rewrites

def rewrite_bullet(bullet):
    """
    Rewrite a weak bullet point to be more impactful
    """
    templates = [
        "Developed {project} using {tech}, resulting in {impact}",
        "Built {project} with {tech}, achieving {metric}",
        "Implemented {feature} using {tech}, improving {metric}",
        "Designed {project} leveraging {tech}, serving {users}"
    ]
    
    # Simple heuristic rewrites
    bullet_lower = bullet.lower()
    
    if 'website' in bullet_lower or 'web' in bullet_lower:
        return "Developed responsive web application using React + Flask, serving 1,000+ users with 95% satisfaction rating"
    elif 'ml' in bullet_lower or 'machine learning' in bullet_lower or 'model' in bullet_lower:
        return "Built machine learning model using PyTorch/TensorFlow, achieving 90%+ accuracy on validation dataset"
    elif 'app' in bullet_lower or 'application' in bullet_lower:
        return "Engineered mobile/web application using modern frameworks, deployed to 500+ active users"
    elif 'project' in bullet_lower:
        return "Implemented end-to-end project using Python/Java, reducing processing time by 40%"
    else:
        return "Developed " + bullet.replace('Worked on', '').replace('worked on', '').strip() + " with measurable impact"

def compile_full_feedback(scoring_result, resume_data):
    """
    Compile complete feedback report with suggestions and rewrites
    """
    suggestions = generate_feedback(scoring_result, resume_data)
    rewrites = generate_bullet_rewrites(resume_data)
    
    return {
        'feedback': suggestions,
        'bullet_rewrites': rewrites
    }
