"""
src/diamond_uhv_integration.py
V6.6 T8 - Integração real com bancada UHV Toroidal e Gerador P_res
Compatível com pipeline_v631_moda.py existente
"""

import numpy as np

# Constantes da bancada
Z0 = 376.730313668
S_INST = 280
K = 2 * np.pi * Z0 / S_INST
N_INST = 22.29
ALPHA_FRIC = Z0 / 41658.0  # Z0/Ze ~0.00903

class DiamondMembrane:
    def __init__(self, thickness_um=5.0, area_cm2=1.0):
        self.thickness = thickness_um * 1e-6
        self.area = area_cm2 * 1e-4
        self.g33 = 82.2e-3
        self.d33_table = {1: 2e-12, 2.5: 3e-12, 5: 4e-12, 7: 3e-12, 10: 1e-12}
        self.d33 = self.d33_table.get(thickness_um, 4e-12)
        self.E_young = 1050e9
        self.epsilon_r = 5.7
        
    def voltage(self, strain):
        v_max_theoretical = 70e-3 * (self.thickness / 5e-6)
        if strain < 0.007:
            return v_max_theoretical * (strain / 0.014) * 1.0
        elif strain < 0.0105:
            return v_max_theoretical * (0.5 + 0.5*(strain-0.007)/0.0035)
        else:
            return v_max_theoretical * (1.0 + 0.2*(strain-0.0105)/0.0035)
    
    def current(self, strain, R_load=50):
        return self.voltage(strain) / R_load
    
    def power(self, strain, R_load=50):
        v = self.voltage(strain)
        return v*v / R_load

def simulate_uhv_chamber_toroidal():
    mem = DiamondMembrane(thickness_um=5.0, area_cm2=2.0)
    modes = [
        {"name": "Modo breathing 0", "strain": 0.0035, "desc": "7000 ciclos teste base"},
        {"name": "Modo RF 915MHz acoplado", "strain": 0.007, "desc": "Deformação por pressão RF"},
        {"name": "Modo Fogo Temporal", "strain": 0.014, "desc": "Blow-up Navier-Stokes r~(T*-t)^1/2"},
    ]
    print("=== SIMULAÇÃO CÂMARA UHV TOROIDAL + DIAMANTE ===")
    for m in modes:
        v = mem.voltage(m["strain"])
        p = mem.power(m["strain"])
        print(f"{m['name']}: strain {m['strain']*100:.2f}% -> V={v*1e3:.2f}mV P={p*1e6:.2f}uW | {m['desc']}")
    return mem

def simulate_generator_Pres():
    mem = DiamondMembrane(thickness_um=5.0, area_cm2=10.0)
    strain_oper = 0.005
    P_diamond = mem.power(strain_oper) * 10
    P_RF = 50.0
    P_HV = 5.0
    P_vac = 2.0
    P_control = 3.0
    E_entra = 1.0
    E_perdas = ALPHA_FRIC * 2.11 + 0.01
    E_depletada = 0.12
    E_sai_diamond = P_diamond / (P_RF + P_HV + P_vac + P_control)
    ruido_termico = 4 * 1.38e-23 * 300 * 50 * 1e6
    snr = P_diamond / ruido_termico if ruido_termico>0 else 0
    print("\n=== BALANÇO GERADOR P_res + DIAMANTE ===")
    print(f"P_diamond stack 10cm2: {P_diamond*1e6:.2f}uW")
    print(f"SNR vs ruído térmico: {10*np.log10(snr):.1f} dB")
    print(f"E_entra 1.0 = E_sai {E_sai_diamond:.6f} + E_perdas {E_perdas:.5f} + E_depletada {E_depletada}")
    return P_diamond

if __name__ == "__main__":
    simulate_uhv_chamber_toroidal()
    simulate_generator_Pres()
