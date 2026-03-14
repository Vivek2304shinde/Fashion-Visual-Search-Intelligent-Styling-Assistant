import React from 'react';
import { Sparkles } from 'lucide-react';

interface AIStylistButtonProps {
  onClick: () => void;
}

const AIStylistButton: React.FC<AIStylistButtonProps> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="
        fixed bottom-6 right-6 z-50
        flex items-center gap-2.5 px-5 py-3.5
        rounded-full
        bg-gradient-to-r from-[#8B4513] via-[#D4AF37] to-[#F7E7CE]
        text-white font-semibold text-sm
        shadow-lg
        cursor-pointer select-none
        border border-white/20
        transition-all duration-300 hover:scale-105 hover:shadow-xl
      "
    >
      <Sparkles className="w-5 h-5" />
      <span>Chat with AI Stylist</span>
    </button>
  );
};

export default AIStylistButton;