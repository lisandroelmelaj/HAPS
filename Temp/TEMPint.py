import numpy as np
import matplotlib.pyplot as plt
import json

# --- CONFIGURACIÓN DEL SISTEMA (HARDWARE) ---
power_gen = 0.1  # Watts generados (Jetson Nano + Sensores + GPS)
thickness = 0.04  # 40mm de grosor de XPS
area_total = 0.25 # m^2 (Ej: Caja de 25x25x25 cm aprox)
masa_interna = 1.2 # kg (Electrónica + estructura interna)
cp_interno = 900   # J/kg*K (Promedio aluminio/plástico/silicio)

# --- PROPIEDADES DE MATERIALES ---
k_xps = 0.03     # Conductivity XPS (W/m*K)
mylar_emissivity = 0.03 # El Mylar refleja el 95% de la radiación IR
sigma = 5.67e-8   # Constante de Stefan-Boltzmann

# --- DATOS DEL VAIZALA RS41 (Simulado a partir de tus JSON) ---
# Extraigo los puntos clave de tu log: tiempo (segundos), altitud, temp_ext
data_log = [
  
    {"t": 50, "alt": 1810, "temp_ext": 11.7},
    {"t": 100, "alt": 2046, "temp_ext": 10.8},
    {"t": 150, "alt": 2281, "temp_ext": 10.3},
    {"t": 200, "alt": 2492, "temp_ext": 9.8},
    {"t": 250, "alt": 2746, "temp_ext": 9.1},
    {"t": 300, "alt": 3003, "temp_ext": 8.6},
    {"t": 350, "alt": 3253, "temp_ext": 8.0},
    {"t": 400, "alt": 3510, "temp_ext": 7.2},
    {"t": 450, "alt": 3754, "temp_ext": 6.3},
    {"t": 500, "alt": 4007, "temp_ext": 5.6},
    {"t": 550, "alt": 4287, "temp_ext": 4.9},
    {"t": 600, "alt": 4568, "temp_ext": 4.2},
    {"t": 650, "alt": 4814, "temp_ext": 3.6},
    {"t": 700, "alt": 5063, "temp_ext": 2.8},
    {"t": 750, "alt": 5320, "temp_ext": 2.3},
    {"t": 800, "alt": 5578, "temp_ext": 1.8},
    {"t": 850, "alt": 5815, "temp_ext": 0.8},
    {"t": 900, "alt": 6058, "temp_ext": 0.2},
    {"t": 950, "alt": 6299, "temp_ext": -0.6},
    {"t": 1000, "alt": 6544, "temp_ext": -1.1},
    {"t": 1050, "alt": 6797, "temp_ext": -1.7},
    {"t": 1100, "alt": 7060, "temp_ext": -2.3},
    {"t": 1150, "alt": 7327, "temp_ext": -2.8},
    {"t": 1200, "alt": 7588, "temp_ext": -3.4},
    {"t": 1250, "alt": 7851, "temp_ext": -4.0},
    {"t": 1300, "alt": 8130, "temp_ext": -4.6},
    {"t": 1350, "alt": 8391, "temp_ext": -5.1},
    {"t": 1400, "alt": 8663, "temp_ext": -5.6},
    {"t": 1450, "alt": 8937, "temp_ext": -6.1},
    {"t": 1500, "alt": 9193, "temp_ext": -6.8},
    {"t": 1550, "alt": 9458, "temp_ext": -7.4},
    {"t": 1600, "alt": 9718, "temp_ext": -7.8},
    {"t": 1650, "alt": 9970, "temp_ext": -8.4},
    {"t": 1700, "alt": 10223, "temp_ext": -9.0},
    {"t": 1750, "alt": 10497, "temp_ext": -9.6},
    {"t": 1800, "alt": 10750, "temp_ext": -10.1},
    {"t": 1850, "alt": 11017, "temp_ext": -10.8},
    {"t": 1900, "alt": 11283, "temp_ext": -11.4},
    {"t": 1950, "alt": 11559, "temp_ext": -11.8},
    {"t": 2000, "alt": 11825, "temp_ext": -12.4},
    {"t": 2050, "alt": 12073, "temp_ext": -13.0},
    {"t": 2100, "alt": 12320, "temp_ext": -13.6},
    {"t": 2150, "alt": 12582, "temp_ext": -14.1},
    {"t": 2200, "alt": 12858, "temp_ext": -14.8},
    {"t": 2250, "alt": 13120, "temp_ext": -15.2},
    {"t": 2300, "alt": 13384, "temp_ext": -15.9},
    {"t": 2350, "alt": 13640, "temp_ext": -16.4},
    {"t": 2400, "alt": 13892, "temp_ext": -16.9},
    {"t": 2450, "alt": 14147, "temp_ext": -17.6},
    {"t": 2500, "alt": 14385, "temp_ext": -18.1},
    {"t": 2550, "alt": 14634, "temp_ext": -18.8},
    {"t": 2600, "alt": 14871, "temp_ext": -19.4},
    {"t": 2650, "alt": 15117, "temp_ext": -20.0},
    {"t": 2700, "alt": 15354, "temp_ext": -20.6},
    {"t": 2750, "alt": 15616, "temp_ext": -21.2},
    {"t": 2800, "alt": 15882, "temp_ext": -21.7},
    {"t": 2850, "alt": 16153, "temp_ext": -22.2},
    {"t": 2900, "alt": 16414, "temp_ext": -22.7},
    {"t": 2950, "alt": 16675, "temp_ext": -23.3},
    {"t": 3000, "alt": 16921, "temp_ext": -23.8},
    {"t": 3050, "alt": 17179, "temp_ext": -24.4},
    {"t": 3100, "alt": 17438, "temp_ext": -24.8},
    {"t": 3150, "alt": 17680, "temp_ext": -25.5},
    {"t": 3200, "alt": 17919, "temp_ext": -26.0},
    {"t": 3250, "alt": 18164, "temp_ext": -26.7},
    {"t": 3300, "alt": 18433, "temp_ext": -27.1},
    {"t": 3350, "alt": 18705, "temp_ext": -27.6},
    {"t": 3400, "alt": 18956, "temp_ext": -28.2},
    {"t": 3450, "alt": 19207, "temp_ext": -28.9},
    {"t": 3500, "alt": 19461, "temp_ext": -29.5},
    {"t": 3550, "alt": 19706, "temp_ext": -30.0},
    {"t": 3600, "alt": 19956, "temp_ext": -30.6},
    {"t": 3650, "alt": 20212, "temp_ext": -31.1},
    {"t": 3700, "alt": 20475, "temp_ext": -31.5},
    {"t": 3750, "alt": 20731, "temp_ext": -32.0},
    {"t": 3800, "alt": 20995, "temp_ext": -32.6},
    {"t": 3850, "alt": 21257, "temp_ext": -33.0},
    {"t": 3900, "alt": 21507, "temp_ext": -33.4},
    {"t": 3950, "alt": 21757, "temp_ext": -33.8},
    {"t": 4000, "alt": 22026, "temp_ext": -34.4},
    {"t": 4050, "alt": 22290, "temp_ext": -34.9},
    {"t": 4100, "alt": 22545, "temp_ext": -35.5},
    {"t": 4150, "alt": 22800, "temp_ext": -35.9},
    {"t": 4200, "alt": 23067, "temp_ext": -36.2},
    {"t": 4250, "alt": 23337, "temp_ext": -36.5},
    {"t": 4300, "alt": 23605, "temp_ext": -36.8},
    {"t": 4350, "alt": 23874, "temp_ext": -37.1},
    {"t": 4400, "alt": 24153, "temp_ext": -37.6},
    {"t": 4450, "alt": 24417, "temp_ext": -38.2},
    {"t": 4500, "alt": 24679, "temp_ext": -38.5},
    {"t": 4550, "alt": 24940, "temp_ext": -39.0},
    {"t": 4600, "alt": 25203, "temp_ext": -39.7},
    {"t": 4650, "alt": 25469, "temp_ext": -40.1},
    {"t": 4700, "alt": 25733, "temp_ext": -40.5},
    {"t": 4750, "alt": 26001, "temp_ext": -41.2},
    {"t": 4800, "alt": 26264, "temp_ext": -42.0},
    {"t": 4850, "alt": 26530, "temp_ext": -42.8},
    {"t": 4900, "alt": 26780, "temp_ext": -43.2},
    {"t": 4950, "alt": 27019, "temp_ext": -43.7},
    {"t": 5000, "alt": 27270, "temp_ext": -44.1},
    {"t": 5050, "alt": 27521, "temp_ext": -44.8},
    {"t": 5100, "alt": 27768, "temp_ext": -45.6},
    {"t": 5150, "alt": 27985, "temp_ext": -46.1},
    {"t": 5200, "alt": 28200, "temp_ext": -46.8},
    {"t": 5250, "alt": 28411, "temp_ext": -47.4},
    {"t": 5300, "alt": 28627, "temp_ext": -48.0},
    {"t": 5350, "alt": 28842, "temp_ext": -48.7},
    {"t": 5400, "alt": 29051, "temp_ext": -49.4},
    {"t": 5450, "alt": 29258, "temp_ext": -50.0},
    {"t": 5500, "alt": 29466, "temp_ext": -50.6},
    {"t": 5550, "alt": 29672, "temp_ext": -51.1},
    {"t": 5600, "alt": 29886, "temp_ext": -51.8},
    {"t": 5650, "alt": 30101, "temp_ext": -52.3},
    {"t": 5700, "alt": 30314, "temp_ext": -52.8},
    {"t": 5750, "alt": 30527, "temp_ext": -53.4},
    {"t": 5800, "alt": 30751, "temp_ext": -53.8},
    {"t": 5850, "alt": 30964, "temp_ext": -54.4},
    {"t": 5900, "alt": 31193, "temp_ext": -55.1},
    {"t": 5950, "alt": 27245, "temp_ext": -51.1},
    {"t": 6000, "alt": 27499, "temp_ext": -50.3},
    {"t": 6050, "alt": 27759, "temp_ext": -49.7},
    {"t": 6100, "alt": 28005, "temp_ext": -48.9},
    {"t": 6150, "alt": 30964, "temp_ext": -54.4},
    {"t": 6200, "alt": 31193, "temp_ext": -55.1},
    {"t": 6250, "alt": 27245, "temp_ext": -51.1},
    {"t": 6300, "alt": 27499, "temp_ext": -50.3},
    {"t": 6350, "alt": 27759, "temp_ext": -49.7},
    {"t": 6400, "alt": 28005, "temp_ext": -48.9},
]

