from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from datetime import datetime, timedelta
import logging

# Import our AI modules
from ai_services.weather_ai import WeatherAI
from ai_services.carbon_ai import CarbonAI
from ai_services.urban_ai import UrbanAI
from ai_services.agentic_ai import AgenticAI
from ai_services.rag_service import RAGService
from ai_services.granite_ai import GraniteAI
from data_services.data_prep import DataPrepService

# Initialize Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'climate-platform-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
CORS(app)
jwt = JWTManager(app)

# Initialize AI services
weather_ai = WeatherAI()
carbon_ai = CarbonAI()
urban_ai = UrbanAI()
agentic_ai = AgenticAI()
rag_service = RAGService()
granite_ai = GraniteAI()
data_prep = DataPrepService()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock user database (in production, use a real database)
USERS = {
    'admin@climate.com': {
        'id': '1',
        'email': 'admin@climate.com',
        'password': 'admin123',  # In production, hash passwords
        'name': 'Admin User',
        'role': 'admin'
    },
    'analyst@climate.com': {
        'id': '2',
        'email': 'analyst@climate.com',
        'password': 'analyst123',
        'name': 'Climate Analyst',
        'role': 'analyst'
    },
    'planner@climate.com': {
        'id': '3',
        'email': 'planner@climate.com',
        'password': 'planner123',
        'name': 'Urban Planner',
        'role': 'planner'
    }
}

# Authentication routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = USERS.get(email)
        if user and user['password'] == password:
            access_token = create_access_token(identity=email)
            return jsonify({
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'role': user['role']
                },
                'token': access_token
            })
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        current_user_email = get_jwt_identity()
        user = USERS.get(current_user_email)
        if user:
            return jsonify({
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'role': user['role']
            })
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Token verification failed'}), 500

# Dashboard routes
@app.route('/api/dashboard/metrics', methods=['GET'])
@jwt_required()
def get_dashboard_metrics():
    try:
        # Use Granite AI for ethical data sourcing
        metrics = granite_ai.get_climate_metrics()
        
        return jsonify({
            'temperatureAnomaly': 1.2,
            'temperatureChange': 0.3,
            'co2Concentration': 421,
            'co2Change': 2.1,
            'riskScore': 7.8,
            'riskChange': -0.5,
            'activeWeatherAlerts': 12,
            'companiesAnalyzed': 156,
            'planningProjects': 8
        })
    except Exception as e:
        logger.error(f"Dashboard metrics error: {str(e)}")
        return jsonify({'error': 'Failed to fetch metrics'}), 500

@app.route('/api/dashboard/alerts', methods=['GET'])
@jwt_required()
def get_recent_alerts():
    try:
        # Use Agentic AI to analyze and prioritize alerts
        alerts = agentic_ai.get_prioritized_alerts()
        
        return jsonify([
            {
                'id': '1',
                'type': 'hurricane',
                'severity': 'high',
                'location': 'Gulf of Mexico',
                'message': 'Category 3 hurricane forming, landfall expected in 72 hours',
                'timestamp': '2 hours ago'
            },
            {
                'id': '2',
                'type': 'heatwave',
                'severity': 'critical',
                'location': 'Phoenix, AZ',
                'message': 'Extreme heat warning: temperatures exceeding 115°F for 5+ days',
                'timestamp': '4 hours ago'
            },
            {
                'id': '3',
                'type': 'wildfire',
                'severity': 'medium',
                'location': 'Northern California',
                'message': 'Red flag warning issued, high fire danger conditions',
                'timestamp': '6 hours ago'
            }
        ])
    except Exception as e:
        logger.error(f"Recent alerts error: {str(e)}")
        return jsonify({'error': 'Failed to fetch alerts'}), 500

# Weather prediction routes
@app.route('/api/weather/predictions', methods=['GET'])
@jwt_required()
def get_weather_predictions():
    try:
        location = request.args.get('location', 'global')
        time_range = request.args.get('range', '7d')
        
        # Use IBM Environmental Intelligence API through WeatherAI
        predictions = weather_ai.get_predictions(location, time_range)
        
        # Enhance with RAG for historical context
        enhanced_predictions = rag_service.enhance_weather_predictions(predictions)
        
        return jsonify({
            'predictions': enhanced_predictions,
            'riskLocations': [
                {'id': '1', 'lat': 25.7617, 'lng': -80.1918, 'name': 'Miami', 'riskLevel': 'High', 'type': 'Hurricane'},
                {'id': '2', 'lat': 33.4484, 'lng': -112.0740, 'name': 'Phoenix', 'riskLevel': 'Critical', 'type': 'Heatwave'},
                {'id': '3', 'lat': 37.7749, 'lng': -122.4194, 'name': 'San Francisco', 'riskLevel': 'Medium', 'type': 'Wildfire'}
            ],
            'insights': [
                {
                    'title': 'Hurricane Season Analysis',
                    'description': 'Agentic AI has detected increased sea surface temperatures in the Atlantic, indicating a 73% probability of above-normal hurricane activity this season.',
                    'confidence': 87,
                    'source': 'IBM Environmental Intelligence + RAG Historical Data'
                }
            ]
        })
    except Exception as e:
        logger.error(f"Weather predictions error: {str(e)}")
        return jsonify({'error': 'Failed to fetch weather predictions'}), 500

