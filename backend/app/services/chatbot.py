import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Intent:
    name: str
    confidence: float
    parameters: Dict

class IntentDetector:
    """
    Intent detection system using TF-IDF + Cosine Similarity
    Production deployments should use transformer-based models (BERT, DistilBERT)
    """
    
    INTENTS = {
        "disease_detection": {
            "keywords": [
                "spots on leaves", "leaf disease", "disease detection",
                "plant infection", "leaf color", "disease name",
                "what disease", "identify disease", "disease symptoms",
                "plant problem", "leaf problem", "leaves spots",
                "brown spots", "yellow leaves", "leaf damage"
            ],
            "slots": ["crop_type", "symptoms"],
            "action": "disease_detection"
        },
        "groundwater_prediction": {
            "keywords": [
                "groundwater", "water level", "water availability",
                "rainfall", "water prediction", "aquifer",
                "well water", "underground water", "water supply",
                "will groundwater", "water enough", "water season"
            ],
            "slots": ["region", "season"],
            "action": "groundwater_prediction"
        },
        "crop_recommendation": {
            "keywords": [
                "crop recommendation", "what crop", "which crop",
                "suitable crop", "best crop", "crop to grow",
                "crop choice", "crop selection", "farming decision",
                "harvest", "growing season", "crop for soil"
            ],
            "slots": ["soil_type", "rainfall", "temperature"],
            "action": "crop_recommendation"
        },
        "production_forecast": {
            "keywords": [
                "production forecast", "yield prediction", "crop yield",
                "expected harvest", "output prediction", "production",
                "yield estimate", "production estimate", "harvest yield"
            ],
            "slots": ["crop_type", "area", "soil_nutrients"],
            "action": "production_forecast"
        },
        "resource_management": {
            "keywords": [
                "irrigation schedule", "fertilizer", "water optimization",
                "resource management", "water usage", "fertilizer amount",
                "irrigation timing", "resource suggestion", "farming schedule"
            ],
            "slots": ["crop_type", "area", "water_availability"],
            "action": "resource_management"
        },
        "general_chat": {
            "keywords": [
                "hello", "hi", "how are you", "help", "information",
                "thanks", "thank you", "okay", "bye", "goodbye"
            ],
            "slots": [],
            "action": "general_chat"
        }
    }
    
    RESPONSES = {
        "disease_detection": {
            "clarify": "I detected you want disease identification. Please upload a leaf image or describe the symptoms (e.g., 'brown spots on tomato leaves').",
            "help": "I can help identify plant diseases. Share an image or describe symptoms including crop type.",
            "error": "Unable to identify disease. Please provide clearer image or more detailed symptoms."
        },
        "groundwater_prediction": {
            "clarify": "You're asking about groundwater. Please share your region and expected rainfall patterns.",
            "help": "I can predict groundwater levels based on rainfall, soil type, and historical data.",
            "error": "Need more data. Please provide location and recent rainfall information."
        },
        "crop_recommendation": {
            "clarify": "I can recommend suitable crops. Tell me your soil type, rainfall, and temperature patterns.",
            "help": "Based on your soil and climate, I'll suggest the best crops to grow.",
            "error": "Please provide soil type, rainfall amount, and temperature range."
        },
        "production_forecast": {
            "clarify": "You want production forecast. Share crop type, area, and soil nutrients.",
            "help": "I can predict your crop yield based on conditions and historical data.",
            "error": "Need crop type, farming area, and nutrient levels for prediction."
        },
        "resource_management": {
            "clarify": "I can create irrigation and fertilizer schedules for you.",
            "help": "I'll optimize your water and fertilizer usage for maximum yield.",
            "error": "Please provide crop type and available resources."
        },
        "general_chat": {
            "greeting": "Hello! I'm your AI agricultural assistant. I can help with disease detection, groundwater prediction, crop recommendations, yield forecasting, and resource management. What can I help you with?",
            "help": "I can assist with:\n1. Disease detection from leaf images\n2. Groundwater level prediction\n3. Crop recommendations\n4. Yield forecasting\n5. Irrigation & fertilizer schedules",
            "goodbye": "Thank you for using Crop Assistant! Happy farming! 🌾"
        }
    }
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self._prepare_vectorizer()
    
    def _prepare_vectorizer(self):
        """Prepare TF-IDF vectorizer with all keywords"""
        all_keywords = []
        for intent_data in self.INTENTS.values():
            all_keywords.extend(intent_data["keywords"])
        self.vectorizer.fit(all_keywords)
    
    def detect(self, user_input: str) -> Intent:
        """
        Detect intent from user input using TF-IDF similarity
        """
        user_input_lower = user_input.lower()
        
        # Quick check for specific patterns
        if re.search(r'(upload|image|photo|picture|leaf)', user_input_lower):
            if re.search(r'(disease|spot|problem|symptom)', user_input_lower):
                return Intent("disease_detection", 0.95, {"mode": "image"})
        
        best_intent = "general_chat"
        best_score = 0.0
        best_slots = {}
        
        # Calculate similarity for each intent
        for intent_name, intent_config in self.INTENTS.items():
            keywords = intent_config["keywords"]
            
            # Calculate average similarity
            scores = []
            for keyword in keywords:
                similarity = self._similarity(user_input_lower, keyword)
                scores.append(similarity)
            
            avg_score = np.mean(scores) if scores else 0
            
            if avg_score > best_score:
                best_score = avg_score
                best_intent = intent_name
                best_slots = self._extract_slots(user_input, intent_config["slots"])
        
        # Confidence threshold
        confidence = min(best_score, 0.99) if best_score > 0.3 else 0.5
        
        return Intent(best_intent, confidence, best_slots)
    
    def _similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""
        try:
            vec1 = self.vectorizer.transform([text1])
            vec2 = self.vectorizer.transform([text2])
            return float(cosine_similarity(vec1, vec2)[0][0])
        except:
            return 0.0
    
    def _extract_slots(self, text: str, slots: List[str]) -> Dict:
        """Extract slot values from text"""
        extracted = {}
        
        # Simple pattern-based extraction
        if "crop" in slots or "crop_type" in slots:
            crops = ["tomato", "rice", "wheat", "corn", "potato", "cotton", "maize", "barley"]
            for crop in crops:
                if crop in text.lower():
                    extracted["crop_type"] = crop
                    extracted["crop"] = crop
                    break
        
        if "soil_type" in slots:
            soils = ["clay", "sandy", "loamy", "silty", "acidic", "alkaline"]
            for soil in soils:
                if soil in text.lower():
                    extracted["soil_type"] = soil
                    break
        
        return extracted
    
    def get_response_template(self, intent_name: str, response_type: str = "help") -> str:
        """Get response template for intent"""
        return self.RESPONSES.get(intent_name, {}).get(
            response_type, 
            "I didn't quite understand. Can you provide more details?"
        )


