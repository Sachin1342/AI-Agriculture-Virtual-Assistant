from typing import Dict, List
from datetime import datetime, timedelta

class ResourceManagementService:
    """
    Resource management service for irrigation, fertilizer, and water optimization
    """
    
    CROP_WATER_REQUIREMENTS = {
        'rice': {'min': 1000, 'max': 1500, 'unit': 'mm/season'},
        'wheat': {'min': 400, 'max': 600, 'unit': 'mm/season'},
        'corn': {'min': 500, 'max': 800, 'unit': 'mm/season'},
        'tomato': {'min': 400, 'max': 600, 'unit': 'mm/season'},
        'potato': {'min': 400, 'max': 650, 'unit': 'mm/season'},
        'cotton': {'min': 600, 'max': 900, 'unit': 'mm/season'},
        'sugarcane': {'min': 1200, 'max': 2250, 'unit': 'mm/season'}
    }
    
    FERTILIZER_REQUIREMENTS = {
        'rice': {'N': 80, 'P': 40, 'K': 40, 'unit': 'kg/hectare'},
        'wheat': {'N': 120, 'P': 60, 'K': 40, 'unit': 'kg/hectare'},
        'corn': {'N': 150, 'P': 70, 'K': 60, 'unit': 'kg/hectare'},
        'tomato': {'N': 100, 'P': 80, 'K': 100, 'unit': 'kg/hectare'},
        'potato': {'N': 120, 'P': 100, 'K': 150, 'unit': 'kg/hectare'},
        'cotton': {'N': 100, 'P': 50, 'K': 50, 'unit': 'kg/hectare'},
        'sugarcane': {'N': 150, 'P': 80, 'K': 100, 'unit': 'kg/hectare'}
    }
    
    IRRIGATION_SCHEDULE_DAYS = {
        'rice': {'germination': 7, 'vegetative': 7, 'reproductive': 5, 'maturity': 15},
        'wheat': {'germination': 10, 'vegetative': 12, 'reproductive': 10, 'maturity': 20},
        'corn': {'germination': 8, 'vegetative': 10, 'reproductive': 8, 'maturity': 25},
        'tomato': {'germination': 5, 'vegetative': 6, 'reproductive': 4, 'maturity': 10},
        'potato': {'germination': 7, 'vegetative': 7, 'reproductive': 5, 'maturity': 15},
        'cotton': {'germination': 12, 'vegetative': 15, 'reproductive': 10, 'maturity': 20}
    }
    
    def __init__(self):
        pass
    
    def generate_irrigation_schedule(self, data: Dict) -> Dict:
        """
        Generate irrigation schedule based on crop and season
        """
        crop = data.get('crop_type', 'rice').lower()
        area = data.get('area', 1.0)
        season = data.get('season', 'monsoon')
        rainfall = data.get('rainfall', 100)
        soil_type = data.get('soil_type', 'loamy')
        
        try:
            water_req = self.CROP_WATER_REQUIREMENTS.get(crop, {'min': 500, 'max': 800})
            schedule_intervals = self.IRRIGATION_SCHEDULE_DAYS.get(crop, {})
            
            # Adjust water requirement based on rainfall
            total_water_needed = (water_req['min'] + water_req['max']) / 2
            irrigation_water_needed = max(0, total_water_needed - rainfall)
            
            # Calculate irrigation intervals based on soil type
            interval_days = self._get_irrigation_interval(soil_type, season)
            
            # Generate schedule for 120 days (typical crop cycle)
            schedule = self._generate_schedule(
                start_date=datetime.now(),
                interval_days=interval_days,
                total_days=120,
                water_per_irrigation=irrigation_water_needed / 15
            )
            
            total_irrigation_water = irrigation_water_needed * area  # in mm for area
            
            return {
                "success": True,
                "crop": crop,
                "season": season,
                "total_water_requirement_mm": float(total_water_needed),
                "expected_rainfall_mm": float(rainfall),
                "irrigation_water_needed_mm": float(irrigation_water_needed),
                "irrigation_interval_days": interval_days,
                "total_irrigation_water_liters": float(irrigation_water_needed * area * 10000),  # mm * hectare to liters
                "schedule": schedule,
                "soil_type": soil_type,
                "recommendations": self._get_irrigation_recommendations(crop, season, soil_type)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_fertilizer_schedule(self, data: Dict) -> Dict:
        """
        Generate fertilizer application schedule
        """
        crop = data.get('crop_type', 'rice').lower()
        area = data.get('area', 1.0)
        soil_nutrients = data.get('current_soil_nutrients', {'N': 20, 'P': 10, 'K': 15})
        
        try:
            requirements = self.FERTILIZER_REQUIREMENTS.get(crop, {'N': 100, 'P': 50, 'K': 50})
            
            # Calculate deficiency
            n_deficiency = max(0, requirements['N'] - soil_nutrients.get('N', 20))
            p_deficiency = max(0, requirements['P'] - soil_nutrients.get('P', 10))
            k_deficiency = max(0, requirements['K'] - soil_nutrients.get('K', 15))
            
            # Split into application stages
            applications = self._split_fertilizer_applications(crop, {
                'N': n_deficiency,
                'P': p_deficiency,
                'K': k_deficiency
            })
            
            # Schedule over crop cycle
            schedule = self._generate_fertilizer_schedule(
                start_date=datetime.now(),
                applications=applications,
                area=area
            )
            
            return {
                "success": True,
                "crop": crop,
                "current_soil_nutrients": soil_nutrients,
                "required_nutrients": requirements,
                "nutrient_deficiency": {
                    'N': float(n_deficiency),
                    'P': float(p_deficiency),
                    'K': float(k_deficiency)
                },
                "total_fertilizer_needed_kg": float((n_deficiency + p_deficiency + k_deficiency) * area),
                "schedule": schedule,
                "recommendations": self._get_fertilizer_recommendations(crop, soil_nutrients)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def optimize_resources(self, data: Dict) -> Dict:
        """
        Comprehensive resource optimization
        Combines water, fertilizer, and labor scheduling
        """
        crop = data.get('crop_type', 'rice').lower()
        area = data.get('area', 1.0)
        budget = data.get('budget', 10000)  # in currency units
        
        # Get all schedules
        irrigation_data = data.copy()
        irrigation_data['area'] = area
        irrigation_schedule = self.generate_irrigation_schedule(irrigation_data)
        
        fertilizer_data = data.copy()
        fertilizer_data['area'] = area
        fertilizer_schedule = self.generate_fertilizer_schedule(fertilizer_data)
        
        # Cost estimation
        costs = self._estimate_costs(crop, area, irrigation_schedule, fertilizer_schedule)
        
        # Check budget feasibility
        feasibility = "FEASIBLE" if costs['total_cost'] <= budget else "OVER_BUDGET"
        
        return {
            "success": True,
            "crop": crop,
            "area": area,
            "total_budget": budget,
            "estimated_cost": costs,
            "feasibility": feasibility,
            "irrigation_schedule": irrigation_schedule,
            "fertilizer_schedule": fertilizer_schedule,
            "optimization_tips": self._get_optimization_tips(crop, feasibility, budget)
        }
    
    def _get_irrigation_interval(self, soil_type: str, season: str) -> int:
        """Determine irrigation interval based on soil and season"""
        soil_intervals = {
            'sandy': 5,
            'loamy': 7,
            'clay': 10,
            'silty': 8
        }
        
        season_adjustment = {
            'monsoon': -2,
            'summer': 2,
            'winter': 1,
            'spring': 0
        }
        
        base_interval = soil_intervals.get(soil_type.lower(), 7)
        adjustment = season_adjustment.get(season.lower(), 0)
        
        return max(3, base_interval + adjustment)
    
    def _generate_schedule(self, start_date: datetime, interval_days: int, total_days: int, water_per_irrigation: float) -> List[Dict]:
        """Generate irrigation schedule"""
        schedule = []
        current_date = start_date
        
        for i in range(0, total_days, interval_days):
            schedule.append({
                "irrigation_number": len(schedule) + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "days_after_sowing": i,
                "water_required_mm": float(water_per_irrigation)
            })
            current_date += timedelta(days=interval_days)
        
        return schedule[:12]  # Limit to 12 irrigations
    
    def _get_irrigation_recommendations(self, crop: str, season: str, soil_type: str) -> List[str]:
        """Get irrigation recommendations"""
        recommendations = [
            "Water early morning or late evening to reduce evaporation",
            "Use drip or sprinkler irrigation for efficiency",
            "Monitor soil moisture before irrigation",
            "Adjust schedule based on rainfall"
        ]
        
        if soil_type.lower() == 'sandy':
            recommendations.append("Increase irrigation frequency due to high permeability")
        elif soil_type.lower() == 'clay':
            recommendations.append("Be cautious of waterlogging; ensure good drainage")
        
        if season.lower() == 'summer':
            recommendations.append("Increase water supply during hot months")
        
        return recommendations
    
    def _split_fertilizer_applications(self, crop: str, deficiency: Dict) -> Dict:
        """Split fertilizer into application stages"""
        if crop in ['rice', 'wheat', 'corn']:
            return {
                'basal': {
                    'N': deficiency['N'] * 0.3,
                    'P': deficiency['P'],
                    'K': deficiency['K'] * 0.5
                },
                'top_dressing_1': {
                    'N': deficiency['N'] * 0.4
                },
                'top_dressing_2': {
                    'N': deficiency['N'] * 0.3,
                    'K': deficiency['K'] * 0.5
                }
            }
        else:
            return {
                'basal': {
                    'N': deficiency['N'] * 0.5,
                    'P': deficiency['P'],
                    'K': deficiency['K'] * 0.5
                },
                'flowering': {
                    'N': deficiency['N'] * 0.3,
                    'K': deficiency['K'] * 0.3
                },
                'fruit_development': {
                    'N': deficiency['N'] * 0.2,
                    'K': deficiency['K'] * 0.2
                }
            }
    
    def _generate_fertilizer_schedule(self, start_date: datetime, applications: Dict, area: float) -> List[Dict]:
        """Generate fertilizer application schedule"""
        schedule = []
        days_offset = {'basal': 0, 'top_dressing_1': 30, 'top_dressing_2': 60, 'flowering': 45, 'fruit_development': 75}
        
        for stage, amount in applications.items():
            date = start_date + timedelta(days=days_offset.get(stage, 0))
            
            total_amount = sum(v * area for v in amount.values())
            
            schedule.append({
                "stage": stage,
                "date": date.strftime("%Y-%m-%d"),
                "nutrients": {k: float(v * area) for k, v in amount.items()},
                "total_kg": float(total_amount)
            })
        
        return schedule
    
    def _estimate_costs(self, crop: str, area: float, irrigation_schedule: Dict, fertilizer_schedule: Dict) -> Dict:
        """Estimate resource costs"""
        # Cost per unit (approximate, in INR)
        costs = {
            'water': 5 * area * 100,  # 5 INR per 1000 liters
            'fertilizer': 50 * fertilizer_schedule.get('total_fertilizer_needed_kg', 0),
            'labor': 100 * area * 4,  # 4 labor days per hectare
            'pesticides': 30 * area * 10,  # 10 INR per hectare per month
            'equipment': 50 * area  # Equipment maintenance
        }
        
        return {
            'water_cost': float(costs['water']),
            'fertilizer_cost': float(costs['fertilizer']),
            'labor_cost': float(costs['labor']),
            'pesticide_cost': float(costs['pesticides']),
            'equipment_cost': float(costs['equipment']),
            'total_cost': float(sum(costs.values()))
        }
    
    def _get_optimization_tips(self, crop: str, feasibility: str, budget: float) -> List[str]:
        """Get cost optimization tips"""
        tips = []
        
        if feasibility == "OVER_BUDGET":
            tips.extend([
                "Consider deficit irrigation to reduce water costs",
                "Use organic fertilizers for cost savings",
                "Apply fertilizer in fewer stages (combine applications)",
                "Use cooperative labor to reduce costs"
            ])
        else:
            tips.extend([
                "Maintain current resource allocation",
                "Plan for contingencies with buffer budget",
                "Invest in premium quality inputs for better yields"
            ])
        
        tips.append("Monitor market prices for bulk fertilizer purchases")
        
        return tips
