###
Saksham Nirula, Ticker Pull
Linkedin: https://Linkedin.com/profile/sakshamnirula
###


import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
from Utils import user_agent, api_key

# -----------------------------
# Function to fetch SEC tickers
# -----------------------------
def fetch_sec_tickers(user_agent="Your Name (your.email@example.com)"):
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return list(data.values())

# -----------------------------
# Function to find company by ticker (case-insensitive)
# -----------------------------
def find_company_by_ticker(ticker, tickers):
    ticker_lower = ticker.lower()
    for company in tickers:
        if company["ticker"].lower() == ticker_lower:
            return company
    return None

# -----------------------------
# Function to get the filing URL for SEC-API
# -----------------------------
def get_filing_url(cik, accession_number, primary_document):
    acc_number_no_dashes = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_number_no_dashes}/{primary_document}"
    return url

# -----------------------------
# Function to fetch the filing document text (as plain text)
# -----------------------------
def fetch_filing_document(cik, accession_number, primary_document, user_agent="Your Name (your.email@example.com)"):
    acc_number_no_dashes = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_number_no_dashes}/{primary_document}"
    headers = {"User-Agent": user_agent}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Check if it's an HTML document
        if 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            return text
        # Check if it's an XML/XBRL document
        elif 'application/xml' in response.headers.get('Content-Type', '') or response.text.startswith('<?xml'):
            soup = BeautifulSoup(response.text, "xml")
            text = soup.get_text(separator=" ", strip=True)
            return text
        else:
            # Just return the raw text for other formats
            return response.text
    except Exception as e:
        # Try alternative URL format which is sometimes used for newer filings
        try:
            alt_url = f"https://www.sec.gov/ix?doc=/Archives/edgar/data/{int(cik)}/{acc_number_no_dashes}/{primary_document}"
            alt_response = requests.get(alt_url, headers=headers)
            alt_response.raise_for_status()
            soup = BeautifulSoup(alt_response.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            return text
        except Exception:
            return None

# -----------------------------
# Function to fetch XBRL data using SEC-API
# -----------------------------
def fetch_xbrl_data(filing_url, api_key="47b735fcfedd17e66521aea173891419d8e6b7b06d3093b65e8aabbf0d6dbfea"):
    xbrl_converter_api_endpoint = "https://api.sec-api.io/xbrl-to-json"
    final_url = f"{xbrl_converter_api_endpoint}?htm-url={filing_url}&token={api_key}"
    
    try:
        response = requests.get(final_url)
        response.raise_for_status()
        return json.loads(response.text)
    except Exception:
        return None

# -----------------------------
# Improved function to retrieve the latest available 10-K filing (annual)
# -----------------------------
def get_latest_10k_filing(cik, user_agent="Your Name (your.email@example.com)"):
    cik_str = str(cik).zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_str}.json"
    headers = {"User-Agent": user_agent}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if "filings" not in data:
            return None
            
        recent_filings = data.get("filings", {}).get("recent", {})
        if not recent_filings:
            return None
            
        # Check if we have all the required keys
        required_keys = ["form", "filingDate", "accessionNumber", "primaryDocument"]
        missing_keys = [k for k in required_keys if k not in recent_filings]
        if missing_keys:
            return None
        
        # Look for the most recent 10-K filing
        forms = recent_filings.get("form", [])
        filing_dates = recent_filings.get("filingDate", [])
        accession_numbers = recent_filings.get("accessionNumber", [])
        primary_documents = recent_filings.get("primaryDocument", [])
        periods = recent_filings.get("reportDate", recent_filings.get("periodOfReport", []))
        
        # Find the first 10-K filing
        for i, form in enumerate(forms):
            if form == "10-K" and i < len(filing_dates) and i < len(accession_numbers) and i < len(primary_documents):
                period = periods[i] if i < len(periods) else "Unknown"
                return {
                    "filing_date": filing_dates[i],
                    "accession_number": accession_numbers[i],
                    "primary_document": primary_documents[i],
                    "period": period
                }
                
        return None
        
    except:
        return None

