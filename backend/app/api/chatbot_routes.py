from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.chatbot import ChatbotEngine
from app.services.disease_detection import MockDiseasePredictorForTesting

router = APIRouter(prefix="/api/v1/chatbot", tags=["chatbot"])

# Initialize services
chatbot_engine = ChatbotEngine()
disease_predictor = MockDiseasePredictorForTesting()

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    user_message: str
    intent: str
    confidence: float
    chatbot_response: str
    action: Optional[str] = None
    requires_action: bool = False

@router.post("/message", response_model=ChatResponse)
async def send_message(chat: ChatMessage):
    """
    Send message to chatbot and get response
    """
    try:
        response = chatbot_engine.process_message(chat.message)
        
        return ChatResponse(
            user_message=response["user_message"],
            intent=response["intent"],
            confidence=response["confidence"],
            chatbot_response=response["chatbot_response"],
            action=response.get("action"),
            requires_action=response.get("action") is not None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/disease-detection")
async def detect_disease(file: UploadFile = File(...)):
    """
    Detect crop disease from image
    """
    try:
        image_data = await file.read()
        result = disease_predictor.predict(image_data)
        
        return {
            "success": True,
            "disease": result.get("disease"),
            "confidence": result.get("confidence"),
            "confidence_percentage": result.get("confidence_percentage"),
            "treatments": result.get("treatments"),
            "prevention": result.get("prevention")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_chat_history():
    """Get conversation history"""
    return {"history": chatbot_engine.get_history()}

@router.post("/clear-history")
async def clear_history():
    """Clear conversation history"""
    chatbot_engine.clear_history()
    return {"message": "History cleared"}

@router.get("/intents")
async def get_available_intents():
    """Get all available intents"""
    intents_list = []
    for intent_name, config in chatbot_engine.INTENTS.items():
        intents_list.append({
            "name": intent_name,
            "action": config.get("action"),
            "description": f"Handles: {', '.join(config['keywords'][:3])}..."
        })
    return {"intents": intents_list}
