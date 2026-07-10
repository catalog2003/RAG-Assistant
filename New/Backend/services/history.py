import json
import os
from typing import Dict, List
from datetime import datetime
from New.Backend.config import HISTORY_PATH

class ChatHistoryManager:
    def __init__(self):
        self.history_path = HISTORY_PATH
        self.history: Dict[str, List[dict]] = {}
        self.load()
    
    def load(self):
        """Load chat history from disk"""
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = {}
        else:
            self.history = {}
    
    def save(self):
        """Save chat history to disk"""
        with open(self.history_path, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_message(self, session_id: str, role: str, message: str):
        """Add a message to history"""
        if session_id not in self.history:
            self.history[session_id] = []
        
        self.history[session_id].append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 50 messages per session
        if len(self.history[session_id]) > 50:
            self.history[session_id] = self.history[session_id][-50:]
        
        self.save()
    
    def get_history(self, session_id: str) -> List[dict]:
        """Get chat history for a session"""
        return self.history.get(session_id, [])
    
    def clear_history(self, session_id: str):
        """Clear history for a session"""
        if session_id in self.history:
            del self.history[session_id]
            self.save()

# Singleton instance
history_manager = ChatHistoryManager()