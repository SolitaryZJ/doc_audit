# 企业文档法规审核

[English](README.en.md)

企业文档法规审核 Codex Skill。根据用户提供的、可版本化的法规包审核企业内部文档，生成可追溯的 Markdown/JSON 报告，并在安全时生成带高亮的 DOCX 副本。

## 功能

- 插拔式法规包，支持不同国家/地区、行业和文档类型
- 每条发现绑定法规来源、条款定位、原文证据和风险等级
- 支持 `明确违反`、`疑似风险`、`信息不足`、`通过` 四类结论
- 提取 DOCX 段落与表格，保留稳定索引和文本哈希
- 复制原文件后生成可选的 DOCX 高亮标注，不覆盖源文件
- 默认本地优先；联网只应访问用户配置的官方来源
- 使用本地 SQLite FTS5 RAG 按段落召回法规，避免把完整法规库塞入上下文
- 使用 sentence-transformers 生成法规 embedding，并对文档段落执行语义召回

## 使用 npx 安装

```bash
npx skills add SolitaryZJ/doc_audit
npx skills add SolitaryZJ/doc_audit --skill enterprise-doc-compliance-audit
npx skills list
```

## 手动加入 Codex

将 `enterprise-doc-compliance-audit` 复制到：

```text
<CODEX_HOME>/skills/enterprise-doc-compliance-audit/
```

Windows 默认位置通常是：

```text
C:\Users\<用户名>\.codex\skills\enterprise-doc-compliance-audit\
```

确认目录中存在 `SKILL.md`，然后重新打开 Codex 或刷新 skills 列表。安装后可直接说：

```text
使用 enterprise-doc-compliance-audit 审核这个 DOCX，并生成报告和标注副本。
```

## 本地脚本

```bash
python -m pip install python-docx
python -m pip install sentence-transformers numpy
python enterprise-doc-compliance-audit/scripts/build_vector_index.py regulation-pack.json regulations.vec.db
python enterprise-doc-compliance-audit/scripts/retrieve_vector.py regulations.vec.db "个人信息保存期限" --k 5
python enterprise-doc-compliance-audit/scripts/build_index.py regulation-pack.json regulations.db
python enterprise-doc-compliance-audit/scripts/retrieve.py regulations.db "个人信息保存期限" --k 5
python enterprise-doc-compliance-audit/scripts/extract_docx.py input.docx -o extracted.json
python enterprise-doc-compliance-audit/scripts/annotate_docx.py input.docx annotated.docx findings.json
python enterprise-doc-compliance-audit/scripts/validate_report.py report.json
```

法规包格式参见 [`regulation-pack-schema.md`](enterprise-doc-compliance-audit/references/regulation-pack-schema.md)。

## RAG 审核流程

1. 本地法规包按条款切分，在导入时生成 embedding 并写入本地 SQLite 向量索引。
2. 网络检索只访问用户配置的官方域名；页面清洗为条款片段，并保存 URL、发布机构、生效日期、访问日期和条款定位。
3. 网络条款使用 `index_web_sources.py` 写入同一向量索引，来源标记为 `official_web`。
4. DOCX 按段落和表格切分；每个审核单元只临时生成 query embedding，不持久化企业文档向量。
5. 混合召回向量结果和关键词结果，按司法辖区、行业、生效日期过滤，再把 Top-K 条款放入模型上下文。
6. 报告逐条引用法规来源；无法验证来源或定位时标记为人工复核。

网络条款输入示例：

```json
[{"text":"条款正文","title":"官方规定","url":"https://official.example/rule","issuer":"监管机构","jurisdiction":"CN","effective_date":"2025-01-01","retrieved_at":"2026-08-03","locator":"第十三条"}]
```

```bash
python enterprise-doc-compliance-audit/scripts/index_web_sources.py web_chunks.json regulations.vec.db
```

## 安全与范围

本项目是辅助审核工具，不是法律意见，也不保证穷尽所有适用法规。法规包由使用者负责维护；无法确认依据、适用性或文档定位时，结果应进入人工复核。原始企业文档不得上传到未配置的服务，日志也应避免记录敏感原文。

首版重点支持 DOCX、法规包驱动审核、报告生成和安全的高亮标注。PDF 原位标注、长期法规数据库和 SaaS 后端不在当前范围内。

## License

License to be selected by the project owner before the first public release.
