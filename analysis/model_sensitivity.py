"""Post-hoc model-by-domain adjustment, with fixed within-domain model counts."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from permutation_check_helpers import pearson

base=Path(__file__).resolve().parents[1]
data=pd.read_csv(base/'data/work/coded.csv')
d=data[(data.dataset=='AgentErrorBench') & (data.unified!='UNMAPPABLE')].copy().reset_index(drop=True)
_,gc=np.unique(d.llm,return_inverse=True)
_,lc=np.unique(d.unified,return_inverse=True)
R,C=len(np.unique(gc)),len(np.unique(lc))
def stat(g): return pearson(np.bincount(g*C+lc,minlength=R*C).reshape(R,C))
observed=stat(gc)
strata=[np.flatnonzero(d.domain.values==v) for v in sorted(d.domain.unique())]
rng=np.random.default_rng(7);ge=0
for _ in range(20_000):
    g=gc.copy()
    for idx in strata:g[idx]=rng.permutation(gc[idx])
    ge+=stat(g)>=observed-1e-10
alf=d[d.domain=='alfworld']
ct=pd.crosstab(alf.unified,alf.llm)
x,p,df,e=chi2_contingency(ct)
result=dict(seed=7,permutations=20_000,observed=observed,exceedances=int(ge),
            within_domain_permutation_p=(ge+1)/20_001,
            alfworld=dict(n=len(alf),chi2=x,p=p,df=df,V=float(np.sqrt(x/len(alf)))))
(base/'analysis/MODEL_SENSITIVITY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
