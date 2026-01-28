# Feature Contract — customer_profile (v1)

## 1. Overview
- **Feature name:** customer_profile
- **Version:** v1
- **Status:** Active
- **Owner (team/person):** Customer Analytics Team
- **Steward / Backup:** Data Platform Team
- **Business purpose:** Provide a stable, governed set of customer behavioral features for churn prediction and lifetime value models.
- **Model(s) / use cases:** Churn prediction, customer segmentation, personalization, retention scoring.

---

## 2. Entity & Join Contract
Defines how this feature attaches to real-world entities.

- **Primary entity:** customer_id
- **Join keys:** customer_id
- **Key uniqueness expectation:** 1:1
- **Join type:** left
- **Join failure policy:** default
- **Expected match rate:** ≥ 98%
- **Fanout / duplication policy:** If multiple records exist for a customer_id, select the most recent record based on event_timestamp.

---

## 3. Time Semantics
Defines temporal correctness and leakage protection.

- **Event timestamp field:** event_timestamp
- **Timestamp timezone:** UTC
- **Point-in-time correctness:** required
- **Lookback window:** 30d
- **Allowed lateness:** 24h
- **Leakage guardrails:** Feature computation must only use events with timestamps ≤ prediction time. Future-dated records are excluded by design.

---

## 4. Source & Lineage
Defines where the feature comes from and how it is produced.

- **Source system(s):** data_warehouse.customer_events
- **Source owner:** Data Engineering
- **Refresh cadence:** hourly
- **Upstream dependencies:** customer_events_ingestion_job, customer_activity_dbt_model
- **Lineage link:** https://catalog.company.com/lineage/customer_profile

---

## 5. Feature Definition

### 5.1 Human-Readable Logic
- **Definition:** Aggregated behavioral metrics representing recent customer activity.
- **Aggregation:** Rolling 30-day window.
- **Filters:** Only active customers with at least one event in the last 30 days.
- **Dedup rules:** Latest event per customer_id per day.
- **Edge cases:** If no events exist in the window, default values are applied.

### 5.2 Schema
- **Data type:** struct
- **Units:** mixed
- **Nullable:** no
- **Default value:** zeros for numeric fields
- **Allowed range / values:**
  - avg_order_value_30d: 0–10,000
  - orders_30d: 0–1,000
  - sessions_30d: 0–10,000

---

## 6. Data Quality Contract
Rules that must always hold true.

- **Completeness:** null rate ≤ 1%
- **Validity:** All numeric fields must be ≥ 0
- **Uniqueness:** One record per customer_id
- **Consistency:** orders_30d ≥ distinct_order_days_30d
- **Outliers:** Values above 99.9th percentile are flagged
- **Freshness:** Feature age ≤ 2 hours
- **Cardinality checks:** Join match rate ≥ 98%, fanout ratio ≤ 1.01

---

## 7. Drift & Monitoring
Defines how drift is detected and acted upon.

- **Baseline window:** last 30 days
- **Drift metrics:** PSI
- **Thresholds:**
  - **Warn:** PSI ≥ 0.1
  - **Fail / block promotion:** PSI ≥ 0.2
- **Semantic drift checks:** Detect changes to aggregation logic or window size.
- **Join drift checks:** Monitor match rate and duplicate customer_id occurrences.
- **Alert routing:** #ml-alerts Slack channel

---

## 8. Training–Serving Parity
Ensures consistency between offline and online computation.

- **Offline computation path:** data_warehouse.customer_features_offline
- **Online computation path:** feature_store.customer_profile_v1
- **Parity required:** yes
- **Shadow compare enabled:** yes
- **Acceptable delta:** ≤ 1% difference across numeric fields

---

## 9. Access, Privacy & Compliance
Defines governance and regulatory constraints.

- **Data classification:** Internal
- **PII / PHI present:** yes (customer_id)
- **Masking / tokenization:** customer_id is hashed in training datasets
- **Retention policy:** 365 days
- **Approved consumers:** ML Platform, Marketing Analytics
- **Audit requirements:** Quarterly access review

---

## 10. Versioning & Change Control
Defines how changes are managed safely.

- **Served versions immutable:** yes
- **Breaking changes require new version:** yes
- **Deprecation plan:** v1 will be supported for 90 days after v2 release
- **Rollback plan:** Switch feature service pointer to previous version
- **Changelog:**
  - v1 — 2026-01-01: Initial release

---

## 11. Test Plan (CI / Pre-Promotion)
Validation required before production use.

- **Unit tests:** Validate aggregation logic on synthetic data
- **Backfill validation:** Compare 7-day historical backfill against baseline
- **Canary materialization:** yes
- **Shadow reads:** yes
- **Performance tests:** p95 latency ≤ 50ms, error rate ≤ 0.1%

---

## 12. Sign-Off
Formal accountability for this feature.

- **Data owner approval:** J. Smith — 2026-01-01
- **ML owner approval:** A. Johnson — 2026-01-01
- **Platform approval:** Platform Lead — 2026-01-01

