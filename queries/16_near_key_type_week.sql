-- key and signature type of every transaction in one week (about 0.93 GB estimate)
SELECT SPLIT(signer_public_key, ':')[OFFSET(0)] AS key_prefix, SPLIT(signature, ':')[OFFSET(0)] AS sig_prefix,
  COUNT(*) AS txs, MIN(LENGTH(signature)) AS min_sig_len, MAX(LENGTH(signature)) AS max_sig_len
FROM `bigquery-public-data.crypto_near_mainnet_us.transactions`
WHERE block_date BETWEEN '2026-11-10' AND '2026-11-16'
GROUP BY key_prefix, sig_prefix ORDER BY txs DESC;