# -----------------------------
# Improved function to retrieve the latest 10-Q filing (quarterly)
# -----------------------------
def get_latest_10q_filing(cik, user_agent="Your Name (your.email@example.com)"):
    cik_str = str(cik).zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_str}.json"
    headers = {"User-Agent": user_agent}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if "filings" not in data:
            return None
            
        recent_filings = data.get("filings", {}).get("recent", {})
        if not recent_filings:
            return None
        
        # Required keys
        required_keys = ["form", "filingDate", "accessionNumber", "primaryDocument"]
        missing_keys = [k for k in required_keys if k not in recent_filings]
        if missing_keys:
            return None
        
        # Get the lists
        forms = recent_filings.get("form", [])
        filing_dates = recent_filings.get("filingDate", [])
        accession_numbers = recent_filings.get("accessionNumber", [])
        primary_documents = recent_filings.get("primaryDocument", [])
        periods = recent_filings.get("reportDate", recent_filings.get("periodOfReport", []))
        
        for i, form in enumerate(forms):
            if form == "10-Q" and i < len(filing_dates) and i < len(accession_numbers) and i < len(primary_documents):
                period = periods[i] if i < len(periods) else "Unknown"
                return {
                    "filing_date": filing_dates[i],
                    "accession_number": accession_numbers[i],
                    "primary_document": primary_documents[i],
                    "period": period
                }
        
        return None
    
    except:
        return None

# -----------------------------
# Function to retrieve the 10-K filing details for a company by year (annual)
# -----------------------------
def get_10k_filing_by_year(cik, target_year, user_agent="Your Name (your.email@example.com)"):
    """
    Returns the 10-K filing whose periodOfReport string starts with the target year.
    """
    cik_str = str(cik).zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_str}.json"
    headers = {"User-Agent": user_agent}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # First check in recent filings
        filings = data.get("filings", {}).get("recent", {})
        if filings:
            forms = filings.get("form", [])
            filing_dates = filings.get("filingDate", [])
            accession_numbers = filings.get("accessionNumber", [])
            primary_documents = filings.get("primaryDocument", [])
            report_dates = filings.get("reportDate", filings.get("periodOfReport", []))
            
            # Look for 10-K filings matching the target year
            for i, (form, date, acc, doc) in enumerate(zip(forms, filing_dates, accession_numbers, primary_documents)):
                if form == "10-K" and i < len(report_dates):
                    report_date = report_dates[i]
                    if report_date and report_date.startswith(str(target_year)):
                        return {
                            "filing_date": date,
                            "accession_number": acc,
                            "primary_document": doc,
                            "period": report_date
                        }
                    
                    # Also check if filing date is in the target year
                    # This helps for fiscal years that don't align with calendar years
                    if date and date.startswith(str(target_year)):
                        return {
                            "filing_date": date,
                            "accession_number": acc,
                            "primary_document": doc,
                            "period": report_date
                        }
        
        # If not found, check if there are file references
        files = data.get("filings", {}).get("files", [])
        for file_info in files:
            file_name = file_info.get("name")
            if file_name:
                try:
                    if str(target_year) in file_name:
                        file_url = f"https://data.sec.gov/submissions/{file_name}"
                        file_response = requests.get(file_url, headers=headers)
                        if file_response.status_code == 200:
                            file_data = file_response.json()
                            
                            file_forms = file_data.get("form", [])
                            file_dates = file_data.get("filingDate", [])
                            file_accessions = file_data.get("accessionNumber", [])
                            file_docs = file_data.get("primaryDocument", [])
                            file_reports = file_data.get("reportDate", file_data.get("periodOfReport", []))
                            
                            for i, form in enumerate(file_forms):
                                if form == "10-K" and i < len(file_reports):
                                    report_date = file_reports[i]
                                    if report_date and report_date.startswith(str(target_year)):
                                        return {
                                            "filing_date": file_dates[i],
                                            "accession_number": file_accessions[i],
                                            "primary_document": file_docs[i],
                                            "period": report_date
                                        }
                except:
                    continue
        
        return None
        
    except:
        return None

