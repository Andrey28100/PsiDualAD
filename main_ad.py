from math import factorial, ceil, log2
from fractions import Fraction
from typing import Dict, Union

Number = Union[int, float]

class PsiNumber:
    def __init__(self, const: Number = 0.0, weights: Dict[Fraction, Number] = None):
        self.const = float(const)
        self.weights = {} if weights is None else dict(weights)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return PsiNumber(self.const + other, self.weights)
        res = PsiNumber(self.const + other.const)
        for w, c in self.weights.items():
            res.weights[w] = res.weights.get(w, 0.0) + c
        for w, c in other.weights.items():
            if float(w) <= 1.0:
                res.weights[w] = res.weights.get(w, 0.0) + c
        return res

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_weights = {w: c * other for w, c in self.weights.items() if float(w) <= 1.0}
            return PsiNumber(self.const * other, new_weights)
        res = PsiNumber(self.const * other.const)
        for w, c in other.weights.items():
            if float(w) <= 1.0:
                res.weights[w] = res.weights.get(w, 0.0) + self.const * c
        for w, c in self.weights.items():
            if float(w) <= 1.0:
                res.weights[w] = res.weights.get(w, 0.0) + other.const * c
        for w1, c1 in self.weights.items():
            for w2, c2 in other.weights.items():
                w = w1 + w2
                if float(w) <= 1.0:
                    res.weights[w] = res.weights.get(w, 0.0) + c1 * c2
        return res

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, k: int):
        if k == 0:
            return PsiNumber(1.0)
        if k == 1:
            return PsiNumber(self.const, self.weights)

        result = PsiNumber(1.0)
        base = PsiNumber(self.const, self.weights)
        for _ in range(k):
            result = result * base
        return result

    def __repr__(self):
        terms = [f"{self.const:.4g}"]
        for w in sorted(self.weights):
            c = self.weights[w]
            if abs(c) > 1e-12:
                terms.append(f"{c:.4g}*ξ_{{{float(w):.4g}}}")
        return " + ".join(terms)

def psi_derivative(f, x: float, n: int) -> float:
    if n == 0:
        return f(x)
    m = ceil(log2(n))
    w = Fraction(1, 2**m)
    delta = PsiNumber(0.0, {w: 1.0})

    F = f(x + delta)

    w_target = Fraction(n, 2**m)
    if w_target > 1:
        coeff = 0.0
    else:
        coeff = F.weights.get(w_target, 0.0)
    return factorial(n) * coeff