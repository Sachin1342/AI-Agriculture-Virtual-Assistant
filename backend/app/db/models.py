from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CropProduction(Base):
    __tablename__ = "crop_production"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100), index=True)
    year = Column(Integer)
    season = Column(String(50))
    area = Column(Float)  # Area harvested in hectares
    production = Column(Float)  # Production in tonnes
    productivity = Column(Float)  # Yield per hectare
    region = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class CropRecommendation(Base):
    __tablename__ = "crop_recommendation"
    
    id = Column(Integer, primary_key=True, index=True)
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    ph = Column(Float)
    rainfall = Column(Float)
    recommended_crop = Column(String(100))
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class DiseaseDetectionLog(Base):
    __tablename__ = "disease_detection_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String(100))
    disease_detected = Column(String(200))
    confidence = Column(Float)
    treatment = Column(Text)
    prevention = Column(Text)
    image_filename = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class GroundwaterPrediction(Base):
    __tablename__ = "groundwater_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(100))
    rainfall = Column(Float)
    temperature = Column(Float)
    soil_type = Column(String(50))
    previous_level = Column(Float)
    predicted_level = Column(Float)
    confidence = Column(Float)
    risk_level = Column(String(20))  # CRITICAL, HIGH, MEDIUM, LOW
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    user_query = Column(Text)
    intent = Column(String(100))
    bot_response = Column(Text)
    context = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
