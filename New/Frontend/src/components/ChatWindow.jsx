import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Loader, 
  Download, 
  Trash2, 
  MessageSquare,
  Bot,           // ← Add this
  User           // ← Add this if used
} from 'lucide-react';
import Message from './Message';
import { askQuestion, clearHistory, getHistory } from '../services/api';

const ChatWindow = ({ sessionId, onMessagesUpdate }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Load history on mount
  useEffect(() => {
    loadHistory();
  }, [sessionId]);

  const loadHistory = async () => {
    try {
      const history = await getHistory(sessionId);
      if (history && history.messages) {
        const formattedMessages = history.messages.map(msg => ({
          role: msg.role,
          content: msg.message,
          timestamp: msg.timestamp,
          sources: msg.sources || []
        }));
        setMessages(formattedMessages);
        if (onMessagesUpdate) onMessagesUpdate(formattedMessages);
      }
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    if (onMessagesUpdate) onMessagesUpdate([...messages, userMessage]);
    
    setInput('');
    setLoading(true);
    setIsTyping(true);
    
    try {
      const response = await askQuestion(input, sessionId);
      
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources || [],
        timestamp: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      if (onMessagesUpdate) onMessagesUpdate([...messages, userMessage, assistantMessage]);
      
    } catch (err) {
      console.error('Failed to get answer:', err);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        sources: [],
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setIsTyping(false);
      inputRef.current?.focus();
    }
  };

  const handleClearHistory = async () => {
    if (confirm('Clear all chat history?')) {
      await clearHistory(sessionId);
      setMessages([]);
      if (onMessagesUpdate) onMessagesUpdate([]);
    }
  };

  const handleExportChat = () => {
    const exportData = {
      sessionId,
      exportDate: new Date().toISOString(),
      messages: messages.map(msg => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp,
        sources: msg.sources
      }))
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-export-${sessionId}-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 rounded-xl overflow-hidden">
      {/* Chat Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-800">Chat Assistant</h2>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleExportChat}
            className="p-2 text-gray-600 hover:text-blue-600 transition-colors"
            title="Export chat"
          >
            <Download className="w-4 h-4" />
          </button>
          <button
            onClick={handleClearHistory}
            className="p-2 text-gray-600 hover:text-red-600 transition-colors"
            title="Clear history"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
      
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && !isTyping && (
          <div className="text-center text-gray-500 mt-20">
            <Bot className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p className="text-lg font-medium">Ask me anything about your documents!</p>
            <p className="text-sm mt-2">Upload a PDF and start asking questions.</p>
          </div>
        )}
        
        {messages.map((message, idx) => (
          <Message key={idx} message={message} />
        ))}
        
        {isTyping && (
          <div className="flex gap-3 justify-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
            </div>
            <div className="bg-white rounded-2xl rounded-tl-sm p-3 shadow-sm border border-gray-200">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="flex gap-3">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about your documents... (Press Enter to send)"
            className="flex-1 resize-none border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows="1"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center gap-2"
          >
            {loading ? (
              <Loader className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            Send
          </button>
        </div>
        <div className="text-xs text-gray-500 mt-2 text-center">
          Answers are generated from your uploaded documents. Always verify important information.
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;