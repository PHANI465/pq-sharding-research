# NEAR data note (N8) -- owner: Namana (T3)

Filled on 2026-11-24 from console queries run by Phaneendra in project quantum-research-515623 on Namana's behalf.
Namana: rerun the queries in queries/13-18 in your own project and confirm or correct every number below.
Labels: Fact = observed in the console on 2026-11-24; Check = inferred, needs confirming; Unknown = not established.

## Dataset and tables
- Dataset: bigquery-public-data.crypto_near_mainnet_us
- Fact: 16 objects. BASE TABLE: account_changes, blocks, chunks, circulating_supply, execution_outcomes, ft_balances_daily,
  ft_events, nft_events, receipt_actions, receipt_details, receipt_origin_transaction, transaction_actions, transactions.
  VIEW: accounts. MATERIALIZED VIEW: ft_events_contracts_by_account, nft_events_contracts_by_account.
- Fact: the NEAR docs list a `receipts` view and a table called `receipt_origin`; neither name appears in the live dataset
  (the live names are `receipt_origin_transaction` and no `receipts` object). Treat the docs as out of date there.
- Fact: partition column is `block_date` (DATE) on transactions, chunks, execution_outcomes, account_changes, receipt_actions.

## Coverage in time
- Fact (from INFORMATION_SCHEMA.PARTITIONS, table transactions): first day 2020-07-23, last day 2026-11-24.
- Fact: 2,305 daily partitions against 2,316 calendar days, so 11 days are missing, in 6 gaps, all in 2020:
  2020-07-25/26, 07-30, 08-01 to 08-04, 08-07, 08-14/15, 08-17. None in 2026.
- Fact: the newest partition (2026-11-24) was last written 2026-11-24 21:07 UTC, the moment we queried. The dataset is still
  being filled. This closes the earlier Unknown "is it still being filled".
- Fact: covers 20 Jul 2026 onward, to today.
- Fact: volume dropped sharply in April 2026. About 3.5 million transactions per day in Jan-Mar 2026
  (3.51M, 3.49M, 3.48M), then 0.95M per day in April and about 0.7-0.8M per day from May to November.
  Why: Unknown (not investigated; the NEAR Lake deprecation of 24 Mar 2026 is a Check, not a conclusion).
  Any count that spans March to April must say which side it is on.

## ML-DSA activity (N4, N6)
- Fact: post-quantum activity is present. In transactions, `signer_public_key` and `signature` start with the text
  prefix `ml-dsa-65` for ML-DSA-65 transactions (Ed25519 ones start with `ed25519`, secp256k1 with `secp256k1`).
- Fact: week 2026-11-10 to 2026-11-16: 6,026,804 ed25519, 1,545 ml-dsa-65, 7 secp256k1 transactions
  (ML-DSA is about 0.026 per cent). The ed25519 control found millions, so the method works.
- Fact: first ML-DSA-65 transaction in the data is on 2026-07-20 (2 transactions, 2 signers), the go-live date.
- Fact: ML-DSA-65 transactions per month: Jul 104; Aug 152; Sep 1,347; Oct 4,564; Nov 1-24: 3,668.
  Share of all transactions in Nov 1-24: 3,668 of 17,446,187 (about 0.021 per cent).
  Most distinct ML-DSA signers in any one day, by month: Jul 7, Aug 5, Sep 24, Oct 38, Nov 35.
- Fact: the unit counted is transactions whose signing key is ML-DSA-65 (the key sits in the transaction's own
  signer_public_key), not keys added or accounts migrated.
- Fact: ML-DSA `signer_public_key` strings are 2,676 characters, which fits a full 1,952-byte key in base58 plus the prefix,
  so transactions carry the full key. (NEP-645's 32-byte hash is for stored access keys; where it appears in
  account_changes or transaction_actions.args is Unknown, not searched.)
- Fact: ML-DSA `signature` strings are 4,528-4,529 characters, which fits a 3,309-byte signature in base58 plus prefix.
  Ed25519 signature strings are 94-96 characters. The base58 length is not the byte length; use the standard's byte sizes.
- Check: ML-DSA-65 is the only post-quantum prefix searched. ML-DSA-44/87 or other schemes were not searched.

## Shard and gas fields (N5)
- Fact: `shard_id` (INT64) is in transactions, chunks, execution_outcomes, receipt_actions.
- Fact: week 2026-11-10 to 16 shows nine distinct shard ids: 4, 6, 7, 8, 9, 10, 11, 12, 13 (consistent with nine shards;
  numbering is not 0-8).
- Fact: gas columns: transactions.receipt_conversion_gas_burnt (INT64), execution_outcomes.gas_burnt (FLOAT64),
  chunks.gas_used and gas_limit (FLOAT64).
- Fact: in that week the smallest conversion gas for ml-dsa-65 transactions was 303,006,125,000 and for ed25519
  203,006,125,000: exactly 100 Ggas higher, as NEP-645 states (100 Ggas per signature).
- Fact: ML-DSA transactions are concentrated: shard 13 had 1,076 of 1,545 (70 per cent), shard 4 238, shard 7 108,
  shard 9 49, shard 12 45, shard 11 23, shards 8 and 10 3 each. Why: Unknown (possibly a few accounts; not checked).
- Fact: key and argument columns: signer_public_key and signature (transactions), signer_public_key and args
  (receipt_actions, transaction_actions), action_kind (both).

## Route chosen
- Data route: BigQuery works and holds post-quantum activity. No alternative route (N7) is needed for week 1.

## Cost
- Fact (console estimates, all within the sandbox): metadata queries 10 MB each; one-week prefix count 928.84 MB;
  gas/shard by key type 452 MB; daily ML-DSA count from 2026-07-01 8.4 GB.

## Open Unknowns
- Why volume fell in April 2026.
- Where ML-DSA keys appear in account_changes / args (the hash form).
- Whether ML-DSA signers are few accounts producing most transactions.
- What replaced NEAR Lake as the source (the dataset is still updating, so something does).
