SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value

FROM {{ source('raw_db', 'bronze_olist_order_payments') }}