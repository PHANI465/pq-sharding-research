# Ethereum dataset findings (P3/P4), 2026-11-24

Source: console queries run by Phaneendra in project quantum-research-515623 on bigquery-public-data.crypto_ethereum.

Fact (observed in the console):
- transactions is a VIEW, not a base table. INFORMATION_SCHEMA.TABLES gives table_type = VIEW and ddl = null; INFORMATION_SCHEMA.VIEWS gives view_definition = null.
- Because it is a view, INFORMATION_SCHEMA.COLUMNS reports is_partitioning_column = NO for every column. That flag cannot be used to find the partition column here.
- Column types: hash, from_address, to_address STRING; value NUMERIC; gas, gas_price, transaction_type INT64; input STRING (hex text, not BYTES); block_timestamp TIMESTAMP.
- Filtering on block_timestamp does reduce the scan: two address columns cost 316.82 GB with no filter and 128.9 MB for one day (2024-01-01).
- Adding LENGTH(input) for the same day costs 2.64 GB.
- 2024-01-01: 1,101,465 transactions; 413,772 distinct senders; 198,165 distinct receivers; 699,451 distinct sender-receiver pairs; 777 with to_address NULL (contract creation).

Check (not yet established):
- Which column the underlying table is partitioned by. The pruning result suggests block_timestamp (inference from the estimates, not from metadata).
- Whether the input STRING is a 0x-prefixed hex string, so that bytes = (LENGTH(input) - 2) / 2.
- Whether the full transaction size is available anywhere. No column in the nine checked holds it.

Unknown:
- Why Google exposes this as a view.
