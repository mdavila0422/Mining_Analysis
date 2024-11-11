# Mining Stock Analysis Tool 📊

## Overview
A Python-based analysis tool for evaluating mining stocks using public financial APIs. This tool provides comprehensive analysis of financial metrics using publicly available data.

## Features
### Current Features
- **Financial Analysis**
  - Balance sheet strength indicators
  - Cash flow analysis
  - Dividend yield assessment
  - Financial ratios and metrics

### Planned Features
- **Operational Analysis** (On Hold - Awaiting Data Source)
  - Mining costs analysis (cash costs, AISC)
  - Asset quality assessment
  - Production profile evaluation

- **Risk Assessment** (On Hold - Awaiting Data Source)
  - Geographic/Political risk evaluation
  - Infrastructure access analysis
  - Market position assessment

## Installation

### Prerequisites
- Python 3.9 or higher
- Git

### Setup
1. Clone the repository
```bash
git clone https://github.com/mdavila0422/Mining_Analysis.git
cd Mining_Analysis
```

2. Create and activate virtual environment
```bash
python -m venv mining-env
# On Windows
mining-env\Scripts\activate
# On Unix or MacOS
source mining-env/bin/activate
```

3. Install required packages
```bash
pip install -r requirements.txt
```

## Project Structure
```
mining-stocks-analyzer/
├── src/
│   ├── data/
│   │   ├── sources/
│   │   │   ├── __init__.py
│   │   │   └── financial_source.py
│   │   └── models.py
│   ├── analysis/
│   │   ├── analyzer.py
│   │   └── reports.py
│   ├── visualization/
│   │   └── dashboards.py
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
- Martin Davila
- GitHub: [@mdavila0422](https://github.com/mdavila0422)

## Project Status
🚧 Under Development

### Development Notes
- Currently focused on financial analysis using YFinance API
- Mining-specific operational data integration is pending identification of suitable data source
- Potential future data sources being evaluated for operational metrics