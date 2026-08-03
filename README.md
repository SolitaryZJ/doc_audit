# Enterprise Document Compliance Audit

企业文档法规审核 Codex Skill。它根据用户提供的、可版本化的法规包审核企业内部文档，生成可追溯的 Markdown/JSON 报告，并在安全时生成带高亮的 DOCX 副本。

An open-source Codex skill for reviewing enterprise documents against versioned, user-provided regulation packs. It produces traceable Markdown/JSON reports and, when safe, a highlighted DOCX copy.

## Features / 功能

- 插拔式法规包，支持不同国家/地区、行业和文档类型
- 每条发现绑定法规来源、条款定位、原文证据和风险等级
- 支持 `明确违反`、`疑似风险`、`信息不足`、`通过` 四类结论
- 提取 DOCX 段落与表格，保留稳定索引和文本哈希
- 复制原文件后生成可选的 DOCX 高亮标注，不覆盖源文件
- 默认本地优先；联网只应访问用户配置的官方来源

- Pluggable regulation packs for jurisdictions, industries, and document types
- Evidence-backed findings with source locators, excerpts, and risk levels
- Four finding states: `明确违反` (confirmed violation), `疑似风险` (suspected risk), `信息不足` (insufficient information), and `通过` (pass)
- Stable paragraph/table indexes and text hashes for DOCX evidence
- Optional highlighted DOCX copy created without overwriting the source
- Local-first processing with configurable official-source lookup

## Repository layout / 目录

```text
enterprise-doc-compliance-audit/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
    ├── extract_docx.py
    ├── annotate_docx.py
    └── validate_report.py
```

## Quick start / 快速开始

1. 将 `enterprise-doc-compliance-audit` 安装或复制到 Codex skills 目录。
2. 准备法规包，参考 [`regulation-pack-schema.md`](enterprise-doc-compliance-audit/references/regulation-pack-schema.md)。
3. 提供 DOCX、适用地区/行业、法规包和输出要求，例如：

   `请使用 enterprise-doc-compliance-audit 审核 contract.docx，适用地区为 CN，行业为 finance，并生成报告和标注副本。`

1. Install or copy `enterprise-doc-compliance-audit` into your Codex skills directory.
2. Prepare a regulation pack using [`regulation-pack-schema.md`](enterprise-doc-compliance-audit/references/regulation-pack-schema.md).
3. Provide the DOCX, jurisdiction/industry, regulation pack, and requested outputs, for example:

   `Use enterprise-doc-compliance-audit to review contract.docx for CN finance, and produce both the report and an annotated copy.`

## Install with npx / 使用 npx 安装

如果你的 Codex 客户端支持 `skills` CLI，可以直接从 GitHub 安装：

```bash
npx skills add SolitaryZJ/doc_audit
```

仓库包含多个目录时，指定 skill：

```bash
npx skills add SolitaryZJ/doc_audit --skill enterprise-doc-compliance-audit
```

验证安装：

```bash
npx skills list
```

If your Codex-compatible client supports the `skills` CLI, install directly from GitHub:

```bash
npx skills add SolitaryZJ/doc_audit
```

For repositories containing multiple skills, select this skill explicitly:

```bash
npx skills add SolitaryZJ/doc_audit --skill enterprise-doc-compliance-audit
```

Then verify it with:

```bash
npx skills list
```

## Add to Codex manually / 手动加入 Codex

将整个 `enterprise-doc-compliance-audit` 目录复制到 Codex skills 目录：

```text
<CODEX_HOME>/skills/enterprise-doc-compliance-audit/
```

Windows 默认位置通常是：

```text
C:\Users\<用户名>\.codex\skills\enterprise-doc-compliance-audit\
```

也可以使用环境变量指定位置：

```bash
%CODEX_HOME%\skills\enterprise-doc-compliance-audit\
```

确认目录中存在 `SKILL.md`，然后重新打开 Codex 或刷新 skills 列表。安装完成后，可直接说：

```text
使用 enterprise-doc-compliance-audit 审核这个 DOCX，并生成报告和标注副本。
```

Copy the complete `enterprise-doc-compliance-audit` directory into:

```text
<CODEX_HOME>/skills/enterprise-doc-compliance-audit/
```

Make sure `SKILL.md` is present, then restart Codex or refresh its skills list.

### Local script usage / 本地脚本

```bash
python enterprise-doc-compliance-audit/scripts/extract_docx.py input.docx -o extracted.json
python enterprise-doc-compliance-audit/scripts/annotate_docx.py input.docx annotated.docx findings.json
python enterprise-doc-compliance-audit/scripts/validate_report.py report.json
```

The DOCX scripts require Python 3 and `python-docx`:

```bash
python -m pip install python-docx
```

## Safety and scope / 安全与范围

本项目是辅助审核工具，不是法律意见，也不保证穷尽所有适用法规。法规包由使用者负责维护；无法确认依据、适用性或文档定位时，结果应进入人工复核。原始企业文档不得上传到未配置的服务，日志也应避免记录敏感原文。

This project provides assistive review, not legal advice, and does not guarantee completeness. Users are responsible for maintaining regulation packs. Uncertain evidence, applicability, or text matching must be sent for human review. Do not upload enterprise documents to unconfigured services or expose sensitive excerpts in logs.

## Status / 状态

首版重点支持 DOCX、法规包驱动审核、报告生成和安全的高亮标注。PDF 原位标注、长期法规数据库和 SaaS 后端不在当前范围内。

The first release focuses on DOCX, regulation-pack-driven review, report generation, and safe highlighting. In-place PDF annotation, a hosted regulation database, and a SaaS backend are outside the current scope.

## License

License to be selected by the project owner before the first public release.
