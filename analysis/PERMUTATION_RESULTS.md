# Monte Carlo permutation robustness checks (100,000 permutations each)

Method: seed=7, Pearson chi-square statistic, labels permuted uniformly with group sizes fixed; p=(exceedances+1)/(100000+1).

## H1 — unified x dataset (n=384)
- asymptotic: chi2=160.48, df=12, p=4.2e-28
- permutation: chi2=160.48, df=12, p_perm=1e-05 (0/100000 permutations >= observed)

## H1 (labeled-only) — unified x dataset (n=322)
- asymptotic: chi2=158.93, df=11, p=2.22e-28
- permutation: chi2=158.93, df=11, p_perm=1e-05 (0/100000 permutations >= observed)

## Domain — unified x domain (n=322)
- asymptotic: chi2=185.29, df=33, p=4.11e-23
- permutation: chi2=185.29, df=33, p_perm=1e-05 (0/100000 permutations >= observed)

## Model — unified x llm, AgentErrorBench labeled (n=173)
- asymptotic: chi2=30.72, df=12, p=0.00217
- permutation: chi2=30.72, df=12, p_perm=0.00196 (195/100000 permutations >= observed)

Conclusion: permutation p-values agree with the asymptotic results — every association remains significant at alpha=0.05. Note the model comparison's permutation p (0.0020) is close to its asymptotic p (0.0022); an earlier version of this script contained a vectorization bug that reported p<1e-5 for all three tests.