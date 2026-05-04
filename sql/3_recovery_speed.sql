WITH base AS(
    SELECT 
        airline,
        AVG(close) AS base_price
    FROM stock_daily
    WHERE date BETWEEN '2019-01-01' AND '2019-12-31'
    GROUP BY airline
),
daily_with_base AS (
    SELECT
        d.airline,
        d.date,
        d.close,
        b.base_price,
        d.close / b.base_price * 100 AS pct_of_base
    FROM stock_daily AS d
    JOIN base AS b
        ON d.airline = b.airline
    WHERE d.date >= '2020-03-01'
)
SELECT DISTINCT ON (airline)
    airline,
    date AS recovery_date,
    ROUND(pct_of_base, 1) AS pct_of_pre_covid
FROM daily_with_base
WHERE pct_of_base >= 100
ORDER BY
    airline,
    date;