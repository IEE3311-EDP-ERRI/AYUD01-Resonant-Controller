import numpy as np
import control as ct
import matplotlib.pyplot as plt

# --- Cálculo e Impresión de Márgenes de Estabilidad ---
def print_margins(name, loop_gain):
    # gm: margen de ganancia, pm: margen de fase, wg: frec cruce ganancia, wp: frec cruce fase
    gm, pm, wg, wp = ct.margin(loop_gain)
    
    print(f"--- Márgenes para {name} ---")
    # El margen de ganancia puede ser infinito (inf) en sistemas de 2do orden
    gm_db = 20 * np.log10(gm) if gm > 0 else np.inf
    print(f"Margen de Ganancia: {gm_db:.2f} dB")
    print(f"Margen de Fase:     {pm:.2f}°")
    print(f"Frecuencia de cruce de ganancia (Banda de paso): {wp/(2*np.pi):.2f} Hz")
    print("-" * 30)

# --- Parámetros del sistema ---
L = 1e-3
R_esr = 10e-3  # Resistencia serie (L y C)
C = 160e-6
Vpeak = 220 * np.sqrt(2)
Iload = 16
R_load = Vpeak / (Iload * np.sqrt(2))

# --- Diseño de Controladores ---
# Lazo de Corriente (iL)
wn_iL = 2 * np.pi * 0.1
xi_iL = 0.707
Kp_iL = 2 * xi_iL * wn_iL * L - R_esr
Ki_iL = (wn_iL**2) * L

# Lazo de Voltaje (Vdc)
wn_vdc = 2 * np.pi * 20
xi_vdc = 0.707
Kp_vdc = 2 * xi_vdc * wn_vdc * C
Ki_vdc = (wn_vdc**2) * C

# --- Definición de Funciones de Transferencia ---
s = ct.TransferFunction.s

# Controlador PR: Kp + Ki/s
C_iL = Kp_iL + Ki_iL / s
C_vdc = Kp_vdc + Ki_vdc / s

# Plantas
G_iL = 1 / (L * s + R_esr)
G_vdc = (R_esr * C * s + 1) / (C * s)

# Funciones de Lazo Abierto (Loop Gain) L(s) = C(s) * G(s)
L_iL = C_iL * G_iL
L_vdc = C_vdc * G_vdc

# --- Gráficos de Nyquist ---
plt.figure()
ct.nyquist_plot(L_iL)
plt.title(f'Nyquist Lazo Corriente\n$\omega_n = 300$ Hz')
plt.grid(True)
#plt.tight_layout()

plt.figure()
ct.nyquist_plot(L_vdc)
plt.title(f'Nyquist Lazo Voltaje\n$\omega_n = 20$ Hz')
plt.grid(True)
#plt.tight_layout()
plt.show()

print_margins("CONTROLADOR DE CORRIENTE (iL)", L_iL)
print_margins("CONTROLADOR DE VOLTAJE (Vdc)", L_vdc)