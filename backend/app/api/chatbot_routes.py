import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.db.models import ChatSession
from app.services.chatbot import ChatbotEngine
from app.services.disease_detection import DiseaseDetectionService, MockDiseasePredictorForTesting

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/chatbot", tags=["chatbot"])

chatbot_engine = ChatbotEngine()
disease_predictor = DiseaseDetectionService()
if not disease_predictor.load_model(settings.disease_model_path):
    disease_predictor = MockDiseasePredictorForTesting()


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    user_message: str
    intent: str
    confidence: float
    chatbot_response: str
    session_id: str
    action: Optional[str] = None
    requires_action: bool = False


@router.post("/message", response_model=ChatResponse)
async def send_message(chat: ChatMessage, db: Session = Depends(get_db)):
    try:
        response = chatbot_engine.process_message(chat.message)
        session_id = chat.session_id or str(uuid.uuid4())

        db.add(
            ChatSession(
                session_id=session_id,
                user_query=chat.message,
                intent=response["intent"],
                bot_response=response["chatbot_response"],
                context=response.get("parameters", {}),
            )
        )
        db.commit()

        return ChatResponse(
            user_message=response["user_message"],
            intent=response["intent"],
            confidence=response["confidence"],
            chatbot_response=response["chatbot_response"],
            session_id=session_id,
            action=response.get("action"),
            requires_action=response.get("action") is not None,
        )
    except Exception as exc:
        logger.exception("Chat endpoint failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/disease-detection")
async def detect_disease(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        result = disease_predictor.predict(image_data)
        return {
            "success": result.get("success", False),
            "disease": result.get("disease"),
            "confidence": result.get("confidence"),
            "confidence_percentage": result.get("confidence_percentage"),
            "treatments": result.get("treatments", []),
            "prevention": result.get("prevention", []),
            "error": result.get("error"),
        }
    except Exception as exc:
        logger.exception("Disease detection failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/history")
async def get_chat_history(db: Session = Depends(get_db), limit: int = 20):
    rows = db.query(ChatSession).order_by(ChatSession.created_at.desc()).limit(limit).all()
    return {
        "history": [
            {
                "session_id": row.session_id,
                "user_query": row.user_query,
                "intent": row.intent,
                "bot_response": row.bot_response,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    }


@router.post("/clear-history")
async def clear_history(db: Session = Depends(get_db)):
    db.query(ChatSession).delete()
    db.commit()
    chatbot_engine.clear_history()
    return {"message": "History cleared"}


@router.get("/intents")
async def get_available_intents():
    intents_list = []
    for intent_name, config in chatbot_engine.INTENTS.items():
        intents_list.append(
            {
                "name": intent_name,
                "action": config.get("action"),
                "description": f"Handles: {', '.join(config['keywords'][:3])}...",
            }
        )
    return {"intents": intents_list}