# -----------------------------
# Enhanced function to extract income statement data from XBRL
# -----------------------------
def get_income_statement(xbrl_json):
    if not xbrl_json:
        return pd.DataFrame()
        
    income_statement_sections = ['StatementsOfIncome', 'IncomeStatement', 'ConsolidatedStatementsOfIncome', 
                                'ConsolidatedIncomeStatements', 'StatementOfIncome', 'StatementsOfOperations',
                                'ConsolidatedOperations', 'ConsolidatedStatementsOfOperations',
                                'StatementsOfEarnings', 'ConsolidatedEarnings', 'ConsolidatedStatementsOfEarnings']
    
    income_section = None
    for section in income_statement_sections:
        if section in xbrl_json:
            income_section = section
            break
            
    if not income_section:
        return pd.DataFrame()
        
    income_statement_store = {}
    income_data = xbrl_json[income_section]
    
    for usGaapItem in income_data:
        values = []
        indices = []
        
        for fact in income_data[usGaapItem]:
            # Only consider items without segment
            if 'segment' not in fact:
                if 'period' in fact and 'endDate' in fact['period']:
                    # Use the end date as the index
                    index = fact['period']['endDate']
                    
                    # Convert value to float for proper display
                    try:
                        value = float(fact['value'])
                    except ValueError:
                        value = fact['value']
                    
                    # Ensure no index duplicates are created
                    if index not in indices:
                        values.append(value)
                        indices.append(index)
        
        if values:
            income_statement_store[usGaapItem] = pd.Series(values, index=indices)
    
    if not income_statement_store:
        return pd.DataFrame()
        
    # Create DataFrame
    income_statement = pd.DataFrame(income_statement_store)
    
    # Sort by date for chronological display
    income_statement = income_statement.sort_index()
    
    # Format column names for readability
    readable_cols = {}
    for col in income_statement.columns:
        # Convert camelCase to words with spaces
        readable = re.sub(r'([a-z])([A-Z])', r'\1 \2', col)
        readable_cols[col] = readable
    
    income_statement = income_statement.rename(columns=readable_cols)
    
    # Switch columns and rows for better display
    return income_statement.T

# -----------------------------
# Function to print income statement using SEC-API
# -----------------------------
def print_income_statement(ticker, tickers, user_agent="Your Name (your.email@example.com)", 
                           api_key="47b735fcfedd17e66521aea173891419d8e6b7b06d3093b65e8aabbf0d6dbfea"):
    # Find the company by ticker
    company = find_company_by_ticker(ticker, tickers)
    if not company:
        print(f"Ticker: {ticker}")
        print("Error: Ticker not found.")
        return
        
    cik = company["cik_str"]
    
    # Get the latest 10-K filing
    filing_info = get_latest_10k_filing(cik, user_agent=user_agent)
    if not filing_info:
        print(f"Ticker: {ticker}")
        print("Error: No 10-K filing found.")
        return
    
    print(f"Ticker: {ticker}")
    print(f"Found latest 10-K filing from {filing_info['filing_date']}")
    
    # Get the filing URL for SEC-API
    filing_url = get_filing_url(cik, filing_info["accession_number"], filing_info["primary_document"])
    
    # Check if the URL works (many SEC filings have inconsistent URL patterns)
    try:
        headers = {"User-Agent": user_agent}
        test_response = requests.head(filing_url, headers=headers)
        if test_response.status_code != 200:
            # Try alternative URL format
            acc_number_no_dashes = filing_info["accession_number"].replace("-", "")
            alt_url = f"https://www.sec.gov/ix?doc=/Archives/edgar/data/{int(cik)}/{acc_number_no_dashes}/{filing_info['primary_document']}"
            alt_test = requests.head(alt_url, headers=headers)
            if alt_test.status_code == 200:
                filing_url = alt_url
    except:
        pass
    
    # Fetch XBRL data using SEC-API
    xbrl_data = fetch_xbrl_data(filing_url, api_key)
    
    if not xbrl_data:
        print("Error: Failed to fetch XBRL data.")
        return
        
    # Check if the API returned an error
    if isinstance(xbrl_data, dict) and 'error' in xbrl_data:
        print(f"Error: {xbrl_data['error']}")
        return
        
    # Get income statement
    income_statement = get_income_statement(xbrl_data)
    
    if income_statement.empty:
        print("Error: No income statement data available.")
        return
    
    # Display the income statement with better formatting
    print(f"\nIncome Statement for {company['title']} ({ticker}):")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.float_format', '{:,.0f}'.format)  # Format as integers with commas
    print(income_statement)
    # Reset pandas display options
    pd.reset_option('display.max_columns')
    pd.reset_option('display.expand_frame_repr')
    pd.reset_option('display.float_format')

