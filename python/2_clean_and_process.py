import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

raw_path = os.path.join(RAW_DIR, "all_airlines_raw.csv")
df = pd.read_csv(raw_path, parse_dates=["date"])

# print(df.shape)
# print(df.dtypes)
# print(df.head())

# print("\n Missing values per column:")
# print(df.isnull().sum())

# print("\n Row counts per airline:")
# print(df.groupby("airline")["close"].count())


# Sort
df = df.sort_values(["airline", "date"])
df.reset_index(drop=True)

# print("\n First rows after sorting:")
# print(df.head())
# print("\n Last rows after sorting:")
# print(df.tail())


# Daily Returns
df["daily_return_pct"] = (
    df.groupby("airline")["close"].pct_change() * 100
)
# print("\n Sample with daily returns:")
# print(df[df["airline"] == "Cathay Pacific"].head(10))


# Normalised Price
df["normalised_price"] = (
    df.groupby("airline")["close"].transform(
        lambda x: x / x.iloc[0] * 100
    )
)
# print("\n Normalised price sample:")
# print(df.groupby("airline").first()[["date", "close", "normalised_price"]])


# Rolling Volatility
df["volatility_30d"] = (
    df.groupby("airline")["daily_return_pct"].transform(
        lambda x: x.rolling(window=30).std()
    )
)
# print("\n Volatility sample:")
# print(df[df["airline"] == "Cathay Pacific"][["date", "close", "daily_return_pct", "volatility_30d"]])


df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["year_month"] = df["date"].dt.to_period('M').astype(str)

# print("\n Final columns:")
# print(df.columns.tolist())
# print(df.head())


# Save Files
os.makedirs(PROCESSED_DIR, exist_ok=True)

# daily
daily_path = os.path.join(PROCESSED_DIR, "all_airlines_combined.csv")
df.to_csv(daily_path, index=False)
print(f"\n Saved daily data: {daily_path}")
print(f"Rows: {len(df)}")

# monthly
monthly = (
    df.groupby(["airline", "ticker", "year", "month", "year_month"]).agg(
        avg_close = ("close", "mean"),
        avg_normalised = ("normalised_price", "mean"),
        avg_daily_return = ("daily_return_pct", "mean"),
        avg_volatility_30d = ("volatility_30d", "mean"),
        trading_days = ("close", "count")
    )
)
monthly = monthly.reset_index()

monthly_path = os.path.join(PROCESSED_DIR, "all_airlines_monthly.csv")
monthly.to_csv(monthly_path, index=False)
print(f"\n Saved monthly data: {monthly_path}")
print(f"Rows: {len(monthly)}")
# print(monthly.head(10))


print("\n COVID low per airline:")
for airline, group in df.groupby("airline"):
    low = group.loc[group["normalised_price"].idxmin()]
    print(f"  {airline}: {low['date'].date()} — {low['normalised_price']:.1f}")