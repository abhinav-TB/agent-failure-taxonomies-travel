# Mapping coverage audit

| Dataset | All records | Substantive class | Unmappable | Substantive coverage | Accounted for |
|---|---:|---:|---:|---:|---:|
| AgentErrorBench | 200 | 173 | 27 | 86.5% | 100% |
| Who&When | 184 | 139 | 45 | 75.5% | 100% |

All384 records are accounted for;312/384(81.25%) have a substantive class. All observed nonempty normalized AgentErrorBench labels have explicit crosswalk entries. This is row accounting and mapping completeness for the available labels, not validated mechanism coverage or annotation accuracy.

AgentErrorBench's native-to-unified crosswalk can populate7 of13 substantive classes. It supplies no crosswalk into GROUNDING,VERIFICATION,NO_RECOVERY,LOOP,GIVE_UP,or COORDINATION. Their zero counts cannot establish absence of these mechanisms. Who&When is coded from free-text explanations, so its pathway into these classes differs.

The45 unresolved Who&When explanations are listed with evidence and rationale in coding/unresolved_reasons_45.csv. The local snapshot contains attribution reasons, not full interaction trajectories. No new trajectory-based mechanism adjudication is claimed.

OTHER is a positively identified residual category; UNMAPPABLE means insufficient evidence to assign any substantive class. Converting unknowns to OTHER would change this meaning and would not improve evidence coverage.
