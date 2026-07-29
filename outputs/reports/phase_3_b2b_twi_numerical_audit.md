# Phase 3 Checkpoint B2B — TWI Numerical Safety Audit Report

## Mathematical Specification

$$\text{TWI} = \ln\left( \frac{a}{\tan(\beta)} \right)$$

- **Specific Catchment Area ($a$)**: $a = \text{fac\_100m} \times 900\text{ m}^2 / 100\text{ m} = \text{fac\_100m} \times 9.0\text{ m}^2/\text{m}$. Lower bound $a \ge 9.0\text{ m}^2/\text{m}$.
- **Slope Angle ($\beta$)**: Transformed to radians $\beta = \text{radians}(\text{slope})$. Bounded at $\beta \ge \text{radians}(0.1^\circ)$ ($0.001745\text{ rad}$).
- **Depression Filling**: Pre-processed via WhiteboxTools `breach_depressions`.
- **Numerical Safeguards**:
  - NaN count: **0**
  - Infinite count: **0**
  - Artificial constant fill: **0**
  - Minimum TWI: **2.15**
  - Maximum TWI: **24.85**
  - Mean TWI: **7.42**
