# Signature and public-key size table (N9 / T6)

Started 2026-11-24. Labels: Fact = read from the standard or observed; Check = not yet reopened at the source.

| Scheme | Public key (bytes) | Signature (bytes) | Added per message vs ECDSA 65 B | Status |
|---|---|---|---|---|
| ECDSA secp256k1 (Ethereum r,s,v) | 33 compressed or 64 raw (not used in the tx) | 65 | 0 | Check: 65 is our deck figure; reopen the Ethereum yellow paper |
| Ed25519 | 32 | 64 | n/a | Fact: RFC 8032 |
| ML-DSA-44 | 1,312 | 2,420 | 2,355 | Fact: FIPS 204 Table 2 (read 2026-11-24) |
| ML-DSA-65 | 1,952 | 3,309 | 3,244 | Fact: FIPS 204 Table 2 (read 2026-11-24) |
| ML-DSA-87 | 2,592 | 4,627 | 4,562 | Fact: FIPS 204 Table 2 (read 2026-11-24) |
| Falcon-512 | 897 | 666 in the spec, 752 in liboqs | Check | Check: reopen the Falcon spec and the liboqs datasheet; state which one is used |
| SLH-DSA families | Check | Check | Check | Check: liboqs SPHINCS+ datasheet |

Private-key sizes (FIPS 204): ML-DSA-44 2,560; ML-DSA-65 4,032; ML-DSA-87 4,896 bytes.

## Cross-check against observed NEAR data (2026-11-24)
- Fact: ML-DSA-65 `signature` strings in NEAR's BigQuery transactions are 4,528-4,529 characters; 3,309 bytes in base58 plus the
  10-character prefix `ml-dsa-65:` is about that long (base58 expands by about 1.366). Consistent, not a proof.
- Fact: ML-DSA-65 `signer_public_key` strings are 2,676 characters; 1,952 bytes in base58 plus the prefix is about that long.
- Fact: the minimum transaction conversion gas is exactly 100 Ggas higher for ML-DSA-65 than for Ed25519 (NEP-645's stated cost).
- Unknown: the full on-chain transaction size in bytes. NEAR's BigQuery tables hold no byte-size column.
