# web/analysis/views.py
import sys
from pathlib import Path
from django.shortcuts import render
from django.utils import timezone

# Add the src directory to Python path
src_path = Path(__file__).resolve().parent.parent.parent / 'src'
sys.path.append(str(src_path))

from data.sources.financial_source import FinancialDataSource

def home(request):
    return render(request, 'analysis/home.html')

def search_company(request):
    symbol = request.GET.get('symbol', '').upper()
    if not symbol:
        return render(request, 'analysis/home.html')
        
    financial_source = FinancialDataSource()
    metrics = financial_source.fetch_data(symbol)
    
    if not metrics:
        return render(request, 'analysis/home.html', {'error': 'Company not found'})
    
    # Create a simple company dict instead of using a model
    company = {
        'symbol': symbol,
        'last_updated': timezone.now()
    }
    
    context = {
        'company': company,
        'metrics': metrics  # Use the metrics directly from FinancialDataSource
    }
    
    return render(request, 'analysis/company_detail.html', context)