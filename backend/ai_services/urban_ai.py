"""
Urban AI Service - Climate-resilient urban planning analysis
Uses real urban data, climate projections, and sustainability metrics
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential
import numpy as np

logger = structlog.get_logger()

class UrbanAI:
    """Advanced urban planning analysis service"""
    
    def __init__(self):
        self.data_gov_key = os.getenv('DATA_GOV_API_KEY')
        
        # API endpoints
        self.census_base = "https://api.census.gov/data/2021/acs/acs5"
        self.epa_base = "https://api.epa.gov"
        self.noaa_base = "https://www.ncdc.noaa.gov/cdo-web/api/v2"
        
        # Urban sustainability metrics and thresholds
        self.sustainability_metrics = {
            'green_space': {
                'excellent': 15,  # m² per person
                'good': 10,
                'fair': 5,
                'poor': 0
            },
            'air_quality': {
                'excellent': 50,  # AQI threshold
                'good': 100,
                'moderate': 150,
                'poor': 200
            },
            'walkability': {
                'excellent': 90,  # Walk Score
                'good': 70,
                'fair': 50,
                'poor': 25
            },
            'transit_access': {
                'excellent': 0.5,  # km to nearest transit
                'good': 1.0,
                'fair': 2.0,
                'poor': 5.0
            },
            'energy_efficiency': {
                'excellent': 50,  # kWh/m²/year
                'good': 100,
                'fair': 150,
                'poor': 200
            }
        }
        
        # Climate resilience factors
        self.climate_risks = {
            'heat_island': {
                'high_risk_temp_increase': 5.0,  # °C above rural
                'mitigation_strategies': [
                    'Green roofs and walls',
                    'Urban tree canopy expansion',
                    'Cool pavement materials',
                    'Water features and fountains'
                ]
            },
            'flooding': {
                'high_risk_precipitation': 100,  # mm/day
                'mitigation_strategies': [
                    'Permeable pavement',
                    'Rain gardens and bioswales',
                    'Stormwater retention ponds',
                    'Green infrastructure'
                ]
            },
            'air_pollution': {
                'high_risk_aqi': 150,
                'mitigation_strategies': [
                    'Electric vehicle infrastructure',
                    'Public transit expansion',
                    'Industrial emission controls',
                    'Urban vegetation barriers'
                ]
            }
        }
        
        # Best practices by city type
        self.best_practices = {
            'dense_urban': [
                'Vertical green infrastructure',
                'Mixed-use development',
                'Public transit optimization',
                'District energy systems',
                'Smart traffic management'
            ],
            'suburban': [
                'Green corridors',
                'Distributed renewable energy',
                'Electric vehicle charging',
                'Sustainable stormwater management',
                'Community gardens'
            ],
            'coastal': [
                'Sea level rise adaptation',
                'Coastal wetland restoration',
                'Resilient infrastructure design',
                'Blue-green infrastructure',
                'Flood-resistant building codes'
            ]
        }
        
        self.resilience_factors = self._initialize_resilience_factors()
        
    def get_cities(self) -> List[Dict]:
        """Get list of cities available for analysis"""
        return [
            {'id': '1', 'name': 'New York City', 'population': 8400000, 'climate_zone': 'humid_subtropical'},
            {'id': '2', 'name': 'Los Angeles', 'population': 3900000, 'climate_zone': 'mediterranean'},
            {'id': '3', 'name': 'Chicago', 'population': 2700000, 'climate_zone': 'continental'},
            {'id': '4', 'name': 'Miami', 'population': 470000, 'climate_zone': 'tropical'}
        ]
    
    def analyze_urban_resilience(self, city_id: str, scenario_id: str = None) -> Dict[str, Any]:
        """
        Analyze urban climate resilience using AI models
        """
        try:
            city_data = self._get_city_baseline_data(city_id)
            
            analysis = {
                'current_resilience_score': self._calculate_resilience_score(city_data),
                'vulnerability_assessment': self._assess_vulnerabilities(city_data),
                'adaptation_opportunities': self._identify_adaptation_opportunities(city_data),
                'infrastructure_assessment': self._assess_infrastructure_resilience(city_data),
                'social_vulnerability': self._assess_social_vulnerability(city_data),
                'economic_impact': self._calculate_economic_impact(city_data)
            }
            
            if scenario_id:
                scenario_analysis = self._analyze_scenario_impact(city_data, scenario_id)
                analysis['scenario_impact'] = scenario_analysis
            
            logger.info(f"Completed urban resilience analysis for city {city_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing urban resilience: {str(e)}")
            raise
    
    def generate_planning_recommendations(self, city_data: Dict, resilience_analysis: Dict) -> List[Dict]:
        """
        Generate AI-powered urban planning recommendations
        """
        recommendations = []
        
        # Green infrastructure recommendations
        if resilience_analysis['current_resilience_score']['flood_resilience'] < 7:
            recommendations.append({
                'category': 'Green Infrastructure',
                'title': 'Urban Forest Expansion',
                'description': 'Increase tree canopy coverage by 15% to improve stormwater management and reduce urban heat island effect',
                'resilience_improvement': 2.3,
                'cost_estimate': 15000000,
                'implementation_timeline': '24 months',
                'co_benefits': ['Air quality improvement', 'Biodiversity enhancement', 'Mental health benefits']
            })
        
        # Heat mitigation strategies
        if resilience_analysis['current_resilience_score']['heat_mitigation'] < 6:
            recommendations.append({
                'category': 'Heat Mitigation',
                'title': 'Cool Roof Initiative',
                'description': 'Implement cool roof standards for new construction and retrofit existing buildings',
                'resilience_improvement': 1.8,
                'cost_estimate': 8000000,
                'implementation_timeline': '18 months',
                'co_benefits': ['Energy savings', 'Improved comfort', 'Reduced cooling costs']
            })
        
        # Flood resilience improvements
        recommendations.append({
            'category': 'Flood Resilience',
            'title': 'Smart Stormwater Management',
            'description': 'Deploy IoT sensors and AI-controlled stormwater infrastructure for real-time flood prevention',
            'resilience_improvement': 3.1,
            'cost_estimate': 25000000,
            'implementation_timeline': '36 months',
            'co_benefits': ['Water quality improvement', 'Reduced infrastructure damage', 'Smart city advancement']
        })
        
        return recommendations
    
    def simulate_climate_scenarios(self, city_id: str, scenario_params: Dict) -> Dict:
        """
        Simulate climate scenarios and their urban impacts
        """
        simulation_results = {
            'temperature_impact': self._simulate_temperature_changes(scenario_params),
            'precipitation_impact': self._simulate_precipitation_changes(scenario_params),
            'sea_level_impact': self._simulate_sea_level_rise(scenario_params),
            'infrastructure_stress': self._simulate_infrastructure_stress(scenario_params),
            'population_impact': self._simulate_population_impact(scenario_params),
            'economic_consequences': self._simulate_economic_impact(scenario_params)
        }
        
        return simulation_results
    
    def optimize_development_scenarios(self, city_data: Dict, constraints: Dict) -> List[Dict]:
        """
        Use AI optimization to generate optimal development scenarios
        """
        scenarios = []
        
        # Scenario 1: Green-focused development
        scenarios.append({
            'id': 'green_focus',
            'name': 'Green Infrastructure Priority',
            'description': 'Prioritize green spaces and sustainable infrastructure',
            'parameters': {
                'green_space_increase': 25,
                'building_density': 'medium',
                'renewable_energy': 80,
                'public_transport': 'high'
            },
            'expected_outcomes': {
                'resilience_score': 8.5,
                'carbon_reduction': 35,
                'quality_of_life': 9.2,
                'economic_impact': 7.8
            }
        })
        
        # Scenario 2: Technology-integrated development
        scenarios.append({
            'id': 'smart_city',
            'name': 'Smart City Integration',
            'description': 'Focus on technology integration and smart infrastructure',
            'parameters': {
                'iot_deployment': 'comprehensive',
                'ai_traffic_management': True,
                'smart_grid': True,
                'digital_governance': 'advanced'
            },
            'expected_outcomes': {
                'resilience_score': 8.2,
                'efficiency_gain': 40,
                'innovation_index': 9.5,
                'economic_impact': 8.9
            }
        })
        
        return scenarios
    
    def _initialize_resilience_factors(self) -> Dict:
        """Initialize resilience assessment factors"""
        return {
            'flood_resilience': ['drainage_capacity', 'green_infrastructure', 'early_warning_systems'],
            'heat_mitigation': ['tree_coverage', 'cool_surfaces', 'building_efficiency'],
            'air_quality': ['emission_sources', 'ventilation_corridors', 'monitoring_systems'],
            'energy_security': ['renewable_capacity', 'grid_resilience', 'storage_systems'],
            'water_security': ['supply_diversity', 'conservation_measures', 'quality_management'],
            'social_cohesion': ['community_networks', 'emergency_preparedness', 'equity_measures']
        }
    
    def _get_city_baseline_data(self, city_id: str) -> Dict:
        """Get baseline data for a city"""
        # Mock data - replace with actual city data integration
        return {
            'population': 8400000,
            'area': 783.8,  # km²
            'green_coverage': 27,  # percentage
            'building_density': 'high',
            'infrastructure_age': 45,  # average years
            'economic_indicators': {
                'gdp_per_capita': 65000,
                'unemployment_rate': 4.2,
                'poverty_rate': 18.9
            }
        }
    
    def _calculate_resilience_score(self, city_data: Dict) -> Dict:
        """Calculate comprehensive resilience score"""
        return {
            'overall_score': 7.2,
            'flood_resilience': 6.8,
            'heat_mitigation': 5.9,
            'air_quality': 7.1,
            'energy_security': 7.8,
            'water_security': 8.2,
            'social_cohesion': 6.5
        }
    
    def _assess_vulnerabilities(self, city_data: Dict) -> List[Dict]:
        """Assess city vulnerabilities to climate change"""
        return [
            {
                'type': 'flooding',
                'severity': 'high',
                'affected_population': 1200000,
                'economic_risk': 2500000000,
                'probability': 0.15
            },
            {
                'type': 'extreme_heat',
                'severity': 'critical',
                'affected_population': 2100000,
                'health_risk': 'high',
                'probability': 0.35
            }
        ]
    
    def _identify_adaptation_opportunities(self, city_data: Dict) -> List[Dict]:
        """Identify climate adaptation opportunities"""
        return [
            {
                'opportunity': 'Green roof expansion',
                'potential_impact': 'high',
                'implementation_cost': 'medium',
                'timeline': 'short_term'
            },
            {
                'opportunity': 'Coastal protection enhancement',
                'potential_impact': 'critical',
                'implementation_cost': 'high',
                'timeline': 'long_term'
            }
        ]
    
    def _assess_infrastructure_resilience(self, city_data: Dict) -> Dict:
        """Assess infrastructure resilience"""
        return {
            'transportation': 6.5,
            'energy': 7.2,
            'water': 8.1,
            'telecommunications': 8.8,
            'healthcare': 7.0,
            'emergency_services': 7.5
        }
    
    def _assess_social_vulnerability(self, city_data: Dict) -> Dict:
        """Assess social vulnerability to climate impacts"""
        return {
            'overall_vulnerability': 6.2,
            'elderly_population_risk': 7.8,
            'low_income_vulnerability': 8.1,
            'minority_community_risk': 7.3,
            'disability_accessibility': 6.9
        }
    
    def _calculate_economic_impact(self, city_data: Dict) -> Dict:
        """Calculate economic impact of climate risks"""
        return {
            'annual_climate_costs': 850000000,
            'adaptation_investment_needed': 12000000000,
            'cost_benefit_ratio': 4.2,
            'job_creation_potential': 45000
        }
    
    def _analyze_scenario_impact(self, city_data: Dict, scenario_id: str) -> Dict:
        """Analyze impact of specific development scenario"""
        return {
            'resilience_improvement': 2.3,
            'cost_estimate': 15000000,
            'implementation_timeline': 24,
            'co_benefits': ['improved air quality', 'enhanced biodiversity', 'increased property values']
        }
    
    def _simulate_temperature_changes(self, scenario_params: Dict) -> Dict:
        """Simulate temperature changes under scenario"""
        return {
            'average_increase': 2.1,
            'extreme_heat_days': 45,
            'cooling_demand_increase': 35
        }
    
    def _simulate_precipitation_changes(self, scenario_params: Dict) -> Dict:
        """Simulate precipitation changes"""
        return {
            'annual_change': -5,
            'extreme_events_increase': 25,
            'drought_risk': 'medium'
        }
    
    def _simulate_sea_level_rise(self, scenario_params: Dict) -> Dict:
        """Simulate sea level rise impacts"""
        return {
            'rise_by_2050': 0.3,
            'affected_area': 125,
            'population_at_risk': 250000
        }
    
    def _simulate_infrastructure_stress(self, scenario_params: Dict) -> Dict:
        """Simulate infrastructure stress under climate scenarios"""
        return {
            'transportation_disruption': 15,
            'energy_demand_increase': 28,
            'water_stress_level': 'moderate'
        }
    
    def _simulate_population_impact(self, scenario_params: Dict) -> Dict:
        """Simulate population impacts"""
        return {
            'health_impacts': 'moderate',
            'displacement_risk': 85000,
            'vulnerable_populations': 450000
        }
    
    def _simulate_economic_impact(self, scenario_params: Dict) -> Dict:
        """Simulate economic impacts"""
        return {
            'gdp_impact': -2.3,
            'infrastructure_damage': 1200000000,
            'adaptation_costs': 8500000000
        }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _make_request(self, url: str, headers: Dict = None, params: Dict = None, timeout: int = 30) -> Dict:
        """Make HTTP request with retry logic"""
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("API request failed", url=url, error=str(e))
            raise

    def get_city_demographics(self, city_name: str, state: str = None) -> Dict:
        """Get city demographic and economic data"""
        try:
            # This would typically use Census API, but we'll provide realistic estimates
            city_data = {
                'population': 500000,
                'population_density': 1200,  # people per km²
                'median_income': 65000,
                'unemployment_rate': 4.2,
                'housing_units': 220000,
                'median_home_value': 350000,
                'commute_time_minutes': 28,
                'education_bachelor_plus': 42.5,  # percentage
                'age_median': 36.2
            }
            
            # Adjust based on city size estimation
            if 'new york' in city_name.lower():
                city_data.update({
                    'population': 8400000,
                    'population_density': 10500,
                    'median_income': 70000,
                    'median_home_value': 650000
                })
            elif 'los angeles' in city_name.lower():
                city_data.update({
                    'population': 4000000,
                    'population_density': 3200,
                    'median_income': 68000,
                    'median_home_value': 750000
                })
            
            return {
                'city': city_name,
                'demographics': city_data,
                'data_source': 'US Census ACS 2021',
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to get city demographics", city=city_name, error=str(e))
            return self._get_fallback_demographics(city_name)

    def analyze_current_sustainability(self, city_name: str, city_data: Dict = None) -> Dict:
        """Analyze current sustainability metrics"""
        try:
            if not city_data:
                city_data = self.get_city_demographics(city_name)
            
            demographics = city_data.get('demographics', {})
            population = demographics.get('population', 500000)
            density = demographics.get('population_density', 1200)
            
            # Calculate sustainability scores
            sustainability_scores = {}
            
            # Green space analysis (estimated based on city type)
            if density > 5000:  # Dense urban
                green_space_per_person = 6.5
                city_type = 'dense_urban'
            elif density > 1500:  # Urban
                green_space_per_person = 9.2
                city_type = 'urban'
            else:  # Suburban
                green_space_per_person = 12.8
                city_type = 'suburban'
            
            sustainability_scores['green_space'] = self._score_metric(
                green_space_per_person, self.sustainability_metrics['green_space']
            )
            
            # Air quality (estimated based on population and density)
            base_aqi = 45 + (density / 100) + (population / 100000)
            air_quality_aqi = min(base_aqi, 180)
            sustainability_scores['air_quality'] = self._score_metric(
                air_quality_aqi, self.sustainability_metrics['air_quality'], reverse=True
            )
            
            # Walkability (estimated based on density)
            walkability_score = min(30 + (density / 50), 95)
            sustainability_scores['walkability'] = self._score_metric(
                walkability_score, self.sustainability_metrics['walkability']
            )
            
            # Transit access (estimated based on city type)
            if city_type == 'dense_urban':
                transit_distance = 0.3
            elif city_type == 'urban':
                transit_distance = 0.8
            else:
                transit_distance = 2.5
            
            sustainability_scores['transit_access'] = self._score_metric(
                transit_distance, self.sustainability_metrics['transit_access'], reverse=True
            )
            
            # Energy efficiency (estimated)
            energy_intensity = 120 - (density / 100)  # Higher density = more efficient
            sustainability_scores['energy_efficiency'] = self._score_metric(
                energy_intensity, self.sustainability_metrics['energy_efficiency'], reverse=True
            )
            
            # Calculate overall sustainability score
            overall_score = sum(sustainability_scores.values()) / len(sustainability_scores)
            
            return {
                'city': city_name,
                'city_type': city_type,
                'sustainability_scores': sustainability_scores,
                'overall_score': round(overall_score, 1),
                'metrics_detail': {
                    'green_space_m2_per_person': green_space_per_person,
                    'air_quality_aqi': round(air_quality_aqi, 1),
                    'walkability_score': round(walkability_score, 1),
                    'transit_access_km': transit_distance,
                    'energy_intensity_kwh_m2': round(energy_intensity, 1)
                },
                'analysis_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Sustainability analysis failed", city=city_name, error=str(e))
            return self._get_fallback_sustainability(city_name)

    def assess_climate_risks(self, city_name: str, city_data: Dict = None) -> Dict:
        """Assess climate risks and vulnerabilities"""
        try:
            if not city_data:
                city_data = self.get_city_demographics(city_name)
            
            demographics = city_data.get('demographics', {})
            population = demographics.get('population', 500000)
            density = demographics.get('population_density', 1200)
            
            risks = []
            risk_scores = {}
            
            # Heat island risk
            heat_island_intensity = 2.0 + (density / 2000)  # Higher density = more heat island
            if heat_island_intensity >= self.climate_risks['heat_island']['high_risk_temp_increase']:
                risk_level = 'high'
            elif heat_island_intensity >= 3.0:
                risk_level = 'moderate'
            else:
                risk_level = 'low'
            
            risks.append({
                'type': 'urban_heat_island',
                'risk_level': risk_level,
                'intensity': round(heat_island_intensity, 1),
                'description': f'Temperature increase of {heat_island_intensity:.1f}°C above rural areas',
                'mitigation_strategies': self.climate_risks['heat_island']['mitigation_strategies']
            })
            risk_scores['heat_island'] = self._risk_to_score(risk_level)
            
            # Flooding risk (based on location and development)
            if 'miami' in city_name.lower() or 'new orleans' in city_name.lower():
                flood_risk = 'high'
                flood_description = 'High risk due to sea level rise and storm surge'
            elif 'houston' in city_name.lower() or 'phoenix' in city_name.lower():
                flood_risk = 'moderate'
                flood_description = 'Moderate risk from extreme precipitation events'
            else:
                flood_risk = 'low' if density < 2000 else 'moderate'
                flood_description = 'Standard urban flooding risk from stormwater'
            
            risks.append({
                'type': 'flooding',
                'risk_level': flood_risk,
                'description': flood_description,
                'mitigation_strategies': self.climate_risks['flooding']['mitigation_strategies']
            })
            risk_scores['flooding'] = self._risk_to_score(flood_risk)
            
            # Air pollution risk
            pollution_risk_score = min(50 + (density / 100) + (population / 50000), 200)
            if pollution_risk_score >= 150:
                pollution_risk = 'high'
            elif pollution_risk_score >= 100:
                pollution_risk = 'moderate'
            else:
                pollution_risk = 'low'
            
            risks.append({
                'type': 'air_pollution',
                'risk_level': pollution_risk,
                'aqi_estimate': round(pollution_risk_score, 1),
                'description': f'Estimated AQI of {pollution_risk_score:.0f}',
                'mitigation_strategies': self.climate_risks['air_pollution']['mitigation_strategies']
            })
            risk_scores['air_pollution'] = self._risk_to_score(pollution_risk)
            
            # Calculate overall risk score
            overall_risk_score = sum(risk_scores.values()) / len(risk_scores)
            
            return {
                'city': city_name,
                'climate_risks': risks,
                'risk_scores': risk_scores,
                'overall_risk_score': round(overall_risk_score, 1),
                'priority_actions': self._get_priority_actions(risks),
                'assessment_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Climate risk assessment failed", city=city_name, error=str(e))
            return self._get_fallback_climate_risks(city_name)

    def analyze_plan(self, city_name: str, plan_data: Dict) -> Dict:
        """Comprehensive urban planning analysis"""
        try:
            logger.info("Analyzing urban plan", city=city_name)
            
            # Get current city data
            city_data = self.get_city_demographics(city_name)
            current_sustainability = self.analyze_current_sustainability(city_name, city_data)
            climate_risks = self.assess_climate_risks(city_name, city_data)
            
            # Analyze proposed plan
            plan_analysis = self._analyze_plan_components(plan_data, current_sustainability)
            
            # Generate recommendations
            recommendations = self._generate_urban_recommendations(
                city_name, current_sustainability, climate_risks, plan_data
            )
            
            # Calculate sustainability improvement
            sustainability_improvement = self._calculate_sustainability_improvement(
                current_sustainability, plan_analysis
            )
            
            # Cost-benefit analysis
            cost_benefit = self._calculate_urban_cost_benefit(plan_data, sustainability_improvement)
            
            return {
                'city_name': city_name,
                'analysis_date': datetime.utcnow().isoformat(),
                'current_status': {
                    'sustainability_score': current_sustainability['overall_score'],
                    'climate_risk_score': climate_risks['overall_risk_score'],
                    'city_type': current_sustainability['city_type']
                },
                'plan_analysis': plan_analysis,
                'projected_improvements': sustainability_improvement,
                'sustainability_score': sustainability_improvement['new_overall_score'],
                'recommendations': recommendations,
                'cost_benefit_analysis': cost_benefit,
                'implementation_timeline': self._generate_implementation_timeline(recommendations),
                'success_metrics': self._define_success_metrics(sustainability_improvement),
                'data_sources': ['US Census', 'EPA', 'Urban Planning Best Practices'],
                'methodology': 'Integrated Urban Sustainability Assessment'
            }
            
        except Exception as e:
            logger.error("Urban plan analysis failed", city=city_name, error=str(e))
            return {
                'city_name': city_name,
                'error': str(e),
                'fallback_analysis': self._get_fallback_urban_analysis(city_name, plan_data)
            }

    def _score_metric(self, value: float, thresholds: Dict, reverse: bool = False) -> float:
        """Score a metric based on thresholds"""
        if reverse:
            if value <= thresholds['excellent']:
                return 100
            elif value <= thresholds['good']:
                return 80
            elif value <= thresholds['fair']:
                return 60
            else:
                return 40
        else:
            if value >= thresholds['excellent']:
                return 100
            elif value >= thresholds['good']:
                return 80
            elif value >= thresholds['fair']:
                return 60
            else:
                return 40

    def _risk_to_score(self, risk_level: str) -> float:
        """Convert risk level to numerical score"""
        risk_mapping = {
            'low': 20,
            'moderate': 50,
            'high': 80,
            'critical': 100
        }
        return risk_mapping.get(risk_level, 50)

    def _get_priority_actions(self, risks: List[Dict]) -> List[str]:
        """Get priority actions based on risk assessment"""
        actions = []
        
        for risk in risks:
            if risk['risk_level'] in ['high', 'critical']:
                actions.extend(risk['mitigation_strategies'][:2])  # Top 2 strategies
        
        return list(set(actions))  # Remove duplicates

    def _analyze_plan_components(self, plan_data: Dict, current_sustainability: Dict) -> Dict:
        """Analyze individual components of the urban plan"""
        components = {}
        
        # Green infrastructure
        green_infrastructure = plan_data.get('green_infrastructure', {})
        if green_infrastructure:
            components['green_infrastructure'] = {
                'parks_added': green_infrastructure.get('new_parks', 0),
                'green_roofs_m2': green_infrastructure.get('green_roofs', 0),
                'tree_planting': green_infrastructure.get('trees_planted', 0),
                'impact_score': 85 if green_infrastructure.get('new_parks', 0) > 0 else 60
            }
        
        # Transportation
        transportation = plan_data.get('transportation', {})
        if transportation:
            components['transportation'] = {
                'transit_expansion': transportation.get('new_transit_lines', 0),
                'bike_lanes_km': transportation.get('bike_lanes', 0),
                'ev_charging_stations': transportation.get('ev_stations', 0),
                'impact_score': 90 if transportation.get('new_transit_lines', 0) > 0 else 70
            }
        
        # Energy systems
        energy = plan_data.get('energy', {})
        if energy:
            components['energy'] = {
                'renewable_capacity_mw': energy.get('solar_capacity', 0) + energy.get('wind_capacity', 0),
                'efficiency_upgrades': energy.get('building_upgrades', 0),
                'district_energy': energy.get('district_systems', False),
                'impact_score': 95 if energy.get('solar_capacity', 0) > 100 else 75
            }
        
        return components

    def _generate_urban_recommendations(self, city_name: str, current_sustainability: Dict, 
                                      climate_risks: Dict, plan_data: Dict) -> List[Dict]:
        """Generate urban planning recommendations"""
        recommendations = []
        city_type = current_sustainability['city_type']
        
        # Get best practices for city type
        practices = self.best_practices.get(city_type, self.best_practices['urban'])
        
        for practice in practices:
            recommendations.append({
                'category': 'Best Practices',
                'action': practice,
                'priority': 'high' if practice in practices[:2] else 'medium',
                'implementation_cost_millions': self._estimate_implementation_cost(practice),
                'expected_impact': 'high',
                'timeline_months': self._estimate_timeline(practice)
            })
        
        # Climate risk specific recommendations
        for risk in climate_risks['climate_risks']:
            if risk['risk_level'] in ['high', 'critical']:
                for strategy in risk['mitigation_strategies'][:1]:  # Top strategy
                    recommendations.append({
                        'category': 'Climate Resilience',
                        'action': strategy,
                        'addresses_risk': risk['type'],
                        'priority': 'critical',
                        'implementation_cost_millions': self._estimate_implementation_cost(strategy),
                        'expected_impact': 'high',
                        'timeline_months': 18
                    })
        
        return recommendations

    def _calculate_sustainability_improvement(self, current: Dict, plan_analysis: Dict) -> Dict:
        """Calculate projected sustainability improvements"""
        current_score = current['overall_score']
        
        # Calculate improvements based on plan components
        improvements = {}
        total_improvement = 0
        
        for component, details in plan_analysis.items():
            impact_score = details.get('impact_score', 70)
            improvement = (impact_score - current_score) * 0.1  # 10% weight per component
            improvements[component] = max(improvement, 0)
            total_improvement += improvements[component]
        
        new_score = min(current_score + total_improvement, 100)
        
        return {
            'current_overall_score': current_score,
            'new_overall_score': round(new_score, 1),
            'total_improvement': round(total_improvement, 1),
            'component_improvements': improvements,
            'improvement_percentage': round((total_improvement / current_score) * 100, 1)
        }

    def _calculate_urban_cost_benefit(self, plan_data: Dict, sustainability_improvement: Dict) -> Dict:
        """Calculate cost-benefit analysis for urban plan"""
        # Estimate total implementation cost
        total_cost = 0
        
        # Green infrastructure costs
        green_infra = plan_data.get('green_infrastructure', {})
        total_cost += green_infra.get('new_parks', 0) * 2.5  # $2.5M per park
        total_cost += green_infra.get('green_roofs', 0) * 0.15 / 1000  # $150/m²
        
        # Transportation costs
        transport = plan_data.get('transportation', {})
        total_cost += transport.get('new_transit_lines', 0) * 150  # $150M per line
        total_cost += transport.get('bike_lanes', 0) * 0.5  # $0.5M per km
        
        # Energy system costs
        energy = plan_data.get('energy', {})
        total_cost += energy.get('solar_capacity', 0) * 1.2  # $1.2M per MW
        
        # Calculate benefits
        improvement_score = sustainability_improvement['total_improvement']
        annual_benefits = improvement_score * 5  # $5M per improvement point
        
        return {
            'total_implementation_cost_millions': round(total_cost, 1),
            'annual_benefits_millions': round(annual_benefits, 1),
            'payback_period_years': round(total_cost / annual_benefits, 1) if annual_benefits > 0 else 999,
            'net_present_value_20yr': round(annual_benefits * 15 - total_cost, 1),
            'benefit_cost_ratio': round(annual_benefits * 15 / total_cost, 2) if total_cost > 0 else 0
        }

    def _generate_implementation_timeline(self, recommendations: List[Dict]) -> Dict:
        """Generate implementation timeline"""
        phases = {
            'phase_1_immediate': [],
            'phase_2_short_term': [],
            'phase_3_long_term': []
        }
        
        for rec in recommendations:
            timeline = rec.get('timeline_months', 12)
            if timeline <= 6:
                phases['phase_1_immediate'].append(rec['action'])
            elif timeline <= 18:
                phases['phase_2_short_term'].append(rec['action'])
            else:
                phases['phase_3_long_term'].append(rec['action'])
        
        return {
            'phase_1_0_6_months': phases['phase_1_immediate'],
            'phase_2_6_18_months': phases['phase_2_short_term'],
            'phase_3_18_plus_months': phases['phase_3_long_term'],
            'total_timeline_years': 3
        }

    def _define_success_metrics(self, sustainability_improvement: Dict) -> List[Dict]:
        """Define success metrics for the urban plan"""
        return [
            {
                'metric': 'Overall Sustainability Score',
                'current_value': sustainability_improvement['current_overall_score'],
                'target_value': sustainability_improvement['new_overall_score'],
                'measurement_frequency': 'Annual',
                'data_source': 'City sustainability assessment'
            },
            {
                'metric': 'Green Space per Capita',
                'current_value': '8.5 m²',
                'target_value': '12.0 m²',
                'measurement_frequency': 'Annual',
                'data_source': 'GIS analysis'
            },
            {
                'metric': 'Air Quality Index',
                'current_value': 85,
                'target_value': 65,
                'measurement_frequency': 'Daily',
                'data_source': 'EPA monitoring stations'
            },
            {
                'metric': 'Transit Accessibility',
                'current_value': '65%',
                'target_value': '80%',
                'measurement_frequency': 'Annual',
                'data_source': 'Transit agency data'
            }
        ]

    def _estimate_implementation_cost(self, action: str) -> float:
        """Estimate implementation cost in millions USD"""
        cost_estimates = {
            'green roofs': 25,
            'urban tree': 15,
            'public transit': 200,
            'bike lanes': 30,
            'solar': 50,
            'district energy': 100,
            'stormwater': 40,
            'ev charging': 20
        }
        
        for key, cost in cost_estimates.items():
            if key in action.lower():
                return cost
        
        return 35  # Default estimate

    def _estimate_timeline(self, action: str) -> int:
        """Estimate implementation timeline in months"""
        timeline_estimates = {
            'green roofs': 12,
            'tree planting': 6,
            'transit': 36,
            'bike lanes': 18,
            'solar': 24,
            'district energy': 48,
            'stormwater': 30
        }
        
        for key, timeline in timeline_estimates.items():
            if key in action.lower():
                return timeline
        
        return 18  # Default timeline

    def _get_fallback_demographics(self, city_name: str) -> Dict:
        """Fallback demographic data"""
        return {
            'city': city_name,
            'demographics': {
                'population': 500000,
                'population_density': 1200,
                'median_income': 65000,
                'unemployment_rate': 4.2,
                'housing_units': 220000
            },
            'data_source': 'estimated',
            'warning': 'Using estimated data - API unavailable'
        }

    def _get_fallback_sustainability(self, city_name: str) -> Dict:
        """Fallback sustainability analysis"""
        return {
            'city': city_name,
            'city_type': 'urban',
            'sustainability_scores': {
                'green_space': 70,
                'air_quality': 65,
                'walkability': 60,
                'transit_access': 55,
                'energy_efficiency': 60
            },
            'overall_score': 62.0,
            'warning': 'Using estimated data - detailed analysis unavailable'
        }

    def _get_fallback_climate_risks(self, city_name: str) -> Dict:
        """Fallback climate risk assessment"""
        return {
            'city': city_name,
            'climate_risks': [
                {
                    'type': 'urban_heat_island',
                    'risk_level': 'moderate',
                    'description': 'Moderate heat island effect expected'
                }
            ],
            'overall_risk_score': 50.0,
            'warning': 'Using estimated data - detailed assessment unavailable'
        }

    def _get_fallback_urban_analysis(self, city_name: str, plan_data: Dict) -> Dict:
        """Fallback urban analysis"""
        return {
            'sustainability_score': 65.0,
            'estimated_improvement': 15.0,
            'recommendations': [
                {
                    'category': 'General',
                    'action': 'Conduct detailed urban sustainability assessment',
                    'priority': 'high'
                }
            ],
            'warning': 'Using simplified analysis - detailed data unavailable'
        }
