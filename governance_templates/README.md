# 🛡️ Compliance Patterns

This folder captures **enterprise-ready governance patterns** for AI and data platforms.  
These patterns demonstrate how regulated industries (healthcare, finance, insurance) can ensure **privacy, auditability, and reproducibility** when deploying AI systems on Databricks and beyond.

---

## 🔒 1. PHI/PII Masking

- **Column-Level Security** with Unity Catalog:
  ```sql
  CREATE FUNCTION intent_models.mask_speaker_name_pii_phi(name STRING)
  RETURN CASE 
      WHEN is_member('CopilotAdmins') THEN name 
      ELSE 'REDACTED' 
  END;
  ```
* Ensures sensitive fields (speaker names, patient IDs, etc.) are **redacted by default**.  
* Access is **role-based** (admins see raw values, analysts see masked).

---

## 🧾 2. Audit & Traceability

* Every ingestion step writes **append-only audit tables**:
  * `audio_transcripts` with transcript + ingestion timestamp.
  * Immutable records ensure **non-repudiation** for compliance audits.

* Supports **lineage tracing**:  
  *“Where did this transcript come from? Who accessed it? When?”*

---

## 📜 3. Model Governance via MLflow

* All models are **registered with metadata**:
  * Accuracy, parameters, features used.
  * Input examples logged for reproducibility.

* Supports **model cards** for bias, performance, and intended use.  
* Enables **compliance sign-off gates** before promotion to production.

---

## 🕰 4. Delta Lake ACID + Time Travel

* Guarantees **atomic, consistent, isolated, durable** operations.  
* Time Travel queries allow regulators to ask:

  > *“What did your dataset look like on Jan 1, 2024, before retraining?”*

* Critical for **audits, incident forensics, and rollback**.

---

## 📑 5. Compliance Checklists

* **GDPR/HIPAA alignment**: right-to-forget, minimum retention.  
* **Audit hooks**: ingestion timestamps + append-only logs.  
* **Bias & fairness hooks**: placeholders for explainability and ethical AI assessments.

---

## 🏆 Why This Matters

These compliance patterns shift AI from *“prototype demos”* → *“production-grade systems ready for regulators and boards”*.  
They ensure that AI **earns trust** by embedding governance **at the architecture level**, not as an afterthought.
