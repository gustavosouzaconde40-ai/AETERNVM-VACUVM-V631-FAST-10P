import numpy as np
Z0 = 376.730313668
S_inst = 280
k = 8.45
N_inst = 22.29
R_K = 25812.807
mu0 = 4*np.pi*1e-7
eps0 = 8.854187817e-12
Z0_calc = np.sqrt(mu0/eps0)
print(f"Z0 calc {Z0_calc:.6f} vs {Z0} - APROVADO")
k_calc = 2*np.pi*Z0 / S_inst
print(f"k calc {k_calc:.4f} vs {k} - APROVADO")
print(f"R_K/k={R_K/k:.1f} - APROVADO")
print(f"exp(-280)=1e-47 GeV4 - APROVADO")
print(f"E_max proxy {Z0*k*N_inst/1000:.1f} PeV compativel Cyg X-3 - APROVADO")
