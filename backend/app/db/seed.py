import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import CropProduction, CropRecommendation
import os

def seed_crop_production(db: Session):
    """Load crop production data from CSV"""
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "crop production", "crop_production.csv")
        
        if not os.path.exists(csv_path):
            print(f"Warning: Crop production CSV not found at {csv_path}")
            return
        
        df = pd.read_csv(csv_path)
        
        # Check if data already exists
        if db.query(CropProduction).count() > 0:
            print("Crop production data already seeded")
            return
        
        # Prepare data with correct column names
        for idx, row in df.iterrows():
            # Handle different possible column names
            crop_name = row.get('Crop', row.get('crop', 'Unknown'))
            year = int(row.get('Year', row.get('year', 2020)))
            season = str(row.get('Season', row.get('season', 'Unknown')))
            area = float(row.get('Area', row.get('area', 0)))
            production = float(row.get('Production', row.get('production', 0)))
            
            # Calculate productivity if not in CSV
            productivity = float(row.get('Productivity', row.get('productivity', 0)))
            if productivity == 0 and area > 0:
                productivity = production / area if area > 0 else 0
            
            region = str(row.get('State', row.get('state', row.get('Region', 'Unknown'))))
            
            crop_prod = CropProduction(
                crop_name=crop_name,
                year=year,
                season=season,
                area=area,
                production=production,
                productivity=productivity,
                region=region
            )
            db.add(crop_prod)
        
        db.commit()
        print(f"✓ Seeded {len(df)} crop production records")
    except Exception as e:
        print(f"Error seeding crop production: {e}")
        db.rollback()

def seed_crop_recommendation(db: Session):
    """Load crop recommendation data from CSV"""
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "crop recommendation", "Crop_recommendation.csv")
        
        if not os.path.exists(csv_path):
            print(f"Warning: Crop recommendation CSV not found at {csv_path}")
            return
        
        df = pd.read_csv(csv_path)
        
        # Check if data already exists
        if db.query(CropRecommendation).count() > 0:
            print("Crop recommendation data already seeded")
            return
        
        for idx, row in df.iterrows():
            recommendation = CropRecommendation(
                nitrogen=float(row.get('N', row.get('nitrogen', 0))),
                phosphorus=float(row.get('P', row.get('phosphorus', 0))),
                potassium=float(row.get('K', row.get('potassium', 0))),
                temperature=float(row.get('temperature', 0)),
                humidity=float(row.get('humidity', 0)),
                ph=float(row.get('ph', 0)),
                rainfall=float(row.get('rainfall', 0)),
                recommended_crop=str(row.get('label', row.get('crop', 'Unknown'))),
                confidence=1.0
            )
            db.add(recommendation)
        
        db.commit()
        print(f"✓ Seeded {len(df)} crop recommendation records")
    except Exception as e:
        print(f"Error seeding crop recommendation: {e}")
        db.rollback()

def seed_all(db: Session):
    """Seed all database tables"""
    print("Starting database seeding...")
    seed_crop_production(db)
    seed_crop_recommendation(db)
    print("Database seeding complete!")
