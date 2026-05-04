SELECT
    airline,
    ROUND(MAX(volatility_30d), 2) AS peak_volatility,
    ROUND(AVG(volatility_30d), 2) AS avg_volatility,
    RANK() OVER (ORDER BY AVG(volatility_30d) DESC) AS risk_rank
FROM stock_daily
WHERE date BETWEEN '2020-01-01' AND '2022-12-31'
    AND volatility_30d IS NOT NULL
GROUP BY airline
ORDER BY avg_volatility DESC;