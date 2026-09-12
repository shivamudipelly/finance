import React, { useEffect, useState } from 'react';
import { Plus, Trash2, TrendingUp, TrendingDown } from 'lucide-react';
import { usePortfolioStore } from '../store/portfolioStore';

const PortfolioPage: React.FC = () => {
  const { stocks, fetchPortfolio, addToPortfolio, removeFromPortfolio, isLoading } = usePortfolioStore();
  const [showAddModal, setShowAddModal] = useState(false);
  const [newStock, setNewStock] = useState({ symbol: '', quantity: '', avgPrice: '' });

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const handleAddStock = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newStock.symbol || !newStock.quantity || !newStock.avgPrice) return;

    await addToPortfolio(
      newStock.symbol.toUpperCase(),
      parseFloat(newStock.quantity),
      parseFloat(newStock.avgPrice)
    );

    setNewStock({ symbol: '', quantity: '', avgPrice: '' });
    setShowAddModal(false);
  };

  const totalValue = stocks.reduce((sum, stock) => sum + (stock.currentValue || 0), 0);
  const totalCost = stocks.reduce((sum, stock) => sum + (stock.avgPrice * stock.quantity), 0);
  const totalPnL = totalValue - totalCost;
  const totalPnLPercent = totalCost > 0 ? (totalPnL / totalCost) * 100 : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Portfolio</h1>
          <p className="text-gray-600 mt-1">Track your holdings and performance</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          <Plus size={20} />
          <span>Add Stock</span>
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <p className="text-sm text-gray-600">Total Value</p>
          <p className="text-2xl font-bold text-gray-900">₹{totalValue.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <p className="text-sm text-gray-600">Total Cost</p>
          <p className="text-2xl font-bold text-gray-900">₹{totalCost.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <p className="text-sm text-gray-600">Total P&L</p>
          <div className={`flex items-center mt-1 ${totalPnL >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {totalPnL >= 0 ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
            <p className="text-2xl font-bold ml-1">
              ₹{Math.abs(totalPnL).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
            </p>
          </div>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <p className="text-sm text-gray-600">P&L %</p>
          <div className={`flex items-center mt-1 ${totalPnLPercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {totalPnLPercent >= 0 ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
            <p className="text-2xl font-bold ml-1">
              {totalPnLPercent >= 0 ? '+' : ''}{totalPnLPercent.toFixed(2)}%
            </p>
          </div>
        </div>
      </div>

      {/* Holdings Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Holdings</h2>
        </div>
        
        {isLoading ? (
          <div className="p-8 text-center">
            <p className="text-gray-600">Loading portfolio...</p>
          </div>
        ) : stocks.length === 0 ? (
          <div className="p-8 text-center">
            <p className="text-gray-600 mb-4">No holdings yet</p>
            <button
              onClick={() => setShowAddModal(true)}
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Add your first stock
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Symbol
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Quantity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avg Price
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Current Price
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Current Value
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    P&L
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {stocks.map((stock) => (
                  <tr key={stock.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-medium text-gray-900">{stock.symbol}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                      {stock.quantity}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                      ₹{stock.avgPrice.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                      ₹{stock.currentPrice?.toFixed(2) || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900 font-medium">
                      ₹{stock.currentValue?.toFixed(2) || '-'}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap ${stock.pnl && stock.pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {stock.pnl ? (
                        <>
                          ₹{stock.pnl.toFixed(2)} ({stock.pnlPercent?.toFixed(2)}%)
                        </>
                      ) : (
                        '-'
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <button
                        onClick={() => removeFromPortfolio(stock.id)}
                        className="text-red-600 hover:text-red-700 p-1"
                      >
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add Stock Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Add Stock to Portfolio</h2>
            <form onSubmit={handleAddStock} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Symbol (e.g., RELIANCE.NS)
                </label>
                <input
                  type="text"
                  value={newStock.symbol}
                  onChange={(e) => setNewStock({ ...newStock, symbol: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="RELIANCE.NS"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Quantity
                </label>
                <input
                  type="number"
                  value={newStock.quantity}
                  onChange={(e) => setNewStock({ ...newStock, quantity: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="10"
                  required
                  min="1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Average Price (₹)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={newStock.avgPrice}
                  onChange={(e) => setNewStock({ ...newStock, avgPrice: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="2500.00"
                  required
                  min="0.01"
                />
              </div>
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Add Stock
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PortfolioPage;
