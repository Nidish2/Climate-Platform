"""
Climate Platform Backend Application
Real-time climate data analysis and prediction platform
"""

import os
import logging
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from dotenv import load_dotenv
import structlog

# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///climate_platform.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE', 'simple')
app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
cache = Cache(app)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
CORS(app, origins=cors_origins, supports_credentials=True)

# Configure rate limiting
# ✅ NEW (Flask-Limiter 3.5.0 compatible)
limiter = Limiter(
    key_func=get_remote_address,  # First positional parameter
    default_limits=["200 per day", "50 per hour"],
    storage_uri=os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://'),
    app=app  # Pass app as keyword argument
)


# Import services after app initialization
from ai_services.weather_ai import WeatherAI
from ai_services.carbon_ai import CarbonAI
from ai_services.urban_ai import UrbanAI

# Initialize AI services
weather_ai = WeatherAI()
carbon_ai = CarbonAI()
urban_ai = UrbanAI()

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password hash"""
        return check_password_hash(self.password_hash, password)

class WeatherPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    prediction_data = db.Column(db.JSON)
    risk_level = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CarbonAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    analysis_data = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UrbanPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)
    plan_data = db.Column(db.JSON)
    sustainability_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error("Internal server error", error=str(error))
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': str(e.description)}), 429

# Authentication Endpoints
@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Login endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        email = data['email']
        password = data['password']
        
        # Find user by email
        user = User.query.filter_by(email=email, is_active=True).first()
        
        # Debug logging
        if not user:
            logger.warning("User not found", email=email)
            # Check if user exists at all
            all_user = User.query.filter_by(email=email).first()
            if all_user:
                logger.warning("User exists but is inactive", email=email, is_active=all_user.is_active)
            else:
                logger.warning("User does not exist in database", email=email)
                # List all users for debugging
                all_users = User.query.all()
                logger.info("All users in database", count=len(all_users), 
                           users=[{"email": u.email, "active": u.is_active} for u in all_users])
        else:
            logger.info("User found", email=email, user_id=user.id)
            if not user.check_password(password):
                logger.warning("Password check failed", email=email)
            else:
                logger.info("Password check passed", email=email)
        
        if not user or not user.check_password(password):
            logger.warning("Failed login attempt", email=email)
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        logger.info("Successful login", user_id=user.id, email=email)
        
        return jsonify({
            'success': True,
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error("Login failed", error=str(e))
        return jsonify({
            'success': False,
            'error': 'Login failed'
        }), 500

@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify JWT token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error("Token verification failed", error=str(e))
        return jsonify({
            'success': False,
            'error': 'Token verification failed'
        }), 401

# Health Check Endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with system status"""
    try:
        # Test database connection
        db.session.execute(text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
        logger.error("Database health check failed", error=str(e))

    # Test API keys
    api_keys_status = {
        'openweather': 'configured' if os.getenv('OPENWEATHER_API_KEY') else 'missing',
        'carbon_interface': 'configured' if os.getenv('CARBON_INTERFACE_KEY') else 'missing',
        'openaq': 'configured' if os.getenv('OPENAQ_API_KEY') else 'missing',
        'tomorrow_io': 'configured' if os.getenv('TOMORROW_API_KEY') else 'missing',
        'airvisual': 'configured' if os.getenv('AIRVISUAL_API_KEY') else 'missing'
    }

    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'database': db_status,
        'api_keys': api_keys_status,
        'services': {
            'weather_ai': 'active',
            'carbon_ai': 'active',
            'urban_ai': 'active'
        }
    })

# Weather Prediction Endpoints
@app.route('/api/weather/predictions', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=300, query_string=True)
def get_weather_predictions():
    """Get weather predictions for a location"""
    try:
        location = request.args.get('location', 'New York')
        range_days = request.args.get('range', '7d')
        
        logger.info("Weather prediction request", location=location, range=range_days)
        
        # Get predictions from AI service
        predictions = weather_ai.get_predictions(location, range_days)
        
        # Save to database
        prediction_record = WeatherPrediction(
            location=location,
            prediction_data=predictions,
            risk_level=predictions.get('risk_level', 'unknown')
        )
        db.session.add(prediction_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': predictions,
            'location': location,
            'range': range_days,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error("Weather prediction failed", error=str(e), location=location)
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get weather predictions'
        }), 500

