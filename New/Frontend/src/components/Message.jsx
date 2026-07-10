import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, FileText, ExternalLink } from 'lucide-react';

const Message = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 ${isUser ? 'order-2' : 'order-1'}`}>
        <div className={`w-8 h-8 rounded-full flex items-center justify-center
          ${isUser ? 'bg-blue-600' : 'bg-gray-600'}`}>
          {isUser ? (
            <User className="w-4 h-4 text-white" />
          ) : (
            <Bot className="w-4 h-4 text-white" />
          )}
        </div>
      </div>
      
      {/* Message Content */}
      <div className={`flex-1 ${isUser ? 'order-1 max-w-[70%]' : 'order-2 max-w-[80%]'}`}>
        <div className={`message-${isUser ? 'user' : 'assistant'} p-3`}>
          {/* Wrap ReactMarkdown in a div with the className */}
          <div className={`prose prose-sm max-w-none ${isUser ? 'text-white' : 'text-gray-800'}`}>
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                ul: ({ children }) => <ul className="list-disc pl-4 mb-2">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal pl-4 mb-2">{children}</ol>,
                li: ({ children }) => <li>{children}</li>,
                strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                code: ({ children }) => <code className="bg-gray-200 px-1 rounded text-sm">{children}</code>,
                pre: ({ children }) => <pre className="bg-gray-100 p-2 rounded text-sm overflow-x-auto">{children}</pre>,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
        
        {/* Citations for assistant messages */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {message.sources.map((source, idx) => (
              <CitationCard key={idx} source={source} />
            ))}
          </div>
        )}
        
        {/* Timestamp */}
        <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

const CitationCard = ({ source }) => {
  return (
    <div className="inline-flex items-center gap-1.5 bg-gray-100 hover:bg-gray-200 rounded-md px-2 py-1 text-xs text-gray-600 transition-colors cursor-pointer">
      <FileText className="w-3 h-3" />
      <span>{source.document}</span>
      <span className="text-gray-400">•</span>
      <span>Page {source.page}</span>
      <ExternalLink className="w-3 h-3 opacity-50" />
    </div>
  );
};

export default Message;