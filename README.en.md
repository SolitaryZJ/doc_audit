# Enterprise Document Compliance Audit

[中文](README.md)

An open-source Codex skill for reviewing enterprise documents against versioned, user-provided regulation packs. It produces traceable Markdown/JSON reports and, when safe, a highlighted DOCX copy.

## Features

- Pluggable regulation packs for jurisdictions, industries, and document types
- Evidence-backed findings with source locators, excerpts, and risk levels
- Four states: `明确违反`, `疑似风险`, `信息不足`, and `通过`
- Stable paragraph/table indexes and text hashes for DOCX evidence
- Optional highlighted DOCX copy without overwriting the source
- Local-first processing with configurable official-source lookup
- Local SQLite FTS5 RAG retrieves relevant rules per document section instead of loading the full corpus into context
- `sentence-transformers` embeddings provide semantic retrieval for regulation clauses

## Install with npx

```bash
npx skills add SolitaryZJ/doc_audit
npx skills add SolitaryZJ/doc_audit --skill enterprise-doc-compliance-audit
npx skills list
```

## Add to Codex manually

Copy `enterprise-doc-compliance-audit` into:

```text
<CODEX_HOME>/skills/enterprise-doc-compliance-audit/
```

On Windows, the default location is usually:

```text
C:\Users\<username>\.codex\skills\enterprise-doc-compliance-audit\
```

Make sure `SKILL.md` is present, then restart Codex or refresh its skills list. After installation, ask:

```text
Use enterprise-doc-compliance-audit to review this DOCX and produce a report and annotated copy.
```

## Local scripts

```bash
python -m pip install python-docx
python -m pip install sentence-transformers numpy
python enterprise-doc-compliance-audit/scripts/build_vector_index.py regulation-pack.json regulations.vec.db
python enterprise-doc-compliance-audit/scripts/retrieve_vector.py regulations.vec.db "personal data retention" --k 5
python enterprise-doc-compliance-audit/scripts/build_index.py regulation-pack.json regulations.db
python enterprise-doc-compliance-audit/scripts/retrieve.py regulations.db "personal data retention" --k 5
python enterprise-doc-compliance-audit/scripts/extract_docx.py input.docx -o extracted.json
python enterprise-doc-compliance-audit/scripts/annotate_docx.py input.docx annotated.docx findings.json
python enterprise-doc-compliance-audit/scripts/validate_report.py report.json
```

See [`regulation-pack-schema.md`](enterprise-doc-compliance-audit/references/regulation-pack-schema.md) for the regulation-pack format.

## RAG review flow

1. Split local regulation packs by clause and embed them at ingest time into a local SQLite vector index.
2. Search only configured official domains; clean pages into clause chunks and retain URL, issuer, effective date, retrieval date, and locator.
3. Add web chunks to the same vector index with `index_web_sources.py`; mark their source as `official_web`.
4. Split DOCX paragraphs and tables; create temporary query embeddings per review unit and do not persist enterprise-document vectors by default.
5. Combine semantic and keyword retrieval, filter by jurisdiction, industry, and effective date, then pass only Top-K clauses to the model context.
6. Cite every conclusion; mark unverifiable sources or locations for human review.

Example web-chunk input:

```json
[{"text":"Clause text","title":"Official rule","url":"https://official.example/rule","issuer":"Authority","jurisdiction":"CN","effective_date":"2025-01-01","retrieved_at":"2026-08-03","locator":"Article 13"}]
```

```bash
python enterprise-doc-compliance-audit/scripts/index_web_sources.py web_chunks.json regulations.vec.db
```

## Safety and scope

This project provides assistive review, not legal advice, and does not guarantee completeness. Users are responsible for maintaining regulation packs. Uncertain evidence, applicability, or text matching must be sent for human review. Do not upload enterprise documents to unconfigured services or expose sensitive excerpts in logs.

The first release focuses on DOCX, regulation-pack-driven review, report generation, and safe highlighting. In-place PDF annotation, a hosted regulation database, and a SaaS backend are outside the current scope.

## License

License to be selected by the project owner before the first public release.
