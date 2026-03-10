import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
import { aiStylistService } from '../services/aiStylist';

interface ChatInterfaceProps {
  isOpen: boolean;
  onClose: () => void;
  onGetRecommendations?: (recommendations: any) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ isOpen, onClose, onGetRecommendations }) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionStarted, setSessionStarted] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen && !sessionStarted) {
      startNewChat();
    }
  }, [isOpen]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const startNewChat = async () => {
    setIsLoading(true);
    try {
      const response = await aiStylistService.startConversation();
      setMessages(aiStylistService.getMessages());
      setSessionStarted(true);
    } catch (error) {
      console.error('Failed to start chat:', error);
      setMessages([{
        role: 'assistant',
        content: "I'm having trouble connecting. Please try again later."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage;
    setInputMessage('');
    
    // Add user message immediately
    setMessages(prev => [...prev, {
      role: 'user',
      content: userMessage
    }]);

    try {
      const response = await aiStylistService.sendMessage(userMessage);
      setMessages(aiStylistService.getMessages());

      if (aiStylistService.isReadyForRecommendations() && onGetRecommendations) {
        const recommendations = await aiStylistService.getRecommendations();
        onGetRecommendations(recommendations);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "Sorry, I'm having trouble responding. Please try again."
      }]);
    }
  };

  const handleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chat Button (when minimized) */}
      {isMinimized ? (
        <button
          onClick={handleMinimize}
          className="bg-gradient-to-r from-[#8B4513] to-[#D4AF37] text-white p-3 rounded-full shadow-lg hover:shadow-xl transition-shadow"
        >
          <MessageCircle className="w-5 h-5" />
        </button>
      ) : (
        /* Chat Window */
        <div className="bg-white rounded-lg shadow-xl w-80 flex flex-col border border-gray-200 overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-[#8B4513] to-[#D4AF37] text-white px-3 py-2 flex justify-between items-center">
            <h3 className="text-sm font-medium">AI Stylist</h3>
            <div className="flex items-center gap-1">
              <button
                onClick={handleMinimize}
                className="hover:bg-white/20 px-1.5 py-1 rounded text-xs"
              >
                −
              </button>
              <button
                onClick={onClose}
                className="hover:bg-white/20 px-1.5 py-1 rounded text-xs"
              >
                ×
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="h-80 overflow-y-auto p-3 bg-gray-50">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`mb-3 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}
              >
                <div
                  className={`inline-block px-3 py-2 rounded-lg text-sm max-w-[85%] ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-r from-[#8B4513] to-[#D4AF37] text-white'
                      : 'bg-white border border-gray-200 text-gray-800'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="text-left">
                <div className="inline-block bg-white border border-gray-200 px-3 py-2 rounded-lg text-sm text-gray-500">
                  Typing...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSendMessage} className="p-2 border-t border-gray-200 bg-white">
            <div className="flex gap-1">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Describe your outfit needs..."
                className="flex-1 px-3 py-1.5 text-sm border border-gray-300 rounded focus:outline-none focus:border-[#8B4513]"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputMessage.trim() || isLoading}
                className="bg-gradient-to-r from-[#8B4513] to-[#D4AF37] text-white px-3 py-1.5 rounded text-sm disabled:opacity-50"
              >
                Send
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;