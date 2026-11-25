-- first day, last day, day count and number of gaps (free metadata)
WITH d AS (
  SELECT SAFE.PARSE_DATE('%Y%m%d', partition_id) AS day, total_rows
  FROM `bigquery-public-data.crypto_near_mainnet_us.INFORMATION_SCHEMA.PARTITIONS`
  WHERE table_name = 'transactions'
)
SELECT MIN(day) AS first_day, MAX(day) AS last_day, COUNT(day) AS n_days,
  DATE_DIFF(MAX(day), MIN(day), DAY) + 1 AS expected_days, SUM(total_rows) AS total_rows,
  (SELECT COUNT(*) FROM (SELECT day, LEAD(day) OVER (ORDER BY day) AS nd FROM d WHERE day IS NOT NULL)
   WHERE DATE_DIFF(nd, day, DAY) > 1) AS gap_count
FROM d;
