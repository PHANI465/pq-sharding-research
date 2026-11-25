-- P5: first proxy for message size, one day only. Assumes `input` is a hex STRING starting with 0x.
-- If 01_ethereum_columns.sql shows `input` is BYTES, use LENGTH(input) instead (see comment).
-- Dry-run first. This reads from_address, to_address, input, so expect a larger estimate than 02.
SELECT
  COUNT(*) AS txs,
  AVG((LENGTH(input) - 2) / 2) AS avg_input_bytes,          -- BYTES variant: AVG(LENGTH(input))
  APPROX_QUANTILES((LENGTH(input) - 2) / 2, 10) AS input_bytes_deciles
FROM `bigquery-public-data.crypto_ethereum.transactions`
WHERE block_timestamp >= TIMESTAMP('2026-11-01')
  AND block_timestamp <  TIMESTAMP('2026-11-02');
-- Proxy leaves out: signature (65 B), nonce, gas fields, RLP overhead. Decide and write the fixed
-- overhead in README. Worked examples in the deck (185 B transfer, 565 B call) are illustrations only.
