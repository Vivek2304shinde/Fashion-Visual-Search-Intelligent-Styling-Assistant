interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

const API_BASE_URL = 'http://localhost:8000';

class AIStylistService {
  private currentSessionId: string | null = null;
  private messages: ChatMessage[] = [];
  private readyForRecommendation: boolean = false;
  private collectedInfo: any = {};

  async startConversation(initialMessage: string = "Hello, I need styling help"): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/stylist/conversation/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initial_message: initialMessage })
      });

      const data = await response.json();
      
      if (data.success) {
        this.currentSessionId = data.session_id;
        this.messages = [{
          role: 'assistant',
          content: data.message,
          timestamp: new Date().toISOString()
        }];
        this.readyForRecommendation = data.ready_for_recommendation || false;
      }
      
      return data;
    } catch (error) {
      console.error('Failed to start conversation:', error);
      throw error;
    }
  }

  async sendMessage(message: string): Promise<any> {
    if (!this.currentSessionId) {
      throw new Error('No active session');
    }

    try {
      // Add user message to local state
      this.messages.push({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      });

      const response = await fetch(`${API_BASE_URL}/api/stylist/conversation/${this.currentSessionId}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      
      if (data.success) {
        // Add assistant message to local state
        this.messages.push({
          role: 'assistant',
          content: data.message,
          timestamp: new Date().toISOString()
        });
        this.readyForRecommendation = data.ready_for_recommendation || false;
        this.collectedInfo = data.collected_info || {};
      }
      
      return data;
    } catch (error) {
      console.error('Failed to send message:', error);
      throw error;
    }
  }

  async getRecommendations(): Promise<any> {
    if (!this.currentSessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/stylist/conversation/${this.currentSessionId}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Failed to get recommendations:', error);
      throw error;
    }
  }

  getMessages(): ChatMessage[] {
    return this.messages;
  }

  isReadyForRecommendations(): boolean {
    return this.readyForRecommendation;
  }

  getCollectedInfo(): any {
    return this.collectedInfo;
  }

  clearSession(): void {
    this.currentSessionId = null;
    this.messages = [];
    this.readyForRecommendation = false;
    this.collectedInfo = {};
  }
}

export const aiStylistService = new AIStylistService();