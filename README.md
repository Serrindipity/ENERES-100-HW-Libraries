## Python Libraries for UC Berkeley's ENE,RES 100 class

Install
```bash
git clone https://github.com/Serrindipity/ENERES-100-HW-Libraries.git
cd eneres_100_hw_libraries
python3 -m venv .venv # Make a virtual environment
source .venv/bin/activate # Activate the venv
pip3 install eneres_100_unum@git+https://github.com/Serrindipity/ENERES-100-Unum.git@main # Install custom unum library
```

Example Usage:
```python
# Assuming this is run from the main project directory (i.e. where the README is)
from src.eneres_100_hw_libraries.convert import convert
from unum.units import *

efficiency = convert("0.3")
wood_energy = convert("15 x 10^6 J / kg") # 15000000.0 [J/kg]
global_consumption = convert("196 billion kWh/year") # 196000000000.0 [kWh/y]

wood_per_year = global_consumption / wood_energy
wood_per_year_eff_adjusted = wood_per_year * efficiency
print(wood_per_year_eff_adjusted.asUnit(ton/year))
```
TODO:
- manage dependencies for upload to PyPi
- pass tests for twine upload