# --- MOTOR DE SIMULACIÓN ---
def simulate_thermal():
    t_int = 20.0  # Temperatura inicial dentro de la caja (°C)
    results_t = []
    results_temp = []
    
    # Iteramos sobre los intervalos de tiempo del log
    for i in range(len(data_log) - 1):
        d_t = data_log[i+1]["t"] - data_log[i]["t"]
        t_ext = data_log[i]["temp_ext"]
        
        # 1. Pérdida por Conducción (XPS)
        # Q = k * A * (T1 - T2) / L
        q_cond = (k_xps * area_total * (t_int - t_ext)) / thickness
        
        # 2. Pérdida por Radiación (Mylar)
        # Consideramos la emisividad baja del Mylar
        t_int_k = t_int + 273.15
        t_ext_k = t_ext + 273.15
        q_rad = sigma * mylar_emissivity * area_total * (t_int_k**4 - t_ext_k**4)
        
        # 3. Balance de Energía
        # El cambio de energía interna es lo generado menos lo perdido
        delta_q = (power_gen - q_cond - q_rad) * d_t
        
        # 4. Cambio de Temperatura
        # dT = dQ / (m * Cp)
        delta_temp = delta_q / (masa_interna * cp_interno)
        t_int += delta_temp
        
        results_t.append(data_log[i]["t"])
        results_temp.append(t_int)
        
    return results_t, results_temp

# Ejecución y Gráfico
tiempos, temps_internas = simulate_thermal()

plt.figure(figsize=(10, 5))
plt.plot(tiempos, temps_internas, label='Temp Interna (Simulada)', color='red', linewidth=2)
plt.axhline(y=0, color='blue', linestyle='--', alpha=0.5, label='Congelamiento')
plt.title('Evolución Térmica del Payload - Fase Estratosférica Mendoza')
plt.xlabel('Tiempo desde inicio log (segundos)')
plt.ylabel('Temperatura Interna (°C)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
