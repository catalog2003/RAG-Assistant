import React, { useState, useEffect } from 'react';
import UploadBox from '../components/UploadBox';
import ChatWindow from '../components/ChatWindow';
import { listDocuments, healthCheck } from '../services/api';
import { Activity, Database, Cpu } from 'lucide-react';

const ChatPage = () => {
  const [documents, setDocuments] = useState([]);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [isHealthy, setIsHealthy] = useState(true);
  const [stats, setStats] = useState({ totalChunks: 0, model: 'Loading...' });

  useEffect(() => {
    loadDocuments();
    checkHealth();
  }, []);

  const loadDocuments = async () => {
    try {
      const docs = await listDocuments();
      setDocuments(docs.documents || []);
    } catch (err) {
      console.error('Failed to load documents:', err);
    }
  };

  const checkHealth = async () => {
    try {
      const health = await healthCheck();
      setIsHealthy(true);
      setStats({
        totalChunks: health.total_chunks || 0,
        model: health.embedding_model || 'Unknown',
      });
    } catch (err) {
      setIsHealthy(false);
      console.error('Backend not reachable:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">R</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">RAG Assistant</h1>
                <p className="text-sm text-gray-500">Retrieval-Augmented Generation with FAISS</p>
              </div>
            </div>
            
            <div className="flex gap-4">
              <div className="flex items-center gap-2 text-sm">
                <Activity className={`w-4 h-4 ${isHealthy ? 'text-green-500' : 'text-red-500'}`} />
                <span className="text-gray-600">{isHealthy ? 'Connected' : 'Disconnected'}</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <Database className="w-4 h-4 text-blue-500" />
                <span className="text-gray-600">{stats.totalChunks} chunks</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <Cpu className="w-4 h-4 text-purple-500" />
                <span className="text-gray-600">Phi-3</span>
              </div>
            </div>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar - Upload */}
          <div className="lg:col-span-1">
            <UploadBox
              onUploadSuccess={loadDocuments}
              documents={documents}
              setDocuments={setDocuments}
            />
            
            {/* Info Card */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mt-6">
              <h3 className="font-semibold text-gray-800 mb-3">How it works</h3>
              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start gap-2">
                  <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-blue-600 text-xs font-bold">1</span>
                  </div>
                  <span>Upload a PDF document</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-blue-600 text-xs font-bold">2</span>
                  </div>
                  <span>AI extracts and chunks the text</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-blue-600 text-xs font-bold">3</span>
                  </div>
                  <span>Creates embeddings and builds FAISS index</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-blue-600 text-xs font-bold">4</span>
                  </div>
                  <span>Ask questions and get answers with citations</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Right Side - Chat */}
          <div className="lg:col-span-2 h-[600px]">
            <ChatWindow sessionId={sessionId} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default ChatPage;