@app.route('/api/weather/alerts', methods=['GET'])
@limiter.limit("20 per minute")
def get_weather_alerts():
    """Get current weather alerts"""
    try:
        location = request.args.get('location', 'New York')
        
        alerts = weather_ai.get_alerts(location)
        
        return jsonify({
            'success': True,
            'data': alerts,
            'location': location,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error("Weather alerts failed", error=str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Carbon Footprint Endpoints
@app.route('/api/carbon/analyze', methods=['POST'])
@limiter.limit("5 per minute")
def analyze_carbon_footprint():
    """Analyze carbon footprint for a company"""
    try:
        data = request.get_json()
        
        if not data or 'company_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Company name is required'
            }), 400
        
        company_name = data['company_name']
        company_data = data.get('data', {})
        
        logger.info("Carbon analysis request", company=company_name)
        
        # Perform analysis
        analysis = carbon_ai.analyze_footprint(company_name, company_data)
        
        # Save to database
        carbon_record = CarbonAnalysis(
            company_name=company_name,
            analysis_data=analysis,
            recommendations=analysis.get('recommendations', [])
        )
        db.session.add(carbon_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': analysis,
            'company': company_name,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error("Carbon analysis failed", error=str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/carbon/benchmarks', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=600, query_string=True)
def get_carbon_benchmarks():
    """Get industry carbon benchmarks"""
    try:
        industry = request.args.get('industry', 'technology')
        
        benchmarks = carbon_ai.get_industry_benchmarks(industry)
        
        return jsonify({
            'success': True,
            'data': benchmarks,
            'industry': industry,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error("Carbon benchmarks failed", error=str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Urban Planning Endpoints
@app.route('/api/urban/analyze', methods=['POST'])
@limiter.limit("3 per minute")
def analyze_urban_plan():
    """Analyze urban planning scenario"""
    try:
        data = request.get_json()
        
        if not data or 'city_name' not in data:
            return jsonify({
                'success': False,
                'error': 'City name is required'
            }), 400
        
        city_name = data['city_name']
        plan_data = data.get('plan_data', {})
        
        logger.info("Urban analysis request", city=city_name)
        
        # Perform analysis
        analysis = urban_ai.analyze_plan(city_name, plan_data)
        
        # Save to database
        urban_record = UrbanPlan(
            city_name=city_name,
            plan_data=analysis,
            sustainability_score=analysis.get('sustainability_score', 0)
        )
        db.session.add(urban_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': analysis,
            'city': city_name,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error("Urban analysis failed", error=str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Dashboard Data Endpoint
@app.route('/api/dashboard/summary', methods=['GET'])
@limiter.limit("30 per minute")
@cache.cached(timeout=180)
def get_dashboard_summary():
    """Get dashboard summary data"""
    try:
        # Get recent predictions count
        recent_predictions = WeatherPrediction.query.filter(
            WeatherPrediction.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Get recent analyses count
        recent_analyses = CarbonAnalysis.query.filter(
            CarbonAnalysis.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Get recent urban plans count
        recent_plans = UrbanPlan.query.filter(
            UrbanPlan.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Get global climate metrics (mock for now, replace with real APIs)
        global_metrics = {
            'co2_level': 421.5,  # ppm
            'global_temp_anomaly': 1.2,  # °C above pre-industrial
            'sea_level_rise': 3.4,  # mm/year
            'arctic_ice_extent': 4.2  # million km²
        }
        
        return jsonify({
            'success': True,
            'data': {
                'recent_activity': {
                    'weather_predictions': recent_predictions,
                    'carbon_analyses': recent_analyses,
                    'urban_plans': recent_plans
                },
                'global_metrics': global_metrics,
                'system_status': {
                    'uptime': '99.9%',
                    'api_calls_today': recent_predictions + recent_analyses + recent_plans,
                    'active_alerts': 3
                }
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error("Dashboard summary failed", error=str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Create demo user if it doesn't exist
        demo_user = User.query.filter_by(email='admin@climate.com').first()
        if not demo_user:
            demo_user = User(email='admin@climate.com')
            demo_user.set_password('admin123')
            db.session.add(demo_user)
            db.session.commit()
            logger.info("Demo user created successfully", email="admin@climate.com")
        else:
            logger.info("Demo user already exists", email="admin@climate.com", is_active=demo_user.is_active)
        
        # Verify demo user can be found
        verify_user = User.query.filter_by(email='admin@climate.com').first()
        if verify_user:
            logger.info("Demo user verification successful", email=verify_user.email, 
                       has_password=bool(verify_user.password_hash))
        else:
            logger.error("Demo user verification failed - user not found after creation")
        
        logger.info("Climate Platform Backend starting...")
    
    # Run the application
    app.run(
        host=os.getenv('FLASK_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
        threaded=True
    )
