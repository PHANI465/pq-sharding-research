-- P3 / P5: confirm columns, types and the partition column of the Ethereum transactions table.
-- Metadata only. Console showed ~10 MB estimate (likely the per-query minimum).
SELECT column_name, data_type, is_partitioning_column
FROM `bigquery-public-data.crypto_ethereum.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'transactions'
  AND (column_name IN ('hash','from_address','to_address','input','value',
                       'gas','gas_price','block_timestamp','block_number',
                       'transaction_type')
       OR is_partitioning_column = 'YES');
