-- P4: ALWAYS dry-run first (editor shows "This query will process X when run").
-- If the estimate is large, the filter is not hitting the partition column.
-- Replace block_timestamp below if 01_ethereum_columns.sql shows a different partition column.
SELECT COUNT(*) AS txs
FROM `bigquery-public-data.crypto_ethereum.transactions`
WHERE block_timestamp >= TIMESTAMP('2026-11-01')
  AND block_timestamp <  TIMESTAMP('2026-11-02');
-- Record bytes processed in docs/quota-log.md.
