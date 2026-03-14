import React, { useState, useEffect, useCallback } from 'react';
import { Heart, Sparkles, Shirt, MessageCircle } from 'lucide-react';
import PageHeader from './layout/PageHeader';
import TabNavigation from './layout/TabNavigation';
import ComplementaryOutfits from './sections/ComplementaryOutfits';
import { apiService, SearchResult } from '../services/api';
import { aiStylistService } from '../services/aiStylist';
import { useLocation } from 'react-router-dom';
import AIStylistChat from './chat/AIStylistChat';

interface ResultsPageProps {
  searchResults?: SearchResult[];
  searchMode?: 'image' | 'text';
  searchQuery?: string;
  uploadedImage?: string | File;
  outfitPlan?: any;
  stylingAdvice?: string;
  recommendedProducts?: Record<string, any[]>;
}

type TabType = 'similar' | 'complementary' | 'foryou';

interface Product extends SearchResult {
  product_id: string;
  image_url: string;
  product_name: string;
  price: number;
  brand: string;
  product_url?: string;
  source?: string;
}

const ProductCard: React.FC<Product & { onToggleSave?: (id: string) => void; saved?: boolean }> = ({
  product_id,
  image_url,
  product_name,
  price,
  brand,
  product_url,
  source,
  onToggleSave,
  saved = false,
}) => {
  const handleClick = () => product_url && window.open(product_url, '_blank');
  const handleSave = (e: React.MouseEvent) => {
    e.stopPropagation();
    onToggleSave?.(product_id);
  };

  return (
    <div className="glass-panel rounded-2xl overflow-hidden hover-lift group border-amber-200/20">
      <div className="relative cursor-pointer" onClick={handleClick}>
        <img
          src={image_url}
          alt={product_name}
          className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://via.placeholder.com/400?text=Image+Not+Found';
          }}
        />
        <button
          onClick={handleSave}
          className={`absolute top-3 right-3 w-10 h-10 rounded-full backdrop-blur-md border border-white/20
            flex items-center justify-center transition-all duration-300 hover:scale-110
            ${saved ? 'bg-red-500/90 text-white' : 'bg-white/70 text-slate-600 hover:bg-white/90'}`}
        >
          <Heart className={`w-5 h-5 ${saved ? 'fill-current' : ''}`} />
        </button>
        {source && (
          <div className="absolute bottom-3 left-3 px-2 py-1 bg-black/60 text-white text-xs rounded-full backdrop-blur-sm">
            {source.toUpperCase()}
          </div>
        )}
      </div>
      <div className="p-4 space-y-2">
        <div className="text-sm text-slate-500 font-medium">{brand}</div>
        <h4 className="font-semibold text-slate-800 line-clamp-2 cursor-pointer hover:text-amber-600" onClick={handleClick}>
          {product_name}
        </h4>
        <div className="text-lg font-bold brand-gold">₹{price}</div>
      </div>
    </div>
  );
};

const CategorySection: React.FC<{ label: string; items: Product[] }> = ({ label, items }) => {
  if (!items || items.length === 0) return null;
  return (
    <div className="mb-8">
      <div className="flex items-baseline justify-between mb-3 px-0.5">
        <h3 className="text-base font-semibold text-slate-800">{label}</h3>
        <span className="text-sm text-slate-400">{items.length} items</span>
      </div>
      <div className="flex gap-4 overflow-x-auto pb-3 snap-x snap-mandatory scrollbar-thin scrollbar-thumb-amber-200">
        {items.map((product) => (
          <div key={product.product_id} className="flex-none w-48 snap-start">
            <ProductCard {...product} />
          </div>
        ))}
      </div>
    </div>
  );
};

