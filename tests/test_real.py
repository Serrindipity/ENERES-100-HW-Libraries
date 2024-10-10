from ..eneres_100_hw_libraries.convert import convert
from unum.units import *

# Declarations
coal_energy_density = convert("29.8 MJ/kg")
gas_energy_density = convert("50.7 MJ/kg")
coal_mass = convert(
    "144.17 g/mol"
)  # https://pubchem.ncbi.nlm.nih.gov/compound/2-Naphthol
gas_mass = convert("16.043 g/mol")  # https://en.wikipedia.org/wiki/Methane
water_mass = convert(
    "18.015 g/mol"
)  # https://www.webqc.org/molecular-weight-of-H2O%28kgmol%29.html
oxy_mass = convert(32 * g / mol)  # https://www.webqc.org/molecular-weight-of-O2.html
co2_mass = convert(
    44 * g / mol
)  # https://pubchem.ncbi.nlm.nih.gov/compound/Carbon-Dioxide

# Coal Emissions
LHS_coal = coal_mass + 12 * oxy_mass
coal_equation_emission_weight = LHS_coal - 4 * water_mass
coal_emission = (coal_equation_emission_weight / coal_energy_density) / co2_mass
print(f"Coal emissions are {coal_emission.asUnit(kg/GJ)}")  # 3 kg/GJ

# Gas Emissions
LHS_gas = gas_mass + 2 * oxy_mass
gas_equation_emission_weight = LHS_gas - 2 * water_mass
gas_emission = gas_equation_emission_weight / gas_energy_density / co2_mass
print(f"Gas emissions are {gas_emission.asUnit(kg/GJ)}")  # 2 kg/GJ


"""
Note: I have a VScode extension called Runme which lets me run code block snippets from within my markdown document.
If you see a string prepending with a '$', it's calling that variable from a previous code snippet.
"""
coal_efficiency = convert("35%")
gas_efficiency = convert("50%")
actual_coal_energy = coal_efficiency * coal_energy_density
actual_gas_energy = gas_efficiency * gas_energy_density

actual_coal_emission = (coal_equation_emission_weight / actual_coal_energy) / co2_mass
print(f"Adjusted coal emissions are {actual_coal_emission.asUnit(kg/kWh)}")

actual_gas_emission = gas_equation_emission_weight / actual_gas_energy / co2_mass
print(f"Adjusted gas emissions are {gas_emission.asUnit(kg/kWh)}")


consumption = 10715 * kWh
c_emission_US = (
    convert("22%") * consumption * actual_coal_emission * convert("1.1")
)  # The 1.1 is to account for the T&D loss
g_emission_US = convert("38%") * consumption * actual_gas_emission * convert("1.1")
sum_n_emission = c_emission_US + g_emission_US
print(f"Emission calculated from US average is {sum_n_emission.asUnit(ton)}")

g_emission_cal = convert("44%") * consumption * actual_gas_emission * convert("1.1")
print(f"Emission calculated from Berkeley average is {g_emission_cal.asUnit(ton)}")

coal_difference = (1733 - 774) * TW * h
efficiency = convert("40%")
eff_adjusted_coal_density = coal_energy_density * efficiency
coal_mass = coal_difference / eff_adjusted_coal_density
print(f"Coal Mass Difference is {coal_mass.asUnit(kg)}")

coal_density_per_kg = convert("800kg/m^3")
campus_area = 1232 * acre
coal_pile_height = coal_mass / coal_density_per_kg / campus_area
print(f"Coal pile height is {coal_pile_height.asUnit(ft)}")
