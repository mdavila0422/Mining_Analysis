import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

import pandas as pd
from data.sources.financial_source import FinancialDataSource

def main():
    print("Starting Mining Stock Analysis Tool...")
    
    # Create an instance of FinancialDataSource
    financial_source = FinancialDataSource()
    
    # List of mining companies to analyze
    mining_tickers = ['VALE']
    
    for ticker in mining_tickers:
        print(f"\nAnalyzing {ticker}...")
        try:
            metrics = financial_source.fetch_data(ticker)
            
            if metrics:
                print("\nFinancial Metrics:")
                print(f"Debt to Equity: {metrics.debt_to_equity:.2f}")
                print(f"Cash Reserves: ${metrics.cash_reserves:,.2f}")
                print(f"Working Capital: ${metrics.working_capital:,.2f}")
                print(f"Free Cash Flow Margin: {metrics.free_cash_flow_margin:.2%}")
                print(f"Capital Expenditures: ${metrics.capex:,.2f}")
                print(f"Dividend Yield: {metrics.dividend_yield:.2%}")
            else:
                print(f"Unable to fetch financial data for {ticker}")
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            continue

if __name__ == "__main__":
    main()