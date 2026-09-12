import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  register: async (username: string, password: string, email?: string) => {
    const response = await api.post('/auth/register', { username, password, email });
    return response.data;
  },

  login: async (username: string, password: string) => {
    const response = await api.post('/auth/login', { username, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

export const stockService = {
  search: async (query: string) => {
    const response = await api.get(`/stocks/search?q=${encodeURIComponent(query)}`);
    return response.data;
  },

  getQuote: async (symbol: string) => {
    const response = await api.get(`/stocks/${encodeURIComponent(symbol)}/quote`);
    return response.data;
  },

  getHistoricalData: async (symbol: string, period: string = '1mo') => {
    const response = await api.get(`/stocks/${encodeURIComponent(symbol)}/history?period=${period}`);
    return response.data;
  },

  getDetails: async (symbol: string) => {
    const response = await api.get(`/stocks/${encodeURIComponent(symbol)}/details`);
    return response.data;
  },
};

export const chatService = {
  analyze: async (query: string) => {
    const response = await api.post('/chat/analyze', { query });
    return response.data;
  },
};

export const portfolioService = {
  getHoldings: async () => {
    const response = await api.get('/portfolio');
    return response.data;
  },

  addStock: async (symbol: string, quantity: number, avgPrice: number) => {
    const response = await api.post('/portfolio/add', { symbol, quantity, avg_price: avgPrice });
    return response.data;
  },

  removeStock: async (id: number) => {
    const response = await api.delete(`/portfolio/remove/${id}`);
    return response.data;
  },

  updateStock: async (id: number, quantity?: number, avgPrice?: number) => {
    const response = await api.put(`/portfolio/update/${id}`, { quantity, avg_price: avgPrice });
    return response.data;
  },
};

export const watchlistService = {
  getWatchlists: async () => {
    const response = await api.get('/watchlist');
    return response.data;
  },

  createWatchlist: async (name: string) => {
    const response = await api.post('/watchlist/create', { name });
    return response.data;
  },

  addToWatchlist: async (watchlistId: number, symbol: string) => {
    const response = await api.post(`/watchlist/${watchlistId}/add`, { symbol });
    return response.data;
  },

  removeFromWatchlist: async (watchlistId: number, stockId: number) => {
    const response = await api.delete(`/watchlist/${watchlistId}/remove/${stockId}`);
    return response.data;
  },

  deleteWatchlist: async (watchlistId: number) => {
    const response = await api.delete(`/watchlist/${watchlistId}`);
    return response.data;
  },
};

export const marketService = {
  getOverview: async () => {
    const response = await api.get('/market/overview');
    return response.data;
  },

  getIndices: async () => {
    const response = await api.get('/market/indices');
    return response.data;
  },

  getTopGainers: async () => {
    const response = await api.get('/market/top-gainers');
    return response.data;
  },

  getTopLosers: async () => {
    const response = await api.get('/market/top-losers');
    return response.data;
  },
};

export default api;
