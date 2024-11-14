import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown } from 'lucide-react';

const FinancialMetricCard = ({ title, value, trend = null }) => {
  const isPositive = trend === 'up';
  return (
    <Card className="bg-white">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {trend && (
          <div className={`rounded-full p-1 ${isPositive ? 'bg-green-100' : 'bg-red-100'}`}>
            {isPositive ? (
              <TrendingUp className="h-4 w-4 text-green-600" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-600" />
            )}
          </div>
        )}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
      </CardContent>
    </Card>
  );
};

const FinancialDashboard = ({ metrics }) => {
  // Add prop type checking
  if (!metrics) {
    return <div>Loading financial data...</div>;
  }
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatRatio = (value) => {
    return Number(value).toFixed(2);
  };

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <FinancialMetricCard 
          title="Debt to Equity" 
          value={formatRatio(metrics.debtToEquity)}
          trend={metrics.debtToEquity < 2 ? 'up' : 'down'}
        />
        <FinancialMetricCard 
          title="Cash Reserves" 
          value={formatCurrency(metrics.cashReserves)}
          trend={metrics.cashReserves > 0 ? 'up' : 'down'}
        />
        <FinancialMetricCard 
          title="Working Capital" 
          value={formatCurrency(metrics.workingCapital)}
          trend={metrics.workingCapital > 0 ? 'up' : 'down'}
        />
        <FinancialMetricCard 
          title="Free Cash Flow Margin" 
          value={`${formatRatio(metrics.freeCashFlowMargin)}%`}
          trend={metrics.freeCashFlowMargin > 0 ? 'up' : 'down'}
        />
      </div>

      <Card className="bg-white">
        <CardHeader>
          <CardTitle>Financial Health Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={[
                  { name: 'Debt/Equity', value: metrics.debtToEquity },
                  { name: 'FCF Margin', value: metrics.freeCashFlowMargin }
                ]}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#4f46e5" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FinancialDashboard;