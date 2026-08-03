# Regulation Pack Schema

Use YAML or JSON with this shape:

```yaml
pack_id: cn-finance-2026
version: 1.0.0
rules:
  - rule_id: R-001
    scope: {jurisdiction: CN, industries: [finance], document_types: [privacy_notice]}
    check: Require a lawful basis and retention period for personal-data processing.
    citations:
      - title: Example official regulation
        issuer: Example authority
        jurisdiction: CN
        effective_date: 2025-01-01
        source_url: https://official.example/rule
        locator: Article 4
        retrieved_at: 2026-08-03
    default_risk: high
    allow_official_lookup: true
```

Reject a pack when `pack_id`, `version`, `rules`, `rule_id`, `scope`, `check`, or complete citation fields are missing. Do not treat examples as legal sources.
