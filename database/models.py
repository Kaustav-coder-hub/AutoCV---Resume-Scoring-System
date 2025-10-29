from database.db import db
from datetime import datetime
import uuid

class Report(db.Model):
    """Model for storing resume analysis reports"""
    __tablename__ = 'reports'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    overall_score = db.Column(db.Float, nullable=False)
    sub_scores = db.Column(db.JSON, nullable=False)
    feedback = db.Column(db.JSON, nullable=False)
    evidence = db.Column(db.JSON, nullable=False)
    target_role = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        """Convert report to dictionary"""
        return {
            'report_id': self.id,
            'timestamp': self.timestamp.isoformat() + 'Z',
            'filename': self.filename,
            'overall_score': round(self.overall_score, 1),
            'sub_scores': self.sub_scores,
            'feedback': self.feedback,
            'evidence': self.evidence,
            'target_role': self.target_role
        }
