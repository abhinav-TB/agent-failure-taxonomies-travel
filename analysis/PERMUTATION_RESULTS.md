# Monte Carlo permutation robustness checks (100,000 permutations each)

Method: seed=7, Pearson chi-square statistic, labels permuted uniformly with group sizes fixed; p=(exceedances+1)/(100000+1).

## H1 — unified x dataset (n=384)
- asymptotic: chi2=167.29, df=12, p=1.71e-29
- permutation: chi2=167.29, df=12, p_perm=1e-05 (0/100000 permutations >= observed)

## H1 (labeled-only) — unified x dataset (n=312)
- asymptotic: chi2=161.38, df=11, p=6.98e-29
- permutation: chi2=161.38, df=11, p_perm=1e-05 (0/100000 permutations >= observed)

## Domain — unified x domain (n=312)
- asymptotic: chi2=189.81, df=33, p=6.2e-24
- permutation: chi2=189.81, df=33, p_perm=1e-05 (0/100000 permutations >= observed)

## Model — unified x llm, AgentErrorBench labeled (n=173)
- asymptotic: chi2=30.72, df=12, p=0.00217
- permutation: chi2=30.72, df=12, p_perm=0.00196 (195/100000 permutations >= observed)

Conclusion: permutation p-values agree with the asymptotic results — every association remains significant at alpha=0.05. Note the model comparison's permutation p (0.0020) is close to its asymptotic p (0.0022); an earlier version of this script contained a vectorization bug that reported p<1e-5 for all three tests.