SELECT
    airline,
    ticker,
    year,
    month,
    year_month,
    avg_close,
    avg_normalised,
    avg_daily_return,
    avg_volatility_30d,
    trading_days,
    CASE
        WHEN year < 2020 THEN 'Pre-COVID'
        WHEN year BETWEEN 2020 AND 2021 THEN 'COVID'
        WHEN year = 2022 THEN 'Recovery Start'
        ELSE 'Recovery'
    END AS era,
    CASE
        WHEN month = 1 THEN 'Jan'
        WHEN month = 2 THEN 'Feb'
        WHEN month = 3 THEN 'Mar'
        WHEN month = 4 THEN 'Apr'
        WHEN month = 5 THEN 'May'
        WHEN month = 6 THEN 'Jun'
        WHEN month = 7 THEN 'Jul'
        WHEN month = 8 THEN 'Aug'
        WHEN month = 9 THEN 'Sep'
        WHEN month = 10 THEN 'Oct'
        WHEN month = 11 THEN 'Nov'
        WHEN month = 12 THEN 'Dec'
    END AS month_name
FROM stock_monthly
ORDER BY
    airline,
    year,
    month;