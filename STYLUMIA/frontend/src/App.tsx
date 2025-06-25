import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import ResultsPage from "./components/ResultsPage"; // Adjust path as needed
import { useLocation } from "react-router-dom";

const queryClient = new QueryClient();


const ResultsPageWrapper = () => {
  const location = useLocation();
  return (
    <ResultsPage 
      searchResults={location.state?.searchResults}
      searchMode={location.state?.searchMode}
      searchQuery={location.state?.searchQuery}
      uploadedImage={location.state?.uploadedImage}
    />
  );
};


const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
           <Route path="/results" element={<ResultsPageWrapper />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
