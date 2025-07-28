# 🌍 Climate Platform Setup Guide

Complete setup instructions for the Climate Change Analysis and Mitigation Platform using your real API keys.

## 📋 Prerequisites

- **Python 3.11+** (Required for compatibility)
- **Node.js 18+** and npm
- **Git** for version control

## 🔑 Your API Keys (Already Configured)

Your API keys have been integrated into the system:

- ✅ **OpenWeather API**: `0e356836821fe7c66466877bd63f9ee7`
- ✅ **Carbon Interface**: `xgX0oIOlDnw0LJhSqtLcw`
- ✅ **OpenAQ**: `9dda02cc6e6b6b3789461f644f219c74eaa190381981150a21fbb4bd1d19defb`
- ✅ **AirVisual**: `1B0EB09D-0947-494F-8E84-B1808638087D`
- ✅ **Tomorrow.io**: `JsFtriyWlKZQJ3jMvon8mQn67zOmOFRH`
- ✅ **Electricity Map**: `vAz9xfQWDRbzAnyU3cL`
- ✅ **Climatic API**: `0V8YJ3B8NN0Q30J6DHNDNEXJ84`
- ✅ **Data.gov**: `O5loUoZgsXTf5TX6EKcATVfOTsa9d314ZXxWkMa4`

## 🚀 Quick Start Commands

### 1. Clone and Setup Backend

\`\`\`bash
# Clone the repository
git clone <repository-url>
cd climate-platform

# Make setup script executable
chmod +x run_dev.sh

# Run the complete setup (this will handle everything)
./run_dev.sh
\`\`\`

### 2. Setup Frontend (New Terminal)

\`\`\`bash
# Install frontend dependencies
npm install

# Start the development server
npm run dev
\`\`\`

## 📝 Manual Setup (Alternative)

If you prefer manual setup:

### Backend Setup

\`\`\`bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file (your keys are already configured)
cp .env.example .env

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Start Flask server
python app.py
\`\`\`

### Frontend Setup

\`\`\`bash
# Install dependencies
npm install

# Start development server
npm run dev
\`\`\`

## 🔍 Verification Steps

### 1. Check Backend Health

\`\`\`bash
curl http://127.0.0.1:5000/api/health
\`\`\`

Expected response:
\`\`\`json
{
  "status": "healthy",
  "apis_configured": {
    "openweather": true,
    "carbon_interface": true,
    "openaq": true,
    "airvisual": true,
    "tomorrow": true
  },
  "real_time_data": true,
  "mock_data_used": false
}
\`\`\`

### 2. Test Weather API

\`\`\`bash
curl "http://127.0.0.1:5000/api/weather/predictions?location=New York&range=7d"
\`\`\`

### 3. Test Carbon Analysis

\`\`\`bash
curl -X POST http://127.0.0.1:5000/api/carbon/upload-and-analyze \
  -H "Content-Type: application/json" \
  -d '{"company_profile": {"name": "Test Corp", "sector": "Technology", "employees": 1000}}'
\`\`\`

### 4. Check Frontend

Open browser to: `http://localhost:3000`

## 🌐 Available Endpoints

### Weather APIs
- `GET /api/weather/predictions` - Real-time weather predictions
- `POST /api/weather/prescriptive-model` - Extreme weather modeling
- `GET /api/weather/risk-assessment` - Weather risk assessment

### Carbon APIs
- `POST /api/carbon/upload-and-analyze` - Carbon footprint analysis
- `POST /api/carbon/policy-recommendations` - Policy recommendations
- `GET /api/carbon/companies` - Company database

### Urban Planning APIs
- `POST /api/urban/adaptive-planning` - Urban resilience planning
- `POST /api/urban/climate-resilience-assessment` - City resilience assessment

### Analytics APIs
- `GET /api/analytics/platform-impact` - Platform impact metrics
- `POST /api/ethics/bias-assessment` - AI bias assessment
- `GET /api/privacy/data-protection-status` - Privacy compliance

## 🔧 Configuration Details

### Environment Variables (.env)

