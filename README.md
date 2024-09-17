Python Libraries for UC Berkeley's ENE,RES 100 class

Make a new pyvenv.cfg file in .math-venv

```
home = /path/to/your/python@3.12/bin
include-system-site-packages = false
version = 3.12.3
executable = /path/to/your/python@3.12/3.12.3/Frameworks/Python.framework/Versions/3.12/bin/python3.12
command = /path/to/your/python@3.12/bin/python3.12 -m venv /path/to/this/directory/.math-venv
```

Alternatively, (and probably a better way) is to make a new venv and copy the unit and init files from this repo to that venv. I'll get around to writing a build script for it eventually.

TODO:
- [] fork actual Unum repo to allow building from requirements.txt


Example Usage:
```python
from UniversalNumbers import UniversalNumber, convert
from unum.units import *

efficiency = convert("0.3")
wood_energy = convert("15 x 10^6 J / kg") # 15000000.0 [J/kg]
global_consumption = convert("196 billion kWh/year") # 196000000000.0 [kWh/y]

wood_per_year = global_consumption / wood_energy
wood_per_year_eff_adjusted = wood_per_year * efficiency
print(wood_per_year_eff_adjusted.asUnit(ton/year))
```
