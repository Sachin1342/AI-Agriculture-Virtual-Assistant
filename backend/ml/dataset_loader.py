import pandas as pd
import numpy as np
from pathlib import Path
import os

class DatasetLoader:
    """
    Load datasets from the available data folders
    """
    
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / '..' / '..' / 'Crop predictor'
    
    @staticmethod
    def load_climate_data():
        """Load climate dataset"""
        try:
            train_data = pd.read_csv(str(DatasetLoader.DATA_DIR / 'climate' / 'DailyDelhiClimateTrain.csv'))
            test_data = pd.read_csv(str(DatasetLoader.DATA_DIR / 'climate' / 'DailyDelhiClimateTest.csv'))
            
            return {
                'train': train_data,
                'test': test_data,
                'shape': train_data.shape
            }
        except Exception as e:
            print(f"Error loading climate data: {e}")
            return None
    
    @staticmethod
    def load_crop_production_data():
        """Load crop production dataset"""
        try:
            data = pd.read_csv(str(DatasetLoader.DATA_DIR / 'crop production' / 'crop_production.csv'))
            return {
                'data': data,
                'shape': data.shape,
                'columns': list(data.columns)
            }
        except Exception as e:
            print(f"Error loading crop production data: {e}")
            return None
    
    @staticmethod
    def load_crop_recommendation_data():
        """Load crop recommendation dataset"""
        try:
            data = pd.read_csv(str(DatasetLoader.DATA_DIR / 'crop recommendation' / 'Crop_recommendation.csv'))
            return {
                'data': data,
                'shape': data.shape,
                'crops': data['label'].unique().tolist() if 'label' in data.columns else []
            }
        except Exception as e:
            print(f"Error loading crop recommendation data: {e}")
            return None
    
    @staticmethod
    def get_disease_image_paths():
        """Get paths to disease images"""
        disease_dir = DatasetLoader.DATA_DIR / 'plant diseases' / 'New Plant Diseases Dataset(Augmented)'
        
        if disease_dir.exists():
            images = []
            for root, dirs, files in os.walk(disease_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        images.append(os.path.join(root, file))
            
            return {
                'count': len(images),
                'sample_paths': images[:10] if images else []
            }
        return None
    
    @staticmethod
    def print_dataset_info():
        """Print information about loaded datasets"""
        print("=" * 60)
        print("DATASET INFORMATION SUMMARY")
        print("=" * 60)
        
        # Climate Data
        climate = DatasetLoader.load_climate_data()
        if climate:
            print(f"\n✓ Climate Data: {climate['shape']}")
        
        # Crop Production
        production = DatasetLoader.load_crop_production_data()
        if production:
            print(f"✓ Crop Production: {production['shape']}")
            print(f"  Columns: {production['columns']}")
        
        # Crop Recommendation
        recommendation = DatasetLoader.load_crop_recommendation_data()
        if recommendation:
            print(f"✓ Crop Recommendation: {recommendation['shape']}")
            print(f"  Available crops: {recommendation['crops']}")
        
        # Disease Images
        diseases = DatasetLoader.get_disease_image_paths()
        if diseases:
            print(f"✓ Disease Images: {diseases['count']} images found")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    # Test dataset loading
    DatasetLoader.print_dataset_info()
    
    # Load and explore
    climate_data = DatasetLoader.load_climate_data()
    if climate_data:
        print("\nClimate Data Sample:")
        print(climate_data['train'].head())
