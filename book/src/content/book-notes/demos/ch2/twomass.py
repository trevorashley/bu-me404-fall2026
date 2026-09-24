"""The two-mass flexible system of lecture §11, shared by demos 4, 5 and 6.

        wall                 u
         |                   |
         |                   v
         |--(k1, c1)--[  m1  ]--(k2, c2)--[  m2  ]
                          x1                  x2
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TwoMass:
    m1: float = 1.0
    m2: float = 0.5
    k1: float = 20.0
    k2: float = 8.0
    c1: float = 0.20
    c2: float = 0.02

    # ------------------------------------------------------------- polynomials
    def A11(self):                      # m1 s^2 + (c1+c2) s + (k1+k2)
        return np.array([self.m1, self.c1 + self.c2, self.k1 + self.k2])

    def A22(self):                      # m2 s^2 + c2 s + k2
        return np.array([self.m2, self.c2, self.k2])

    def K2(self):                       # c2 s + k2   (the coupling impedance)
        return np.array([self.c2, self.k2])

    def D(self):
        """Common denominator D(s) = det of the 2x2 matrix in §12."""
        return np.polysub(np.polymul(self.A11(), self.A22()),
                          np.polymul(self.K2(), self.K2()))

    # ------------------------------------------------------ transfer functions
    def G_collocated(self):
        """X1/U -- actuator and sensor both on m1 (§13). num, den."""
        return self.A22(), self.D()

    def G_noncollocated(self):
        """X2/U -- actuator on m1, sensor on m2 (§16). num, den."""
        return self.K2(), self.D()

    # ------------------------------------------------------------- state space
    def rhs(self, t, z, u_of_t):
        """z = [x1, v1, x2, v2]."""
        x1, v1, x2, v2 = z
        u = u_of_t(t, z)
        a1 = (u - self.c1 * v1 - self.k1 * x1
              - self.c2 * (v1 - v2) - self.k2 * (x1 - x2)) / self.m1
        a2 = (-self.c2 * (v2 - v1) - self.k2 * (x2 - x1)) / self.m2
        return [v1, a1, v2, a2]

    def antiresonance(self) -> float:
        return float(np.sqrt(self.k2 / self.m2))
