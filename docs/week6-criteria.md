# Week-6 go / no-go criteria

STATUS: DRAFT until all three members agree (step G3). Commit the agreed version before any result exists.
Thresholds below are our own proposal, not from the literature.

The full study goes ahead only if all four checks pass.

1. Controls. Uniform growth gives no gain (pipeline sanity check; see src/test_control.py).
   Pass rule: partition and cut cost ratio unchanged when every edge weight is multiplied by the same constant.
2. Uneven growth. Growth factors differ clearly across account pairs.
   Pass rule: TO AGREE (for example, ratio of 90th to 10th percentile of per-pair growth factor >= ___).
3. Exact check. On 20 to 40 account graphs, the exact best placement changes after migration.
   Pass rule: TO AGREE (for example, in at least ___ of ___ sampled graphs).
4. Size and stability. Gain >= 2% (proposed), above 3 times run-to-run noise, and still present on window t+1.
   Gain definition: TO AGREE (cross-shard bytes, re-optimised placement vs placement kept from before migration).

Agreed by: Phaneendra [ ]  Namana [ ]  Meet [ ]   Date: ____
