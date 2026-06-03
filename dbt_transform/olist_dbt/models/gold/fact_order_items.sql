SELECT
    oi.order_id,
    oi.order_item_id,

    oi.product_id,
    oi.seller_id,

    o.customer_id,

    o.order_purchase_timestamp,
    o.order_delivered_customer_date,

    oi.price,
    oi.freight_value,

    (oi.price + oi.freight_value) AS total_amount

FROM {{ ref('silver_order_items') }} oi

LEFT JOIN {{ ref('silver_orders') }} o
    ON oi.order_id = o.order_id