SELECT
    o.order_id,
    o.customer_id,

    c.customer_city,
    c.customer_state,

    oi.product_id,
    oi.seller_id,

    r.review_score,

    o.order_status,
    o.delivery_status,

    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    oi.price,
    oi.freight_value,

    (oi.price + oi.freight_value) AS total_amount

FROM {{ ref('silver_orders') }} o

LEFT JOIN {{ ref('silver_customers') }} c
    ON o.customer_id = c.customer_id

LEFT JOIN {{ ref('silver_order_items') }} oi
    ON o.order_id = oi.order_id

LEFT JOIN {{ ref('silver_reviews') }} r
    ON o.order_id = r.order_id