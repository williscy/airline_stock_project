WITH covid_prices AS (
    SELECT
        airline,
        date,
        normalised_price,
        MAX(normalised_price) OVER(
            PARTITION BY airline
            ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_peak
    FROM stock_daily
    WHERE date BETWEEN '2020-01-01' AND '2022-12-31'
)
SELECT
    airline,
    ROUND(MIN(normalised_price), 1) AS lowest_price,
    ROUND(MIN((normalised_price - running_peak) / running_peak * 100), 1) AS max_drawdown_pct
FROM covid_prices
GROUP BY airline
ORDER BY max_drawdown_pct;