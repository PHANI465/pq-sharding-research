-- shard and conversion gas by key type for one week (about 0.45 GB estimate)
SELECT SPLIT(signer_public_key, ':')[OFFSET(0)] AS key_prefix, shard_id, COUNT(*) AS txs,
  ROUND(AVG(receipt_conversion_gas_burnt)) AS avg_conv_gas,
  MIN(receipt_conversion_gas_burnt) AS min_conv_gas, MAX(receipt_conversion_gas_burnt) AS max_conv_gas
FROM `bigquery-public-data.crypto_near_mainnet_us.transactions`
WHERE block_date BETWEEN '2026-11-10' AND '2026-11-16'
GROUP BY key_prefix, shard_id ORDER BY key_prefix, shard_id;
