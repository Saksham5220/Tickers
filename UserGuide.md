# Saksham Nirula
# User Guide - SEC Financial Data CLI

## Overview

This tool provides quick access to financial metrics from SEC filings. It's designed to be simple and display clean, focused output for financial analysis.

## Getting Started

### Setting Up Your Credentials

Before using the tool, you must configure your SEC access credentials:

1. Edit file named `Utils.py` in the same directory as the script
2. Add your information to this file:

```python
# Utils.py
user_agent = "John Smith (john.smith@example.com)"  # Your real name and email
api_key = "your-sec-api-key-here"  # Your SEC-API.io key
```

> **Important**: SEC.gov requires a legitimate user agent with your real name and email. Automated access without proper identification may be blocked.

### Running the Tool

Open your terminal and run:

```bash
python ticker.py
```

The tool will display the number of companies loaded from the SEC database and prompt you for commands.

## Command Reference

### Looking Up Free Cash Flow

Free Cash Flow (FCF) is a key metric that represents the cash a company generates after accounting for capital expenditures.

#### Quarterly FCF

To check the most recent quarterly free cash flow:

```
TICKER_FCF_QRT
```

Example: `AMZN_FCF_QRT`

Output:
```
Ticker: AMZN
Retrieving quarterly free cash flow...
Found latest 10-Q filing from 2024-10-31 for period 2024-09-30
AMZN Quarterly Free Cash Flow (Period: 2024-09-30): $27.3 B (27,345,000,000.00 dollars)
```

#### Annual FCF for a Specific Year

To check annual free cash flow for a specific year:

```
TICKER_FCF_YR_XX
```

- Use the last two digits of the year for XX
- For full year format, use TICKER_FCF_YR_20XX

Examples:
- `AAPL_FCF_YR_23` or `2023` (for 2023)
- `MSFT_FCF_YR_2022` (for 2022)

Output:
```
Ticker: AAPL
Retrieving annual free cash flow for 2023...
Found 10-K filing from 2023-11-03 for period 2023-09-30
AAPL Annual Free Cash Flow (Period: 2023-09-30): $99.6 B (99,604,000,000.00 dollars)
```

### Getting Income Statements

To retrieve the full income statement from the latest annual report:

```
TICKER INC
```

Example: `META INC`

This will display a formatted income statement with all line items from the company's most recent 10-K filing.

### Looking Up Company Information

To get basic company information:

```
TICKER
```

Example: `NVDA`

Output:
```
Ticker: NVDA
Company Name: NVIDIA CORP
CIK: 1045810
```

### Exiting the Program

To exit:

```
quit
```

## Tips for Using the Tool

1. **Understanding Currency Units**: Values are displayed with appropriate scaling:
   - `$X.X T` = Trillions of dollars
   - `$X.X B` = Billions of dollars
   - `$X.X M` = Millions of dollars
   - `$X.X K` = Thousands of dollars

2. **Working with Periods vs. Years**: SEC filings have specific periods that may not align with calendar years. The tool will show the exact period of the report (e.g., "Period: 2023-09-30").

3. **Error Messages**: If you encounter an error message, it will be prefixed with "Error:" and provide a brief explanation. Common errors include:
   - "Error: Ticker not found" - Check the ticker symbol
   - "Error: No 10-Q filing found" - The company may not have recent quarterly filings
   - "Error: Free cash flow not found" - The tool couldn't extract FCF data from the filing

4. **Speed**: The first query may take longer as the tool downloads the full SEC ticker database. Subsequent queries will be faster.
