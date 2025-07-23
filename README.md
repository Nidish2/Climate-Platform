# Climate Change Analysis and Mitigation Platform

A comprehensive full-stack web application for climate change analysis, prediction, and mitigation planning using advanced AI technologies.

## 🌍 Overview

This platform integrates multiple AI technologies to provide comprehensive climate intelligence across three core domains:

- **Extreme Weather Prediction System**: AI-powered weather forecasting and risk assessment
- **Corporate Carbon Footprint Analyzer**: Carbon analysis and policy recommendations  
- **Climate-Resilient Urban Planning Assistant**: Urban development scenario modeling

## 🚀 Key Features

### AI Technologies Integrated
- **IBM Environmental Intelligence API**: Weather data and environmental insights
- **Agentic AI**: Autonomous decision-making and analysis
- **RAG (Retrieval-Augmented Generation)**: Context-aware information retrieval
- **Granite AI**: Ethical and accurate information sourcing
- **Data-Prep-Kit**: Advanced data processing and preparation

### Core Modules

#### 1. Weather Prediction System
- Real-time extreme weather forecasting
- Hurricane tracking and formation prediction
- Wildfire risk assessment
- Interactive weather risk mapping
- AI-generated insights and recommendations

#### 2. Carbon Footprint Analyzer
- Corporate emissions analysis (Scope 1, 2, 3)
- Industry benchmarking and best practices
- Regulatory compliance assessment
- AI-powered reduction strategies
- Data upload and processing capabilities

#### 3. Urban Planning Assistant
- Climate resilience modeling
- Scenario simulation and optimization
- Green infrastructure recommendations
- Interactive urban development mapping
- Multi-criteria decision analysis

## 🛠 Technology Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Query** for data fetching
- **React Router** for navigation
- **Recharts** for data visualization
- **Leaflet** for interactive maps

### Backend
- **Python Flask** RESTful API
- **PostgreSQL** with PostGIS for spatial data
- **Redis** for caching
- **JWT** authentication
- **SQLAlchemy** ORM
- **Pandas/NumPy** for data processing

### AI Services
- Custom AI service integrations
- Modular architecture for different AI providers
- Ethical AI framework with Granite AI
- Advanced data preparation pipelines

### Infrastructure
- **Docker** containerization
- **Nginx** reverse proxy
- **Docker Compose** for orchestration
- Health checks and monitoring
- SSL/TLS security configuration

## 📦 Installation & Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Quick Start with Docker

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd climate-platform
   \`\`\`

2. **Set up environment variables**
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   \`\`\`

3. **Start the application**
   \`\`\`bash
   docker-compose up -d
   \`\`\`

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Database: localhost:5432

### Local Development Setup

#### Frontend Setup
\`\`\`bash
# Install dependencies
npm install

# Start development server
npm run dev
\`\`\`

#### Backend Setup
\`\`\`bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
python run.py
\`\`\`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

\`\`\`env
# API Keys
IBM_ENVIRONMENTAL_API_KEY=your_ibm_api_key
OPENAI_API_KEY=your_openai_api_key

# Database
DATABASE_URL=postgresql://climate_user:climate_pass@localhost:5432/climate_db

# JWT
JWT_SECRET_KEY=your_jwt_secret_key

# Flask
FLASK_ENV=development
FLASK_DEBUG=true
\`\`\`

### Database Setup

The database is automatically initialized with the schema and sample data when using Docker Compose. For manual setup:

\`\`\`bash
# Connect to PostgreSQL
psql -h localhost -U climate_user -d climate_db

# Run initialization script
\i database/init.sql
\`\`\`

## 📊 API Documentation

### Authentication
\`\`\`bash
# Login
POST /api/auth/login
{
  "email": "admin@climate.com",
  "password": "admin123"
}

# Verify token
GET /api/auth/verify
Authorization: Bearer <token>
\`\`\`

### Weather Endpoints
\`\`\`bash
# Get weather predictions
GET /api/weather/predictions?location=global&range=7d

# Get risk assessment
GET /api/weather/risk?location=global

# Get historical data
GET /api/weather/historical?location=global
\`\`\`

### Carbon Endpoints
\`\`\`bash
# Get companies
GET /api/carbon/companies

# Get carbon data
GET /api/carbon/data/{company_id}

# Upload carbon data
POST /api/carbon/upload
Content-Type: multipart/form-data
\`\`\`

### Urban Planning Endpoints
\`\`\`bash
# Get cities
GET /api/urban/cities

# Get city data
GET /api/urban/cities/{city_id}

# Run simulation
POST /api/urban/simulate
{
  "cityId": "city_id",
  "scenarioId": "scenario_id"
}
\`\`\`

## 🧪 Testing

### Frontend Tests
\`\`\`bash
npm run test
\`\`\`

### Backend Tests
\`\`\`bash
cd backend
python -m pytest tests/
\`\`\`

### Integration Tests
\`\`\`bash
# Run full test suite
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
\`\`\`

## 🚀 Deployment

### Production Deployment

1. **Configure production environment**
   \`\`\`bash
   cp .env.production .env
   # Update with production values
   \`\`\`

2. **Build and deploy**
   \`\`\`bash
   docker-compose -f docker-compose.prod.yml up -d
   \`\`\`

3. **Set up SSL certificates**
   \`\`\`bash
   # Place SSL certificates in nginx/ssl/
   # Uncomment HTTPS configuration in nginx.conf
   \`\`\`

### Cloud Deployment Options

- **AWS**: Use ECS/Fargate with RDS and ElastiCache
- **Google Cloud**: Use Cloud Run with Cloud SQL and Memorystore
- **Azure**: Use Container Instances with Azure Database
- **Vercel**: Frontend deployment with serverless functions

## 📈 Monitoring & Observability

### Health Checks
- Frontend: `http://localhost:3000/health`
- Backend: `http://localhost:5000/api/health`
- Database: Built-in PostgreSQL monitoring

### Logging
- Application logs via Docker Compose
- Structured logging with JSON format
- Error tracking and alerting

### Metrics
- API response times
- Database query performance
- AI model inference times
- User engagement analytics

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, Analyst, Planner)
- Secure password hashing with bcrypt

### Data Security
- SQL injection prevention with parameterized queries
- XSS protection with content security policies
- HTTPS encryption in production
- Rate limiting on API endpoints

### AI Ethics & Governance
- Granite AI for ethical information sourcing
- Bias detection and mitigation
- Transparency in AI decision-making
- Data lineage and audit trails

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow TypeScript/Python coding standards
- Write comprehensive tests
- Update documentation
- Ensure AI ethics compliance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- IBM Environmental Intelligence for weather data
- OpenAI for AI capabilities
- Climate science community for research insights
- Open source contributors and maintainers

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation wiki

---

**Built with ❤️ for climate action and sustainability**
