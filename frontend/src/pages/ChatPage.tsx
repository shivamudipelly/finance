import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, TrendingUp, TrendingDown, AlertTriangle, CheckCircle } from 'lucide-react';
import { useChatStore } from '../store/chatStore';

const ChatPage: React.FC = () => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { messages, isLoading, sendMessage } = useChatStore();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    await sendMessage(input);
    setInput('');
  };

  const suggestedQuestions = [
    "Analyze TCS for long-term investment",
    "Is this a good time for swing trading?",
    "What's happening in the Indian market today?",
    "Find fundamentally strong companies that have fallen",
    "Should I apply for this IPO?",
    "Analyze my portfolio risk",
  ];

  return (
    <div className="h-full flex flex-col max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-gray-900">AI Market Analyst</h1>
        <p className="text-gray-600 mt-1">
          Ask me anything about stocks, markets, IPOs, or your portfolio
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center px-4">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <TrendingUp className="w-8 h-8 text-blue-600" />
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Welcome to Market AI
            </h2>
            <p className="text-gray-600 mb-6 max-w-md">
              Your personal market intelligence assistant. Ask me to analyze stocks, 
              identify opportunities, or research market trends.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
              {suggestedQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => setInput(question)}
                  className="p-3 text-left text-sm bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-white border border-gray-200'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  
                  {message.analysis && (
                    <div className="mt-4 space-y-3">
                      {message.analysis.intent && (
                        <div className="flex items-center space-x-2 text-sm">
                          <CheckCircle size={16} className="text-green-600" />
                          <span className="font-medium">Intent:</span>
                          <span className="text-gray-700">{message.analysis.intent}</span>
                        </div>
                      )}
                      
                      {message.analysis.timeframe && (
                        <div className="flex items-center space-x-2 text-sm">
                          <TrendingUp size={16} className="text-blue-600" />
                          <span className="font-medium">Timeframe:</span>
                          <span className="text-gray-700">{message.analysis.timeframe}</span>
                        </div>
                      )}
                      
                      {message.analysis.evidence && message.analysis.evidence.length > 0 && (
                        <div className="bg-green-50 rounded-lg p-3">
                          <p className="font-medium text-green-800 text-sm mb-2">Evidence:</p>
                          <ul className="space-y-1">
                            {message.analysis.evidence.map((item, idx) => (
                              <li key={idx} className="text-sm text-green-700 flex items-start">
                                <span className="mr-2">+</span>
                                {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {message.analysis.risks && message.analysis.risks.length > 0 && (
                        <div className="bg-red-50 rounded-lg p-3">
                          <p className="font-medium text-red-800 text-sm mb-2">Risks:</p>
                          <ul className="space-y-1">
                            {message.analysis.risks.map((item, idx) => (
                              <li key={idx} className="text-sm text-red-700 flex items-start">
                                <AlertTriangle size={14} className="mr-2 mt-0.5" />
                                {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {message.analysis.conclusion && (
                        <div className="bg-blue-50 rounded-lg p-3">
                          <p className="font-medium text-blue-800 text-sm mb-1">Conclusion:</p>
                          <p className="text-sm text-blue-900">{message.analysis.conclusion}</p>
                        </div>
                      )}
                    </div>
                  )}
                  
                  <p className={`text-xs mt-2 ${message.role === 'user' ? 'text-blue-100' : 'text-gray-400'}`}>
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                  <div className="flex items-center space-x-2">
                    <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                    <span className="text-gray-600">Analyzing...</span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-gray-200 pt-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about stocks, markets, IPOs, or your portfolio..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <Send size={20} />
            <span>Send</span>
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Note: Analysis is based on available data and should not be considered as financial advice.
        </p>
      </form>
    </div>
  );
};

export default ChatPage;
