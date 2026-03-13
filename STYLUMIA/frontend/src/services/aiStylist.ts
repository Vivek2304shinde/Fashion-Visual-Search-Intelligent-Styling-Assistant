
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface StylistResponse {
  success: boolean;
  session_id: string;
  message: string;
  ready_for_recommendation: boolean;
  collected_info: Record<string, any>;
}

interface ChatResponse {
  success: boolean;
  session_id: string;
  message: string;
  collected_info: Record<string, any>;
  ready_for_recommendation: boolean;
}

interface OutfitPlan {
  outfit_plan: Record<string, any>;
  styling_advice: string;
  color_rationale?: string;
  trend_notes?: string;
}

interface RecommendationResponse {
  success: boolean;
  outfit_plan: Record<string, any>;
  styling_advice: string;
  products_found?: Record<string, number>;
  products?: Record<string, any[]>;
}

const API_BASE_URL = 'http://localhost:8000';

class AIStylistService {
  private sessionId: string | null = null;
  private messages: Message[] = [];
  private collectedInfo: Record<string, any> = {};

  async startConversation(initialMessage: string = "Hello, I need styling help", gender?: string): Promise<StylistResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/stylist/conversation/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          initial_message: initialMessage,
          gender: gender 
        })
      });

      if (!response.ok) throw new Error('Failed to start conversation');
      
      const data = await response.json();
      this.sessionId = data.session_id;
      this.collectedInfo = data.collected_info || {};
      
      // Add messages to history
      this.messages = [
        { id: 'welcome', role: 'assistant', content: data.message }
      ];
      
      return data;
    } catch (error) {
      console.error('Error starting conversation:', error);
      throw error;
    }
  }

  async sendMessage(message: string): Promise<ChatResponse> {
    if (!this.sessionId) {
      await this.startConversation();
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/stylist/conversation/${this.sessionId}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      if (!response.ok) throw new Error('Failed to send message');
      
      const data = await response.json();
      
      // Update collected info
      this.collectedInfo = data.collected_info || {};
      
      // Add messages to history
      this.messages.push(
        { id: `user-${Date.now()}`, role: 'user', content: message },
        { id: `assistant-${Date.now()}`, role: 'assistant', content: data.message }
      );
      
      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getRecommendations(): Promise<RecommendationResponse> {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/stylist/conversation/${this.sessionId}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{}'
      });

      if (!response.ok) throw new Error('Failed to get recommendations');
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error getting recommendations:', error);
      throw error;
    }
  }

  async getSessionProducts(): Promise<Record<string, any[]>> {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/stylist/conversation/${this.sessionId}/products`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });

      if (!response.ok) throw new Error('Failed to get products');
      
      const data = await response.json();
      return data.products || {};
    } catch (error) {
      console.error('Error getting products:', error);
      throw error;
    }
  }

  isReadyForRecommendations(): boolean {
    // Check if we have minimum required info (occasion + gender + at least 2 other details)
    const hasOccasion = !!this.collectedInfo.occasion;
    const hasGender = !!this.collectedInfo.gender;
    
    const otherFields = ['style_preference', 'color_preference', 'budget_tier', 'season']
      .filter(field => !!this.collectedInfo[field]).length;
    
    return hasOccasion && hasGender && otherFields >= 1;
  }

  getMessages(): Message[] {
    return this.messages;
  }

  getSessionId(): string | null {
    return this.sessionId;
  }

  getCollectedInfo(): Record<string, any> {
    return this.collectedInfo;
  }

  reset(): void {
    this.sessionId = null;
    this.messages = [];
    this.collectedInfo = {};
  }
}

export const aiStylistService = new AIStylistService();