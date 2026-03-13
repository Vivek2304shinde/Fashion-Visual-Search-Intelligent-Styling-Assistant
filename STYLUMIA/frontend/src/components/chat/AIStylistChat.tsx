import React, { useState, useRef, useEffect, useCallback } from 'react';
import { X, Send, Sparkles } from 'lucide-react';
import { aiStylistService } from '../../services/aiStylist';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface AIStylistChatProps {
  isOpen: boolean;
  onClose: () => void;
  onRecommendationsReady: (outfitPlan?: any) => void;
}

const TypingIndicator: React.FC = () => (
  <div className="flex items-center gap-1 px-4 py-3">
    <div className="flex items-center gap-1.5">
      <span className="text-xs text-gray-500 italic">AI Stylist is thinking</span>
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-1.5 h-1.5 rounded-full bg-[#D4AF37] animate-pulse"
          style={{ animationDelay: `${i * 0.2}s` }}
        />
      ))}
    </div>
  </div>
);

const AIStylistChat: React.FC<AIStylistChatProps> = ({ isOpen, onClose, onRecommendationsReady }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionStarted, setSessionStarted] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [show, setShow] = useState(false);

  // Initialize chat when opened
  useEffect(() => {
    if (isOpen && !sessionStarted) {
      startNewChat();
    }
    if (isOpen) {
      setShow(true);
      setTimeout(() => inputRef.current?.focus(), 400);
    } else {
      setShow(false);
    }
  }, [isOpen]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const startNewChat = async () => {
    setIsTyping(true);
    try {
      await aiStylistService.startConversation();
      setMessages(aiStylistService.getMessages());
      setSessionStarted(true);
    } catch (error) {
      console.error('Failed to start chat:', error);
      setMessages([{
        id: 'error',
        role: 'assistant',
        content: "Sorry, I'm having trouble connecting. Please try again."
      }]);
    } finally {
      setIsTyping(false);
    }
  };

const handleSend = useCallback(async () => {
  const text = input.trim();
  if (!text || isTyping || !sessionStarted) return;

  const userMsg: Message = { id: `u-${Date.now()}`, role: 'user', content: text };
  setMessages((prev) => [...prev, userMsg]);
  setInput('');
  setIsTyping(true);

  try {
    const response = await aiStylistService.sendMessage(text);
    setMessages(aiStylistService.getMessages());

    if (aiStylistService.isReadyForRecommendations()) {
      // Optionally add a temporary message
      setMessages((prev) => [...prev, {
        id: `temp-${Date.now()}`,
        role: 'assistant',
        content: '✨ Looking for the perfect outfit recommendations for you...'
      }]);
      
      const recommendations = await aiStylistService.getRecommendations();
      onRecommendationsReady(recommendations);
      onClose(); // <-- close the chat
    }
  } catch (error) {
    console.error('Failed to send message:', error);
    setMessages((prev) => [...prev, {
      id: `a-${Date.now()}`,
      role: 'assistant',
      content: "Sorry, I'm having trouble responding. Please try again."
    }]);
  } finally {
    setIsTyping(false);
  }
}, [input, isTyping, sessionStarted, onRecommendationsReady, onClose]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className={`fixed inset-0 z-[60] bg-black/50 backdrop-blur-sm transition-opacity duration-300 ${
          show ? 'opacity-100' : 'opacity-0'
        }`}
        onClick={onClose}
      />

      {/* Modal */}
      <div
        className={`
          fixed z-[70] 
          inset-4 sm:inset-auto
          sm:left-1/2 sm:top-1/2 sm:-translate-x-1/2 sm:-translate-y-1/2
          sm:w-[560px] sm:max-h-[680px]
          flex flex-col
          rounded-3xl overflow-hidden
          bg-white/90 backdrop-blur-xl border border-[#D4AF37]/30
          shadow-2xl shadow-black/20
          transition-all duration-300 transform
          ${show ? 'opacity-100 scale-100' : 'opacity-0 scale-95'}
        `}
      >
        {/* Header */}
        <div className="flex items-center gap-3 px-5 py-4 border-b border-gray-200/50 bg-gradient-to-r from-[#D4AF37]/5 to-transparent">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#8B4513] to-[#D4AF37] flex items-center justify-center shadow-md">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-800 text-sm">AI Stylist Assistant</h3>
            <p className="text-xs text-gray-500">
              {aiStylistService.isReadyForRecommendations() 
                ? "Ready to style you! ✨" 
                : "Tell me about your outfit needs"}
            </p>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-gray-100 transition-colors"
          >
            <X className="w-4 h-4 text-gray-500" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3 min-h-0" style={{ maxHeight: 'calc(100% - 140px)' }}>
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <Sparkles className="w-12 h-12 mx-auto mb-3 text-[#D4AF37] animate-pulse" />
              <p>Starting your styling session...</p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                {msg.role === 'assistant' && (
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#8B4513] to-[#D4AF37] flex items-center justify-center mr-2 mt-1 flex-shrink-0 shadow-sm">
                    <Sparkles className="w-3.5 h-3.5 text-white" />
                  </div>
                )}
                <div
                  className={`
                    max-w-[80%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed
                    ${msg.role === 'user'
                      ? 'bg-gradient-to-r from-[#8B4513] to-[#D4AF37] text-white rounded-br-md'
                      : 'bg-gray-100 text-gray-800 rounded-bl-md'
                    }
                  `}
                >
                  {msg.content}
                </div>
              </div>
            ))
          )}

          {isTyping && <TypingIndicator />}
          <div ref={chatEndRef} />
        </div>

        {/* Input */}
        <div className="px-4 py-3 border-t border-gray-200/50 bg-white/80 backdrop-blur-sm">
          <div className="flex items-center gap-2 rounded-2xl border border-gray-200 bg-white px-4 py-2 focus-within:border-[#D4AF37] focus-within:shadow-[0_0_0_3px_rgba(212,175,55,0.1)] transition-all duration-200">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Describe your outfit needs…"
              className="flex-1 bg-transparent text-sm text-gray-800 placeholder:text-gray-400 outline-none"
              disabled={isTyping || !sessionStarted}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isTyping || !sessionStarted}
              className="
                w-8 h-8 rounded-full flex items-center justify-center
                bg-gradient-to-r from-[#8B4513] to-[#D4AF37]
                text-white
                disabled:opacity-40 disabled:cursor-not-allowed
                hover:shadow-md hover:scale-105
                transition-all duration-200
              "
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default AIStylistChat;