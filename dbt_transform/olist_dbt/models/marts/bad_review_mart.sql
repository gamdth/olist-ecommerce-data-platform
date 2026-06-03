SELECT
    customer_state,

    delivery_status,

    COUNT(order_id) AS total_orders,

    AVG(review_score) AS avg_review_score,

    SUM(
        CASE
            WHEN review_score <= 2 THEN 1
            ELSE 0
        END
    ) AS bad_reviews,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN review_score <= 2 THEN 1
                ELSE 0
            END
        ) / COUNT(order_id),
        2
    ) AS bad_review_rate

FROM {{ ref('fact_orders') }}

GROUP BY
    customer_state,
    delivery_status

ORDER BY bad_review_rate DESC