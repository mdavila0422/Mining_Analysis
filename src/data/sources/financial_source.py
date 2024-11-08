import yfinance as yf
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from .session_manager import YFinanceSessionManager

@dataclass
class FinancialMetrics:
    debt_to_equity: float
    cash_reserves: float
    working_capital: float
    free_cash_flow_margin: float
    capex: float
    dividend_yield: float
    hedging_percentage: float

class FinancialDataSource:
    def __init__(self):
        self.session_manager = YFinanceSessionManager()

    def fetch_data(self, symbol: str) -> Optional[FinancialMetrics]:
        """
        Fetch financial data for a given stock symbol using yfinance.
        
        Args:
            symbol (str): Stock symbol to fetch data for.
        
        Returns:
            Optional[FinancialMetrics]: Financial metrics for the given stock, or None if data is unavailable.
        """
        if not symbol:
            return None
            
        try:
            # Get ticker using the session manager
            stock = self.session_manager.get_ticker(symbol)
            if stock is None:
                return None
            
            # Fetch all required data first
            try:
                financials = stock.get_financials()
                balance_sheet = stock.get_balance_sheet()
                cashflow = stock.get_cashflow()
                info = stock.info
                
            except Exception as e:
                print(f"Error fetching data: {e}")
                return None

            # Verify we have all required data
            if financials.empty or balance_sheet.empty or cashflow.empty:
                print("One or more DataFrames are empty")
                return None

            try:
                # Get the most recent date (first column)
                recent_date = financials.columns[0]

                # Calculate total debt (use TotalDebt if available, otherwise sum components)
                if 'TotalDebt' in balance_sheet.index:
                    total_debt = float(balance_sheet.loc['TotalDebt', recent_date])
                else:
                    # Fallback to summing components
                    long_term_debt = float(balance_sheet.loc['LongTermDebt', recent_date]) if 'LongTermDebt' in balance_sheet.index else 0
                    current_debt = float(balance_sheet.loc['CurrentDebt', recent_date]) if 'CurrentDebt' in balance_sheet.index else 0
                    total_debt = long_term_debt + current_debt

                # Get total equity
                total_equity = float(balance_sheet.loc['StockholdersEquity', recent_date])
                debt_to_equity = total_debt / total_equity if total_equity != 0 else None

                # Get cash and cash equivalents
                if 'CashAndCashEquivalents' in balance_sheet.index:
                    cash_reserves = float(balance_sheet.loc['CashAndCashEquivalents', recent_date])
                else:
                    cash_reserves = float(balance_sheet.loc['CashFinancial', recent_date])
                
                # Working Capital (use direct field if available)
                if 'WorkingCapital' in balance_sheet.index:
                    working_capital = float(balance_sheet.loc['WorkingCapital', recent_date])
                else:
                    current_assets = float(balance_sheet.loc['CurrentAssets', recent_date])
                    current_liabilities = float(balance_sheet.loc['CurrentLiabilities', recent_date])
                    working_capital = current_assets - current_liabilities

                # Get Free Cash Flow and calculate margin
                free_cash_flow = float(cashflow.loc['FreeCashFlow', recent_date])
                total_revenue = float(financials.loc['TotalRevenue', recent_date])
                free_cash_flow_margin = free_cash_flow / total_revenue if total_revenue != 0 else None

                # Get capital expenditures
                capex = float(cashflow.loc['CapitalExpenditure', recent_date])
                
                # Get dividend yield
                dividend_yield = float(info.get('dividendYield', 0))
                
                # If any critical calculations returned None, return None
                if any(x is None for x in [debt_to_equity, free_cash_flow_margin]):
                    print("Critical calculations returned None")
                    return None

                return FinancialMetrics(
                    debt_to_equity=debt_to_equity,
                    cash_reserves=cash_reserves,
                    working_capital=working_capital,
                    free_cash_flow_margin=free_cash_flow_margin,
                    capex=capex,
                    dividend_yield=dividend_yield,
                    hedging_percentage=0.0  # Default value as we don't have this data yet
                )
                
            except (KeyError, IndexError, ValueError) as e:
                print(f"Error calculating metrics: {e}")
                return None
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None