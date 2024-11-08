import unittest
from unittest.mock import patch, MagicMock
from src.data.sources.financial_source import FinancialDataSource, FinancialMetrics
from src.data.sources.session_manager import YFinanceSessionManager
import pandas as pd
import yfinance as yf

class TestFinancialDataSource(unittest.TestCase):
    def setUp(self):
        self.data_source = FinancialDataSource()
        
    def create_mock_stock_data(self):
        """Helper method to create mock financial data"""
        dates = ['2023-12-31']
        
        mock_financials = pd.DataFrame({
            dates[0]: [2000000]  # Just revenue, since TotalDebt comes from balance sheet
        }, index=['TotalRevenue'])
        
        mock_balance_sheet = pd.DataFrame({
            dates[0]: [1000000, 500000, 200000, 800000, 300000]
        }, index=['TotalDebt', 'StockholdersEquity', 'CashAndCashEquivalents', 'CurrentAssets', 'CurrentLiabilities'])
        
        mock_cashflow = pd.DataFrame({
            dates[0]: [400000, -100000]
        }, index=['FreeCashFlow', 'CapitalExpenditure'])
        
        return mock_financials, mock_balance_sheet, mock_cashflow

    @patch('yfinance.Ticker')
    def test_successful_data_fetch_with_fallback(self, mock_yf_ticker):
        """Test successful retrieval and processing of financial data using fallback calculations"""
        # Setup mock data
        mock_financials, mock_balance_sheet, mock_cashflow = self.create_mock_stock_data()
        
        # Configure mock
        mock_ticker = MagicMock()
        mock_ticker.get_financials.return_value = mock_financials
        mock_ticker.get_balance_sheet.return_value = mock_balance_sheet
        mock_ticker.get_cashflow.return_value = mock_cashflow
        mock_ticker.info = {'dividendYield': 0.05}
        mock_yf_ticker.return_value = mock_ticker

        # Execute
        result = self.data_source.fetch_data('VALE')

        # Add debug output
        if result is None:
            print("\nDebug - Mock Data:")
            print(f"Balance Sheet:\n{mock_balance_sheet}")
            print(f"\nFinancials:\n{mock_financials}")
            print(f"\nCash Flow:\n{mock_cashflow}")
        else:
            print(f"\nDebug - Result metrics:")
            print(f"Debt to Equity: {result.debt_to_equity}")
            print(f"Cash Reserves: {result.cash_reserves}")
            print(f"Working Capital: {result.working_capital}")

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, FinancialMetrics)
        self.assertEqual(result.debt_to_equity, 2.0)  # (700000 + 300000) / 500000
        self.assertEqual(result.cash_reserves, 200000)
        self.assertEqual(result.working_capital, 500000)  # 800000-300000
        self.assertEqual(result.free_cash_flow_margin, 0.2)  # 400000/2000000
        self.assertEqual(result.capex, -100000)
        self.assertEqual(result.dividend_yield, 0.05)
        self.assertEqual(result.hedging_percentage, 0.0)

    @patch('yfinance.Ticker')
    def test_missing_data_handling(self, mock_yf_ticker):
        """Test handling of missing or incomplete data"""
        mock_ticker = MagicMock()
        mock_ticker.get_financials.side_effect = KeyError('Missing data')
        mock_yf_ticker.return_value = mock_ticker

        result = self.data_source.fetch_data('INVALID')
        self.assertIsNone(result)

    @patch('yfinance.Ticker')
    def test_api_error_handling(self, mock_yf_ticker):
        """Test handling of API errors"""
        mock_ticker = MagicMock()
        mock_ticker.get_financials.side_effect = Exception('API Error')
        mock_yf_ticker.return_value = mock_ticker

        result = self.data_source.fetch_data('VALE')
        self.assertIsNone(result)

    def test_invalid_symbol_handling(self):
        """Test handling of invalid stock symbols"""
        result = self.data_source.fetch_data('')
        self.assertIsNone(result)

    @patch('yfinance.Ticker')
    def test_zero_division_handling(self, mock_yf_ticker):
        """Test handling of zero division scenarios"""
        dates = ['2023-12-31']
        mock_financials = pd.DataFrame({
            dates[0]: [0]  # Zero revenue
        }, index=['TotalRevenue'])
        
        mock_balance_sheet = pd.DataFrame({
            dates[0]: [700000, 300000, 0, 200000, 800000, 300000]  # Zero equity
        }, index=[
            'LongTermDebt',
            'CurrentDebt',
            'StockholdersEquity',
            'CashAndCashEquivalents',
            'CurrentAssets',
            'CurrentLiabilities'
        ])
        
        mock_cashflow = pd.DataFrame({
            dates[0]: [400000, -100000]
        }, index=['FreeCashFlow', 'CapitalExpenditure'])

        mock_ticker = MagicMock()
        mock_ticker.get_financials.return_value = mock_financials
        mock_ticker.get_balance_sheet.return_value = mock_balance_sheet
        mock_ticker.get_cashflow.return_value = mock_cashflow
        mock_ticker.info = {'dividendYield': 0.05}
        mock_yf_ticker.return_value = mock_ticker

        result = self.data_source.fetch_data('VALE')
        self.assertIsNone(result)

    @patch('yfinance.Ticker')
    def test_missing_data_handling(self, mock_yf_ticker):
        """Test handling of missing or incomplete data"""
        mock_ticker = MagicMock()
        mock_ticker.get_financials.side_effect = KeyError('Missing data')
        mock_yf_ticker.return_value = mock_ticker

        result = self.data_source.fetch_data('INVALID')
        self.assertIsNone(result)

    @patch('yfinance.Ticker')
    def test_api_error_handling(self, mock_yf_ticker):
        """Test handling of API errors"""
        mock_ticker = MagicMock()
        mock_ticker.get_financials.side_effect = Exception('API Error')
        mock_yf_ticker.return_value = mock_ticker

        result = self.data_source.fetch_data('VALE')
        self.assertIsNone(result)

    def test_invalid_symbol_handling(self):
        """Test handling of invalid stock symbols"""
        result = self.data_source.fetch_data('')
        self.assertIsNone(result)

    @patch('yfinance.Ticker')
    def test_zero_division_handling(self, mock_yf_ticker):
        """Test handling of zero division scenarios"""
        dates = ['2023-12-31']
        mock_financials = pd.DataFrame({
            dates[0]: [1000000, 0]  # Zero revenue
        }, index=['TotalDebt', 'TotalRevenue'])
        
        mock_balance_sheet = pd.DataFrame({
            dates[0]: [0, 200000, 800000, 300000]  # Zero equity
        }, index=['StockholdersEquity', 'CashAndCashEquivalents', 'CurrentAssets', 'CurrentLiabilities'])
        
        mock_cashflow = pd.DataFrame({
            dates[0]: [400000, -100000]
        }, index=['FreeCashFlow', 'CapitalExpenditure'])

        mock_ticker = MagicMock()
        mock_ticker.get_financials.return_value = mock_financials
        mock_ticker.get_balance_sheet.return_value = mock_balance_sheet
        mock_ticker.get_cashflow.return_value = mock_cashflow
        mock_ticker.info = {'dividendYield': 0.05}
        mock_yf_ticker.return_value = mock_ticker

        result = self.data_source.fetch_data('VALE')
        self.assertIsNone(result)

class TestYFinanceSessionManager(unittest.TestCase):
    def setUp(self):
        self.session_manager = YFinanceSessionManager()

    def test_singleton_pattern(self):
        """Test that the session manager implements singleton pattern correctly"""
        another_manager = YFinanceSessionManager()
        self.assertIs(self.session_manager, another_manager)

    def test_session_initialization(self):
        """Test that the session is properly initialized"""
        session = self.session_manager.get_session()
        self.assertIsNotNone(session)
        self.assertEqual(session.headers['User-agent'], 'mining-analysis-tool/1.0')

    def test_get_ticker(self):
        """Test ticker creation with session"""
        ticker = self.session_manager.get_ticker('VALE')
        self.assertIsNotNone(ticker)

if __name__ == '__main__':
    unittest.main()