## Probe contribution checklist

- [ ] Probe YAML lints (CI will check; run `python .github/scripts/lint_probes.py` locally to verify)
- [ ] All required fields present per [SCHEMA.md](../SCHEMA.md): `id`, `name`, `category`, `target_class`, `prompts`, `mappings`, `judge_model`, `judge_rubric_path`
- [ ] `id` is globally unique (`grep -r "id: <your_id>" probes/` returns only your file)
- [ ] All 4 mapping arrays populated (`atlas`, `owasp_llm`, `nist_ai_rmf`, `eu_ai_act`); empty list `[]` is OK if N/A but the field must exist
- [ ] `judge_rubric_path` resolves to an existing `rubrics/<file>.md` (or new file added in this PR)
- [ ] Manually tested against ≥1 real agent — describe the test in the PR body
- [ ] License: contribution under MIT (PR submission == agreement)

## Description

<!-- What does this probe cover? Why is it interesting? -->

## Test results

<!-- Paste output of running this probe against a real agent. Include the
target type, your verdict expectation, and the actual ATHelper verdict. -->
