"""Independent checks for row provenance, table/statistic consistency and audit scope."""
from pathlib import Path
import hashlib, json, math
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, binomtest

base=Path(__file__).resolve().parents[1]
c=pd.read_csv(base/'coding/whowhen_184_coding.csv')
r=pd.read_csv(base/'data/work/whowhen_reasons.csv')
a=pd.read_csv(base/'coding/recoding_audit_37.csv')
d=pd.read_csv(base/'data/work/coded.csv')
assert c.row_id.tolist()==r.row_id.tolist()==list(range(184))
assert c.mistake_reason.equals(r.mistake_reason)
changed=c[c.consensus_label!=c.original_consensus_label]
assert len(changed)==37 and changed.row_id.tolist()==a.row_id.tolist()
assert (changed.original_consensus_label=='TOOL_FORMAT').all()
assert (changed.consensus_label=='UNMAPPABLE').all()
assert (c.loc[c.previous_revised_label.ne(c.original_consensus_label),'coder2_label']=='UNMAPPABLE').all()
assert c[['coder1_label','coder2_label']].notna().all().all()
assert len(d)==384 and d.cluster_id.notna().all()
w=d[d.dataset=='Who&When']
assert w.unified.tolist()==c.consensus_label.tolist()
assert w.cluster_id.nunique()==139 and (w.cluster_id.value_counts()==2).sum()==45
agree=(c.coder1_label==c.coder2_label).sum()
p1=c.coder1_label.value_counts(normalize=True);p2=c.coder2_label.value_counts(normalize=True)
pe=sum(p1.get(k,0)*p2.get(k,0) for k in set(p1.index)|set(p2.index))
kappa=(agree/184-pe)/(1-pe)
assert agree==128 and math.isclose(kappa,.661776,abs_tol=1e-6)
out={'rows':len(d),'recoded_rows':len(changed),'agreement':int(agree),'kappa':kappa,'checks':{}}
for label,frame,group in [('h1',d,'dataset'),('mapped',d[d.unified!='UNMAPPABLE'],'dataset'),('domain',d[d.unified!='UNMAPPABLE'],'domain')]:
    table=pd.crosstab(frame.unified,frame[group]).to_numpy()
    expected=np.outer(table.sum(1),table.sum(0))/table.sum()
    independent=sum((float(table[i,j])-float(expected[i,j]))**2/float(expected[i,j])
                    for i in range(table.shape[0]) for j in range(table.shape[1]))
    x,p,df,_=chi2_contingency(table)
    assert math.isclose(independent,x,rel_tol=1e-12)
    out['checks'][label]=dict(n=len(frame),chi2=x,p=p,df=df,V=math.sqrt(x/(table.sum()*min(table.shape[0]-1,table.shape[1]-1))))
out['h3_p']=binomtest(27,200,p=.15,alternative='greater').pvalue
out['sha256']={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in [base/'coding/whowhen_184_coding.csv',base/'coding/recoding_audit_37.csv',base/'data/work/whowhen_reasons.csv']}
(base/'analysis/VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
