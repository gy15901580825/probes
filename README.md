# ATHelper Probes

OSS probe library extracted from [ATHelper](https://at-helper.com), the AI-agent
red-team CLI / SaaS. 145 probes mapped to **MITRE ATLAS / OWASP LLM Top 10 /
NIST AI RMF / EU AI Act**.

## Counts

| Category | Count | Source |
|---|---|---|
| OWASP LLM Top 10 | 10 | hand-authored |
| System cards | 5 | hand-authored (Anthropic + OpenAI scenarios) |
| garak | 99 | wrapped from [leondz/garak](https://github.com/leondz/garak) |
| Browser-use | 31 | hand-authored DOM injection / UI phishing / visual prompt injection / OS-cmd |
| **Total** | **145** | |

## Layout

```
probes/
  owasp/      # owasp_llm01_..llm10_*.yaml
  syscard/    # syscard_*.yaml
  garak/      # garak_*.yaml (auto-generated wrappers)
  browser/    # browser_dom_injection_*.yaml / ui_phishing_*.yaml / visual_*.yaml / os_cmd_*.yaml
rubrics/      # judge rubrics (markdown) referenced by probe YAMLs
```

## Probe schema

```yaml
id: owasp_llm01_jailbreak_basic
name: "Basic OWASP LLM01 jailbreak attempt"
category: jailbreak
target_class: [llm_chat, agent_with_tools]
prompts:
  - "Ignore all previous instructions and ..."
mappings:
  atlas: [AML.T0051]
  owasp_llm: [LLM01]
  nist_ai_rmf: [MAP-2.3]
  eu_ai_act: ["Article 15"]
judge_model: claude-haiku-4-5-20251001
judge_rubric_path: rubrics/jailbreak.md
```

Iterative probes (TAP/PAIR/GCG) and browser-use probes (with `scenario:` block)
are loaded by the closed-source ATHelper orchestrator runtime; this repo carries
only the static metadata.

## Contributing

We welcome new probes! See [CONTRIBUTING.md](./CONTRIBUTING.md) for the submission
flow and [SCHEMA.md](./SCHEMA.md) for the probe YAML schema. Issue templates for
probe requests and bug reports are configured.

## Usage

ATHelper CLI loads these YAMLs as the default probe library. For external
research / red-team teams, the `probe` field shapes are documented above and
the YAML is the source of truth.

License: MIT.