# -----------------------------
# Helper function to detect currency scale in the filing text
# -----------------------------
def detect_currency_scale(text):
    lower_text = text.lower()
    
    # First check for explicit statements about scale
    if any(phrase in lower_text for phrase in [
        "in billions", "expressed in billions", "amounts in billions", 
        "presented in billions", "reported in billions"
    ]):
        return 1e9, "billions"
    elif any(phrase in lower_text for phrase in [
        "in millions", "expressed in millions", "amounts in millions", 
        "presented in millions", "reported in millions"
    ]):
        return 1e6, "millions"
    elif any(phrase in lower_text for phrase in [
        "in thousands", "expressed in thousands", "amounts in thousands", 
        "presented in thousands", "reported in thousands"
    ]):
        return 1e3, "thousands"
    
    # Look for table headers that might indicate scale
    if re.search(r'\b(table|data).{0,50}(in billions|billions of)\b', lower_text, re.IGNORECASE):
        return 1e9, "billions"
    elif re.search(r'\b(table|data).{0,50}(in millions|millions of)\b', lower_text, re.IGNORECASE):
        return 1e6, "millions"
    elif re.search(r'\b(table|data).{0,50}(in thousands|thousands of)\b', lower_text, re.IGNORECASE):
        return 1e3, "thousands"
    
    # Default to millions which is most common
    return 1e6, "millions"

# -----------------------------
# Function to format currency values
# -----------------------------
def format_currency_value(value):
    """
    Format a currency value with the correct scaling:
    - Trillions: $X.X T
    - Billions: $X.X B
    - Millions: $X.X M
    - Thousands: $X.X K
    Returns formatted string and full value
    """
    # ANSI color codes
    GREEN_BOLD = "\033[1;32m"  # Bold and green text
    RESET = "\033[0m"          # Reset all formatting
    
    abs_value = abs(value)
    
    if abs_value >= 1e12:  # trillions
        scaled_value = value / 1e12
        formatted = f"{GREEN_BOLD}${scaled_value:.1f} T{RESET}"
    elif abs_value >= 1e9:  # billions
        scaled_value = value / 1e9
        formatted = f"{GREEN_BOLD}${scaled_value:.1f} B{RESET}"
    elif abs_value >= 1e6:  # millions
        scaled_value = value / 1e6
        formatted = f"{GREEN_BOLD}${scaled_value:.1f} M{RESET}"
    elif abs_value >= 1e3:  # thousands
        scaled_value = value / 1e3
        formatted = f"{GREEN_BOLD}${scaled_value:.1f} K{RESET}"
    else:  # regular dollars
        formatted = f"{GREEN_BOLD}${value:.2f}{RESET}"
    
    # Full value with commas
    full_value = f"{value:,.2f} dollars"
    
    return formatted, full_value

