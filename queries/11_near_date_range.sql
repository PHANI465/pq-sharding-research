-- N3 (Namana): first and last date. Dry-run first. block_date is the partition column (Fact: NEAR docs).
SELECT MIN(block_date) AS first_day, MAX(block_date) AS last_day
FROM `bigquery-public-data.crypto_near_mainnet_us.transactions`;
-- Then check for missing days in the middle (days with zero rows between first and last).
