import { Search as SearchIcon } from 'lucide-react';
import React, { useState, useCallback, useEffect } from 'react';
import { Upload, Image as ImageIcon, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { apiService, SearchResult } from '../services/api';
import { searchByText } from '../api/search';
import { useNavigate } from 'react-router-dom';

interface UploadZoneProps {
  onFileUpload?: (file: File) => void;
  onSearchResults?: (results: SearchResult[]) => void;
  onTextSearch?: (query: string) => void;
}

const UploadZone: React.FC<UploadZoneProps> = ({ 
  onFileUpload, 
  onSearchResults, 
  onTextSearch 
}) => {
  const navigate = useNavigate();
  const [isDragOver, setIsDragOver] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  const [statusMessage, setStatusMessage] = useState<string>('');
  const [searchMode, setSearchMode] = useState<'image' | 'text'>('image');
  const [searchQuery, setSearchQuery] = useState('');

  // Check backend connection
  useEffect(() => {
    const checkConnection = async () => {
      setBackendStatus('checking');
      try {
        const isConnected = await apiService.testConnection();
        setBackendStatus(isConnected ? 'connected' : 'disconnected');
      } catch (error) {
        console.error('Connection check failed:', error);
        setBackendStatus('disconnected');
      }
    };
    checkConnection();
  }, []);

  // Handle drag events
  const handleDragEvents = {
    onDragOver: (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(true);
    },
    onDragLeave: (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
    },
    onDrop: (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
      const file = Array.from(e.dataTransfer.files).find(f => f.type.startsWith('image/'));
      file ? handleImageUpload(file) : showStatus('Please drop a valid image file', 'error');
    }
  };

  // Handle file selection
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    file?.type.startsWith('image/') 
      ? handleImageUpload(file) 
      : showStatus('Please select a valid image file', 'error');
  };

  // Show status message with type
  const showStatus = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    setStatusMessage(message);
    setTimeout(() => setStatusMessage(''), type === 'error' ? 5000 : 3000);
  };

  // Handle image upload and search
  const handleImageUpload = async (file: File) => {
    if (backendStatus !== 'connected') {
      showStatus('Backend connection failed', 'error');
      return;
    }

    setIsSearching(true);
    showStatus('Uploading and analyzing image...', 'info');
    onFileUpload?.(file);

    try {
      const { results, total_found } = await apiService.searchByImage(file, 8);
      showStatus(`Found ${total_found} similar products!`, 'success');
      onSearchResults?.(results);
    } catch (error) {
      console.error('Image search failed:', error);
      showStatus(getErrorMessage(error), 'error');
    } finally {
      setIsSearching(false);
    }
  };

  // Handle text search
  const handleTextSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim() || backendStatus !== 'connected') return;

    setIsSearching(true);
    showStatus('Searching for products...', 'info');

    try {
      const results = await searchByText(searchQuery);
      showStatus(`Found ${results.length} products!`, 'success');
      
      // Navigate with results
      navigate('/results', {
        state: {
          searchResults: results,
          searchMode: 'text',
          searchQuery: searchQuery
        }
      });

      onTextSearch?.(searchQuery);
      onSearchResults?.(results);
    } catch (error) {
      console.error('Text search failed:', error);
      showStatus(getErrorMessage(error), 'error');
    } finally {
      setIsSearching(false);
    }
  };

  // Get appropriate error message
  const getErrorMessage = (error: unknown): string => {
    if (error instanceof Error) {
      if (error.message.includes('Failed to fetch')) return 'Cannot connect to server';
      if (error.message.includes('400')) return 'Invalid request';
      if (error.message.includes('500')) return 'Server error';
    }
    return 'Search failed. Please try again.';
  };

  // Backend status indicator component
  const BackendStatusIndicator = () => (
    <div className={`flex items-center gap-2 text-sm ${
      backendStatus === 'checking' ? 'text-slate-500' :
      backendStatus === 'connected' ? 'text-green-600' : 'text-red-500'
    }`}>
      {backendStatus === 'checking' ? (
        <>
          <Loader2 className="w-4 h-4 animate-spin" />
          Connecting to server...
        </>
      ) : backendStatus === 'connected' ? (
        <>
          <CheckCircle className="w-4 h-4" />
          Server connected
        </>
      ) : (
        <>
          <AlertCircle className="w-4 h-4" />
          Server disconnected
          <button 
            onClick={() => setBackendStatus('checking')}
            className="text-blue-500 hover:text-blue-700 underline ml-1"
          >
            Retry
          </button>
        </>
      )}
    </div>
  );

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full max-w-2xl text-center">
        {/* Logo */}
        <div className="mb-8">
          <h1 className="text-5xl font-bold mb-2 stylumia-gradient font-clash">Stylumia</h1>
          <div className="w-12 h-1 bg-gradient-to-r from-transparent via-amber-400 to-transparent mx-auto"></div>
        </div>

        {/* Backend Status */}
        <div className="mb-6 flex justify-center">
          <BackendStatusIndicator />
        </div>

        {/* Search Mode Toggle */}
        <div className="mb-6 flex justify-center">
          <div className="inline-flex bg-amber-50 rounded-full p-1">
            <button
              onClick={() => setSearchMode('image')}
              className={`px-6 py-2 rounded-full transition-all ${
                searchMode === 'image' ? 'bg-amber-500 text-white shadow-md' : 'text-amber-600 hover:bg-amber-100'
              }`}
            >
              Image Search
            </button>
            <button
              onClick={() => setSearchMode('text')}
              className={`px-6 py-2 rounded-full transition-all ${
                searchMode === 'text' ? 'bg-amber-500 text-white shadow-md' : 'text-amber-600 hover:bg-amber-100'
              }`}
            >
              Text Search
            </button>
          </div>
        </div>

        {searchMode === 'image' ? (
          /* Image Upload Zone */
          <div
            className={`
              glass-panel rounded-3xl p-12 hover-lift glow-on-hover
              border-2 border-dashed transition-all duration-300
              ${isDragOver ? 'border-amber-400 bg-amber-50/30 shadow-2xl shadow-amber-500/20' : 'border-amber-300/50 hover:border-amber-400/70'}
              ${isSearching ? 'pointer-events-none opacity-75' : ''}
            `}
            {...handleDragEvents}
          >
            <div className="space-y-6">
              {/* Icon */}
              <div className={`
                mx-auto w-20 h-20 rounded-full flex items-center justify-center
                transition-all duration-300
                ${isDragOver ? 'bg-amber-100 text-amber-600 scale-110' : 'bg-amber-50 text-amber-500 hover:bg-amber-100'}
              `}>
                {isSearching ? (
                  <Loader2 className="w-10 h-10 animate-spin" />
                ) : isDragOver ? (
                  <ImageIcon className="w-10 h-10" />
                ) : (
                  <Upload className="w-10 h-10" />
                )}
              </div>

              {/* Main Text */}
              <div className="space-y-3">
                <h2 className="text-3xl font-semibold text-slate-800">
                  {isSearching ? 'Analyzing your image...' : 'Find looks you will love—start with an image.'}
                </h2>
                <p className="text-lg text-slate-500 italic font-light">
                  {isSearching ? 'Please wait while we search for similar products' : 'Drop a pic—your next outfit is waiting!'}
                </p>
              </div>

              {/* Status Message */}
              {statusMessage && (
                <div className={`
                  p-3 rounded-lg text-sm font-medium
                  ${statusMessage.includes('failed') || statusMessage.includes('error') || statusMessage.includes('Cannot connect')
                    ? 'bg-red-50 text-red-700 border border-red-200' 
                    : statusMessage.includes('Found')
                    ? 'bg-green-50 text-green-700 border border-green-200'
                    : 'bg-blue-50 text-blue-700 border border-blue-200'
                  }
                `}>
                  {statusMessage}
                </div>
              )}

              {/* Upload Button */}
              <div className="pt-4">
                <label className={`
                  inline-flex items-center gap-2 px-8 py-4 
                  bg-gradient-to-r from-amber-600 to-amber-500
                  hover:from-amber-700 hover:to-amber-600
                  text-white font-medium rounded-2xl
                  cursor-pointer transition-all duration-300
                  hover:shadow-xl hover:shadow-amber-500/25
                  transform hover:scale-105
                  ${isSearching || backendStatus !== 'connected' ? 'opacity-50 cursor-not-allowed' : ''}
                `}>
                  {isSearching ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Upload className="w-5 h-5" />
                  )}
                  {isSearching ? 'Searching...' : 'Choose Image'}
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                    disabled={isSearching || backendStatus !== 'connected'}
                  />
                </label>
              </div>

              {/* Supported formats */}
              <p className="text-sm text-slate-400 mt-4">
                Supports JPG, PNG, WebP, and GIF
              </p>
            </div>
          </div>
        ) : (
          /* Text Search Zone */
          <div className="glass-panel rounded-3xl p-12">
            <form onSubmit={handleTextSearch} className="space-y-6">
              <div className="mx-auto w-20 h-20 rounded-full bg-amber-50 text-amber-500 flex items-center justify-center">
                <SearchIcon className="w-10 h-10" />
              </div>

              <div className="space-y-3">
                <h2 className="text-3xl font-semibold text-slate-800">
                  Search for fashion items
                </h2>
                <p className="text-lg text-slate-500 italic font-light">
                  Describe what you're looking for...
                </p>
              </div>

              <div className="relative mb-4">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="e.g. 'red summer dress' or 'black leather jacket'"
                  className="w-full px-6 py-4 pr-16 rounded-2xl border border-amber-200 focus:border-amber-400 focus:ring-2 focus:ring-amber-200 outline-none transition-all"
                  disabled={isSearching || backendStatus !== 'connected'}
                />
                <button
                  type="submit"
                  disabled={!searchQuery.trim() || isSearching || backendStatus !== 'connected'}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-amber-500 text-white p-2 rounded-full hover:bg-amber-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  {isSearching ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <SearchIcon className="w-5 h-5" />
                  )}
                </button>
              </div>

              {/* Status Message */}
              {statusMessage && (
                <div className={`
                  p-3 rounded-lg text-sm font-medium
                  ${statusMessage.includes('failed') || statusMessage.includes('error')
                    ? 'bg-red-50 text-red-700 border border-red-200' 
                    : 'bg-green-50 text-green-700 border border-green-200'
                  }
                `}>
                  {statusMessage}
                </div>
              )}
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadZone;