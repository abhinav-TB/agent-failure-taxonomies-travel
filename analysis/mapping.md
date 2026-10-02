# AgentErrorBench native → unified mapping (v1.0, 2026-09-26)

Source: AgentErrorTaxonomy definitions verbatim from
`data/raw/agentdebug/detector/error_definitions.py` (ulab-uiuc/AgentDebug).
Normalization applied before mapping: strip whitespace, lowercase, `plan`→`planning`,
`plan_inefficient`→`inefficient_plan`, `Parameter_error`→`parameter_error`,
trailing-space `tool_execution_error `→`tool_execution_error`.

## Mapping table

| Native (module.failure_type) | Unified | Decision | Rationale |
|---|---|---|---|
| memory.over_simplification | MEMORY | direct | False/partial recall pattern; definition is memory-based |
| memory.memory_retrieval_failure | MEMORY | direct | Canonical forgetting |
| memory.hallucination | MEMORY | direct | False recall of events never observed |
| reflection.hallucination | MEMORY | partial | Module says reflection, but definition ("believes it performed actions that never occurred") is false recall |
| reflection.progress_misjudge | OBS_MISREAD | direct | Correct state, wrong inference about progress |
| reflection.outcome_misinterpretation | OBS_MISREAD | direct | Correct action, wrong reading of its result |
| reflection.causal_misattribution | OBS_MISREAD | direct | Right phenomenon, wrong inferred cause |
| planning.constraint_ignorance | PLAN | direct | Goal/constraint misunderstanding |
| planning.impossible_action | PLAN | direct | Infeasible decomposition |
| planning.inefficient_plan | PLAN | direct | Incoherent/illogical strategy |
| action.misalignment | TOOL_SELECT | direct | Wrong action vs. plan intent |
| action.invalid_action | TOOL_FORMAT | partial | Nonexistent action ≈ rejected call; not a clean schema violation |
| action.format_error | TOOL_FORMAT | direct | Unparseable call |
| action.parameter_error | TOOL_FORMAT | direct | Wrong parameter values |
| system.step_limit | OTHER | direct | Resource exhaustion; no unified class covers it (scheme gap, reported) |
| system.tool_execution_error | TOOL_EXEC | direct | Tool-side failure |
| system.llm_limit | TOOL_EXEC | partial | Provider-side timeout/limit; tool-like character, not a tool call |
| system.environment_error | TOOL_EXEC | direct | Matches unified example "environment crashes mid-episode" |
| others.others | OTHER | direct | Residual |
| (empty failure_type) | UNMAPPABLE | — | 27/200 annotations have empty failure_type AND empty reasoning; not codable without guessing |

## Known source-data issues (reported as findings, not silently fixed)

1. **27/200 (13.5%) annotations have empty `failure_type`** with empty reasoning —
   systematic: 24/57 Llama3.3-70B-Turbo, 3/62 Qwen3-8B, 0/81 GPT-4o.
2. **Inconsistent label strings**: `plan_inefficient` vs `inefficient_plan`;
   `Parameter_error` vs `parameter_error`; `tool_execution_error` vs `tool_execution_error␣`.
3. **Inconsistent module key**: `plan` (webshop) vs `planning` (gaia).
