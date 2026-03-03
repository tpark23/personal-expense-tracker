import re
import pdfplumber
from io import BytesIO

# Define regex patterns for all known transaction formats
TRANSACTION_PATTERNS = [
    re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<posting_date>\d{2}/\d{2})\s+(?P<description>.+?)\s+(?P<amount>\d+\.\d{2}),?$'),
    re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<posting_date>\d{2}/\d{2})\s+(?P<description>.+?)\s+(?P<amount>-?\d+\.\d{2}),?$'), # negative
    re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<description>.+?)\s+(?P<amount>\d+\.\d{2})$'),
    re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<description>.+?)\s+(?P<amount>-?\d+\.\d{2})$'), # negative
    re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<posting_date>\d{2}/\d{2})\s+\S+\s+\S+\s+(?P<description>.+?)\s+\$(?P<amount>\d+\.\d{2})$'),
    re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<posting_date>\d{2}/\d{2})\s+\S+\s+\S+\s+(?P<description>.+?)\s+\$(?P<amount>\d+\.\d{2}-?)$')
]


def extract_transactions_from_statement(file_stream: BytesIO) -> list:
    """
    Extract transactions from a bank statement PDF file.
    """
    with pdfplumber.open(file_stream) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()

    # Split the text into lines
    lines = text.split('\n')

    # Extract transactions
    transactions = []
    for line in lines:
        for pattern in TRANSACTION_PATTERNS:
            match = pattern.match(line)
            if match:
                transactions.append({
                    "transaction_date": match.group("transaction_date"),
                    "posting_date": match.group("posting_date") if "posting_date" in match.groupdict() else None,
                    "description": match.group("description").strip(),
                    "amount": -float(match.group("amount")[:-1]) if match.group("amount").endswith('-') else float(match.group("amount")),
                })
                break  # Stop checking other patterns once a match is found

    return transactions
