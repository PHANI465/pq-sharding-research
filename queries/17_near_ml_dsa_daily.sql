-- ML-DSA-65 transactions and distinct signers per day since July (about 8.4 GB estimate)
SELECT block_date,
  COUNTIF(STARTS_WITH(signer_public_key, 'ml-dsa-65')) AS ml_dsa_txs,
  COUNT(DISTINCT IF(STARTS_WITH(signer_public_key, 'ml-dsa-65'), signer_account_id, NULL)) AS ml_dsa_signers,
  COUNT(*) AS all_txs,
  MAX(IF(STARTS_WITH(signer_public_key, 'ml-dsa-65'), LENGTH(signer_public_key), NULL)) AS max_key_len
FROM `bigquery-public-data.crypto_near_mainnet_us.transactions`
WHERE block_date >= '2026-07-01'
GROUP BY block_date ORDER BY block_date;
