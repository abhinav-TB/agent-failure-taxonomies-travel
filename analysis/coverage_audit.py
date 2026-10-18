"""Account for every released row and every normalized AEB native label.
Coverage is not classification accuracy. Zero mapped counts do not establish
absence of a mechanism; source vocabulary coverage is reported separately.
"""
from pathlib import Path
import ast,json
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
def main():
    tree=ast.parse((BASE/'analysis/run_analysis.py').read_text())
    mapping=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NATIVE2UNI' for t in n.targets))
    d=pd.read_csv(BASE/'data/work/coded.csv')
    c=pd.read_csv(BASE/'coding/whowhen_184_coding.csv').fillna('')
    assert len(d)==384 and len(c)==184 and c.row_id.is_unique
    ww=d[d.dataset=='Who&When'];assert ww.unified.tolist()==c.consensus_label.tolist()
    a=d[d.dataset=='AgentErrorBench']
    rows=[]
    for (native,unified),g in a.groupby(['native','unified'],sort=True):
        mod,ft=native.split('.',1)
        if ft=='<empty>':assert unified=='UNMAPPABLE';status='empty native label'
        else:assert (mod,ft) in mapping and mapping[(mod,ft)]==unified;status='explicit crosswalk'
        rows.append(dict(native=native,unified=unified,n=len(g),mapping_status=status))
    pd.DataFrame(rows).to_csv(BASE/'analysis/NATIVE_MAPPING_COVERAGE.csv',index=False)
    covered=[]
    for name,g in d.groupby('dataset',sort=True):
        n=len(g);mapped=int(g.unified.ne('UNMAPPABLE').sum())
        covered.append(dict(dataset=name,total=n,mapped=mapped,unmappable=n-mapped,coverage=mapped/n,accounted_for=n))
    pd.DataFrame(covered).to_csv(BASE/'analysis/MAPPING_COVERAGE.csv',index=False)
    unresolved=c[c.consensus_label=='UNMAPPABLE'][['row_id','mistake_reason','resolution_note']]
    assert len(unresolved)==45
    unresolved.to_csv(BASE/'coding/unresolved_reasons_45.csv',index=False)
    allclasses=['PLAN','TOOL_SELECT','TOOL_FORMAT','TOOL_EXEC','OBS_MISREAD','GROUNDING','NO_RECOVERY','LOOP','GIVE_UP','VERIFICATION','MEMORY','COORDINATION','OTHER']
    vocab=pd.DataFrame([dict(unified=cl,aeb_explicit_native_crosswalk=cl in set(mapping.values()),aeb_observed=int((a.unified==cl).sum()),whowhen_observed=int((ww.unified==cl).sum())) for cl in allclasses])
    vocab.to_csv(BASE/'analysis/CLASS_VOCABULARY_COVERAGE.csv',index=False)
    lines=['# Mapping coverage audit','', '| Dataset | All records | Substantive class | Unmappable | Substantive coverage | Accounted for |','|---|---:|---:|---:|---:|---:|']
    for q in covered:lines.append(f"| {q['dataset']} | {q['total']} | {q['mapped']} | {q['unmappable']} | {q['coverage']:.1%} | 100% |")
    lines+=['','All384 records are accounted for;312/384(81.25%) have a substantive class. All observed nonempty normalized AgentErrorBench labels have explicit crosswalk entries. This is row accounting and mapping completeness for the available labels, not validated mechanism coverage or annotation accuracy.','', 'AgentErrorBench\'s native-to-unified crosswalk can populate7 of13 substantive classes. It supplies no crosswalk into GROUNDING,VERIFICATION,NO_RECOVERY,LOOP,GIVE_UP,or COORDINATION. Their zero counts cannot establish absence of these mechanisms. Who&When is coded from free-text explanations, so its pathway into these classes differs.','', 'The45 unresolved Who&When explanations are listed with evidence and rationale in coding/unresolved_reasons_45.csv. The local snapshot contains attribution reasons, not full interaction trajectories. No new trajectory-based mechanism adjudication is claimed.','', 'OTHER is a positively identified residual category; UNMAPPABLE means insufficient evidence to assign any substantive class. Converting unknowns to OTHER would change this meaning and would not improve evidence coverage.']
    (BASE/'analysis/MAPPING_COVERAGE.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines[:8]))
if __name__=='__main__':main()
