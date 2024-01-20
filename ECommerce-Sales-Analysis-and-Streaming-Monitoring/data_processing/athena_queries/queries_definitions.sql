SELECT distinct(order_type) as order_type, count(order_type) as qty
FROM "ecommerce_kinesis_DB.EcommerceTableKinesis"
group by 1 order by 2 desc;