const ResultsPage: React.FC<ResultsPageProps> = ({
  searchResults,
  searchMode = 'image',
  searchQuery,
  uploadedImage,
  outfitPlan: propOutfitPlan,
  stylingAdvice: propStylingAdvice,
  recommendedProducts: propRecommendedProducts,
}) => {
  const location = useLocation();
  const [activeTab, setActiveTab] = useState<TabType>('similar');
  const [savedItems, setSavedItems] = useState<Set<string>>(new Set());
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string>('');

  const [outfitPlan, setOutfitPlan] = useState<any>(propOutfitPlan || null);
  const [stylingAdvice, setStylingAdvice] = useState<string>(propStylingAdvice || '');
  const [recommendedProducts, setRecommendedProducts] = useState<Record<string, any[]>>(
    propRecommendedProducts || {}
  );

  // Log the received props for debugging
  console.log('🎯 ResultsPage props:', {
    propOutfitPlan: !!propOutfitPlan,
    propStylingAdvice: !!propStylingAdvice,
    propRecommendedProductsKeys: Object.keys(propRecommendedProducts || {}),
    propRecommendedProductsLengths: Object.fromEntries(
      Object.entries(propRecommendedProducts || {}).map(([k, v]) => [k, v.length])
    ),
  });

  useEffect(() => {
    if (propOutfitPlan) {
      console.log('📦 Updating from props:', {
        outfitPlanKeys: Object.keys(propOutfitPlan),
        recommendedProductsKeys: Object.keys(propRecommendedProducts || {}),
      });
      setOutfitPlan(propOutfitPlan);
      setStylingAdvice(propStylingAdvice || '');
      setRecommendedProducts(propRecommendedProducts || {});
      setActiveTab('foryou');
    }
  }, [propOutfitPlan, propStylingAdvice, propRecommendedProducts]);

  useEffect(() => {
    if (location.state) {
      if (location.state.searchResults && !searchResults) {
        setProducts(location.state.searchResults);
      }
    }
  }, [location.state, searchResults]);

  useEffect(() => {
    if (location.state?.fromChat && !outfitPlan) {
      const storedPlan = sessionStorage.getItem('outfitPlan');
      const storedAdvice = sessionStorage.getItem('stylingAdvice');
      const storedProducts = sessionStorage.getItem('recommendedProducts');
      if (storedPlan) {
        try {
          setOutfitPlan(JSON.parse(storedPlan));
          setStylingAdvice(storedAdvice || '');
          setRecommendedProducts(JSON.parse(storedProducts || '{}'));
          setActiveTab('foryou');
          sessionStorage.removeItem('outfitPlan');
          sessionStorage.removeItem('stylingAdvice');
          sessionStorage.removeItem('recommendedProducts');
        } catch (e) {
          console.error('Error parsing stored data', e);
        }
      }
    }
  }, [location.state, outfitPlan]);

  const fetchProducts = useCallback(async () => {
    if (!uploadedImage) return;
    setLoading(true);
    try {
      let fileToUpload: File;
      if (typeof uploadedImage === 'string') {
        const response = await fetch(uploadedImage);
        const blob = await response.blob();
        fileToUpload = new File([blob], 'uploaded_image.jpg', { type: blob.type || 'image/jpeg' });
      } else {
        fileToUpload = uploadedImage;
      }
      const searchResponse = await apiService.searchByImage(fileToUpload, 5);
      setProducts(searchResponse.results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [uploadedImage]);

  useEffect(() => {
    if (searchMode === 'text' && searchResults) {
      setProducts(searchResults);
      setLoading(false);
    } else if (searchMode === 'image' && uploadedImage) {
      fetchProducts();
    }
  }, [searchResults, searchMode, uploadedImage, fetchProducts]);

  const toggleSaved = (id: string) => {
    setSavedItems(prev => {
      const newSaved = new Set(prev);
      newSaved.has(id) ? newSaved.delete(id) : newSaved.add(id);
      return newSaved;
    });
  };

  const showStatus = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    setStatusMessage(message);
    setTimeout(() => setStatusMessage(''), 3000);
  };

  const handleChatRecommendations = async (recommendations: any) => {
    if (recommendations?.outfit_plan) {
      setOutfitPlan(recommendations.outfit_plan);
      setStylingAdvice(recommendations.styling_advice || '');
      setRecommendedProducts(recommendations.products || {});
      setActiveTab('foryou');
      showStatus('Got personalized styling recommendations!', 'success');
    }
  };

  const EmptyState = ({ type }: { type: TabType }) => {
    const states = {
      similar: {
        icon: <Shirt className="w-16 h-16 text-slate-300" strokeWidth={1} />,
        title: "Your style journey begins here.",
        subtitle: searchMode === 'image' ? "Upload a pic to discover similar items!" : "Search for items to get started!",
      },
      complementary: {
        icon: <Sparkles className="w-16 h-16 text-amber-400" strokeWidth={1} />,
        title: "Perfect matches coming soon!",
        subtitle: "We're curating complementary pieces for your style.",
      },
      foryou: {
        icon: <Sparkles className="w-16 h-16 text-slate-300" strokeWidth={1} />,
        title: "Your closet's lonely!",
        subtitle: "Chat with AI Stylist to get personalized recommendations ✨",
      },
    };
    const { icon, title, subtitle } = states[type];
    return (
      <div className="flex flex-col items-center justify-center h-96 text-center space-y-6 tab-transition">
        <div className="glass-panel rounded-2xl p-8 border-amber-200/20">{icon}</div>
        <div className="space-y-2">
          <h3 className="text-xl font-semibold text-slate-700">{title}</h3>
          <p className="text-slate-500">{subtitle}</p>
        </div>
        {type === 'foryou' && (
          <button
            onClick={() => setIsChatOpen(true)}
            className="px-6 py-3 rounded-full bg-gradient-to-r from-[#8B4513] to-[#D4AF37] text-white font-medium hover:shadow-xl transition-all flex items-center gap-2"
          >
            <MessageCircle className="w-4 h-4" />
            Chat with AI Stylist
          </button>
        )}
      </div>
    );
  };

  const getImageAsString = (): string => {
    return typeof uploadedImage === 'string' ? uploadedImage : uploadedImage ? URL.createObjectURL(uploadedImage) : '';
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-500"></div>
          <p className="ml-4 text-slate-600">
            {searchMode === 'image' ? "Searching for similar products..." : "Loading search results..."}
          </p>
        </div>
      );
    }
    if (error) {
      return (
        <div className="text-center py-10">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
            <h3 className="text-red-800 font-semibold mb-2">Search Failed</h3>
            <p className="text-red-600 mb-4">{error}</p>
            <button onClick={fetchProducts} className="px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition-colors">
              Try Again
            </button>
          </div>
        </div>
      );
    }
    if (activeTab === 'complementary') {
      return <ComplementaryOutfits uploadedImage={getImageAsString()} />;
    }
    if (activeTab === 'foryou') {
      if (outfitPlan && Object.keys(outfitPlan).length > 0) {
        const categoryEntries = Object.entries(recommendedProducts).filter(([_, items]) => items.length > 0);
        console.log('🎨 For You tab – categoryEntries:', categoryEntries.map(([k, v]) => `${k}: ${v.length}`));
        if (categoryEntries.length === 0) {
          console.warn('⚠️ No category entries with products');
          return <EmptyState type="foryou" />;
        }
        return (
          <div>
            {stylingAdvice && (
              <div className="bg-gradient-to-r from-[#8B4513]/10 to-[#D4AF37]/10 rounded-2xl p-6 mb-6 border border-[#D4AF37]/20">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#8B4513] to-[#D4AF37] flex items-center justify-center flex-shrink-0">
                    <Sparkles className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-gray-700 text-sm leading-relaxed">{stylingAdvice}</p>
                </div>
              </div>
            )}
            {categoryEntries.map(([category, items]) => (
              <CategorySection
                key={category}
                label={category.charAt(0).toUpperCase() + category.slice(1)}
                items={items}
              />
            ))}
          </div>
        );
      }
      return <EmptyState type="foryou" />;
    }
    if (products.length > 0) {
      return (
        <div className="space-y-4">
          <div className="text-center py-4">
            <p className="text-slate-600">
              {searchMode === 'image'
                ? `Found ${products.length} similar products`
                : `Found ${products.length} products for "${searchQuery}"`}
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 tab-transition">
            {products.map(product => (
              <ProductCard key={product.product_id} {...product} onToggleSave={toggleSaved} saved={savedItems.has(product.product_id)} />
            ))}
          </div>
        </div>
      );
    }
    return <EmptyState type={activeTab} />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
      <PageHeader uploadedImage={getImageAsString()} />
      {statusMessage && (
        <div className="fixed top-20 left-1/2 transform -translate-x-1/2 z-50">
          <div className="bg-green-50 text-green-700 border border-green-200 p-3 rounded-lg text-sm font-medium shadow-lg">
            {statusMessage}
          </div>
        </div>
      )}
      <div className="max-w-7xl mx-auto px-6 py-6">
        <TabNavigation activeTab={activeTab} onTabChange={(tab: string) => setActiveTab(tab as TabType)} />
        <div className="space-y-6 tab-transition">{renderContent()}</div>
      </div>
      <button
        onClick={() => setIsChatOpen(true)}
        className="fixed bottom-6 right-6 bg-gradient-to-r from-[#8B4513] to-[#D4AF37] text-white p-4 rounded-full shadow-2xl hover:shadow-xl transform hover:scale-110 transition-all duration-300 z-40"
      >
        <MessageCircle className="w-6 h-6" />
      </button>
      <AIStylistChat
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        onGetRecommendations={handleChatRecommendations}
      />
    </div>
  );
};

export default ResultsPage;