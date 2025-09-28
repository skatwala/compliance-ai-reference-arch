# 🤝 Contributing Guidelines

Thank you for your interest in improving the **Compliance AI Reference Architecture**!  
This project aims to provide **reusable compliance patterns and governance templates** for regulated AI systems.  

To keep contributions **high-quality and consistent**, please follow these guidelines.

---

## 📂 Repository Structure

- **`compliance_patterns/`** → Architecture-level patterns (masking, audit, governance, time travel, checklists).  
- **`governance_templates/`** → Templates & workflows (model cards, approval gates, monitoring).  
- **`README.md`** → Top-level overview of the repo.  
- **`CONTRIBUTING.md`** → This file.

---

## 🛠️ How to Contribute

1. **Fork the repository** and create a feature branch:
   ```bash
   git checkout -b feature/my-new-pattern
   ```

2. **Add your contribution** inside the correct folder:
   - `compliance_patterns/` for new compliance techniques.  
   - `governance_templates/` for new governance templates.  

3. **Documentation is required**:  
   - Every new item must include a `README.md` with:
     - Purpose / rationale.  
     - Example code or template.  
     - Compliance relevance (GDPR, HIPAA, SOX, etc.).  

4. **Formatting**:  
   - Use **Markdown** for readability.  
   - Include **code fences** for SQL, Python, YAML, etc.  
   - Keep language **clear, enterprise-friendly, regulator-ready**.  

5. **Testing & Validation**:  
   - If adding code snippets (e.g., SQL, Python), ensure they run cleanly.  
   - If adding a governance template, validate it aligns with **real-world compliance workflows**.  

---

## ✅ Contribution Checklist

Before submitting a PR, confirm that:

- [ ] Your addition is in the correct folder.  
- [ ] Documentation (`README.md`) is included.  
- [ ] Code snippets are tested and runnable.  
- [ ] Compliance relevance is explicitly explained.  
- [ ] Language is professional, regulator-ready, and non-academic.  

---

## 🔍 Review Process

- PRs will be reviewed for **clarity, compliance accuracy, and enterprise relevance**.  
- Approved contributions will be merged into `main`.  
- Larger contributions may require **additional sign-off** (e.g., adding new categories).  

---

## 🙏 Acknowledgements

Every contribution helps this project serve as a **blueprint for trustworthy AI**.  
By contributing, you are helping teams in healthcare, finance, and other regulated industries **scale AI responsibly**.

---

> 💡 Pro Tip: Contributions that include **real-world scenarios** (e.g., GDPR right-to-forget, HIPAA audit hooks) are especially valuable!
