# Enterprise Document Compliance Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build and publish a reusable Codex skill for traceable, regulation-pack-driven DOCX compliance review with Markdown/JSON reports and optional annotated copies.

**Architecture:** Keep domain judgment in `SKILL.md` and reference policies; use deterministic Python scripts for DOCX extraction, annotation, and report validation. Regulation packs remain user-owned YAML/JSON inputs and are never hard-coded into the skill.

**Tech Stack:** Markdown, Python 3, `python-docx`, JSON/YAML-compatible data, OOXML comments where supported.

---

### Task 1: Create skill metadata and workflow

**Files:** `enterprise-doc-compliance-audit/SKILL.md`, `enterprise-doc-compliance-audit/agents/openai.yaml`

- [ ] Define triggering description, audit workflow, evidence rules, privacy boundaries, and output contract.
- [ ] Add concise UI metadata matching the skill purpose.

### Task 2: Add reusable references and schemas

**Files:** `enterprise-doc-compliance-audit/references/regulation-pack-schema.md`, `report-schema.md`, `review-policy.md`

- [ ] Document required regulation fields, finding fields, status/risk semantics, and source traceability.

### Task 3: Implement deterministic DOCX utilities

**Files:** `enterprise-doc-compliance-audit/scripts/extract_docx.py`, `annotate_docx.py`, `validate_report.py`

- [ ] Extract paragraphs and tables with stable indexes and text hashes.
- [ ] Copy input before applying safe highlights/comments and emit a machine-readable annotation map.
- [ ] Validate report structure, finding enums, and citation completeness.

### Task 4: Validate and publish

**Files:** `enterprise-doc-compliance-audit/tests/fixtures/*`

- [ ] Run representative script checks and skill `quick_validate.py`.
- [ ] Initialize Git, commit the skill and spec, add the supplied remote, and push the default branch.
