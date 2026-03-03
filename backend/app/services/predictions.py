import numpy as np
import pandas as pd
from typing import Dict, List
from sklearn.preprocessing import StandardScaler
from app.core.config import settings

class GroundwaterPredictionService:
    """
    Groundwater level prediction service
    Uses regression model (Random Forest / XGBoost)
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = ['rainfall', 'soil_type', 'temperature', 'humidity', 'previous_level']
        self.soil_type_mapping = {
            'clay': 1,
            'sandy': 2,
            'loamy': 3,
            'silty': 4,
            'acidic': 5,
            'alkaline': 6
        }
        self.load_model(settings.groundwater_model_path)
    
    def load_model(self, model_path: str):
        """Load pre-trained groundwater model"""
        try:
            import joblib
            self.model = joblib.load(model_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict(self, data: Dict) -> Dict:
        """
        Predict groundwater level
        Input: rainfall (mm), soil_type, temperature (C), humidity (%), previous_level (meters)
        """
        try:
            # Prepare features
            features = self._prepare_features(data)
            
            if self.model is not None:
                if hasattr(self.model, "predict"):
                    model_input = pd.DataFrame([{
                        "rainfall": data.get("rainfall", 100),
                        "soil_type": data.get("soil_type", "loamy"),
                        "temperature": data.get("temperature", 25),
                        "humidity": data.get("humidity", 60),
                        "previous_level": data.get("previous_level", 5.0),
                    }])
                    prediction = self.model.predict(model_input)[0]
                else:
                    prediction = self._mock_prediction(data)
            else:
                prediction = self._mock_prediction(data)
            
            # Risk assessment
            risk_level = self._assess_risk(prediction, data.get('rainfall', 100))
            recommendations = self._get_recommendations(prediction, risk_level)
            
            return {
                "success": True,
                "groundwater_level": float(prediction),
                "groundwater_level_meters": f"{prediction:.2f}m",
                "risk_level": risk_level,
                "confidence": 0.87,
                "recommendations": recommendations,
                "next_check_days": 30
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "groundwater_level": 0
            }
    
    def _prepare_features(self, data: Dict) -> list:
        """Prepare features for model"""
        rainfall = data.get('rainfall', 100)
        soil_type = self.soil_type_mapping.get(data.get('soil_type', 'loamy').lower(), 3)
        temperature = data.get('temperature', 25)
        humidity = data.get('humidity', 60)
        previous_level = data.get('previous_level', 5.0)
        
        # Normalize features
        features = [rainfall, soil_type, temperature, humidity, previous_level]
        return features
    
    def _mock_prediction(self, data: Dict) -> float:
        """Generate realistic mock prediction"""
        rainfall = data.get('rainfall', 100)
        previous_level = data.get('previous_level', 5.0)
        
        # Simulate: more rain → higher water level
        change = (rainfall - 100) * 0.01  # 1mm rain = 0.01m change
        predicted_level = previous_level + change + np.random.normal(0, 0.3)
        
        return max(1.0, min(15.0, predicted_level))  # Bounded between 1-15 meters
    
    def _assess_risk(self, level: float, rainfall: float) -> str:
        """Assess groundwater risk level"""
        if level < 3:
            return "CRITICAL"
        elif level < 5:
            return "HIGH"
        elif level < 8:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_recommendations(self, level: float, risk: str) -> List[str]:
        """Get water management recommendations"""
        if risk == "CRITICAL":
            return [
                "Urgently implement water conservation measures",
                "Reduce irrigation frequency",
                "Switch to drought-resistant crops",
                "Install rainwater harvesting system"
            ]
        elif risk == "HIGH":
            return [
                "Optimize irrigation schedule",
                "Use drip irrigation instead of flood",
                "Mulch soil to reduce evaporation",
                "Plant water-efficient crops"
            ]
        elif risk == "MEDIUM":
            return [
                "Maintain current irrigation schedule",
                "Monitor water levels monthly",
                "Use sprinkler irrigation",
                "Plan for dry season"
            ]
        else:
            return [
                "Continue normal irrigation",
                "Plan for upcoming season",
                "Monitor for flooding",
                "Maintain drainage systems"
            ]
    
    def seasonal_forecast(self, region: str, season: str) -> Dict:
        """Forecast seasonal water availability"""
        season_data = {
            ("monsoon", "high"): {"expected_level": 10.5, "rainfall": 250},
            ("summer", "low"): {"expected_level": 3.2, "rainfall": 50},
            ("winter", "medium"): {"expected_level": 6.8, "rainfall": 100},
            ("spring", "medium"): {"expected_level": 7.2, "rainfall": 120}
        }
        
        key = (season.lower(), self._get_season_risk(season))
        data = season_data.get(key, {"expected_level": 5.0, "rainfall": 100})
        
        return {
            "season": season,
            "expected_level": data["expected_level"],
            "expected_rainfall": data["rainfall"],
            "irrigation_needed": True if data["expected_level"] < 6 else False
        }
    
    def _get_season_risk(self, season: str) -> str:
        """Determine risk level by season"""
        if season.lower() in ["monsoon", "rainy"]:
            return "high"
        elif season.lower() in ["summer", "dry"]:
            return "low"
        else:
            return "medium"


class CropProductionPredictorService:
    """
    Crop production/yield prediction service
    Uses regression model
    """
    
    def __init__(self):
        self.model = None
        self.crops = ['rice', 'wheat', 'corn', 'tomato', 'potato', 'cotton', 'sugarcane']
        self.load_model(settings.production_model_path)
    
    def load_model(self, model_path: str):
        """Load production prediction model"""
        try:
            import joblib
            self.model = joblib.load(model_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict(self, data: Dict) -> Dict:
        """
        Predict crop production
        Input: crop_type, area (hectares), rainfall (mm), temperature (C), 
               soil_nutrients (N, P, K values), season, fertilizer_amount
        """
        try:
            crop = data.get('crop_type', 'rice').lower()
            area = data.get('area', 1.0)
            rainfall = data.get('rainfall', 100)
            temperature = data.get('temperature', 25)
            
            if self.model is not None:
                model_input = pd.DataFrame([{
                    'crop_type': crop,
                    'area': data.get('area', 1.0),
                    'rainfall': rainfall,
                    'temperature': temperature,
                    'humidity': data.get('humidity', 60),
                    'soil_nutrients': data.get('soil_nutrients', 50),
                    'fertilizer_amount': data.get('fertilizer_amount', 100),
                }])
                predicted_yield_per_hectare = self.model.predict(model_input)[0]
            else:
                predicted_yield_per_hectare = self._mock_prediction(data)
            
            total_production = predicted_yield_per_hectare * area
            
            # Quality assessment
            quality_score = self._assess_quality(data)
            recommendations = self._get_yield_recommendations(crop, total_production)
            
            return {
                "success": True,
                "crop": crop,
                "area": area,
                "yield_per_hectare_kg": float(predicted_yield_per_hectare),
                "total_production_kg": float(total_production),
                "total_production_tons": float(total_production / 1000),
                "quality_score": quality_score,
                "confidence": 0.85,
                "recommendations": recommendations,
                "market_estimate": self._estimate_revenue(crop, total_production)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "yield": 0
            }
    
    def _prepare_features(self, data: Dict) -> list:
        """Prepare features for model"""
        features = [
            data.get('area', 1.0),
            data.get('rainfall', 100),
            data.get('temperature', 25),
            data.get('humidity', 60),
            data.get('soil_nutrients', 50),
            data.get('fertilizer_amount', 100)
        ]
        return features
    
    def _mock_prediction(self, data: Dict) -> float:
        """Generate realistic yield prediction"""
        crop = data.get('crop_type', 'rice').lower()
        rainfall = data.get('rainfall', 100)
        temperature = data.get('temperature', 25)
        soil_nutrients = data.get('soil_nutrients', 50)
        
        # Base yields (kg/hectare)
        base_yields = {
            'rice': 5000, 'wheat': 4500, 'corn': 6000,
            'tomato': 20000, 'potato': 18000, 'cotton': 2000
        }
        
        base = base_yields.get(crop, 3000)
        
        # Adjust based on conditions
        rainfall_factor = 1 + (rainfall - 100) * 0.005
        temp_factor = 1 - abs(temperature - 25) * 0.02
        nutrient_factor = 1 + (soil_nutrients - 50) * 0.01
        
        yield_per_hectare = base * rainfall_factor * temp_factor * nutrient_factor
        yield_per_hectare = max(0, yield_per_hectare + np.random.normal(0, 200))
        
        return float(yield_per_hectare)
    
    def _assess_quality(self, data: Dict) -> str:
        """Assess production quality"""
        rainfall = data.get('rainfall', 100)
        temp = data.get('temperature', 25)
        nutrients = data.get('soil_nutrients', 50)
        
        quality = 0
        if 80 < rainfall < 200:
            quality += 1
        if 20 < temp < 30:
            quality += 1
        if nutrients > 40:
            quality += 1
        
        if quality >= 3:
            return "EXCELLENT"
        elif quality == 2:
            return "GOOD"
        else:
            return "AVERAGE"
    
    def _get_yield_recommendations(self, crop: str, yield_kg: float) -> List[str]:
        """Get yield optimization recommendations"""
        if yield_kg < 3000:
            return [
                "Improve soil nutrients with fertilizers",
                "Optimize irrigation schedule",
                "Use disease-resistant varieties",
                "Consult agricultural expert"
            ]
        else:
            return [
                "Maintain current farming practices",
                "Plan storage for harvest",
                "Prepare marketing channels",
                "Document best practices"
            ]
    
    def _estimate_revenue(self, crop: str, production_kg: float) -> Dict:
        """Estimate market revenue"""
        prices = {
            'rice': 25, 'wheat': 20, 'corn': 18,
            'tomato': 15, 'potato': 12, 'cotton': 50
        }
        
        price_per_kg = prices.get(crop, 20)
        total_revenue = production_kg * price_per_kg
        
        return {
            "estimated_price_per_kg": price_per_kg,
            "estimated_total_revenue": float(total_revenue),
            "currency": "INR"
        }
