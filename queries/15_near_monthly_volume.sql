-- monthly transactions from partition metadata (free)
SELECT SUBSTR(partition_id, 1, 6) AS month, COUNT(*) AS days, SUM(total_rows) AS txs,
  CAST(SUM(total_rows) / COUNT(*) AS INT64) AS txs_per_day
FROM `bigquery-public-data.crypto_near_mainnet_us.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'transactions' AND partition_id >= '20250101' AND partition_id <> '__NULL__'
GROUP BY month ORDER BY month;
