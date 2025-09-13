## API Reference

Comprehensive documentation for all public Python functions in this repository, with examples and usage notes.

### Module: `Gauss.py`

- **Purpose**: Generate independent Gaussian random variables via a polar/Box–Muller-style transform.

### `gauss(sigma)`

- **Parameters**
  - **sigma** (float): Desired standard deviation. Should be positive.
- **Returns**
  - `list[float]`: Two independent Gaussian samples `[x, y]` with mean 0 and standard deviation approximately `sigma`.
- **Raises**
  - May produce unexpected behavior if `sigma <= 0`.
- **Notes**
  - Relies on NumPy’s RNG; set a seed for reproducibility in examples.
  - The module currently invokes `gauss(-1)` at import time, which you should avoid relying on. Prefer calling `gauss` explicitly from your own code.

Example:

```python
import numpy as np
from Gauss import gauss

np.random.seed(42)
samples = gauss(1.0)
print(samples)  # Example: [0.087, -1.421]
```

Generating many samples and computing empirical statistics:

```python
import numpy as np
from Gauss import gauss

np.random.seed(0)
sigma = 2.5
num_pairs = 10000
xs, ys = [], []
for _ in range(num_pairs):
    x, y = gauss(sigma)
    xs.append(x)
    ys.append(y)

print(np.mean(xs), np.std(xs))  # mean ~ 0, std ~ sigma
print(np.mean(ys), np.std(ys))
```

---

### Module: `Monte_Carlo.py`

- **Purpose**: Monte Carlo routines related to estimating integrals and their dispersion. The file contains top-level code that executes on import (computing and printing values). Treat the functions below as the public API.

### `f_x(x)`

- **Parameters**
  - **x** (float): Real input.
- **Returns**
  - `float`: Value of the integrand \( f(x) = \frac{1}{x^2 + \cos^2(x)} \).

Example:

```python
from Monte_Carlo import f_x

val0 = f_x(0.0)
val1 = f_x(1.0)
print(val0, val1)
```

### `crude_MC(n)`

- **Parameters**
  - **n** (int): Number of Monte Carlo samples.
- **Returns**
  - `float`: A crude Monte Carlo estimate. In the current implementation, this computes `(pi - 0) * mean(U[0,1])`, which tends to `pi/2` as `n` grows. It does not evaluate `f_x`; consider this a placeholder for a proper integrand-based estimator.
- **Notes**
  - For a traditional crude MC integral estimator of \(\int_a^b f(x) \, dx\), you would typically draw `x ~ U[a, b]` and return `(b - a) * mean(f(x))`. Adjust the implementation accordingly if you intend to integrate `f_x`.

Example:

```python
import numpy as np
from Monte_Carlo import crude_MC

np.random.seed(0)
estimate = crude_MC(100_000)
print(estimate)  # ~ 1.5708 (pi/2)
```

### `crude_MC_variance(n)`

- **Parameters**
  - **n** (int): Number of Monte Carlo samples.
- **Returns**
  - `float`: An estimate related to the variance of the crude estimator per the current implementation.
- **Notes**
  - The present implementation maintains accumulators across two loops and combines them. If you adapt `crude_MC` to use an actual integrand `f(x)`, update this function similarly to compute the variance of `f(x)` under the proposal distribution.

Example:

```python
import numpy as np
from Monte_Carlo import crude_MC_variance

np.random.seed(1)
var_est = crude_MC_variance(100_000)
print(var_est)
```

### `mc_error(n)`

- **Parameters**
  - **n** (int): Number of Monte Carlo samples.
- **Returns**
  - `float`: Estimated standard error \(\approx \sqrt{\text{variance} / n}\) based on the variable `z` computed at module scope.
- **Important**
  - This function references a module-level variable `z` defined by a prior call to `crude_MC_variance(n)` at import time. If you import the module but do not execute the top-level code, you should compute or pass the variance explicitly in your own workflow.

Example (recomputing variance, recommended):

```python
import numpy as np
from Monte_Carlo import crude_MC_variance, mc_error

np.random.seed(123)
n = 50_000
# Recreate the module-level behavior to ensure z exists
z = crude_MC_variance(n)  # variance-like quantity
err = np.sqrt(z / n)      # equivalent to mc_error(n) given z
print(err)
```

Example (using the module as-is after import):

```python
# Not recommended for library use due to top-level execution,
# but shown here to match the current module behavior.
import Monte_Carlo  # triggers computation of y, z, e at import

from Monte_Carlo import mc_error
err = mc_error(Monte_Carlo.n)
print(err)
```

---

### Best practices for using these modules

- **Set RNG seeds for reproducibility**: Use `np.random.seed(seed_value)` before stochastic routines if you want repeatable results.
- **Avoid top-level side effects**: If you plan to reuse these functions as a library, consider wrapping script-style code in `if __name__ == "__main__":` blocks in your own scripts, rather than relying on module import-time execution.
- **Parameter validation**: Ensure inputs such as `sigma` and `n` are valid (e.g., `sigma > 0`, `n` large enough for stable estimates).

