-- Opción 'IF NOT EXISTS' puede usarse para proteger el esquema existente
DROP TABLE IF EXISTS your_stream_name;

CREATE TABLE your_stream_name (
  `purchase_ID` VARCHAR(50), 
  `Product_name` VARCHAR(50), 
  `Pricing` DECIMAL(10, 2), 
  `Commission` DECIMAL(10, 2), 
  `Revenue` DECIMAL(10, 2), 
  `Payment_Method` VARCHAR(50), 
  `Status` VARCHAR(50), 
  `Order_Type` VARCHAR(50), 
  `City` VARCHAR(50), 
  `Latitude` DECIMAL(10, 6), 
  `Longitude` DECIMAL(10, 6), 
  `Source` VARCHAR(50), 
  `Brand` VARCHAR(50), 
  `Category` VARCHAR(50), 
  `Created_at` TIMESTAMP(3),
  `USER_ID` VARCHAR(10),  -- Added USER_ID column
  WATERMARK FOR Created_at AS Created_at - INTERVAL '5' SECOND  
)
PARTITIONED BY (USER_ID)  -- Partitioned by USER_ID
WITH (
  'connector' = 'kinesis',
  'stream' = 'data_stream_pipeline_ingestion_useast1',
  'aws.region' = 'your_aws_region',
  'scan.stream.initpos' = 'LATEST',
  'format' = 'json',
  'json.timestamp-format.standard' = 'ISO-8601'
);

----------------------------------
-- CONVERTION RATE
----------------------------------

CREATE OR REPLACE STREAM SalesByProduct AS
SELECT
   Product_name,
   COUNT(*) AS TotalSales
FROM
   your_stream_name
WHERE
   Order_Type = 'ONLINE'
   AND Status = 'COMPLETED'
GROUP BY
   Product_name;

CREATE OR REPLACE STREAM ConversionRate AS
SELECT
    DATE_TRUNC('HOUR', CAST(Created_at AS TIMESTAMP)) AS Hour,
    SUM(CASE WHEN Status = 'COMPLETED' THEN 1 ELSE 0 END) / COUNT(*) AS ConversionRate
FROM
    your_stream_name
GROUP BY
    Hour;

-- Define your output Kinesis stream for results
CREATE TABLE OutputDataStream (
  `Result` ROW<EventType VARCHAR(50), Count BIGINT>, -- Define the schema for the output data
  WATERMARK FOR Created_at AS CURRENT_TIMESTAMP
)
WITH (
  'connector' = 'kinesis',
  'stream' = 'data_stream_pipeline_processing_useast1',
  'aws.region' = 'your_aws_region',
  'format' = 'json',
  'json.timestamp-format.standard' = 'ISO-8601'
);

-- Send SalesByProduct results to OutputDataStream
INSERT INTO OutputDataStream
SELECT
    ROW('SalesByProduct', Product_name, TotalSalesByProduct)
FROM
    SalesByProduct;

-- Send ConversionRate results to OutputDataStream
INSERT INTO OutputDataStream
SELECT
    ROW('ConversionRate', Hour, ConversionRate)
FROM
    ConversionRate;
