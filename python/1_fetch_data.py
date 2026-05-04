import yfinance as yf
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR  = os.path.join(BASE_DIR, "..", "data", "raw")

AIRLINES = {
    "Cathay Pacific": "0293.HK",
    "Singapore Airlines": "C6L.SI",
    "Qantas": "QAN.AX",
    "Korean Air": "003490.KS"
}

START_DATE = "2015-01-01"
END_DATE = "2025-12-31"


def fetch_airlines(name, ticker):
    print(f"Fetching {name} ({ticker})...")

    df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
    df = df[["Close"]]
    df["airline"] = name
    df["ticker"] = ticker
    df = df.reset_index()
    df.columns = ["date", "close", "airline", "ticker"]

    return df


all_data = []
for name, ticker in AIRLINES.items():
    df = fetch_airlines(name, ticker)
    all_data.append(df)
    print(f"{name} completed: {len(df)} rows")

combined = pd.concat(all_data, ignore_index=True)
# print(combined.head(10))
# print(combined.tail(10))


os.makedirs(RAW_DIR, exist_ok=True)

output_path = os.path.join(RAW_DIR, "all_airlines_raw.csv")
combined.to_csv(output_path, index=False)

print(f"\n Saved to {output_path}")
print(f"Total rows: {len(combined)}")