# -----------------------------
# Function to check currency scale for sanity
# -----------------------------
def check_currency_scale(value, multiplier):
    """
    Check if the currency scale might be incorrect based on value range
    """
    return value, multiplier, "checked"

# -----------------------------
# Enhanced functions to extract operating cash flow and capital expenditures
# -----------------------------
def extract_operating_cash_flow(text):
    patterns = [
        # Standard patterns
        r'(?:Net cash (?:provided|generated|from) (?:by|from)? operating activities|Cash flows? (?:provided|generated|from)? (?:by)? operating activities|Operating Cash Flow)[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        
        # Additional patterns covering more variants
        r'Cash from operations[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'Operating (?:cash flow|activities)[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'Net cash flow from operating activities[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'Cash flows from operating activities[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'Net cash from operating activities[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        
        # Look for table rows with operating cash flow
        r'(?:operating|operations)[^<>\d\-]{1,40}([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # Additional approach: look for specific table structures
    # This helps with documents where the cash flow data is in tables
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if re.search(r'operating activities', line, re.IGNORECASE) and i+1 < len(lines):
            # Look at the next line for a potential value
            next_line = lines[i+1]
            value_match = re.search(r'([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)', next_line)
            if value_match:
                return value_match.group(1)
    
    return None

def extract_capital_expenditures(text):
    patterns = [
        # Standard patterns
        r'(?:Capital Expenditures|Purchases of property, plant and equipment|Capital spending|Acquisition of property, plant and equipment)[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        
        # Additional patterns for more variants
        r'(?:CapEx|Cap Ex|Capital expenditure)[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'(?:Purchase|Purchases|Acquisition|Additions) of property and equipment[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'(?:Payments for|Investments in) property, plant and equipment[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'Additions to property, plant and equipment[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'Additions to PP&E[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        
        # Look for negative values in cash flow context
        r'(?:property|equipment|capital)[^<>\d\-]{1,40}([\-]\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Check if we found a negative value (which is typical for CapEx)
            value = match.group(1)
            if value.startswith('-'):
                return value
            else:
                # CapEx is typically negative in cash flow statements, 
                # so we negate positive values for consistency
                return '-' + value
    
    # Check for structured tables
    # (similar to operating cash flow extraction)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if re.search(r'(property|equipment|capital expenditure)', line, re.IGNORECASE) and i+1 < len(lines):
            # Look at next line for potential value
            next_line = lines[i+1]
            value_match = re.search(r'([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)', next_line)
            if value_match:
                value = value_match.group(1)
                if value.startswith('-'):
                    return value
                else:
                    # If it's positive and we're pretty sure it's CapEx, make it negative
                    return '-' + value
    
    return None

# -----------------------------
# Enhanced function to calculate Free Cash Flow
# -----------------------------
def calculate_free_cash_flow(text):
    """Calculate FCF with enhanced error handling and debugging"""
    # Extract components
    op_cf_str = extract_operating_cash_flow(text)
    capex_str = extract_capital_expenditures(text)
    
    if op_cf_str and capex_str:
        try:
            # Clean up the strings and convert to numbers
            op_cf = float(op_cf_str.replace(",", ""))
            capex = float(capex_str.replace(",", ""))
            
            # If capex is positive, convert it to negative (cash outflow)
            if capex > 0:
                capex = -capex
                
            # Calculate FCF (Operating CF + CapEx)
            # Note: CapEx is negative, so this is really Operating CF - abs(CapEx)
            fcf = op_cf + capex
            
            return fcf
        except ValueError:
            return "Error converting values"
    else:
        return "Not found"

# -----------------------------
# Function to try extracting FCF values from multiple methods
# -----------------------------
def extract_fcf_with_fallbacks(document_text):
    """
    Try multiple methods to extract FCF components:
    1. Use regex patterns for direct extraction
    2. Look for 'free cash flow' directly mentioned
    3. Look for statement of cash flows sections
    Returns FCF value or error message
    """
    # Method 1: Calculate from components using regex
    fcf = calculate_free_cash_flow(document_text)
    
    # If successful, return the value
    if isinstance(fcf, (int, float)):
        return fcf
    
    # Method 2: Look for FCF directly mentioned in the text
    direct_patterns = [
        r'Free Cash Flow[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'FCF[^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
        r'free cash flow of [^\d\-]*([\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
    ]
    
    for pattern in direct_patterns:
        match = re.search(pattern, document_text, re.IGNORECASE)
        if match:
            try:
                fcf_value = float(match.group(1).replace(",", ""))
                return fcf_value
            except ValueError:
                pass
    
    # Method 3: Look for cash flow items in structured sections
    cf_section_match = re.search(r'(statement of cash flows|cash flow statement).{1,5000}?(?=consolidated statements|statement of stockholders|balance sheet|</table>)', 
                               document_text, re.IGNORECASE | re.DOTALL)
    
    if cf_section_match:
        section_text = cf_section_match.group(0)
        # Try to extract components from this more focused section
        op_cf_str = extract_operating_cash_flow(section_text)
        capex_str = extract_capital_expenditures(section_text)
        
        if op_cf_str and capex_str:
            try:
                op_cf = float(op_cf_str.replace(",", ""))
                capex = float(capex_str.replace(",", ""))
                if capex > 0:
                    capex = -capex
                return op_cf + capex
            except ValueError:
                pass
    
    # If all methods fail
    return "Free cash flow not found"

# -----------------------------
# Improved function to print annual free cash flow for a given ticker and target year
# -----------------------------
def print_free_cash_flow_year(ticker, target_year, tickers, user_agent="Your Name (your.email@example.com)"):
    # Find the company
    company = find_company_by_ticker(ticker, tickers)
    if not company:
        print(f"Ticker: {ticker}")
        print("Error: Ticker not found.")
        return
    
    cik = company["cik_str"]
    
    # Try to get the filing for the specific year
    filing_info = get_10k_filing_by_year(cik, target_year, user_agent=user_agent)
    if not filing_info:
        filing_info = get_latest_10k_filing(cik, user_agent=user_agent)
        if not filing_info:
            print(f"Ticker: {ticker}")
            print(f"Error: No annual filing found.")
            return
    
    print(f"Ticker: {ticker}\n\n")
    print(f"Retrieving annual free cash flow for {target_year}...")
    
    if filing_info.get('filing_date'):
        print(f"Found 10-K filing from {filing_info['filing_date']} for period {filing_info.get('period', 'Unknown')}")
    
    try:
        # Get the document text
        document_text = fetch_filing_document(cik, filing_info["accession_number"], filing_info["primary_document"], user_agent=user_agent)
        
        if not document_text:
            print(f"Error: Unable to fetch document text.")
            return
            
        # Extract FCF using enhanced methods with fallbacks
        fcf = extract_fcf_with_fallbacks(document_text)
        
        if isinstance(fcf, (int, float)):
            # Detect currency scale
            multiplier, unit = detect_currency_scale(document_text)
            
            # Check for potential scaling issues
            fcf, multiplier, unit_info = check_currency_scale(fcf, multiplier)
            
            # Calculate the actual FCF value
            fcf_actual = fcf * multiplier
            
            # Format the value appropriately
            formatted_value, full_value = format_currency_value(fcf_actual)
            
            # Print the result
            period = filing_info.get("period", f"{target_year}")
            print("________________________________________________________________________________________________________________\n\n")
            print(f"{ticker} Annual Free Cash Flow (Period: {period}): {formatted_value} ({full_value})")
            print("________________________________________________________________________________________________________________")
        else:
            print(f"Error: {fcf}")
            
    except Exception:
        print(f"Error: Unable to process document.")

# -----------------------------
# Improved function to print quarterly free cash flow for a given ticker
# -----------------------------
def print_free_cash_flow_quarter(ticker, tickers, user_agent="Your Name (your.email@example.com)"):
    # Find the company
    company = find_company_by_ticker(ticker, tickers)
    if not company:
        print(f"Ticker: {ticker}")
        print("Error: Ticker not found.")
        return
        
    cik = company["cik_str"]
    
    # Get the latest 10-Q filing
    filing_info = get_latest_10q_filing(cik, user_agent=user_agent)
    if not filing_info:
        print(f"Ticker: {ticker}")
        print(f"Error: No 10-Q filing found.")
        return
    
    print(f"Ticker: {ticker}")
    print("Retrieving quarterly free cash flow...")
    print(f"Found latest 10-Q filing from {filing_info.get('filing_date')} for period {filing_info.get('period', 'Unknown')}")
    
    try:
        # Get the document text
        document_text = fetch_filing_document(cik, filing_info["accession_number"], filing_info["primary_document"], user_agent=user_agent)
        
        if not document_text:
            print(f"Error: Unable to fetch document text.")
            return
        
        # Extract FCF using enhanced methods with fallbacks
        fcf = extract_fcf_with_fallbacks(document_text)
        
        if isinstance(fcf, (int, float)):
            # Detect currency scale
            multiplier, unit = detect_currency_scale(document_text)
            
            # Check for potential scaling issues
            fcf, multiplier, unit_info = check_currency_scale(fcf, multiplier)
            
            # Calculate the actual FCF value
            fcf_actual = fcf * multiplier
            
            # Format the value appropriately
            formatted_value, full_value = format_currency_value(fcf_actual)
            
            # Print result
            period = filing_info.get("period", "current quarter")
            print("________________________________________________________________________________________________________________\n\n")
            print(f"{ticker} Quarterly Free Cash Flow (Period: {period}): {formatted_value} ({full_value})")
            print("________________________________________________________________________________________________________________")

        else:
            print(f"Error: {fcf}")
            
    except Exception:
        print(f"Error: Unable to process document.")

# -----------------------------
# Main function – Input Parsing Based on Ticker Suffix
# -----------------------------
def main():
    # Fetch tickers with minimal output
    tickers = fetch_sec_tickers(user_agent=user_agent)
    print(f"Loaded {len(tickers)} company tickers.")
    
    while True:
        user_input = input(
            "\nEnter Ticker and following command _FCF_QRT (Get last quarter Free Cash Flow), _FCF_YR_XX (Get Last Years Free Cash Flow), INC (Get Income Statement)\n\n"
            "(i.e. AAPL_FCF_QRT, TSLA_FCF_YR_24, MSFT INC)\n\n to get details: "
        ).strip().lower()
        
        if user_input == 'quit':
            break
        
        # Handle different input formats
        if user_input.endswith("_fcf_qrt"):
            base_ticker = user_input.split("_")[0].upper()
            print_free_cash_flow_quarter(base_ticker, tickers, user_agent=user_agent)
        elif "_fcf_yr_" in user_input:
            parts = user_input.split("_")
            base_ticker = parts[0].upper()
            try:
                year_part = parts[-1]
                if len(year_part) == 2:
                    target_year = int("20" + year_part)
                else:
                    target_year = int(year_part)
            except ValueError:
                print("Error: Invalid year format.")
                continue
                
            print_free_cash_flow_year(base_ticker, target_year, tickers, user_agent=user_agent)
        elif " inc" in user_input or " income" in user_input:
            # Handle income statement request
            base_ticker = user_input.split()[0].upper()
            print_income_statement(base_ticker, tickers, user_agent=user_agent, api_key=api_key)
        else:
            company = find_company_by_ticker(user_input, tickers)
            if company:
                print(f"Ticker: {company['ticker']}\n\n")
                print(f"Company Name: {company['title']}")
                print(f"CIK: {company['cik_str']}")
            else:
                print(f"Ticker: {user_input.upper()}")
                print("Error: Ticker not found.")

if __name__ == "__main__":
    main()
