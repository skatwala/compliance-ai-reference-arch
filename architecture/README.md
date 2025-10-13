# 🏗️ Architecture Blueprints

This folder provides **high-level architecture views** that show how compliance and governance are embedded into AI systems.  
The diagrams and notes here are intended for **executives, regulators, and technical architects** to understand the **big picture**.

 
 
---

## 🧭 Narrative Overview

The Compliance-AI architecture operationalizes a **governed machine-learning workflow** that prioritizes *traceability, reproducibility, and accountability*.

1. **Data Ingestion & Masking**  
   - All incoming data (e.g., audio transcripts or call logs) passes through PHI/PII masking layers.  
   - Unity Catalog applies column-level governance, ensuring no sensitive data leaves the secure perimeter.

2. **Delta Lake Storage & ACID Guarantees**  
   - Every transformation is stored in **Delta tables**, providing ACID transactions and **time-travel rollback**.  
   - This ensures a model can always be reproduced at the same data state for audits or FDA/GxP reviews.

3. **Model Training & Governance (MLflow + TrustGate)**  
   - Models such as **DistilBERT** are fine-tuned on versioned datasets.  
   - All runs are wrapped in **TrustGate decorators** that log correlation IDs, retries, and metadata to MLflow.  
   - Every experiment includes tags for owner, dataset hash, risk rating, and validation fold count.

4. **Evaluation & Fold Strategy**  
   - Each model run is validated using multiple stratified folds to ensure fairness, stability, and reliability (see below).  
   - Results and metrics are stored alongside lineage artifacts for end-to-end auditability.

5. **Governance, Approval & Monitoring**  
   - MLflow Registry + Compliance Templates enforce approval gates.  
   - Dashboards surface drift, bias, and latency to Compliance and Risk teams.  
   - Reports are automatically versioned for regulator-ready evidence.

---

## 🧩 Fold-Strategy Explanation (3-Fold / 5-Fold / 30-Fold)

| Fold Type | Purpose | Typical Usage | Governance Benefit |
|------------|----------|----------------|--------------------|
| **3-Fold Validation** | Quick reliability check for small datasets or early experimentation | Used in rapid iteration phases or exploratory notebooks | Provides minimal yet repeatable baseline with short runtime |
| **5-Fold Validation** | Balanced trade-off between runtime and statistical confidence | Used in production candidate evaluation before model promotion | Delivers moderate robustness while maintaining compute efficiency |
| **30-Fold Cross-Validation** | Deep reliability audit for regulated releases (e.g., clinical / finance) | Applied during final model assurance prior to regulatory filing | Produces statistically stable results and **reduces overfitting risk** |

**Rationale:**  
- The fold count is logged as a **governance parameter** (`fold_strategy`) in MLflow.  
- Higher folds trigger longer runtime but yield more defensible model metrics under audit.  
- For regulated AI, reproducibility across folds is **a compliance control**, not just a technical choice.

---

## 🖼️ Example: Compliance-Aware AI Pipeline

```mermaid
flowchart LR
    subgraph Ingestion
        A[📥 Audio Upload] --> B[🔒 PHI/PII Masking]
        B --> C[🧾 Append-Only Audit Logs]
    end

    subgraph Storage
        C --> D[🗂️ Delta Lake<br/>ACID + Time Travel]
    end

    subgraph ModelOps
        D --> E[📜 MLflow Registry<br/>Model Metadata]
        E --> F[🚦 Approval Gates<br/>(Fold-Aware Evaluation)]
    end

    subgraph Monitoring
        F --> G[📊 Compliance Dashboards<br/>Bias · Latency · Drift]
    end

    G -->|Reports| H[📑 Regulators & Boards]