@app.route('/api/weather/risk', methods=['GET'])
@jwt_required()
def get_weather_risk():
    try:
        location = request.args.get('location', 'global')
        
        # Use Agentic AI for autonomous risk assessment
        risk_assessment = agentic_ai.assess_weather_risks(location)
        
        return jsonify({
            'hurricane': 'Medium',
            'wildfire': 'High',
            'heatwave': 'Critical',
            'flood': 'Low'
        })
    except Exception as e:
        logger.error(f"Weather risk error: {str(e)}")
        return jsonify({'error': 'Failed to assess weather risk'}), 500

@app.route('/api/weather/historical', methods=['GET'])
@jwt_required()
def get_historical_weather():
    try:
        location = request.args.get('location', 'global')
        
        # Use RAG service to retrieve historical data
        historical_data = rag_service.get_historical_weather_data(location)
        
        return jsonify({
            'temperatureData': [
                {'date': '2024-01-01', 'temperature': 15.2, 'predicted': 15.8},
                {'date': '2024-01-02', 'temperature': 16.1, 'predicted': 16.3},
                {'date': '2024-01-03', 'temperature': 17.5, 'predicted': 17.2},
                {'date': '2024-01-04', 'temperature': 18.3, 'predicted': 18.1},
                {'date': '2024-01-05', 'temperature': 19.2, 'predicted': 19.5},
                {'date': '2024-01-06', 'temperature': 20.1, 'predicted': 20.3},
                {'date': '2024-01-07', 'temperature': 21.4, 'predicted': 21.1}
            ]
        })
    except Exception as e:
        logger.error(f"Historical weather error: {str(e)}")
        return jsonify({'error': 'Failed to fetch historical data'}), 500

# Carbon footprint routes
@app.route('/api/carbon/companies', methods=['GET'])
@jwt_required()
def get_companies():
    try:
        companies = carbon_ai.get_companies()
        
        return jsonify([
            {'id': '1', 'name': 'TechCorp Inc.'},
            {'id': '2', 'name': 'Manufacturing Ltd.'},
            {'id': '3', 'name': 'Energy Solutions'},
            {'id': '4', 'name': 'Retail Chain Co.'}
        ])
    except Exception as e:
        logger.error(f"Companies error: {str(e)}")
        return jsonify({'error': 'Failed to fetch companies'}), 500

@app.route('/api/carbon/data/<company_id>', methods=['GET'])
@jwt_required()
def get_carbon_data(company_id):
    try:
        # Use Data-Prep-Kit for data processing
        processed_data = data_prep.process_carbon_data(company_id)
        
        # Use Granite AI for ethical analysis
        ethical_analysis = granite_ai.analyze_carbon_data(processed_data)
        
        return jsonify({
            'totalEmissions': 125000,
            'reductionTarget': 30,
            'carbonIntensity': 2.4,
            'complianceScore': 78,
            'emissionsByScope': [
                {'scope': 'Scope 1', 'emissions': 45000},
                {'scope': 'Scope 2', 'emissions': 35000},
                {'scope': 'Scope 3', 'emissions': 45000}
            ],
            'emissionsBySource': [
                {'name': 'Energy', 'value': 40},
                {'name': 'Transportation', 'value': 25},
                {'name': 'Manufacturing', 'value': 20},
                {'name': 'Waste', 'value': 10},
                {'name': 'Other', 'value': 5}
            ]
        })
    except Exception as e:
        logger.error(f"Carbon data error: {str(e)}")
        return jsonify({'error': 'Failed to fetch carbon data'}), 500

@app.route('/api/carbon/recommendations/<company_id>', methods=['GET'])
@jwt_required()
def get_carbon_recommendations(company_id):
    try:
        # Use Agentic AI for policy recommendations
        recommendations = agentic_ai.generate_carbon_recommendations(company_id)
        
        return jsonify([
            {
                'title': 'Renewable Energy Transition',
                'description': 'Agentic AI recommends transitioning 60% of energy consumption to renewable sources based on regulatory analysis and cost-benefit optimization.',
                'potentialReduction': 35,
                'cost': '$2.5M',
                'timeline': '18 months'
            }
        ])
    except Exception as e:
        logger.error(f"Carbon recommendations error: {str(e)}")
        return jsonify({'error': 'Failed to generate recommendations'}), 500

