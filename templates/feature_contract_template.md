# Feature Contract — <feature_name> (v<version>)

## 1. Overview
- **Feature name:** <feature_name>
- **Version:** v<version>
- **Status:** Draft | Active | Deprecated
- **Owner (team/person):** <owner>
- **Steward / Backup:** <backup_owner>
- **Business purpose:** <what decision or outcome this feature supports>
- **Model(s) / use cases:** <training and serving consumers>

---

## 2. Entity & Join Contract
Defines how this feature attaches to real-world entities.

- **Primary entity:** <entity_name>
- **Join keys:** <key1>, <key2>, ...
- **Key uniqueness expectation:** 1:1 | 1:many (must be explicit)
- **Join type:** left | inner | other
- **Join failure policy:** drop | default | quarantine
- **Expected match rate:** ≥ <x%>
- **Fanout / duplication policy:** <what happens if join explodes>

---

## 3. Time Semantics
Defines temporal correctness and leakage protection.

- **Event timestamp field:** <field_name>
- **Timestamp timezone:** <UTC / local + offset>
- **Point-in-time correctness:** required | not required
- **Lookback window:** <e.g. 7d, 30d>
- **Allowed lateness:** <e.g. 24h>
- **Leakage guardrails:** <how future data is prevented>

---

## 4. Source & Lineage
Defines where the feature comes from and how it is produced.

- **Source system(s):** <db / table / topic / API>
- **Source owner:** <team>
- **Refresh cadence:** real-time | hourly | daily | batch
- **Upstream dependencies:** <pipelines / dbt models / jobs>
- **Lineage link:** <URL to catalog / DAG if available>

---

## 5. Feature Definition

### 5.1 Human-Readable Logic
- **Definition:** <plain English definition>
- **Aggregation:** <sum / avg / count / max / window>
- **Filters:** <eligibility rules>
- **Dedup rules:** <latest record / distinct keys / tie-breakers>
- **Edge cases:** <nulls, missing joins, partial history>

### 5.2 Schema
- **Data type:** int | float | string | bool | enum | array | struct
- **Units:** <e.g. USD, seconds, count>
- **Nullable:** yes | no
- **Default value:** <value + rationale>
- **Allowed range / values:** <min/max or categorical set>

---

## 6. Data Quality Contract
Rules that must always hold true.

- **Completeness:** null rate ≤ <x%>
- **Validity:** <range checks, enum checks>
- **Uniqueness:** <if applicable>
- **Consistency:** <cross-field invariants>
- **Outliers:** <clip / flag / winsorize>
- **Freshness:** feature age ≤ <x>
- **Cardinality checks:** <join match rate, fanout ratio>

---

## 7. Drift & Monitoring
Defines how drift is detected and acted upon.

- **Baseline window:** <e.g. last 30 days>
- **Drift metrics:** PSI | KS | JS | custom
- **Thresholds:**
  - **Warn:** <value>
  - **Fail / block promotion:** <value>
- **Semantic drift checks:** <definition change detection>
- **Join drift checks:** <match rate, fanout, duplicates>
- **Alert routing:** <Slack / PagerDuty / email>

---

## 8. Training–Serving Parity
Ensures consistency between offline and online computation.

- **Offline computation path:** <how / where>
- **Online computation path:** <how / where>
- **Parity required:** yes | no
- **Shadow compare enabled:** yes | no
- **Acceptable delta:** <tolerance>

---

## 9. Access, Privacy & Compliance
Defines governance and regulatory constraints.

- **Data classification:** Public | Internal | Confidential | Restricted
- **PII / PHI present:** yes | no
- **Masking / tokenization:** <approach>
- **Retention policy:** <duration>
- **Approved consumers:** <teams / systems>
- **Audit requirements:** <if any>

---

## 10. Versioning & Change Control
Defines how changes are managed safely.

- **Served versions immutable:** yes | no
- **Breaking changes require new version:** yes | no
- **Deprecation plan:** <timeline + communication>
- **Rollback plan:** <how to revert>
- **Changelog:**
  - v1 — <date>: <initial release>
  - v2 — <date>: <summary of changes>

---

## 11. Test Plan (CI / Pre-Promotion)
Validation required before production use.

- **Unit tests:** <logic tests>
- **Backfill validation:** <sample checks>
- **Canary materialization:** yes | no
- **Shadow reads:** yes | no
- **Performance tests:** <latency / throughput targets>

---

## 12. Sign-Off
Formal accountability for this feature.

- **Data owner approval:** <name / date>
- **ML owner approval:** <name / date>
- **Platform approval:** <name / date>

