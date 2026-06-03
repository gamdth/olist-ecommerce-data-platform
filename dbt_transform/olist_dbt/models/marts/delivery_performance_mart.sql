SELECT
    customer_state,

    COUNT(order_id) AS total_orders,

    SUM(
        CASE
            WHEN delivery_status = 'Late' THEN 1
            ELSE 0
        END
    ) AS late_orders,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN delivery_status = 'Late' THEN 1
                ELSE 0
            END
        ) / COUNT(order_id),
        2
    ) AS late_delivery_rate

FROM {{ ref('fact_orders') }}

GROUP BY customer_state

ORDER BY late_delivery_rate DESC