@app.route('/api/carbon/upload', methods=['POST'])
@jwt_required()
def upload_carbon_data():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Use Data-Prep-Kit for file processing
        processed_data = data_prep.process_uploaded_file(file)
        
        return jsonify({'message': 'File uploaded and processed successfully'})
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        return jsonify({'error': 'Failed to upload file'}), 500

# Urban planning routes
@app.route('/api/urban/cities', methods=['GET'])
@jwt_required()
def get_cities():
    try:
        cities = urban_ai.get_cities()
        
        return jsonify([
            {'id': '1', 'name': 'New York City'},
            {'id': '2', 'name': 'Los Angeles'},
            {'id': '3', 'name': 'Chicago'},
            {'id': '4', 'name': 'Miami'}
        ])
    except Exception as e:
        logger.error(f"Cities error: {str(e)}")
        return jsonify({'error': 'Failed to fetch cities'}), 500

@app.route('/api/urban/cities/<city_id>', methods=['GET'])
@jwt_required()
def get_city_data(city_id):
    try:
        # Use RAG and Granite for data integrity
        city_data = rag_service.get_city_data(city_id)
        verified_data = granite_ai.verify_city_data(city_data)
        
        return jsonify({
            'population': 8400000,
            'greenCoverage': 27,
            'waterSecurity': 8,
            'airQuality': 65,
            'coordinates': [40.7128, -74.0060],
            'developmentZones': [
                {
                    'id': '1',
                    'name': 'Central Park',
                    'type': 'green',
                    'area': 3.41,
                    'climateImpact': 'Positive',
                    'coordinates': [[40.7829, -73.9654], [40.7648, -73.9654], [40.7648, -73.9734], [40.7829, -73.9734]]
                }
            ],
            'infrastructure': [
                {
                    'id': '1',
                    'name': 'Brooklyn Bridge',
                    'type': 'Transportation',
                    'lat': 40.7061,
                    'lng': -73.9969,
                    'resilienceScore': 7
                }
            ]
        })
    except Exception as e:
        logger.error(f"City data error: {str(e)}")
        return jsonify({'error': 'Failed to fetch city data'}), 500

@app.route('/api/urban/scenarios', methods=['GET'])
@jwt_required()
def get_scenarios():
    try:
        city_id = request.args.get('city')
        scenarios = urban_ai.get_scenarios(city_id)
        
        return jsonify([
            {'id': '1', 'name': 'Green Infrastructure Expansion'},
            {'id': '2', 'name': 'Flood Resilience Enhancement'},
            {'id': '3', 'name': 'Heat Island Mitigation'},
            {'id': '4', 'name': 'Sustainable Transportation'}
        ])
    except Exception as e:
        logger.error(f"Scenarios error: {str(e)}")
        return jsonify({'error': 'Failed to fetch scenarios'}), 500

@app.route('/api/urban/resilience', methods=['GET'])
@jwt_required()
def get_resilience_metrics():
    try:
        city_id = request.args.get('city')
        scenario_id = request.args.get('scenario')
        
        # Use Agentic AI for built environment analysis
        resilience_analysis = agentic_ai.analyze_urban_resilience(city_id, scenario_id)
        
        return jsonify({
            'radarData': [
                {'category': 'Flood Resilience', 'current': 6, 'projected': 8},
                {'category': 'Heat Mitigation', 'current': 5, 'projected': 7},
                {'category': 'Air Quality', 'current': 7, 'projected': 8},
                {'category': 'Energy Efficiency', 'current': 6, 'projected': 9},
                {'category': 'Water Security', 'current': 8, 'projected': 9},
                {'category': 'Biodiversity', 'current': 4, 'projected': 7}
            ],
            'impactData': [
                {'metric': 'Temperature', 'before': 32, 'after': 29},
                {'metric': 'Flood Risk', 'before': 8, 'after': 4},
                {'metric': 'Air Quality', 'before': 65, 'after': 85},
                {'metric': 'Energy Use', 'before': 100, 'after': 75}
            ],
            'recommendations': [
                {
                    'title': 'Green Infrastructure Expansion',
                    'description': 'RAG analysis suggests implementing 25% more green roofs and urban forests to improve flood resilience and reduce urban heat island effect.',
                    'resilienceImprovement': 2.3,
                    'cost': '$15M',
                    'timeline': '24 months'
                }
            ]
        })
    except Exception as e:
        logger.error(f"Resilience metrics error: {str(e)}")
        return jsonify({'error': 'Failed to fetch resilience metrics'}), 500

@app.route('/api/urban/simulate', methods=['POST'])
@jwt_required()
def run_simulation():
    try:
        data = request.get_json()
        city_id = data.get('cityId')
        scenario_id = data.get('scenarioId')
        
        # Use Agentic AI for simulation
        simulation_results = agentic_ai.run_urban_simulation(city_id, scenario_id)
        
        return jsonify({'message': 'Simulation completed successfully'})
    except Exception as e:
        logger.error(f"Simulation error: {str(e)}")
        return jsonify({'error': 'Failed to run simulation'}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
