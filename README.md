# Post-Quantum Sharding Research

Phaneendra Gavara, Namana, Meet Vyas. No leads; decisions are mutual. Working title: *Quantum-Assisted
Optimization of Blockchain Sharding Under Post-Quantum Cryptographic Migration*.

Labels used everywhere: **Fact** = confirmed in a source we opened. **Check** = verify yourself.
**Unknown** = not confirmed. Never write "first" or "no one has done this" unless `docs/novelty-search-log.md` supports it.

## Research questions (STATUS: pending professor feedback, task T1; wording from the 2026-11-12 "Where We Stand" doc)
1. Does migration change the best account-to-shard placement?
2. Do shards stay balanced as accounts migrate gradually?
3. Are migrated transactions priced for the resources they use?

Note: the v4 problem statement (2026-10-27) frames four research questions (RQ1 to RQ4). Reconcile the two framings
when the professor's feedback is recorded (G1/G2), then replace this section with the agreed wording.

## Plan
16 weeks, go / no-go gate in week 6. Week-6 criteria (draft, thresholds are our own proposal): `docs/week6-criteria.md`.
Week 1 plan: project doc `claude/2026-11-23_Week-1-Plan.md`; interactive page https://claude.ai/artifact/V8UARjnTvRwhzbaYQoJgqm

## Data sources (all free)
- Ethereum (workload trace; Ethereum itself is not execution-sharded): `bigquery-public-data.crypto_ethereum`
  (Fact: dataset name confirmed in the console on 2026-11-23, project quantum-research-515623).
- NEAR (real sharded behaviour): `bigquery-public-data.crypto_near_mainnet_us`; docs https://docs.near.org/data-infrastructure/big-query
  Last available date and ML-DSA coverage: see `docs/near-data-note.md` (Unknown until T3 finishes).
- MultiversX (BigQuery), TON (AWS): later weeks.

## How to run a query
1. Open BigQuery in your own sandbox project (no billing account, no card).
2. Paste a query from `queries/`. **Dry-run first:** the editor shows "This query will process X when run".
3. If X is large, the filter is not hitting the partition column. Fix it before running.
4. Run it, then add one line to `docs/quota-log.md` (who, purpose, bytes, date).
Sandbox limits (Fact: Google docs): 1 TiB of queries a month, 10 GiB lifetime storage (not refunded on deletion),
tables and partitions expire after 60 days, no streaming inserts, no DML, no Data Transfer Service.
A single query over about 100 GiB needs the others' agreement first.

## Sandbox sharing finding (step P2)
TO FILL: can a sandbox project be shared with the other two? Unknown (not documented). If not, each member uses
their own project (separate 1 TiB a month each) and we keep queries identical so results match.

## Message-size choice (step P5)
TO FILL after `queries/01_ethereum_columns.sql` and `queries/03_ethereum_message_size_proxy.sql`:
which column(s) give message size, the fixed overhead added, and what the proxy leaves out.
The deck's worked examples (185 B transfer, 565 B call) are illustrations, not measurements.

## Repository layout
- `data/` small samples only (results are rebuilt from queries, not stored in git)
- `queries/` BigQuery SQL, numbered; `src/` solver code and tests; `notebooks/`; `docs/` notes and decisions
- `requirements.txt` pinned environment; setup and test results in `docs/setup-solvers.md`
- Run all solver tests: `python src/run_all.py`

## Conventions
- Use "Phaneendra" in team-facing documents.
- Never commit credentials, keys or tokens (see `.gitignore`).
- Commits carry the author's own name only; no co-author lines.
- Decisions are recorded in `docs/` and agreed by all three before they are built on.
