# Sensitivity analyses — contested Who&When coding decisions

## Coder-specific distributions (Who&When, n=184)

| class | coder 1 (primary analyst) | coder 2 (independent) | strict primary (analysis) |
|---|---|---|---
| COORDINATION | 13 | 5 | 6 |
| GIVE_UP | 4 | 3 | 3 |
| GROUNDING | 38 | 37 | 36 |
| LOOP | 3 | 5 | 5 |
| MEMORY | 0 | 1 | 1 |
| OBS_MISREAD | 5 | 8 | 7 |
| OTHER | 14 | 9 | 10 |
| PLAN | 23 | 21 | 20 |
| TOOL_EXEC | 16 | 15 | 15 |
| TOOL_FORMAT | 40 | 9 | 0 |
| TOOL_SELECT | 8 | 8 | 8 |
| UNMAPPABLE | 0 | 34 | 45 |
| VERIFICATION | 20 | 29 | 28 |

Inter-annotator agreement: 128/184 = 69.6%, Cohen's kappa = 0.662 (substantial). 34 rows have coder2=UNMAPPABLE against a coder-1 substantive class (27 of those are TOOL_FORMAT-vs-UNMAPPABLE: generic or specific implementation/code-defect explanations).

## Headline tests under each labeling

### primary (strict rule)
- H1 (full): chi2=167.29, df=12, p=1.7e-29, V=0.660
- H1 (labeled-only): n=312, chi2=161.38, df=11, p=7e-29, V=0.719
- Domain: n=312, chi2=189.81, df=33, p=6.2e-24
- Who&When TOOL_FORMAT share: 0/184 (0.0%); top class: UNMAPPABLE (45/184)

### S1 coder2-UNMAPPABLE rows->UNMAPPABLE
- H1 (full): chi2=167.29, df=12, p=1.7e-29, V=0.660
- H1 (labeled-only): n=312, chi2=161.38, df=11, p=7e-29, V=0.719
- Domain: n=312, chi2=189.81, df=33, p=6.2e-24
- Who&When TOOL_FORMAT share: 0/184 (0.0%); top class: UNMAPPABLE (45/184)

### S2 coder-2 labels
- H1 (full): chi2=157.41, df=12, p=1.8e-27, V=0.640
- H1 (labeled-only): n=323, chi2=156.16, df=11, p=8.2e-28, V=0.695
- Domain: n=323, chi2=183.15, df=33, p=1e-22
- Who&When TOOL_FORMAT share: 9/184 (4.9%); top class: GROUNDING (37/184)

### S3 previous broader revised labels
- H1 (full): chi2=160.48, df=12, p=4.2e-28, V=0.646
- H1 (labeled-only): n=322, chi2=158.93, df=11, p=2.2e-28, V=0.703
- Domain: n=322, chi2=185.29, df=33, p=4.1e-23
- Who&When TOOL_FORMAT share: 10/184 (5.4%); top class: GROUNDING (36/184)

### Historical consensus (before correction)
- H1 (full): chi2=192.53, df=12, p=1.1e-34, V=0.708
- H1 (labeled-only): n=349, chi2=182.53, df=11, p=3.1e-33, V=0.723
- Domain: n=349, chi2=210.07, df=33, p=1.2e-27
- Who&When TOOL_FORMAT share: 37/184 (20.1%); top class: TOOL_FORMAT (37/184)
