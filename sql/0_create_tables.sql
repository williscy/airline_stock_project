CREATE TABLE stock_daily(
    date DATE,
    close NUMERIC,
    airline VARCHAR(50),
    ticker VARCHAR(20),
    daily_return_pct NUMERIC,
    normalised_price NUMERIC,
    volatility_30d NUMERIC,
    year INT,
    month INT,
    year_month VARCHAR(10)
);
CREATE TABLE stock_monthly(
    airline VARCHAR(50),
    ticker VARCHAR(20),
    year INT,
    month INT,
    year_month VARCHAR(10),
    avg_close NUMERIC,
    avg_normalised NUMERIC,
    avg_daily_return NUMERIC,
    avg_volatility_30d NUMERIC,
    trading_days INT
);
COPY stock_daily 
FROM 'all_airlines_combined.csv' 
CSV HEADER;

COPY stock_monthly 
FROM 'all_airlines_monthly.csv' 
CSV HEADER;

SELECT airline, COUNT(*) FROM stock_daily GROUP BY airline ORDER BY airline;
SELECT airline, COUNT(*) FROM stock_monthly GROUP BY airline ORDER BY airline;