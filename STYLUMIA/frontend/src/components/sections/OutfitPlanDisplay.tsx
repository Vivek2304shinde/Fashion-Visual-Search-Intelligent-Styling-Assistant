import React from 'react';
import { Sparkles, ChevronRight, ShoppingBag } from 'lucide-react';

interface OutfitPlanDisplayProps {
  outfitPlan: Record<string, any>;
  stylingAdvice: string;
  products?: Record<string, any[]>;
  onViewProduct?: (product: any) => void;
}

const OutfitPlanDisplay: React.FC<OutfitPlanDisplayProps> = ({ 
  outfitPlan, 
  stylingAdvice,
  products = {},
  onViewProduct 
}) => {
  return (
    <div className="space-y-6">
      {/* Styling Advice Banner */}
      <div className="bg-gradient-to-r from-[#8B4513]/10 to-[#D4AF37]/10 rounded-2xl p-6 border border-[#D4AF37]/20">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#8B4513] to-[#D4AF37] flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-[#8B4513] mb-2">✨ Styling Advice</h3>
            <p className="text-gray-700 text-sm leading-relaxed">{stylingAdvice}</p>
          </div>
        </div>
      </div>

      {/* Outfit Items Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(outfitPlan).map(([category, details]: [string, any]) => (
          <div 
            key={category}
            className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all overflow-hidden"
          >
            <div className="p-4">
              <div className="flex items-center gap-2 mb-3">
                <h4 className="font-semibold text-[#8B4513] capitalize">{category}</h4>
                <ChevronRight className="w-4 h-4 text-[#D4AF37]" />
              </div>
              
              <div className="space-y-2 text-sm">
                {details.color && (
                  <p><span className="text-gray-500">Color:</span> {details.color}</p>
                )}
                {details.style && (
                  <p><span className="text-gray-500">Style:</span> {details.style}</p>
                )}
                {details.fabric && (
                  <p><span className="text-gray-500">Fabric:</span> {details.fabric}</p>
                )}
                {details.fit && (
                  <p><span className="text-gray-500">Fit:</span> {details.fit}</p>
                )}
                {details.why_it_works && (
                  <p className="text-xs text-gray-600 italic mt-2">{details.why_it_works}</p>
                )}
              </div>
            </div>

            {/* Show products if available */}
            {products[category] && products[category].length > 0 && (
              <div className="border-t border-gray-100 bg-gray-50 p-3">
                <p className="text-xs font-medium text-gray-600 mb-2">Recommended products:</p>
                <div className="space-y-2">
                  {products[category].slice(0, 2).map((product, idx) => (
                    <div 
                      key={idx}
                      className="flex items-center gap-2 text-xs cursor-pointer hover:bg-white p-1 rounded transition-colors"
                      onClick={() => onViewProduct && onViewProduct(product)}
                    >
                      <img 
                        src={product.image_url} 
                        alt={product.product_name}
                        className="w-8 h-8 object-cover rounded"
                      />
                      <div className="flex-1">
                        <p className="font-medium truncate">{product.brand}</p>
                        <p className="text-gray-500">₹{product.price}</p>
                      </div>
                      <ShoppingBag className="w-3 h-3 text-[#D4AF37]" />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default OutfitPlanDisplay;