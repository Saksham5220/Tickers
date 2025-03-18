# Saksham Nirula
# SEC Financial Data CLI

This command-line tool retrieves financial data from SEC filings for publicly traded companies. It extracts free cash flow metrics and income statements directly from 10-K and 10-Q reports.

## Features

- **Free Cash Flow Lookup**: Retrieve quarterly or annual free cash flow for any publicly traded company
- **Income Statement Retrieval**: Extract and display full income statements from annual reports
- **Company Information**: Look up basic company details by ticker symbol

## Setup

### Prerequisites

- Python 3.6+
- Required Python packages: `requests`, `pandas`, `beautifulsoup4`

### Installation

1. Install required packages:
   ```bash
   pip install requests pandas beautifulsoup4
   ```

2. Create a `Utils.py` file in the same directory with the following content:
   ```python
   # Utils.py
   # SEC API access credentials

   # User agent for SEC.gov access (required)
   user_agent = "Your Name (your.email@example.com)"  # ← Replace with your info

   # API key for SEC-API.io
   api_key = "your-api-key-here"  # ← Replace with your SEC-API key
   ```

3. Ensure your user agent follows SEC.gov guidelines - use your real name and email.

## Usage

Run the script:
```bash
python ticker.py
```

### Commands

The tool supports the following command formats:

1. **Quarterly Free Cash Flow**:
   ```
   TICKER_FCF_QRT
   ```
   Example: `AAPL_FCF_QRT`

2. **Annual Free Cash Flow for a specific year**:
   ```
   TICKER_FCF_YR_XX
   ```
   Example: `TSLA_FCF_YR_23` (for year 2023)

3. **Income Statement**:
   ```
   TICKER INC
   ```
   Example: `MSFT INC`

4. **Company Information**:
   ```
   TICKER
   ```
   Example: `AMZN`

5. **Exit the program**:
   ```
   quit
   ```

## Examples

### Quarterly Free Cash Flow

```
Enter Ticker and following command *FCF*QRT (Print last quarter Free Cash Flow), *FCF*YR_XX (Print Last Years Free Cash Flow), INC (Print Income Statement)
(i.e. AAPL_FCF_QRT, TSLA_FCF_YR_24, MSFT INC) to get details: AAPL_FCF_QRT

Ticker: AAPL
Retrieving quarterly free cash flow...
Found latest 10-Q filing from 2024-07-31 for period 2024-06-30
AAPL Quarterly Free Cash Flow (Period: 2024-06-30): $28.5 B (28,525,000,000.00 dollars)
```

### Annual Free Cash Flow

```
Enter Ticker and following command *FCF*QRT (Print last quarter Free Cash Flow), *FCF*YR_XX (Print Last Years Free Cash Flow), INC (Print Income Statement)
(i.e. AAPL_FCF_QRT, TSLA_FCF_YR_24, MSFT INC) to get details: MSFT_FCF_YR_23

Ticker: MSFT
Retrieving annual free cash flow for 2023...
Found 10-K filing from 2023-07-27 for period 2023-06-30
MSFT Annual Free Cash Flow (Period: 2023-06-30): $59.5 B (59,476,000,000.00 dollars)
```

### Income Statement

```
Enter Ticker and following command *FCF*QRT (Print last quarter Free Cash Flow), *FCF*YR_XX (Print Last Years Free Cash Flow), INC (Print Income Statement)
(i.e. AAPL_FCF_QRT, TSLA_FCF_YR_24, MSFT INC) to get details: GOOG INC

Ticker: GOOG
Found latest 10-K filing from 2024-02-01

Income Statement for Alphabet Inc. (GOOG):
...
```

## Notes

- The script uses data from SEC.gov and SEC-API.io
- Currency values are displayed with appropriate scaling (millions, billions, etc.)
- The tool handles various document formats and structures from different companies
