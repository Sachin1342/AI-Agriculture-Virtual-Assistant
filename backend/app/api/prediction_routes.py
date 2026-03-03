from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.predictions import GroundwaterPredictionService, CropProductionPredictorService
from app.services.resource_management import ResourceManagementService

router = APIRouter(prefix="/api/v1/predictions", tags=["predictions"])

# Initialize services
groundwater_service = GroundwaterPredictionService()
production_service = CropProductionPredictorService()
resource_service = ResourceManagementService()

# Pydantic models
class GroundwaterRequest(BaseModel):
    rainfall: float
    soil_type: str
    temperature: float
    humidity: float
    previous_level: float = 5.0
    region: str = "Unknown"

class GroundwaterResponse(BaseModel):
    success: bool
    groundwater_level: float
    risk_level: str
    recommendations: list

@router.post("/groundwater", response_model=GroundwaterResponse)
async def predict_groundwater(request: GroundwaterRequest):
    """Predict groundwater level"""
    try:
        data = {
            'rainfall': request.rainfall,
            'soil_type': request.soil_type,
            'temperature': request.temperature,
            'humidity': request.humidity,
            'previous_level': request.previous_level
        }
        result = groundwater_service.predict(data)
        
        return GroundwaterResponse(
            success=result['success'],
            groundwater_level=result.get('groundwater_level', 0),
            risk_level=result.get('risk_level', 'UNKNOWN'),
            recommendations=result.get('recommendations', [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ProductionRequest(BaseModel):
    crop_type: str
    area: float
    rainfall: float
    temperature: float
    humidity: float = 60
    soil_nutrients: float = 50
    season: str = "monsoon"
    fertilizer_amount: float = 100

class ProductionResponse(BaseModel):
    success: bool
    crop: str
    yield_per_hectare_kg: float
    total_production_kg: float
    total_production_tons: float
    quality_score: str
    confidence: float

@router.post("/production", response_model=ProductionResponse)
async def predict_production(request: ProductionRequest):
    """Predict crop production/yield"""
    try:
        data = {
            'crop_type': request.crop_type,
            'area': request.area,
            'rainfall': request.rainfall,
            'temperature': request.temperature,
            'humidity': request.humidity,
            'soil_nutrients': request.soil_nutrients,
            'season': request.season,
            'fertilizer_amount': request.fertilizer_amount
        }
        result = production_service.predict(data)
        
        return ProductionResponse(
            success=result['success'],
            crop=result.get('crop', ''),
            yield_per_hectare_kg=result.get('yield_per_hectare_kg', 0),
            total_production_kg=result.get('total_production_kg', 0),
            total_production_tons=result.get('total_production_tons', 0),
            quality_score=result.get('quality_score', 'UNKNOWN'),
            confidence=result.get('confidence', 0.8)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class IrrigationRequest(BaseModel):
    crop_type: str
    area: float
    season: str
    rainfall: float = 100
    soil_type: str = "loamy"

@router.post("/irrigation-schedule")
async def get_irrigation_schedule(request: IrrigationRequest):
    """Get optimized irrigation schedule"""
    try:
        data = {
            'crop_type': request.crop_type,
            'area': request.area,
            'season': request.season,
            'rainfall': request.rainfall,
            'soil_type': request.soil_type
        }
        result = resource_service.generate_irrigation_schedule(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FertilizerRequest(BaseModel):
    crop_type: str
    area: float
    current_soil_nutrients: dict = {"N": 20, "P": 10, "K": 15}

@router.post("/fertilizer-schedule")
async def get_fertilizer_schedule(request: FertilizerRequest):
    """Get optimized fertilizer schedule"""
    try:
        data = {
            'crop_type': request.crop_type,
            'area': request.area,
            'current_soil_nutrients': request.current_soil_nutrients
        }
        result = resource_service.generate_fertilizer_schedule(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ResourceOptimizationRequest(BaseModel):
    crop_type: str
    area: float
    budget: float = 10000
    season: str = "monsoon"
    rainfall: float = 100
    soil_type: str = "loamy"
    temperature: float = 25
    humidity: float = 60
    current_soil_nutrients: dict = {"N": 20, "P": 10, "K": 15}

@router.post("/optimize-resources")
async def optimize_resources(request: ResourceOptimizationRequest):
    """Get comprehensive resource optimization plan"""
    try:
        data = {
            'crop_type': request.crop_type,
            'area': request.area,
            'budget': request.budget,
            'season': request.season,
            'rainfall': request.rainfall,
            'soil_type': request.soil_type,
            'temperature': request.temperature,
            'humidity': request.humidity,
            'current_soil_nutrients': request.current_soil_nutrients
        }
        result = resource_service.optimize_resources(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
