import { create } from 'zustand';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  analysis?: {
    intent?: string;
    timeframe?: string;
    objective?: string;
    evidence?: string[];
    risks?: string[];
    conclusion?: string;
  };
}

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  sendMessage: (content: string) => Promise<void>;
  clearChat: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,

  sendMessage: async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    set((state) => ({
      messages: [...state.messages, userMessage],
      isLoading: true,
    }));

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/chat/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ query: content }),
      });

      if (!response.ok) {
        throw new Error('Failed to get analysis');
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response || 'No response received',
        timestamp: new Date(),
        analysis: {
          intent: data.intent,
          timeframe: data.timeframe,
          objective: data.objective,
          evidence: data.evidence,
          risks: data.risks,
          conclusion: data.conclusion,
        },
      };

      set((state) => ({
        messages: [...state.messages, assistantMessage],
        isLoading: false,
      }));
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };

      set((state) => ({
        messages: [...state.messages, errorMessage],
        isLoading: false,
      }));
    }
  },

  clearChat: () => set({ messages: [] }),
}));
