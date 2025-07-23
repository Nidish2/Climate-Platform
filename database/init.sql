-- Climate Platform Database Schema
-- Initialize database for climate change analysis platform

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'analyst', 'planner')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Companies table for carbon footprint analysis
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    size VARCHAR(50) CHECK (size IN ('small', 'medium', 'large', 'enterprise')),
    country VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Carbon emissions data
CREATE TABLE carbon_emissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    reporting_year INTEGER NOT NULL,
    scope_1_emissions DECIMAL(15,2),
    scope_2_emissions DECIMAL(15,2),
    scope_3_emissions DECIMAL(15,2),
    total_emissions DECIMAL(15,2),
    carbon_intensity DECIMAL(10,4),
    verification_status VARCHAR(50) DEFAULT 'unverified',
    data_quality_score DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, reporting_year)
);

-- Cities table for urban planning
CREATE TABLE cities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    population INTEGER,
    area_km2 DECIMAL(10,2),
    coordinates GEOMETRY(POINT, 4326),
    climate_zone VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Urban planning scenarios
CREATE TABLE urban_scenarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_id UUID REFERENCES cities(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    scenario_type VARCHAR(100),
    parameters JSONB,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather data and predictions
CREATE TABLE weather_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_name VARCHAR(255),
    coordinates GEOMETRY(POINT, 4326),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    pressure DECIMAL(7,2),
    wind_speed DECIMAL(5,2),
    precipitation DECIMAL(6,2),
    data_source VARCHAR(100),
    data_quality VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather alerts and predictions
CREATE TABLE weather_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    location_name VARCHAR(255),
    coordinates GEOMETRY(POINT, 4326),
    message TEXT NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    confidence_score DECIMAL(3,2),
    ai_generated BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- AI model predictions and insights
CREATE TABLE ai_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    domain VARCHAR(50) NOT NULL CHECK (domain IN ('weather', 'carbon', 'urban')),
    entity_id UUID, -- References companies, cities, or weather locations
    insight_type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    confidence_score DECIMAL(3,2),
    ai_model VARCHAR(100),
    supporting_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Data processing jobs and lineage
CREATE TABLE data_processing_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    input_data JSONB,
    output_data JSONB,
    processing_metadata JSONB,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit log for tracking changes
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    user_id UUID REFERENCES users(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_carbon_emissions_company_year ON carbon_emissions(company_id, reporting_year);
CREATE INDEX idx_weather_data_location_time ON weather_data(coordinates, timestamp);
CREATE INDEX idx_weather_alerts_active ON weather_alerts(is_active, severity) WHERE is_active = true;
CREATE INDEX idx_ai_insights_domain_entity ON ai_insights(domain, entity_id);
CREATE INDEX idx_audit_log_table_record ON audit_log(table_name, record_id);

-- Insert sample data
INSERT INTO users (email, password_hash, name, role) VALUES
('admin@climate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PmvlG.', 'Admin User', 'admin'),
('analyst@climate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PmvlG.', 'Climate Analyst', 'analyst'),
('planner@climate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PmvlG.', 'Urban Planner', 'planner');

INSERT INTO companies (name, sector, size, country) VALUES
('TechCorp Inc.', 'Technology', 'large', 'United States'),
('Manufacturing Ltd.', 'Manufacturing', 'medium', 'Germany'),
('Energy Solutions', 'Energy', 'large', 'United Kingdom'),
('Retail Chain Co.', 'Retail', 'enterprise', 'Canada');

INSERT INTO cities (name, country, population, area_km2, coordinates, climate_zone) VALUES
('New York City', 'United States', 8400000, 783.8, ST_GeomFromText('POINT(-74.0060 40.7128)', 4326), 'humid_subtropical'),
('Los Angeles', 'United States', 3900000, 1302.0, ST_GeomFromText('POINT(-118.2437 34.0522)', 4326), 'mediterranean'),
('Chicago', 'United States', 2700000, 606.1, ST_GeomFromText('POINT(-87.6298 41.8781)', 4326), 'continental'),
('Miami', 'United States', 470000, 143.1, ST_GeomFromText('POINT(-80.1918 25.7617)', 4326), 'tropical');

-- Insert sample carbon emissions data
INSERT INTO carbon_emissions (company_id, reporting_year, scope_1_emissions, scope_2_emissions, scope_3_emissions, total_emissions, carbon_intensity, verification_status, data_quality_score)
SELECT 
    c.id,
    2023,
    CASE 
        WHEN c.name = 'TechCorp Inc.' THEN 45000
        WHEN c.name = 'Manufacturing Ltd.' THEN 85000
        WHEN c.name = 'Energy Solutions' THEN 120000
        ELSE 35000
    END,
    CASE 
        WHEN c.name = 'TechCorp Inc.' THEN 35000
        WHEN c.name = 'Manufacturing Ltd.' THEN 65000
        WHEN c.name = 'Energy Solutions' THEN 95000
        ELSE 25000
    END,
    CASE 
        WHEN c.name = 'TechCorp Inc.' THEN 45000
        WHEN c.name = 'Manufacturing Ltd.' THEN 95000
        WHEN c.name = 'Energy Solutions' THEN 150000
        ELSE 40000
    END,
    CASE 
        WHEN c.name = 'TechCorp Inc.' THEN 125000
        WHEN c.name = 'Manufacturing Ltd.' THEN 245000
        WHEN c.name = 'Energy Solutions' THEN 365000
        ELSE 100000
    END,
    CASE 
        WHEN c.name = 'TechCorp Inc.' THEN 2.4
        WHEN c.name = 'Manufacturing Ltd.' THEN 4.8
        WHEN c.name = 'Energy Solutions' THEN 6.2
        ELSE 3.1
    END,
    'verified',
    0.92
FROM companies c;

-- Insert sample weather alerts
INSERT INTO weather_alerts (alert_type, severity, location_name, coordinates, message, start_time, end_time, confidence_score, ai_generated, is_active)
VALUES
('hurricane', 'high', 'Gulf of Mexico', ST_GeomFromText('POINT(-90.0 25.0)', 4326), 'Category 3 hurricane forming, landfall expected in 72 hours', NOW(), NOW() + INTERVAL '5 days', 0.87, true, true),
('heatwave', 'critical', 'Phoenix, AZ', ST_GeomFromText('POINT(-112.0740 33.4484)', 4326), 'Extreme heat warning: temperatures exceeding 115°F for 5+ days', NOW(), NOW() + INTERVAL '7 days', 0.92, true, true),
('wildfire', 'medium', 'Northern California', ST_GeomFromText('POINT(-122.0 39.0)', 4326), 'Red flag warning issued, high fire danger conditions', NOW(), NOW() + INTERVAL '3 days', 0.78, true, true);

-- Insert sample AI insights
INSERT INTO ai_insights (domain, insight_type, title, description, confidence_score, ai_model, supporting_data)
VALUES
('weather', 'pattern_analysis', 'Hurricane Season Analysis', 'Agentic AI has detected increased sea surface temperatures in the Atlantic, indicating a 73% probability of above-normal hurricane activity this season.', 0.87, 'agentic_weather_ai', '{"sst_anomaly": 1.2, "wind_shear": "low", "mjo_phase": "favorable"}'),
('carbon', 'reduction_opportunity', 'Manufacturing Sector Optimization', 'AI analysis identified 15% reduction opportunity in manufacturing sector through energy efficiency improvements and renewable energy adoption.', 0.91, 'carbon_optimization_ai', '{"sector": "manufacturing", "potential_reduction": 15, "primary_strategies": ["energy_efficiency", "renewable_energy"]}'),
('urban', 'infrastructure_recommendation', 'Green Infrastructure Priority', 'RAG analysis suggests implementing 25% more green roofs and urban forests to improve flood resilience and reduce urban heat island effect.', 0.89, 'urban_planning_ai', '{"green_infrastructure_increase": 25, "flood_resilience_improvement": 2.3, "heat_reduction": 1.8}');

-- Create functions for audit logging
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values)
        VALUES (TG_TABLE_NAME, OLD.id, TG_OP, row_to_json(OLD));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values, new_values)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, new_values)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(NEW));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create audit triggers for main tables
CREATE TRIGGER audit_users AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_companies AFTER INSERT OR UPDATE OR DELETE ON companies
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_carbon_emissions AFTER INSERT OR UPDATE OR DELETE ON carbon_emissions
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_cities AFTER INSERT OR UPDATE OR DELETE ON cities
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO climate_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO climate_user;
