from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

import config
from database.db import db, init_db
from database.models import Report
from core.parser import parse_pdf, parse_docx
from core.scorer import score_resume
from core.feedback import compile_full_feedback

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'  # Use a strong, random value in production!
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE

# Initialize database
init_db(app)

# Ensure upload folder exists
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page with upload form"""
    return render_template('upload.html')

@app.route('/api/score-resume', methods=['POST'])
def score_resume_api():
    """
    API endpoint to score a resume
    Accepts: multipart/form-data with file, optional target_role, jd_text
    Returns: JSON report
    """
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF and DOCX allowed'}), 400
    
    # Get optional parameters
    target_role = request.form.get('target_role', None)
    jd_text = request.form.get('jd_text', None)
    
    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_ext = filename.rsplit('.', 1)[1].lower()
        temp_filename = f"{file_id}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        file.save(filepath)
        
        # Parse resume
        if file_ext == 'pdf':
            resume_data = parse_pdf(filepath)
        else:  # docx
            resume_data = parse_docx(filepath)
        
        # Score resume
        scoring_result = score_resume(resume_data, target_role, jd_text)
        
        # Generate feedback
        feedback_result = compile_full_feedback(scoring_result, resume_data)
        
        # Create report
        report = Report(
            id=file_id,
            filename=filename,
            overall_score=scoring_result['overall_score'],
            sub_scores=scoring_result['sub_scores'],
            feedback=feedback_result['feedback'],
            evidence={
                'missing_sections': scoring_result['evidence'].get('missing_sections', {}),
                'skill_gaps': scoring_result['evidence'].get('skill_gaps', []),
                'weak_bullets': [r['original'] for r in feedback_result['bullet_rewrites']],
                'ats_issues': scoring_result['evidence'].get('ats', [])
            },
            target_role=target_role
        )
        
        # Save to database
        db.session.add(report)
        db.session.commit()
        
        # Cleanup temp file
        os.remove(filepath)
        
        # Build response
        response = report.to_dict()
        response['bullet_rewrites'] = feedback_result['bullet_rewrites']
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/report/<report_id>', methods=['GET'])
def get_report_api(report_id):
    """
    API endpoint to retrieve a stored report
    """
    report = Report.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    return jsonify(report.to_dict()), 200

@app.route('/report/<report_id>')
def view_report(report_id):
    """Web page to view report"""
    report = Report.query.get(report_id)
    
    if not report:
        return "Report not found", 404
    
    return render_template('report.html', report=report.to_dict())

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload from web form"""
    f = request.files.get('file')
    if not f:
        flash('No file uploaded')
        return redirect(url_for('index'))
    
    if f.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if not allowed_file(f.filename):
        flash('Invalid file type. Only PDF and DOCX allowed')
        return redirect(url_for('index'))
    
    try:
        # Save and process
        filename = secure_filename(f.filename)
        file_id = str(uuid.uuid4())
        file_ext = filename.rsplit('.', 1)[1].lower()
        temp_filename = f"{file_id}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        f.save(filepath)
        
        # --- FIX: Extract form fields ---
        target_role = request.form.get('target_role', None)
        jd_text = request.form.get('jd_text', None)
        # -------------------------------

        # Parse
        if file_ext == 'pdf':
            resume_data = parse_pdf(filepath)
        else:
            resume_data = parse_docx(filepath)
        
        # Score
        scoring_result = score_resume(resume_data, target_role, jd_text)
        feedback_result = compile_full_feedback(scoring_result, resume_data)
        
        # Save report
        report = Report(
            id=file_id,
            filename=filename,
            overall_score=scoring_result['overall_score'],
            sub_scores=scoring_result['sub_scores'],
            feedback=feedback_result['feedback'],
            evidence={
                'missing_sections': scoring_result['evidence'].get('missing_sections', {}),
                'skill_gaps': scoring_result['evidence'].get('skill_gaps', []),
                'weak_bullets': [r['original'] for r in feedback_result['bullet_rewrites']],
                'ats_issues': scoring_result['evidence'].get('ats', [])
            },
            target_role=target_role
        )
        
        db.session.add(report)
        db.session.commit()
        
        # Cleanup
        os.remove(filepath)
        
        # Redirect to report page
        return redirect(url_for('view_report', report_id=file_id))
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("ERROR IN /upload:")
        print(error_details)
        return f"Error processing resume: {str(e)}<br><pre>{error_details}</pre>", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
