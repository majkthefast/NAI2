import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Tworzenie zmiennych lingwistycznych
speed = ctrl.Antecedent(np.arange(0, 101, 1), 'speed')
engine_rpm = ctrl.Antecedent(np.arange(0, 8001, 1), 'engine_rpm')
throttle = ctrl.Antecedent(np.arange(0, 101, 1), 'throttle')
driving_mode = ctrl.Antecedent(np.arange(0, 11, 1), 'driving_mode')
shift = ctrl.Consequent(np.arange(1, 7, 1), 'shift')

# Definiowanie funkcji przynależności
speed['low'] = fuzz.trimf(speed.universe, [0, 0, 50])
speed['medium'] = fuzz.trimf(speed.universe, [0, 50, 100])
speed['high'] = fuzz.trimf(speed.universe, [50, 100, 100])

engine_rpm['low'] = fuzz.trimf(engine_rpm.universe, [0, 0, 2500])
engine_rpm['medium'] = fuzz.trimf(engine_rpm.universe, [1500, 2500, 3500])
engine_rpm['high'] = fuzz.trimf(engine_rpm.universe, [3000, 8000, 8000])

throttle['low'] = fuzz.trimf(throttle.universe, [0, 0, 50])
throttle['medium'] = fuzz.trimf(throttle.universe, [0, 50, 100])
throttle['high'] = fuzz.trimf(throttle.universe, [50, 100, 100])

driving_mode['eco'] = fuzz.trimf(driving_mode.universe, [0, 0, 3])
driving_mode['normal'] = fuzz.trimf(driving_mode.universe, [2, 5, 8])
driving_mode['sport'] = fuzz.trimf(driving_mode.universe, [7, 10, 10])

shift['low'] = fuzz.trimf(shift.universe, [1, 1, 3])
shift['medium'] = fuzz.trimf(shift.universe, [2, 3, 4])
shift['high'] = fuzz.trimf(shift.universe, [3, 6, 6])

# Tworzenie reguł
rule1 = ctrl.Rule(speed['low'] & engine_rpm['low'] & throttle['low'] & driving_mode['eco'], shift['low'])
rule2 = ctrl.Rule(speed['medium'] & engine_rpm['low'] & throttle['medium'] & driving_mode['eco'], shift['medium'])
rule3 = ctrl.Rule(speed['medium'] & engine_rpm['medium'] & throttle['medium'] & driving_mode['eco'], shift['high'])

# Dodatkowe reguły dla trybu "normal" i "sport" mogą być dodane w podobny sposób

# Tworzenie systemu logiki rozmytej
shift_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

# Symulacja
shift_simulation = ctrl.ControlSystemSimulation(shift_ctrl)
shift_simulation.input['speed'] = 30  # Prędkość pojazdu (np. 30 km/h)
shift_simulation.input['engine_rpm'] = 2000  # Obroty silnika (np. 2000 RPM)
shift_simulation.input['throttle'] = 40  # Stopień wciskania gazu (np. 40%)
shift_simulation.input['driving_mode'] = 2  # Tryb jazdy (np. "eco")

# Obliczenia
shift_simulation.compute()

# Wyświetlanie wyniku
print("Suggested Shift:", shift_simulation.output['shift'])
shift.view(sim=shift_simulation)

# Wyświetlenie wykresu funkcji przynależności
speed.view()
engine_rpm.view()
throttle.view()
driving_mode.view()
shift.view()
plt.show()