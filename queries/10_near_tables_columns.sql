-- N2 (Namana): list NEAR tables and their columns. Metadata only.
SELECT table_name, column_name, data_type, is_partitioning_column
FROM `bigquery-public-data.crypto_near_mainnet_us.INFORMATION_SCHEMA.COLUMNS`
ORDER BY table_name, ordinal_position;
