import numpy as np
from scipy.stats import poisson

class BettingEngine:
    @staticmethod
    def predict_match(gl, gv):
        # Matriz de probabilidades 10x10
        p_l = poisson.pmf(np.arange(10), gl)
        p_v = poisson.pmf(np.arange(10), gv)
        matrix = np.outer(p_l, p_v)
        
        prob_local = np.sum(np.tril(matrix, -1))
        prob_draw = np.sum(np.diag(matrix))
        prob_visit = np.sum(np.triu(matrix, 1))
        
        # Probabilidad Over 2.5
        over_25 = 0
        for i in range(10):
            for j in range(10):
                if i + j >= 3:
                    over_25 += matrix[i, j]
                    
        return round(prob_local, 3), round(prob_draw, 3), round(prob_visit, 3), round(over_25, 3)