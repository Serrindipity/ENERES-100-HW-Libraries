## Python Libraries for UC Berkeley's ENE,RES 100 class
Install
```bash
# These steps are optional. 
python3 -m venv .venv # I recommend making a new virtual environment to put this library in, though.
source .venv/bin/activate # Activate the venv

pip3 install eneres_100_hw_library@git+https://github.com/Serrindipity/ENERES-100-HW-Libraries.git@main # Install this library!
```

If for some reason you use [xonsh](https://xon.sh/) (why would you do that to yourself?), you can take also look at the [build script](/build.xsh).

Example Usage:
```python
from eneres_100_hw_libraries.convert import convert
from unum.units import *

efficiency = convert("0.3")
wood_energy = convert("15 x 10^6 J / kg") # 15000000.0 [J/kg]
global_consumption = convert("196 billion kWh/year") # 196000000000.0 [kWh/y]

wood_per_year = global_consumption / wood_energy
wood_per_year_eff_adjusted = wood_per_year * efficiency
print(wood_per_year_eff_adjusted.asUnit(ton/year))
```

You can also use the `unit()` function to define your own units:
```python
from unim.units import *
mpge = MPGe = unit(
        "mpge", mile / (3.37e1 * kWh), "miles per gallon of gasoline-equivalent"
    )
electricity_cost_per_year = (
        (0.14 * dollar / kWh) / (100 * mpge) * (12000 * mile / year)
    )
```
TODO:
- [ ] manage dependencies for upload to PyPi
- [ ] pass tests for twine upload
