# Week 1 results (2026-11-24)

Project: Quantum-Assisted Optimization of Blockchain Sharding Under Post-Quantum Cryptographic Migration.
Prepared for Phaneendra, Namana and Meet. Phaneendra's, Meet's and Namana's week-1 data and code steps were done in one session (queries run in
Phaneendra's console, project quantum-research-515623). Namana and Meet should rerun and confirm their own parts.
Labels: Fact = observed or read at the source; Check = inferred, needs confirming; Unknown = not established.

## 1. Phaneendra (T2): Ethereum data and setup

Fact:
- `crypto_ethereum.transactions` is a VIEW, not a base table. INFORMATION_SCHEMA.TABLES: table_type VIEW, ddl null. INFORMATION_SCHEMA.VIEWS: view_definition null.
- No column reports is_partitioning_column = YES. This is because it is a view; the flag cannot find the partition column here.
- Columns: hash, from_address, to_address STRING; value NUMERIC; gas, gas_price, transaction_type INT64; input STRING; block_timestamp TIMESTAMP.
- Filtering on block_timestamp does prune the scan. from_address + to_address: 316.82 GB with no filter, 128.9 MB for one day (2024-01-01).
  Adding LENGTH(input) for that day: 2.64 GB.
- 2024-01-01: 1,101,465 transactions; 413,772 senders; 198,165 receivers; 699,451 distinct sender-receiver pairs; 777 contract creations.
- Quota used this month (console estimates): about 10 GB of 1 TiB.

Check: the partition column is block_timestamp (inferred from estimates only). Input is 0x-prefixed hex so bytes = (LENGTH - 2) / 2.
Unknown: any column holding full transaction size; why Google exposes the table as a view.

Not done (needs people or accounts): P2 sharing test (needs Namana's Google account); P7 GitHub repo, push and invites; P9 push test; G1-G5 group items.

## 2. Namana (T3): NEAR data note

Full detail in docs/near-data-note.md and queries/13-18. Highlights, all Fact unless marked:
- Dataset bigquery-public-data.crypto_near_mainnet_us has 16 objects. The docs' `receipts` view and `receipt_origin` table are not in the live dataset (live name: receipt_origin_transaction).
- Coverage: 2020-07-23 to 2026-11-24. Still being filled (newest partition written at the time of the query). 11 missing days, all in Jul-Aug 2020.
- Volume fell about 3.7x in April 2026 (3.5M to 0.8M transactions per day). Why: Unknown.
- ML-DSA-65 is present. Prefix `ml-dsa-65` in transactions.signer_public_key and .signature. First transaction 2026-07-20.
  Monthly ML-DSA-65 transactions: Jul 104, Aug 152, Sep 1,347, Oct 4,564, Nov 1-24 3,668 (about 0.02 per cent of all transactions).
  Week 10-16 Nov: 1,545 ML-DSA-65 vs 6,026,804 Ed25519 vs 7 secp256k1.
- Transactions carry the full ML-DSA public key (2,676-character string), not the 32-byte hash.
- Shard and gas: shard_id in transactions, chunks, execution_outcomes, receipt_actions. Nine distinct shard ids in the week checked (4, 6-13).
  Gas: transactions.receipt_conversion_gas_burnt, execution_outcomes.gas_burnt, chunks.gas_used.
- Minimum conversion gas is exactly 100 Ggas higher for ML-DSA-65 than for Ed25519, matching NEP-645.
- ML-DSA transactions are concentrated on shard 13 (1,076 of 1,545). Why: Unknown.
- Data route: BigQuery works; no alternative route needed for week 1. Size table started in docs/size-table.md (FIPS 204 Table 2 read).

## 3. Meet (T4): solvers

Fact (fresh run of the full suite, 8 seconds, Python 3.13): all tests pass (M2 METIS smoke, M4 exact CP-SAT, M5 QUBO simulated annealing, M6 known answer,
M7 four-account worked example, M8 control, fair-balance test).
- Four-account example: before migration {A,B}|{C,D} costs 3,700 and {A,C}|{B,D} costs 4,260; after (+3,244 B per message) 68,580 vs 17,236. The best layout flips.
- METIS returns an 11/9 split on a 20-account graph even at ufactor 1 (cut 988); the exact solver strict 10/10 gives 1,056 and gives 988 with the same size range.
  The comparison must use the same balance tolerance. Why METIS allows 11/9: Unknown.
- QUBO penalty window is narrow on a harder graph: weights 100-1000 matched the exact answer; 1, 10, 50, 5000 and 20000 did not.
- Exact solver: 2 shards optimal at n=20/30/40 in 0.0/0.2/1.0 s; 4 shards 1.2 s (n=20), 10.2 s (n=30); n=40 hit the 120 s limit without proof of optimality.
- Not done (needs his machine): M1 install on Windows, M9 repeat of tests there. The device's Python 3.10 is too old for the D-Wave Ocean install; use 3.11+.
- D-Wave: the Leap Quantum LaunchPad programme (announced Jan 2025) offers a 3-month free trial to "qualified participants". Whether we qualify, and whether it is still open now, is Unknown.
- TxAllo: no public code found (Fact per our code finder; one search, so not a claim of absence).

## 4. What this changes
- The week-6 data question has a better start than assumed: NEAR has real ML-DSA transactions, but only about 0.02 per cent of traffic. Adoption levels of 25, 50 and 100 per cent therefore have to be simulation, labelled as such.
- NEAR pricing data (T15): the 100 Ggas per signature is visible in the data, so pricing can be checked against real gas, not only the spec.
- Ethereum has no post-quantum signatures; sizes there come from the standard, and our message-size proxy uses LENGTH(input) with the 3,244 B addition modelled.
- Published pages still say to look for a YES partition row (P3) and describe the hash form of keys (N4). Those two passages need updating.

## 5. Still open
Professor feedback and the week-1 start date; framing decision (RQ1-RQ4 vs three ranked candidates); week-6 criteria 2 and 3 still "TO AGREE"; sandbox sharing; repo creation and invites.
