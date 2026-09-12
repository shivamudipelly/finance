import { create } from 'zustand';

export interface Stock {
  symbol: string;
  name: string;
  sector?: string;
  industry?: string;
}

export interface PortfolioStock {
  id: number;
  symbol: string;
  quantity: number;
  avgPrice: number;
  currentPrice?: number;
  currentValue?: number;
  pnl?: number;
  pnlPercent?: number;
}

export interface Watchlist {
  id: number;
  name: string;
  stocks: Stock[];
}

interface PortfolioState {
  stocks: PortfolioStock[];
  watchlists: Watchlist[];
  isLoading: boolean;
  fetchPortfolio: () => Promise<void>;
  addToPortfolio: (symbol: string, quantity: number, avgPrice: number) => Promise<void>;
  removeFromPortfolio: (id: number) => Promise<void>;
  fetchWatchlists: () => Promise<void>;
  createWatchlist: (name: string) => Promise<void>;
  addToWatchlist: (watchlistId: number, symbol: string) => Promise<void>;
  removeFromWatchlist: (watchlistId: number, stockId: number) => Promise<void>;
}

export const usePortfolioStore = create<PortfolioState>((set, get) => ({
  stocks: [],
  watchlists: [],
  isLoading: false,

  fetchPortfolio: async () => {
    set({ isLoading: true });
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/portfolio', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        set({ stocks: data.holdings || [], isLoading: false });
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      set({ isLoading: false });
    }
  },

  addToPortfolio: async (symbol: string, quantity: number, avgPrice: number) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/portfolio/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ symbol, quantity, avg_price: avgPrice }),
      });

      if (response.ok) {
        get().fetchPortfolio();
      }
    } catch (error) {
      console.error('Failed to add to portfolio', error);
    }
  },

  removeFromPortfolio: async (id: number) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/portfolio/remove/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        get().fetchPortfolio();
      }
    } catch (error) {
      console.error('Failed to remove from portfolio', error);
    }
  },

  fetchWatchlists: async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/watchlist', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        set({ watchlists: data.watchlists || [] });
      }
    } catch (error) {
      console.error('Failed to fetch watchlists', error);
    }
  },

  createWatchlist: async (name: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/watchlist/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ name }),
      });

      if (response.ok) {
        get().fetchWatchlists();
      }
    } catch (error) {
      console.error('Failed to create watchlist', error);
    }
  },

  addToWatchlist: async (watchlistId: number, symbol: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/watchlist/${watchlistId}/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ symbol }),
      });

      if (response.ok) {
        get().fetchWatchlists();
      }
    } catch (error) {
      console.error('Failed to add to watchlist', error);
    }
  },

  removeFromWatchlist: async (watchlistId: number, stockId: number) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/watchlist/${watchlistId}/remove/${stockId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        get().fetchWatchlists();
      }
    } catch (error) {
      console.error('Failed to remove from watchlist', error);
    }
  },
}));
