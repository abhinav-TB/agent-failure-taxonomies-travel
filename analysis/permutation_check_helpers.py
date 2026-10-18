"""Independent small-matrix Pearson statistic used by cluster sensitivity."""
import numpy as np

def pearson(table):
    table=np.asarray(table,dtype=float)
    expected=np.outer(table.sum(axis=1),table.sum(axis=0))/table.sum()
    mask=expected>0
    return float(np.sum((table[mask]-expected[mask])**2/expected[mask]))