\`\`\`bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Your API Keys (Pre-configured)
OPENWEATHER_API_KEY=0e356836821fe7c66466877bd63f9ee7
CARBON_INTERFACE_KEY=xgX0oIOlDnw0LJhSqtLcw
OPENAQ_API_KEY=9dda02cc6e6b6b3789461f644f219c74eaa190381981150a21fbb4bd1d19defb
AIRVISUAL_API_KEY=1B0EB09D-0947-494F-8E84-B1808638087D
TOMORROW_API_KEY=JsFtriyWlKZQJ3jMvon8mQn67zOmOFRH
ELECTRICITY_MAP_KEY=vAz9xfQWDRbzAnyU3cL
CLIMATIC_API_KEY=0V8YJ3B8NN0Q30J6DHNDNEXJ84
DATA_GOV_API_KEY=O5loUoZgsXTf5TX6EKcATVfOTsa9d314ZXxWkMa4

# Notification (Optional)
TELEGRAM_BOT_TOKEN=7982181803:AAE3rqrU9-c8li2oz208e8oIAakUWm08U-g
TELEGRAM_CHAT_ID=5380608179
\`\`\`

## 🧪 Testing Real-Time Data

### Test Weather Data

\`\`\`bash
# Test OpenWeather API
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=0e356836821fe7c66466877bd63f9ee7"

# Test Tomorrow.io API
curl "https://api.tomorrow.io/v4/weather/forecast?location=40.7128,-74.0060&apikey=JsFtriyWlKZQJ3jMvon8mQn67zOmOFRH"
\`\`\`

### Test Air Quality Data

\`\`\`bash
# Test AirVisual API
curl "https://api.airvisual.com/v2/nearest_city?lat=40.7128&lon=-74.0060&key=1B0EB09D-0947-494F-8E84-B1808638087D"

# Test OpenAQ API
curl -H "X-API-Key: 9dda02cc6e6b6b3789461f644f219c74eaa190381981150a21fbb4bd1d19defb" \
  "https://api.openaq.org/v2/latest?limit=5"
\`\`\`

### Test Carbon Data

\`\`\`bash
# Test Carbon Interface API
curl -H "Authorization: Bearer xgX0oIOlDnw0LJhSqtLcw" \
  -H "Content-Type: application/json" \
  "https://www.carboninterface.com/api/v1/estimates"
\`\`\`

## 🚨 Troubleshooting

### Common Issues

1. **Python Version Error**
   \`\`\`bash
   # Check Python version
   python3 --version
   # Should be 3.11 or higher
   \`\`\`

2. **Virtual Environment Issues**
   \`\`\`bash
   # Recreate virtual environment
   rm -rf backend/venv
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   \`\`\`

3. **API Key Issues**
   \`\`\`bash
   # Verify API keys are loaded
   cd backend
   python -c "
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print('OpenWeather:', bool(os.getenv('OPENWEATHER_API_KEY')))
   print('Carbon Interface:', bool(os.getenv('CARBON_INTERFACE_KEY')))
   "
   \`\`\`

4. **Database Issues**
   \`\`\`bash
   # Reset database
   cd backend
   rm -f climate_platform.db
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   \`\`\`

5. **Port Already in Use**
   \`\`\`bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9
   
   # Or use different port
   export FLASK_PORT=5001
   python app.py
   \`\`\`

### API Rate Limits

Your APIs have the following limits:
- **OpenWeather**: 1,000 calls/day (free tier)
- **Tomorrow.io**: 500 calls/day (free tier)
- **AirVisual**: 10,000 calls/month (free tier)
- **OpenAQ**: No strict limits (free)
- **Carbon Interface**: 200 requests/month (free tier)

## 📊 Real-Time Data Features

### Weather Module
- ✅ Real-time weather conditions
- ✅ 7-day forecasts
- ✅ Extreme weather alerts
- ✅ Air quality monitoring
- ✅ Earthquake tracking
- ✅ Wildfire risk assessment

### Carbon Module
- ✅ Real-time carbon intensity
- ✅ Emission factor calculations
- ✅ Industry benchmarking
- ✅ Regulatory compliance
- ✅ Reduction strategies

### Urban Planning Module
- ✅ Climate resilience assessment
- ✅ Vulnerability mapping
- ✅ Adaptive planning tools

## 🔄 Development Workflow

### Making Changes

1. **Backend Changes**
   \`\`\`bash
   cd backend
   source venv/bin/activate
   # Make your changes
   python app.py  # Server auto-reloads
   \`\`\`

2. **Frontend Changes**
   \`\`\`bash
   # Frontend auto-reloads on save
   npm run dev
   \`\`\`

3. **Testing Changes**
   \`\`\`bash
   # Backend tests
   cd backend
   pytest tests/

   # Frontend tests
   npm test
   \`\`\`

### Adding New APIs

1. Add API key to `.env`
2. Update API service files in `backend/ai_services/`
3. Add new endpoints in `backend/app.py`
4. Update frontend services in `src/services/`

## 📈 Performance Optimization

### Backend Optimization
- API response caching (5-minute cache for weather data)
- Async API calls for better performance
- Database connection pooling
- Request rate limiting

### Frontend Optimization
- Component lazy loading
- API response caching
- Optimized bundle size
- Progressive loading

## 🔒 Security Features

- JWT token authentication
- API key encryption
- Rate limiting
- CORS protection
- Input validation
- SQL injection prevention

## 📱 Mobile Responsiveness

The platform is fully responsive and works on:
- ✅ Desktop (1920x1080+)
- ✅ Tablet (768x1024)
- ✅ Mobile (375x667+)

## 🌍 Deployment Options

### Local Development
\`\`\`bash
./run_dev.sh  # Backend
npm run dev   # Frontend
\`\`\`

### Production Deployment
\`\`\`bash
# Build frontend
npm run build

# Deploy to Vercel/Netlify
# Configure environment variables
# Set up database (PostgreSQL recommended)
\`\`\`

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all API keys are working
3. Check the console for error messages
4. Review the logs in `backend/logs/`

## 🎯 Next Steps

1. **Run the setup**: `./run_dev.sh`
2. **Test the APIs**: Use the verification steps above
3. **Explore the platform**: Open `http://localhost:3000`
4. **Check real-time data**: Verify no mock data is being used
5. **Customize**: Add your own features and improvements

The platform is now configured with your real API keys and ready for development! 🚀
