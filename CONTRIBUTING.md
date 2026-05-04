# Contributing to athelper-research/probes

ATHelper's probe library is open-source under MIT. This repo is the canonical
source — probes here ship to the closed-source ATHelper runtime
(`gy15901580825/at_helper_orchestrator`) on a monthly sync.

## Adding a probe

1. Fork this repo.
2. Add your probe YAML under `probes/<category>/`. Categories:
   - `owasp/` — OWASP LLM Top 10 mappings
   - `syscard/` — System-card scenarios (Anthropic / OpenAI)
   - `garak/` — Generally garak-derived (auto-generated)
   - `browser/` — Browser-using agent specific
   - `community/` — Community-contributed, anything that doesn't fit above
3. Reference an existing rubric in `rubrics/`, or add a new one in the same PR.
4. Open a PR. The `lint-probe-yaml` CI checks YAML schema; a maintainer reviews.

## What makes a good probe

- **Reproducible** — same prompt → same finding category across runs
- **Real threat** — maps to ATLAS / OWASP LLM / NIST AI RMF / EU AI Act
- **Not a dead jailbreak** — don't submit "DAN-style" prompts that no modern model
  falls for; those waste judge LLM cost and produce uniform "pass" findings
- **Clear rubric** — a human (or judge LLM) can verdict "fail" / "pass"
  unambiguously. If the rubric is hand-wavy, the probe will produce noisy verdicts.

## Maintainers

- @gy15901580825 (initial)

Add yourself here in your contribution PR if you want to take on review duty.

## License

Contributions are MIT-licensed. By submitting a PR you agree your contribution
is yours to license under MIT.

## How probes ship to ATHelper users

The first day of each month, the ATHelper team runs
`scripts/sync_probes_to_oss.sh` in the *opposite* direction (this OSS repo
into the closed-source `at_helper_orchestrator` for distribution to all
ATHelper users). Your contributions reach all ATHelper customers automatically.

Probes that fail the runtime's lint or break runtime compatibility get reverted
in the sync direction with an issue filed against the original PR.
