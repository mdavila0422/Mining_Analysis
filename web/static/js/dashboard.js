// static/js/dashboard.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import FinancialDashboard from './components/FinancialDashboard';

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('financial-dashboard');
    if (container) {
        const root = createRoot(container);
        // Use the new variable name
        root.render(<FinancialDashboard metrics={window.financialMetricsData} />);
    }
});