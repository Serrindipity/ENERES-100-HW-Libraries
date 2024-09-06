from Universal_Numbers import UniversalNumber, convert
from unum.units import *
from decimal import Decimal
import math

# Some stuff I'd like to represent: 160 billion, 7.05e9, 7.05*10^9, 7.5x10^9, 30%, 346,567,000

# print(convert("6.3 billion") * kg)




# Problem Solving
efficiency = convert("0.3")
wood_energy = convert("15 x 10^6 J / kg") # 15000000.0 [J/kg]
global_consumption = convert("196 billion kWh/year") # 196000000000.0 [kWh/y]

wood_per_year = global_consumption / wood_energy
wood_per_year_eff_adjusted = wood_per_year * efficiency
print(efficiency)
print(wood_per_year)
print(wood_per_year_eff_adjusted)


coal_energy = convert("29.3 x 10^6 J/kg")
coal_per_year = global_consumption / coal_energy
coal_per_year_eff_adjusted = coal_per_year * efficiency
print(coal_per_year_eff_adjusted)

natural_gas = convert("0.0373 GJ/m^3") # Source: https://apps.cer-rec.gc.ca/Conversion/conversion-tables.aspx?GoCTemplateCulture=en-CA
gas_per_year = global_consumption / natural_gas
gas_per_year_eff_adjusted = gas_per_year * efficiency
print(gas_per_year_eff_adjusted) # 1.9e+10

solar_energy = convert("5.7 kWh/m^2/day")
print(solar_energy)
efficiency = convert("14%")
actual_output = solar_energy * efficiency
amount = global_consumption / actual_output
print(amount)

efficiency = convert("30%")
Water_energy = convert("10 J / kg / m")
Niagara_energy = Water_energy * convert("57 m") # [J / kg]
print(global_consumption / Niagara_energy * efficiency)

print(f"mton is {mton}")

oil_energy = convert("6.1 x 10^9 J/bbl")
nuclear_energy = convert("270,000 MW*d per mton")
gas_energy = natural_gas / convert("0.68 kg / m^3") # Source : https://www.plinovodi.si/en/transmission-system/environment-and-safety/about-natural-gas/


energies = {
    "gas" : gas_energy,
    "oil" : oil_energy,
    "coal" : coal_energy,
    "wood" : wood_energy,
    "water" : Niagara_energy,
    "nuclear" : nuclear_energy
    }

print(energies)

equalized_energies = energies.copy()
for k, v in equalized_energies.items():
    equalized_energies[k] = v.asUnit(MJ / kg)

print([i._unitTable == coal_energy._unitTable for i in equalized_energies.values()])
sorted_dict = sorted(equalized_energies.items(), key=lambda x : x[1].asNumber(), reverse=True)
print(sorted_dict)

print(gas_energy)
print(gas_energy.asUnit(MJ / kg).round(1))


consumptions_per_capital = {
    "US" : convert("94 quadrillion btu") / convert("334,998,398"),
    "World" : convert("537 quadrillion btu") / convert("7,772,850,805"),
    "Mexico" : convert("7.5 quadrillion btu") / convert("130,207,371"),
    "India" : convert("27 quadrillion btu") / convert("1,339,330,514"),
    "Germany" : convert("12.8 quadrillion btu") / convert("79,903,481"),
    "South Korea" : convert("11.8 quadrillion btu") / convert("51,715,162"),
    "Niger" : convert("0.035 quadrillion btu") / convert("219,463,862")
}

for thing,value in consumptions_per_capital.items():
    print(value)
    consumptions_per_capital[thing] = value.asUnit(MBtu)

print(consumptions_per_capital)
print(consumptions_per_capital["Niger"])

print(consumptions_per_capital["US"] / consumptions_per_capital["Niger"])

print(60200/4900)

def calulate_rog_converted(start, end, time):
    start = convert(start)
    end = convert(end)
    time = convert(time)
    return calculate_rog(start, end, time)

def calculate_rog(s, e, t):
    return Decimal(e/s).ln() / t

def convert_list(l : list[str]):
    return [convert(i) for i in l]
time_period = 9
consumption_vals = {
    "US" : [convert(i) for i in ["92.91", "94.9"]],
    "Brazil" : convert_list(["10.95", "12.42"]),
    "Russia" : convert_list(["27.99", "28.31"]),
    "India" :  convert_list(["22.48", "33.89"]),
    "China" : convert_list(["104.29", "142.03"]),
}
rogs = {
        
    }
for k,v in consumption_vals.items():
    rogs[k] = calulate_rog_converted(v[0], v[1], time_period)
    print(f"{k} rog is {calulate_rog_converted(v[0], v[1], time_period)}")

print(rogs)

# When will India pass the US?
def calculate_projection(b, time_period, r):
    rt = r * time_period
    return b * Decimal(math.e) ** rt

# Sanity check
print(calculate_projection(consumption_vals["US"][0], time_period, calulate_rog_converted(consumption_vals["US"][0], consumption_vals["US"][1], time_period)))

done = False
time = 1
while not done:
    
    us_energy = calculate_projection(consumption_vals["US"][0], time, rogs["US"])
    india_energy = calculate_projection(consumption_vals["India"][0], time, rogs["India"])
    if india_energy > us_energy:
        print(f"time is {time}")
        done = True
        break
    time += 1