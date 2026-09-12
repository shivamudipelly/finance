"""
AI Chat API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.tables import User, Conversation, Message
from app.schemas.schemas import ChatMessage, ChatResponse, AnalysisRequest, AnalysisReport
from app.services.ai_service import ai_service
from app.services.market_data import market_data_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    data: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response."""
    
    # Get conversation history if conversation_id provided
    conversation_history = []
    conversation_id = data.conversation_id
    
    if conversation_id:
        # Load previous messages
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        conversation_history = [
            {"role": m.role, "content": m.content}
            for m in messages[-10:]  # Last 10 messages
        ]
    
    # Get AI response
    response = await ai_service.chat(data.message, conversation_history)
    
    # Save to database if we have a conversation
    if not conversation_id:
        # Create new conversation
        conversation = Conversation(user_id=current_user.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        conversation_id = conversation.id
    
    # Save user message
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=data.message
    )
    db.add(user_msg)
    
    # Save assistant response
    assistant_msg = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=response.response,
        metadata={
            "intent": response.intent,
            "entities": response.entities,
            "confidence": response.confidence
        }
    )
    db.add(assistant_msg)
    db.commit()
    
    response.conversation_id = conversation_id
    return response


@router.post("/analyze", response_model=AnalysisReport)
async def analyze_stock(
    data: AnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """Get detailed AI analysis of a stock."""
    
    # Fetch market data
    quote = await market_data_service.get_current_quote(data.symbol)
    fundamentals = await market_data_service.get_fundamentals(data.symbol)
    prices = await market_data_service.get_historical_prices(data.symbol, period="6mo")
    
    # Prepare market data for analysis
    market_data = {
        "current_price": quote.price if quote else None,
        "change_percent": quote.change_percent if quote else None,
        "recent_prices": [
            {"date": str(p.date), "close": p.close}
            for p in prices[-20:]  # Last 20 days
        ] if prices else []
    }
    
    # Get fundamentals as dict
    fundamentals_dict = fundamentals.dict() if fundamentals else {}
    
    # Generate analysis
    report = await ai_service.analyze_stock(
        symbol=data.symbol,
        time_horizon=data.time_horizon,
        market_data=market_data,
        fundamentals=fundamentals_dict,
        context=data.context
    )
    
    return report


@router.get("/conversations")
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's conversation history."""
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at.desc()).limit(20).all()
    
    return {
        "conversations": [
            {
                "id": str(c.id),
                "created_at": c.created_at,
                "message_count": len(c.messages)
            }
            for c in conversations
        ]
    }


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific conversation with messages."""
    from uuid import UUID
    
    conversation = db.query(Conversation).filter(
        Conversation.id == UUID(conversation_id),
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()
    
    return {
        "conversation": {
            "id": str(conversation.id),
            "created_at": conversation.created_at
        },
        "messages": [
            {
                "id": str(m.id),
                "role": m.role,
                "content": m.content,
                "metadata": m.metadata,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }
