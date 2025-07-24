"""
Enhanced Database Models
Comprehensive data models for the climate platform
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
from typing import Dict, Any, Optional

db = SQLAlchemy()

class User(db.Model):
    """Enhanced User model with comprehensive profile and activity tracking"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    organization = db.Column(db.String(100))
    role = db.Column(db.String(50), default='user')
    
    # Profile information
    profile_data = db.Column(db.Text)  # JSON field for flexible profile data
    preferences = db.Column(db.Text)   # JSON field for user preferences
    
    # Activity tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    
    # Status and permissions
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Text)  # JSON field for permissions
    
    # Relationships
    weather_predictions = db.relationship('WeatherPrediction', backref='user', lazy='dynamic')
    carbon_analyses = db.relationship('CarbonAnalysis', backref='user', lazy='dynamic')
    urban_plans = db.relationship('UrbanPlan', backref='user', lazy='dynamic')
    
    def set_password(self, password: str):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def authenticate(email: str, password: str) -> Optional['User']:
        """Authenticate user"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.is_active:
            user.login_count += 1
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user
        return None
    
    @staticmethod
    def get_active_user_count() -> int:
        """Get count of active users"""
        return User.query.filter_by(is_active=True).count()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'organization': self.organization,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'profile_data': json.loads(self.profile_data) if self.profile_data else {},
            'preferences': json.loads(self.preferences) if self.preferences else {}
        }

class WeatherPrediction(db.Model):
    """Weather prediction records"""
    __tablename__ = 'weather_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Location and time
    location = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
    forecast_period = db.Column(db.String(50))  # e.g., '7d', '14d'
    
    # Prediction data
    prediction_data = db.Column(db.Text)  # JSON field for prediction results
    confidence_score = db.Column(db.Float)
    model_version = db.Column(db.String(50))
    
    # AI processing metadata
    ibm_api_used = db.Column(db.Boolean, default=False)
    agentic_ai_applied = db.Column(db.Boolean, default=False)
    rag_enhanced = db.Column(db.Boolean, default=False)
    granite_validated = db.Column(db.Boolean, default=False)
    
    # Impact assessment
    impact_assessment = db.Column(db.Text)  # JSON field for impact data
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CarbonAnalysis(db.Model):
    """Carbon footprint analysis records"""
    __tablename__ = 'carbon_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Organization information
    organization_name = db.Column(db.String(200), nullable=False)
    organization_sector = db.Column(db.String(100))
    reporting_year = db.Column(db.Integer)
    
    # Analysis data
    analysis_data = db.Column(db.Text)  # JSON field for analysis results
    data_quality_score = db.Column(db.Float)
    processing_report = db.Column(db.Text)  # JSON field for DPK processing report
    
    # AI processing metadata
    dpk_processed = db.Column(db.Boolean, default=False)
    agentic_regulatory_scan = db.Column(db.Boolean, default=False)
    granite_ethical_recommendations = db.Column(db.Boolean, default=False)
    
    # Results
    total_emissions = db.Column(db.Float)
    scope_1_emissions = db.Column(db.Float)
    scope_2_emissions = db.Column(db.Float)
    scope_3_emissions = db.Column(db.Float)
    
    # Recommendations and impact
    policy_recommendations = db.Column(db.Text)  # JSON field
    impact_assessment = db.Column(db.Text)  # JSON field
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UrbanPlan(db.Model):
    """Urban planning records"""
    __tablename__ = 'urban_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # City information
    city_name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100))
    population = db.Column(db.Integer)
    area_km2 = db.Column(db.Float)
    
    # Planning data
    city_profile = db.Column(db.Text)  # JSON field for city profile
    climate_projections = db.Column(db.Text)  # JSON field for climate data
    planning_constraints = db.Column(db.Text)  # JSON field for constraints
    
    # AI processing metadata
    rag_data_sourcing = db.Column(db.Boolean, default=False)
    granite_data_integrity = db.Column(db.Boolean, default=False)
    agentic_adaptive_modeling = db.Column(db.Boolean, default=False)
    
    # Results
    adaptive_planning_model = db.Column(db.Text)  # JSON field
    vulnerability_assessment = db.Column(db.Text)  # JSON field
    resilience_strategies = db.Column(db.Text)  # JSON field
    impact_projections = db.Column(db.Text)  # JSON field
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DataProcessingLog(db.Model):
    """Data processing logs for audit and monitoring"""
    __tablename__ = 'data_processing_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Processing information
    process_type = db.Column(db.String(50), nullable=False)  # 'weather', 'carbon', 'urban'
    process_stage = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'started', 'completed', 'failed'
    
    # Data and metadata
    input_data_hash = db.Column(db.String(64))
    output_data_hash = db.Column(db.String(64))
    processing_metadata = db.Column(db.Text)  # JSON field
    
    # Performance metrics
    processing_time_seconds = db.Column(db.Float)
    memory_usage_mb = db.Column(db.Float)
    cpu_utilization = db.Column(db.Float)
    
    # Error information
    error_message = db.Column(db.Text)
    error_traceback = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EthicsAuditLog(db.Model):
    """Ethics audit logs for compliance tracking"""
    __tablename__ = 'ethics_audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Audit information
    audit_type = db.Column(db.String(50), nullable=False)  # 'bias_assessment', 'fairness_check', etc.
    audit_scope = db.Column(db.String(50))  # 'all', 'weather', 'carbon', 'urban'
    
    # Results
    audit_results = db.Column(db.Text)  # JSON field for audit results
    compliance_score = db.Column(db.Float)
    violations_found = db.Column(db.Integer, default=0)
    
    # Recommendations
    recommendations = db.Column(db.Text)  # JSON field
    remediation_actions = db.Column(db.Text)  # JSON field
    
    # Status
    status = db.Column(db.String(20), default='completed')
    reviewed_by = db.Column(db.String(100))
    review_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ImpactMetric(db.Model):
    """Impact metrics tracking"""
    __tablename__ = 'impact_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Metric information
    metric_category = db.Column(db.String(50), nullable=False)  # 'environmental', 'social', 'economic'
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    metric_unit = db.Column(db.String(50))
    
    # Context
    measurement_period = db.Column(db.String(50))  # 'daily', 'weekly', 'monthly', 'yearly'
    geographic_scope = db.Column(db.String(100))
    user_segment = db.Column(db.String(50))
    
    # Metadata
    measurement_method = db.Column(db.String(100))
    confidence_level = db.Column(db.Float)
    data_sources = db.Column(db.Text)  # JSON field
    
    # Verification
    verified = db.Column(db.Boolean, default=False)
    verification_method = db.Column(db.String(100))
    verified_by = db.Column(db.String(100))
    verification_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    measurement_date = db.Column(db.DateTime, nullable=False)

class SystemHealth(db.Model):
    """System health monitoring"""
    __tablename__ = 'system_health'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Service information
    service_name = db.Column(db.String(50), nullable=False)
    service_version = db.Column(db.String(20))
    status = db.Column(db.String(20), nullable=False)  # 'healthy', 'degraded', 'unhealthy'
    
    # Performance metrics
    response_time_ms = db.Column(db.Float)
    cpu_usage_percent = db.Column(db.Float)
    memory_usage_percent = db.Column(db.Float)
    disk_usage_percent = db.Column(db.Float)
    
    # Health check details
    health_check_details = db.Column(db.Text)  # JSON field
    last_error = db.Column(db.Text)
    error_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create all tables
def create_tables():
    """Create all database tables"""
    db.create_all()

# Database initialization function
def init_db(app):
    """Initialize database with app"""
    db.init_app(app)
    with app.app_context():
        create_tables()
