# BigQuery quota log

Sandbox limit: 1 TiB of queries per month (Fact: Google sandbox docs). Dry-run every query first.
Anything over about 100 GiB for a single query needs the other two members' agreement.

| Date | Who | Project | Purpose | Bytes processed | Running total this month |
|---|---|---|---|---|---|
| 2026-11-23 | Phaneendra | quantum-research-515623 | P3: list columns of crypto_ethereum.transactions (INFORMATION_SCHEMA) | ~10 MB (console estimate; likely the per-query minimum, Check) | ~10 MB |
| 2026-11-24 | Phaneendra | quantum-research-515623 | P3 rerun: narrowed column list incl. is_partitioning_column (9 rows, none marked YES) | ~10 MB (estimate) | ~20 MB |
| 2026-11-24 | Phaneendra | quantum-research-515623 | INFORMATION_SCHEMA.TABLES on transactions (table_type = VIEW, ddl null) | ~10 MB (estimate) | ~30 MB |
| 2026-11-24 | Phaneendra | quantum-research-515623 | INFORMATION_SCHEMA.VIEWS on transactions (view_definition null) | ~10 MB (estimate) | ~40 MB |
| 2026-11-24 | Phaneendra | quantum-research-515623 | One-day graph size, 2024-01-01 (txs, senders, receivers, pairs) | 128.9 MB (estimate) | ~169 MB |

Dry-run only, not executed (2026-11-24, estimates from the console):
- from_address + to_address, no date filter: 316.82 GB. Never run this.
- from_address + to_address, one day (2024-01-01): 128.9 MB.
- from_address + to_address + LENGTH(input), one day: 2.64 GB (input is the expensive column).

NEAR queries run 2026-11-24 by Phaneendra for Namana's N2-N6 (console estimates):
| 2026-11-24 | Phaneendra | quantum-research-515623 | N2/N3: table list, all columns, newest partitions, first/last day and gap count, gap list, monthly volume (6 metadata queries) | ~60 MB total | ~229 MB |
| 2026-11-24 | Phaneendra | quantum-research-515623 | N4: key/signature type counts, week 2026-11-10..16 (queries/16) | 928.84 MB | ~1.16 GB |
| 2026-11-24 | Phaneendra | quantum-research-515623 | N6: daily ML-DSA-65 transactions since 2026-07-01 (queries/17) | 8.4 GB | ~9.6 GB |
| 2026-11-24 | Phaneendra | quantum-research-515623 | N5: gas and shard by key type, same week (queries/18) | 452 MB | ~10.0 GB |
