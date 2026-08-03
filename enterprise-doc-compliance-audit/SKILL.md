---
name: enterprise-doc-compliance-audit
description: Review enterprise DOCX documents against user-provided, versioned regulation packs and configured official sources. Use for compliance audits that need traceable findings, risk levels, evidence citations, Markdown/JSON reports, and optional annotated DOCX copies.
---

# Enterprise Document Compliance Audit

Use this workflow when a user provides a business document and asks whether it complies with laws, regulations, standards, or internal policy.

## Workflow

1. Identify the document type, jurisdiction, industry, effective date, and requested outputs. Never infer jurisdiction silently.
2. Load and validate the user's regulation pack using [regulation-pack-schema.md](references/regulation-pack-schema.md). Prefer local sources; only use configured official domains for online retrieval. Record title, issuer, version/effective date, locator, URL/path, and retrieval date. At pack-ingest time, create embeddings with `scripts/build_vector_index.py`; use `scripts/retrieve_vector.py` for semantic retrieval and `scripts/retrieve.py` for exact-term retrieval. Do not place the entire regulation corpus in context.
3. Extract paragraphs and tables with `scripts/extract_docx.py`. Preserve paragraph/table indexes and text hashes for evidence locations. Generate temporary query embeddings for each paragraph/table, retrieve relevant rules, and include only the top candidates plus their source metadata in the review context. Do not persist user-document embeddings unless the user explicitly requests an isolated document index.
4. Apply each retrieved applicable rule. Quote the smallest relevant document passage and cite the exact regulation locator. Classify each result as `明确违反`, `疑似风险`, `信息不足`, or `通过`; use risk `低`, `中`, `高`, or `严重`, plus a confidence value.
5. Produce JSON and Markdown reports following [report-schema.md](references/report-schema.md). A conclusion without a source citation must be `信息不足` or `需人工确认`.
6. For editable DOCX, copy the original to a new path and run `scripts/annotate_docx.py` with findings. Never overwrite the source. If matching is ambiguous, leave the document unchanged for that finding and record the reason.
7. Apply the safeguards in [review-policy.md](references/review-policy.md), including privacy, uncertainty, and human-review language.

## Output contract

Return the report paths, annotated-copy path when created, source list, coverage summary, and unresolved review items. Do not present output as legal advice or claim that the review is exhaustive.
