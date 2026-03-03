import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import PredictionHistory
from app.services.predictions import (
    CropProductionPredictorService,
    GroundwaterPredictionService,
)
from app.services.resource_management import ResourceManagementService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/predictions", tags=["predictions"])

groundwater_service = GroundwaterPredictionService()
production_service = CropProductionPredictorService()
resource_service = ResourceManagementService()


class GroundwaterRequest(BaseModel):
    rainfall: float = Field(..., ge=0)
    soil_type: str
    temperature: float = Field(..., ge=-20, le=60)
    humidity: float = Field(..., ge=0, le=100)
    previous_level: float = Field(default=5.0, ge=0)


class GroundwaterResponse(BaseModel):
    success: bool
    groundwater_level: float
    risk_level: str
    recommendations: List[str]


class ProductionRequest(BaseModel):
    crop_type: str
    area: float = Field(..., gt=0)
    rainfall: float = Field(..., ge=0)
    temperature: float = Field(..., ge=-20, le=60)
    humidity: float = Field(default=60, ge=0, le=100)
    soil_nutrients: float = Field(default=50, ge=0)
    season: str = "monsoon"
    fertilizer_amount: float = Field(default=100, ge=0)


class ProductionResponse(BaseModel):
    success: bool
    crop: str
    yield_per_hectare_kg: float
    total_production_kg: float
    total_production_tons: float
    quality_score: str
    confidence: float


class IrrigationRequest(BaseModel):
    crop_type: str
    area: float = Field(..., gt=0)
    season: str
    rainfall: float = Field(default=100, ge=0)
    soil_type: str = "loamy"


class FertilizerRequest(BaseModel):
    crop_type: str
    area: float = Field(..., gt=0)
    current_soil_nutrients: Dict[str, float] = {"N": 20, "P": 10, "K": 15}


class ResourceOptimizationRequest(BaseModel):
    crop_type: str
    area: float = Field(..., gt=0)
    budget: float = Field(default=10000, gt=0)
    season: str = "monsoon"
    rainfall: float = Field(default=100, ge=0)
    soil_type: str = "loamy"
    temperature: float = Field(default=25, ge=-20, le=60)
    humidity: float = Field(default=60, ge=0, le=100)
    current_soil_nutrients: Dict[str, float] = {"N": 20, "P": 10, "K": 15}


def _store_prediction(db: Session, prediction_type: str, payload_in: Dict, payload_out: Dict) -> None:
    record = PredictionHistory(
        prediction_type=prediction_type,
        input_payload=payload_in,
        output_payload=payload_out,
    )
    db.add(record)
    db.commit()


@router.post("/groundwater", response_model=GroundwaterResponse)
async def predict_groundwater(request: GroundwaterRequest, db: Session = Depends(get_db)):
    try:
        payload = request.model_dump()
        result = groundwater_service.predict(payload)
        _store_prediction(db, "groundwater", payload, result)
        return GroundwaterResponse(
            success=result["success"],
            groundwater_level=result.get("groundwater_level", 0),
            risk_level=result.get("risk_level", "UNKNOWN"),
            recommendations=result.get("recommendations", []),
        )
    except Exception as exc:
        logger.exception("Groundwater prediction failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/production", response_model=ProductionResponse)
async def predict_production(request: ProductionRequest, db: Session = Depends(get_db)):
    try:
        payload = request.model_dump()
        result = production_service.predict(payload)
        _store_prediction(db, "production", payload, result)
        return ProductionResponse(
            success=result["success"],
            crop=result.get("crop", ""),
            yield_per_hectare_kg=result.get("yield_per_hectare_kg", 0),
            total_production_kg=result.get("total_production_kg", 0),
            total_production_tons=result.get("total_production_tons", 0),
            quality_score=result.get("quality_score", "UNKNOWN"),
            confidence=result.get("confidence", 0.8),
        )
    except Exception as exc:
        logger.exception("Production prediction failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/irrigation-schedule")
async def get_irrigation_schedule(request: IrrigationRequest, db: Session = Depends(get_db)):
    try:
        payload = request.model_dump()
        result = resource_service.generate_irrigation_schedule(payload)
        _store_prediction(db, "irrigation", payload, result)
        return result
    except Exception as exc:
        logger.exception("Irrigation schedule generation failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/fertilizer-schedule")
async def get_fertilizer_schedule(request: FertilizerRequest, db: Session = Depends(get_db)):
    try:
        payload = request.model_dump()
        result = resource_service.generate_fertilizer_schedule(payload)
        _store_prediction(db, "fertilizer", payload, result)
        return result
    except Exception as exc:
        logger.exception("Fertilizer schedule generation failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/optimize-resources")
async def optimize_resources(request: ResourceOptimizationRequest, db: Session = Depends(get_db)):
    try:
        payload = request.model_dump()
        result = resource_service.optimize_resources(payload)
        _store_prediction(db, "resource_optimization", payload, result)
        return result
    except Exception as exc:
        logger.exception("Resource optimization failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/history")
async def get_prediction_history(db: Session = Depends(get_db), limit: int = 20):
    rows = (
        db.query(PredictionHistory)
        .order_by(PredictionHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "history": [
            {
                "id": row.id,
                "prediction_type": row.prediction_type,
                "input": row.input_payload,
                "output": row.output_payload,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    }
