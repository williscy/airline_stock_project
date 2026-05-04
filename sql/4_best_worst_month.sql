WITH monthly_avg AS(
    SELECT
        airline,
        month,
        ROUND(AVG(avg_daily_return), 3) AS avg_return
    FROM stock_monthly
    GROUP BY 
        airline,
        month
),
monthly_rank AS(
    SELECT
        airline,
        month,
        avg_return,
        RANK() OVER(
            PARTITION BY airline
            ORDER BY avg_return DESC
        ) AS best_rank,
        RANK() OVER(
            PARTITION BY airline
            ORDER BY avg_return ASC
        ) AS worst_rank
    FROM monthly_avg
)
SELECT
    airline,
    MAX(CASE WHEN best_rank = 1 THEN month 
        END
    ) AS best_month,
    MAX(CASE WHEN worst_rank = 1 THEN month
        END
    ) AS worst_month
FROM monthly_rank
GROUP BY airline
ORDER BY airline;
