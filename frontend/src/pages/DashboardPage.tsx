import React from 'react';
import { TrendingUp, TrendingDown, Activity, DollarSign } from 'lucide-react';

const DashboardPage: React.FC = () => {
  // Mock data for now - will be replaced with real API calls
  const marketOverview = {
    nifty50: { value: 24580.35, change: 125.40, changePercent: 0.51 },
    bankNifty: { value: 53420.15, change: -85.20, changePercent: -0.16 },
    sensex: { value: 80850.75, change: 420.30, changePercent: 0.52 },
    midcap: { value: 15680.90, change: 45.60, changePercent: 0.29 },
  };

  const topGainers = [
    { symbol: 'RELIANCE.NS', price: 2850.40, change: 3.2 },
    { symbol: 'INFY.NS', price: 1680.25, change: 2.8 },
    { symbol: 'HDFCBANK.NS', price: 1720.50, change: 2.5 },
  ];

  const topLosers = [
    { symbol: 'TATASTEEL.NS', price: 145.30, change: -2.1 },
    { symbol: 'JSWSTEEL.NS', price: 890.75, change: -1.8 },
    { symbol: 'ADANIENT.NS', price: 2340.60, change: -1.5 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Market Dashboard</h1>
        <p className="text-gray-600 mt-1">Real-time market overview and insights</p>
      </div>

      {/* Market Indices */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <IndexCard
          name="NIFTY 50"
          value={marketOverview.nifty50.value}
          change={marketOverview.nifty50.change}
          changePercent={marketOverview.nifty50.changePercent}
        />
        <IndexCard
          name="BANK NIFTY"
          value={marketOverview.bankNifty.value}
          change={marketOverview.bankNifty.change}
          changePercent={marketOverview.bankNifty.changePercent}
        />
        <IndexCard
          name="SENSEX"
          value={marketOverview.sensex.value}
          change={marketOverview.sensex.change}
          changePercent={marketOverview.sensex.changePercent}
        />
        <IndexCard
          name="MIDCAP"
          value={marketOverview.midcap.value}
          change={marketOverview.midcap.change}
          changePercent={marketOverview.midcap.changePercent}
        />
      </div>

      {/* Top Gainers & Losers */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Gainers */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp className="w-5 h-5 text-green-600" />
            <h2 className="text-lg font-semibold text-gray-900">Top Gainers</h2>
          </div>
          <div className="space-y-3">
            {topGainers.map((stock) => (
              <div
                key={stock.symbol}
                className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
              >
                <div>
                  <p className="font-medium text-gray-900">{stock.symbol}</p>
                  <p className="text-sm text-gray-600">₹{stock.price.toFixed(2)}</p>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-sm font-medium rounded">
                  +{stock.change}%
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Losers */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            <TrendingDown className="w-5 h-5 text-red-600" />
            <h2 className="text-lg font-semibold text-gray-900">Top Losers</h2>
          </div>
          <div className="space-y-3">
            {topLosers.map((stock) => (
              <div
                key={stock.symbol}
                className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
              >
                <div>
                  <p className="font-medium text-gray-900">{stock.symbol}</p>
                  <p className="text-sm text-gray-600">₹{stock.price.toFixed(2)}</p>
                </div>
                <span className="px-2 py-1 bg-red-100 text-red-800 text-sm font-medium rounded">
                  {stock.change}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Market Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard
          icon={<Activity className="w-6 h-6 text-blue-600" />}
          label="Market Breadth"
          value="Positive"
          subtext="Advancers: 1,245 | Decliners: 892"
        />
        <StatCard
          icon={<DollarSign className="w-6 h-6 text-green-600" />}
          label="Foreign Flow"
          value="₹2,450 Cr"
          subtext="Net Buy (Today)"
        />
        <StatCard
          icon={<TrendingUp className="w-6 h-6 text-purple-600" />}
          label="VIX"
          value="12.45"
          subtext="-2.3% (Low Volatility)"
        />
      </div>

      {/* AI Insights Placeholder */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">AI Market Insights</h2>
        <p className="text-gray-700 mb-4">
          The Indian market is showing resilience with NIFTY testing new highs. Banking sector 
          shows mixed signals while IT stocks demonstrate strength. Market breadth remains 
          positive with advance-decline ratio favoring buyers.
        </p>
        <div className="flex flex-wrap gap-2">
          <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
            Bullish Trend
          </span>
          <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
            Low Volatility
          </span>
          <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full">
            Sector Rotation
          </span>
        </div>
      </div>
    </div>
  );
};

interface IndexCardProps {
  name: string;
  value: number;
  change: number;
  changePercent: number;
}

const IndexCard: React.FC<IndexCardProps> = ({ name, value, change, changePercent }) => {
  const isPositive = change >= 0;
  
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4">
      <p className="text-sm font-medium text-gray-600">{name}</p>
      <p className="text-2xl font-bold text-gray-900 mt-1">{value.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</p>
      <div className={`flex items-center mt-2 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
        {isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
        <span className="ml-1 text-sm font-medium">
          {isPositive ? '+' : ''}{change.toFixed(2)} ({isPositive ? '+' : ''}{changePercent.toFixed(2)}%)
        </span>
      </div>
    </div>
  );
};

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  subtext: string;
}

const StatCard: React.FC<StatCardProps> = ({ icon, label, value, subtext }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-4 flex items-start space-x-3">
    <div className="p-2 bg-gray-50 rounded-lg">{icon}</div>
    <div>
      <p className="text-sm text-gray-600">{label}</p>
      <p className="text-lg font-semibold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500">{subtext}</p>
    </div>
  </div>
);

export default DashboardPage;
