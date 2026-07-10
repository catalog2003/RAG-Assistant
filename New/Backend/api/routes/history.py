from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from New.Backend.api.models.schemas import HistoryResponse, ChatMessage
from New.Backend.services.history import history_manager


router = APIRouter(prefix="/history", tags=["Chat History"])

@router.get("/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    history = history_manager.get_history(session_id)
    messages = []
    for msg in history:
        timestamp_value = msg.get("timestamp")
        if isinstance(timestamp_value, str):
            timestamp = datetime.fromisoformat(timestamp_value)
        else:
            timestamp = datetime.fromtimestamp(timestamp_value)

        messages.append(
            ChatMessage(
                role=msg["role"],
                message=msg["message"],
                timestamp=timestamp
            )
        )

    return HistoryResponse(
        session_id=session_id,
        messages=messages
    )

@router.delete("/{session_id}")
async def clear_history(session_id: str):
    history_manager.clear_history(session_id)
    return {
        "status": "success",
        "message": f"History cleared for session {session_id}"
    }
@router.get("/")
async def list_sessions():
    sessions = list(history_manager.history.keys())
    return {
        "sessions": sessions,
        "total_sessions": len(sessions)
    }

