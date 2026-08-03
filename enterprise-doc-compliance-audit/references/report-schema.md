# Report Schema

Top-level JSON fields: `input`, `review`, `sources`, `summary`, `findings`, `generated_at`.

Each finding must contain `finding_id`, `location`, `excerpt`, `summary`, `status`, `risk`, `confidence`, `citations`, `reason`, `recommendation`, `annotated`, and `human_review`. Status values are `明确违反`, `疑似风险`, `信息不足`, `通过`; risk values are `低`, `中`, `高`, `严重`.