class ChatbotEngine:
    """Main chatbot logic combining intent detection and responses"""
    
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.conversation_history: List[Dict] = []
    
    def process_message(self, user_message: str) -> Dict:
        """
        Process user message and generate response
        """
        # Detect intent
        intent = self.intent_detector.detect(user_message)
        
        # Store in history
        self.conversation_history.append({
            "user": user_message,
            "intent": intent.name,
            "confidence": intent.confidence,
            "parameters": intent.parameters
        })
        
        # Generate response based on intent
        response = self._generate_response(intent)
        
        return {
            "user_message": user_message,
            "intent": intent.name,
            "confidence": float(intent.confidence),
            "parameters": intent.parameters,
            "chatbot_response": response,
            "action": self.INTENTS.get(intent.name, {}).get("action")
        }
    
    def _generate_response(self, intent: Intent) -> str:
        """Generate contextual response"""
        
        if intent.name == "disease_detection":
            return self.intent_detector.get_response_template("disease_detection", "clarify")
        
        elif intent.name == "groundwater_prediction":
            return "To predict groundwater levels, I need:\n- Your region/location\n- Recent rainfall data\n- Soil type\nCan you provide these details?"
        
        elif intent.name == "crop_recommendation":
            params = intent.parameters
            if params:
                return f"Based on your {params.get('soil_type', 'soil type')}, I'll recommend suitable crops. Please wait..."
            return self.intent_detector.get_response_template("crop_recommendation", "clarify")
        
        elif intent.name == "production_forecast":
            return "For yield prediction, share:\n- Crop type\n- Farming area\n- Soil nutrients\n- Expected rainfall"
        
        elif intent.name == "resource_management":
            return "I'll create an optimized irrigation and fertilizer schedule for you. What's your crop type and available water?"
        
        else:  # general_chat
            if any(word in intent.parameters.get("query", "").lower() for word in ["hello", "hi", "hey"]):
                return self.intent_detector.get_response_template("general_chat", "greeting")
            elif any(word in intent.parameters.get("query", "").lower() for word in ["help", "assist"]):
                return self.intent_detector.get_response_template("general_chat", "help")
            elif any(word in intent.parameters.get("query", "").lower() for word in ["bye", "goodbye"]):
                return self.intent_detector.get_response_template("general_chat", "goodbye")
            
            return "How can I assist you with your farming today?"
    
    @property
    def INTENTS(self):
        return self.intent_detector.INTENTS
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
