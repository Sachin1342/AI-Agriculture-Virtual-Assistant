import numpy as np
import cv2
from PIL import Image
from typing import Tuple, Dict, List
import io

class DiseaseDetectionService:
    """
    Disease detection service for plant leaf images
    Uses CNN model (ResNet50/MobileNetV2)
    """
    
    # Plant disease categories from PlantVillage dataset
    DISEASE_CLASSES = {
        "Apple": ["Apple___Apple scab", "Apple___Black rot", "Apple___Cedar apple rust", "Apple___healthy"],
        "Blueberry": ["Blueberry___healthy", "Blueberry___leaf scorch"],
        "Cherry": ["Cherry_(including_sour)___Powdery mildew", "Cherry_(including_sour)___healthy"],
        "Corn": ["Corn_(maize)___Cercospora leaf spot Gray leaf spot", "Corn_(maize)___Common rust", 
                 "Corn_(maize)___Northern Leaf Blight", "Corn_(maize)___healthy"],
        "Grape": ["Grape___Black rot", "Grape___Esca (Black Measles)", "Grape___Leaf blight (Isariopsis Leaf Spot)",
                  "Grape___healthy"],
        "Orange": ["Orange___Haunglongbing (Citrus greening)"],
        "Peach": ["Peach___Bacterial spot", "Peach___healthy"],
        "Pepper": ["Pepper,_bell___Bacterial spot", "Pepper,_bell___healthy"],
        "Potato": ["Potato___Early blight", "Potato___Late blight", "Potato___healthy"],
        "Raspberry": ["Raspberry___healthy"],
        "Rice": ["Rice___Brown spot", "Rice___Leaf blast", "Rice___Leaf scald"],
        "Soybean": ["Soybean___healthy", "Soybean___Septoria brown spot"],
        "Squash": ["Squash___Powdery mildew"],
        "Strawberry": ["Strawberry___healthy", "Strawberry___Leaf scorch"],
        "Tomato": ["Tomato___Bacterial spot", "Tomato___Early blight", "Tomato___Late blight",
                   "Tomato___Leaf Mold", "Tomato___Septoria leaf spot", "Tomato___Spider mites",
                   "Tomato___Target Spot", "Tomato___Tomato Yellow Leaf Curl Virus", "Tomato___Tomato mosaic virus",
                   "Tomato___healthy"],
        "Wheat": ["Wheat___Brown rust", "Wheat___Healthy", "Wheat___Septoria"]
    }
    
    # Treatment suggestions for diseases
    TREATMENT_SUGGESTIONS = {
        "apple scab": ["Use fungicide spray", "Remove infected leaves", "Improve air circulation", "Prune affected branches"],
        "black rot": ["Apply copper-based fungicide", "Remove infected fruit", "Burn infected materials", "Improve drainage"],
        "early blight": ["Remove lower leaves", "Apply fungicide", "Increase air circulation", "Avoid overhead watering"],
        "late blight": ["Apply copper or sulfur fungicide", "Remove infected tissue", "Improve drainage", "Crop rotation"],
        "leaf mold": ["Remove affected leaves", "Reduce humidity", "Apply fungicide", "Improve ventilation"],
        "septoria": ["Apply fungicide", "Remove infected leaves", "Avoid overhead irrigation", "Sanitize tools"],
        "powdery mildew": ["Apply sulfur dust", "Improve air circulation", "Remove infected leaves", "Use fungicide"],
        "leaf scorch": ["Prune affected branches", "Improve irrigation", "Remove infected leaves", "Apply fungicide"],
        "healthy": ["Maintain regular care", "Monitor for diseases", "Continue watering schedule", "Apply preventive fungicide"]
    }
    
    def __init__(self):
        self.model = None
        self.image_size = (224, 224)  # Standard for MobileNetV2/ResNet
    
    def load_model(self, model_path: str):
        """Load pre-trained disease detection model"""
        try:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(model_path)
            return True
        except FileNotFoundError:
            print(f"Model not found at {model_path}. Using mock predictor.")
            return False
        except Exception as e:
            print(f"Error loading model: {e}. Using mock predictor.")
            return False
    
    def preprocess_image(self, image_data: bytes) -> np.ndarray:
        """Convert image bytes to preprocessed numpy array"""
        try:
            # Load image from bytes
            img = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Resize to model input size
            img_array = np.array(img.resize(self.image_size))
            
            # Normalize to [0, 1]
            img_array = img_array.astype('float32') / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def predict(self, image_data: bytes) -> Dict:
        """
        Predict disease from image
        Returns: disease name, confidence, treatment suggestions
        """
        if self.model is None:
            return {
                "success": False,
                "error": "Model not loaded",
                "disease": "Unknown",
                "confidence": 0.0
            }
        
        try:
            # Preprocess
            img_array = self.preprocess_image(image_data)
            if img_array is None:
                return {"success": False, "error": "Failed to process image"}
            
            # Predict
            predictions = self.model.predict(img_array, verbose=0)
            confidence = float(np.max(predictions))
            class_idx = np.argmax(predictions[0])
            
            # Get disease name from class index
            all_diseases = [d for diseases in self.DISEASE_CLASSES.values() for d in diseases]
            if class_idx < len(all_diseases):
                disease_name = all_diseases[class_idx]
            else:
                disease_name = "Unknown disease"
            
            # Extract disease keyword for treatment
            disease_keyword = disease_name.lower().split("___")[-1] if "___" in disease_name else disease_name.lower()
            
            # Get treatment suggestions
            treatments = self._get_treatments(disease_keyword)
            
            return {
                "success": True,
                "disease": disease_name,
                "confidence": confidence,
                "confidence_percentage": f"{confidence * 100:.2f}%",
                "treatments": treatments,
                "prevention": self._get_prevention(disease_keyword)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "disease": "Unknown"
            }
    
    def _get_treatments(self, disease_keyword: str) -> List[str]:
        """Get treatment suggestions for disease"""
        disease_keyword = disease_keyword.lower()
        
        for key, suggestions in self.TREATMENT_SUGGESTIONS.items():
            if key in disease_keyword or disease_keyword in key:
                return suggestions
        
        return [
            "Consult a local agricultural expert",
            "Isolate affected plant",
            "Monitor other plants",
            "Maintain proper hygiene"
        ]
    
    def _get_prevention(self, disease_keyword: str) -> List[str]:
        """Get prevention measures"""
        return [
            "Maintain good plant hygiene",
            "Ensure proper air circulation",
            "Water at soil level, not leaves",
            "Remove infected leaves promptly",
            "Rotate crops annually",
            "Use disease-resistant varieties"
        ]
    
    def batch_predict(self, images: List[bytes]) -> List[Dict]:
        """Predict for multiple images"""
        results = []
        for image_data in images:
            result = self.predict(image_data)
            results.append(result)
        return results


class MockDiseasePredictorForTesting:
    """Mock predictor for testing without trained model"""
    
    MOCK_DISEASES = [
        {"disease": "Early Blight", "confidence": 0.94},
        {"disease": "Late Blight", "confidence": 0.89},
        {"disease": "Leaf Spot", "confidence": 0.85},
        {"disease": "Powdery Mildew", "confidence": 0.91},
        {"disease": "Healthy", "confidence": 0.98}
    ]
    
    def predict(self, image_data: bytes = None) -> Dict:
        """Return mock prediction"""
        import random
        mock = random.choice(self.MOCK_DISEASES)
        return {
            "success": True,
            "disease": mock["disease"],
            "confidence": mock["confidence"],
            "confidence_percentage": f"{mock['confidence'] * 100:.2f}%",
            "treatments": [
                "Apply organic fungicide",
                "Remove infected leaves",
                "Improve air circulation",
                "Water at soil level"
            ],
            "prevention": [
                "Maintain plant hygiene",
                "Ensure proper spacing",
                "Avoid overhead watering",
                "Rotate crops"
            ]
        }
