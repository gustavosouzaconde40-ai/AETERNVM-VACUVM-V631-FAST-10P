"""
AETERNVM VACUVM V631.2 / V6.3.7 - EMULACAO GW150914 T4 - FUNDO ESTOCASTICO
Autor: Gustavo Alves Condé - ORCID 0009-0003-8264-7907
Base: 10.5281/zenodo.22700008 + 10.5281/zenodo.22735900 + 10.5281/zenodo.22740041
Evento: GW150914 - 14/09/2015 - 11 anos - Abbott et al. 2016 PRL 116, 061102
Objetivo: Gerar Teste Falsificavel T4 para NANOGrav / LISA / ET
"""

import numpy as np
import matplotlib.pyplot as plt

# CONSTANTES FRAMEWORK - NAO ALTERAR
Z0 = 376.73 # Ohm
k = 8.45 # Ohm - 2pi*Z0/S_inst S_inst=280 N_inst=22
N_inst = 22
S_inst = 280
R_K = 25812.80745
R_K_k_ratio = R_K / k # ~3053.6

c = 299792458.0
G = 6.67430e-11
M_sun = 1.98847e30

print(f"[AETERNVM VACUVM GW] ORCID 0009-0003-8264-7907 Z0={Z0} k={k} R_K/k={R_K_k_ratio:.1f}")

# DADOS GW150914
m1 = 36 * M_sun
m2 = 29 * M_sun
E_rad = 3.0 * M_sun * c**2
h_observed = 1e-21
Delta_L = h_observed * 4000 # 4e-18 m

print(f"GW150914: E_rad={E_rad:.2e} J ~3 Msun, h={h_observed}, ΔL={Delta_L:.1e} m")

def E_depletada_GW(M1, M2, Gamma=0.12):
    M_total = M1+M2
    M_final = 62 * M_sun
    E_in = M_total * c**2
    E_out_mass = M_final * c**2
    E_GW_trad = E_in - E_out_mass
    E_dep = Gamma * E_GW_trad
    return E_GW_trad, E_dep

E_gw_trad, E_dep = E_depletada_GW(m1, m2, Gamma=0.12)
print(f"E_GW trad {E_gw_trad:.2e} J, E_dep Gamma=0.12 {E_dep:.2e} J")

def gamma_nanoGrav(Gamma):
    Delta_gamma = - (Gamma * R_K_k_ratio) / 1000.0
    gamma_trad = 13/3
    gamma_aet = gamma_trad + Delta_gamma
    return gamma_trad, gamma_aet, Delta_gamma

gamma_t, gamma_a, d_gamma = gamma_nanoGrav(0.12)
print(f"\n=== T4 FALSIFICAVEL ===")
print(f"Tradicional NANOGrav gamma={gamma_t:.3f}")
print(f"AETERNVM gamma={gamma_a:.3f} Delta={d_gamma:.3f}")
print(f"Se NANOGrav+SKA medir gamma=4.33 ±0.1 -> FAIL. Se medir {gamma_a:.2f} -> sustenta Gamma.")

c_gw_limit = 1e-15
delta_Z_allowed = 2 * Z0 * c_gw_limit
print(f"Limite delta_Z GW170817: {delta_Z_allowed:.2e} Ohm")

f = np.logspace(-9, -7, 100)
Omega_trad = 2e-9 * (f/1e-8)**(2/3)
Omega_aet = 2e-9 * (f/1e-8)**(2/3 + d_gamma*0.2)

plt.figure(figsize=(10,6))
plt.loglog(f, Omega_trad, '--', label=f'Tradicional Ω∝f^2/3 γ={gamma_t:.2f}')
plt.loglog(f, Omega_aet, '-', label=f'AETERNVM VACUVM γ={gamma_a:.2f} Δγ={d_gamma:.2f} Γ=0.12 Z0={Z0}Ω')
plt.axvline(1e-8, color='gray', linestyle=':', label='NANOGrav 15yr')
plt.xlabel('Frequência [Hz]'); plt.ylabel('Ω_GW')
plt.title('T4: Fundo Estocástico GW - Previsão Falsificável - ORCID 0009-0003-8264-7907')
plt.legend(); plt.grid(True, alpha=0.3)
plt.savefig('fig_GW150914_T4_fundo.png', dpi=300, bbox_inches='tight')
print("[OK] fig_GW150914_T4_fundo.png")
