import React, { useEffect, useState } from 'react';
import { Plus, Trash2, Eye, TrendingUp, TrendingDown } from 'lucide-react';
import { usePortfolioStore } from '../store/portfolioStore';

const WatchlistPage: React.FC = () => {
  const { watchlists, fetchWatchlists, createWatchlist, addToWatchlist, removeFromWatchlist, isLoading } = usePortfolioStore();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newWatchlistName, setNewWatchlistName] = useState('');
  const [newStockSymbol, setNewStockSymbol] = useState<{ [key: number]: string }>({});

  useEffect(() => {
    fetchWatchlists();
  }, []);

  const handleCreateWatchlist = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newWatchlistName.trim()) return;

    await createWatchlist(newWatchlistName.trim());
    setNewWatchlistName('');
    setShowCreateModal(false);
  };

  const handleAddStock = async (watchlistId: number) => {
    const symbol = newStockSymbol[watchlistId];
    if (!symbol || !symbol.trim()) return;

    await addToWatchlist(watchlistId, symbol.toUpperCase());
    setNewStockSymbol({ ...newStockSymbol, [watchlistId]: '' });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Watchlists</h1>
          <p className="text-gray-600 mt-1">Track stocks you're interested in</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          <Plus size={20} />
          <span>Create Watchlist</span>
        </button>
      </div>

      {/* Watchlists Grid */}
      {isLoading ? (
        <div className="p-8 text-center">
          <p className="text-gray-600">Loading watchlists...</p>
        </div>
      ) : watchlists.length === 0 ? (
        <div className="p-8 text-center bg-white rounded-xl border border-gray-200">
          <Eye className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 mb-4">No watchlists yet</p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            Create your first watchlist
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {watchlists.map((watchlist) => (
            <div
              key={watchlist.id}
              className="bg-white rounded-xl border border-gray-200 overflow-hidden"
            >
              <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">{watchlist.name}</h2>
                <span className="text-sm text-gray-500">
                  {watchlist.stocks?.length || 0} stocks
                </span>
              </div>

              <div className="p-4">
                {/* Add Stock Input */}
                <div className="flex space-x-2 mb-4">
                  <input
                    type="text"
                    value={newStockSymbol[watchlist.id] || ''}
                    onChange={(e) =>
                      setNewStockSymbol({ ...newStockSymbol, [watchlist.id]: e.target.value })
                    }
                    onKeyPress={(e) => e.key === 'Enter' && handleAddStock(watchlist.id)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    placeholder="Add stock symbol (e.g., TCS.NS)"
                  />
                  <button
                    onClick={() => handleAddStock(watchlist.id)}
                    className="px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-sm"
                  >
                    Add
                  </button>
                </div>

                {/* Stocks List */}
                {watchlist.stocks && watchlist.stocks.length > 0 ? (
                  <div className="space-y-2">
                    {watchlist.stocks.map((stock: any, index: number) => (
                      <div
                        key={index}
                        className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-lg"
                      >
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <TrendingUp size={16} className="text-blue-600" />
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">{stock.symbol}</p>
                            <p className="text-xs text-gray-500">{stock.name || 'Stock'}</p>
                          </div>
                        </div>
                        <button
                          onClick={() => removeFromWatchlist(watchlist.id, stock.id || index)}
                          className="text-red-600 hover:text-red-700 p-1"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <p className="text-gray-500 text-sm">No stocks in this watchlist</p>
                    <p className="text-gray-400 text-xs mt-1">Add stocks to track them</p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Watchlist Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Create New Watchlist</h2>
            <form onSubmit={handleCreateWatchlist} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Watchlist Name
                </label>
                <input
                  type="text"
                  value={newWatchlistName}
                  onChange={(e) => setNewWatchlistName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Long-term Investments, Swing Trades, IPO Watchlist"
                  required
                />
              </div>
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default WatchlistPage;
