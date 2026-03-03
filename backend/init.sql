-- PostgreSQL initialization script for Crop Predictor Database

-- Create main database (will be created by POSTGRES_DB env var, so we just initialize it)

-- Create tables in cropdb
CREATE TABLE IF NOT EXISTS crop_production (
    id SERIAL PRIMARY KEY,
    crop_name VARCHAR(100) NOT NULL,
    year INTEGER,
    season VARCHAR(50),
    area FLOAT,
    production FLOAT,
    productivity FLOAT,
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS crop_recommendation (
    id SERIAL PRIMARY KEY,
    nitrogen FLOAT,
    phosphorus FLOAT,
    potassium FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    ph FLOAT,
    rainfall FLOAT,
    recommended_crop VARCHAR(100),
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS disease_detection_logs (
    id SERIAL PRIMARY KEY,
    crop_type VARCHAR(100),
    disease_detected VARCHAR(200),
    confidence FLOAT,
    treatment TEXT,
    prevention TEXT,
    image_filename VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS groundwater_predictions (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100),
    rainfall FLOAT,
    temperature FLOAT,
    soil_type VARCHAR(50),
    previous_level FLOAT,
    predicted_level FLOAT,
    confidence FLOAT,
    risk_level VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE,
    user_query TEXT,
    intent VARCHAR(100),
    bot_response TEXT,
    context JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(100) UNIQUE,
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_crop_production_crop_name ON crop_production(crop_name);
CREATE INDEX IF NOT EXISTS idx_crop_production_year ON crop_production(year);
CREATE INDEX IF NOT EXISTS idx_disease_detection_crops_type ON disease_detection_logs(crop_type);
CREATE INDEX IF NOT EXISTS idx_groundwater_location ON groundwater_predictions(location);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_id ON chat_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "user";

