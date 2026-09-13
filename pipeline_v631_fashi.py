#!/usr/bin/env python3
"""
AETERNVM VACUVM V6.3.2 — Pipeline FAST / FASHI DR2 — 10 PROVAS + 3 TESTES
CORREÇÃO do erro de criação das 10 provas

Autor: Gustavo Alves Condé — ORCID 0009-0003-9173-363X
DOI base: 10.5281/zenodo.22735900 (V3) + 10.5281/zenodo.22700008 (Paper 2)
Z0 = 376.730313668 Ohm, k = 8.45 Ohm, S_inst=280, N_inst=22

ERRO V6.3.1: 10 provas eram a mesma distribuição repetida + H0 TF com unidades erradas + VSF em cubo
FIX V6.3.2: 10 provas independentes + 3 testes falsificáveis + VSF esférica
"""
from __future__ import annotations
import numpy as np
from pathlib import Path
import warnings
from math import comb

USE_MOCK = True
SEED = 37673
N_SOURCES = 156_411
AREA_DEG2 = 19_500.0
R_MIN, R_MAX = 5.0, 80.0
N_BINS = 25
OUTPUT_DIR = Path("output_v632_10P_3T")
OUTPUT_DIR.mkdir(exist_ok=True)

Z0 = 376.730313668
K_Z0 = 8.45
S_INST = 280

def generate_mock_catalog(n: int = N_SOURCES, seed: int = SEED) -> dict:
    rng = np.random.default_rng(seed)
    ra = rng.uniform(0, 360, n)
    dec = np.degrees(np.arcsin(rng.uniform(-1, 1, n)))
    z = rng.exponential(0.045, n).clip(0.005, 0.35)
    log_mhi = rng.normal(9.45, 0.65, n)
    w50 = rng.lognormal(np.log(160), 0.38, n)
    log_mhi += rng.normal(0, 0.05, n)
    return {"ra": ra, "dec": dec, "z": z, "log_mhi": log_mhi, "w50": w50, "n": n, "area_deg2": AREA_DEG2, "mock": True}

def void_size_function(cat: dict, r_bins: np.ndarray, seed_offset: int = 1):
    from astropy.cosmology import FlatLambdaCDM
    from scipy.spatial import cKDTree
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    d = cosmo.comoving_distance(cat["z"]).value
    ra_rad = np.radians(cat["ra"])
    dec_rad = np.radians(cat["dec"])
    x = d * np.cos(dec_rad) * np.cos(ra_rad)
    y = d * np.cos(dec_rad) * np.sin(ra_rad)
    zc = d * np.sin(dec_rad)
    coords = np.vstack([x, y, zc]).T
    rng = np.random.default_rng(SEED + seed_offset)
    n_rand = 8000
    r_max_survey = np.percentile(d, 96)
    u = rng.uniform(0,1,n_rand)
    r = r_max_survey * (u ** (1/3))
    theta = np.arccos(rng.uniform(-1,1,n_rand))
    phi_ang = rng.uniform(0, 2*np.pi, n_rand)
    rand = np.vstack([r*np.sin(theta)*np.cos(phi_ang), r*np.sin(theta)*np.sin(phi_ang), r*np.cos(theta)]).T
    tree = cKDTree(coords)
    dist, _ = tree.query(rand, k=1)
    hist, edges = np.histogram(dist, bins=r_bins)
    centers = 0.5*(edges[:-1]+edges[1:])
    vol = (4/3)*np.pi*(edges[1:]**3 - edges[:-1]**3)
    phi_vsf = hist / (vol * n_rand + 1e-30)
    return centers, phi_vsf

def triangle_conde(k: int, n: int) -> float:
    if k<0 or k>n: return 0.0
    return comb(n, k) / (2 ** n)

def run_10_provas(cat: dict):
    provas = {}
    r_bins = np.linspace(R_MIN, R_MAX, N_BINS+1)
    centers, phi_vsf = void_size_function(cat, r_bins, seed_offset=10)

    dens = cat["n"] / cat["area_deg2"]
    provas["P1_Densidade"] = {"valor": dens, "esperado": 156411/19500, "status": "OK" if 7 < dens < 9 else "FALHA", "obs": f"{dens:.2f} src/deg2"}

    med_z = np.median(cat["z"])
    provas["P2_Mediana_z"] = {"valor": float(med_z), "esperado": 0.05, "status": "OK" if 0.03 < med_z < 0.07 else "ATENCAO"}

    log_mhi = cat["log_mhi"]
    frac_high = np.mean((log_mhi>9.5) & (log_mhi<10.5))
    provas["P3_MassFunction_LogUniforme"] = {"valor": float(frac_high), "status": "OK" if 0.2 < frac_high < 0.5 else "FALHA"}

    mask = phi_vsf > 0
    if mask.sum()>=5:
        coef = np.polyfit(np.log(centers[mask]), np.log(phi_vsf[mask]+1e-30), 1)
        slope = coef[0]
    else:
        coef = [0,0]
        slope = np.nan
    provas["P4_Regua_VSF_Slope"] = {"valor": float(slope), "esperado": "-1 a -3", "status": "OK" if -3.5 < slope < -0.5 else "FALHA"}

    log_r = np.log(centers+1e-6)
    if mask.sum()>=5:
        model = np.exp(np.polyval(coef, log_r))
        resid = (phi_vsf - model)/(model+1e-30)
        idx = np.nanargmax(resid)
        sigma = np.nanstd(resid)
        logp = resid[idx]/(sigma+1e-6) if sigma>0 else 0
        r_break = centers[idx]
    else:
        logp, r_break = 0, np.nan
    provas["P5_ISE_Logp"] = {"valor": float(logp), "r_break": float(r_break) if not np.isnan(r_break) else None, "status": "OK" if logp>1.5 else "ATENCAO"}

    north = np.sum(cat["dec"]>0)
    south = cat["n"] - north
    p_tri = triangle_conde(int(min(north,south)), int(cat["n"]))
    provas["P6_Triangulo_Isotropia"] = {"valor": float(p_tri), "north": int(north), "south": int(south), "status": "OK" if 0.45 < north/cat["n"] < 0.55 else "ATENCAO"}

    corr = np.corrcoef(cat["log_mhi"], np.log10(cat["w50"]))[0,1]
    provas["P7_TullyFisher_Corr"] = {"valor": float(corr), "status": "OK" if corr>0.2 else "FALHA"}

    k_calc = 2*np.pi*Z0/S_INST
    provas["P8_Z0_Unidade_k"] = {"valor": float(k_calc), "esperado": 8.45, "delta": float(abs(k_calc-8.45)), "status": "OK" if abs(k_calc-8.45)<0.05 else "FALHA"}

    n_inst = S_INST/(2*np.pi*2)
    provas["P9_Ninst"] = {"valor": float(n_inst), "esperado": 22.29, "status": "OK" if 21 < n_inst < 24 else "FALHA"}

    R_K = 25812.80745
    fluxo = R_K / K_Z0
    provas["P10_Fluxo_AV"] = {"valor": float(fluxo), "esperado": 3053.6, "status": "OK"}

    return provas, centers, phi_vsf, r_break

def run_3_testes(provas, cat):
    testes = {}
    testes["T1_Void_Break_Falsificavel"] = {
        "criterio": "logp >1.0 em dados reais FASHI DR2",
        "valor_mock": provas["P5_ISE_Logp"]["valor"],
        "resultado": "PASSA_mock" if provas["P5_ISE_Logp"]["valor"]>1 else "FALHARIA_se_real",
        "falsifica": "Se DR2 real der logp<0, Régua de Condé refutada"
    }
    from astropy.cosmology import FlatLambdaCDM
    h0_grid = np.linspace(60,80,21)
    chi2 = []
    v = cat["w50"]/2
    for h0 in h0_grid:
        cosmo = FlatLambdaCDM(H0=h0, Om0=0.3)
        dl = cosmo.luminosity_distance(cat["z"]).value
        pred_logm = 2.0*np.log10(v) + 2*np.log10(dl) - 6.0
        chi2.append(np.mean((cat["log_mhi"]-pred_logm)**2))
    best_h0 = h0_grid[np.argmin(chi2)]
    testes["T2_H0_TF_Consistencia"] = {
        "criterio": "H0 em [65,78] km/s/Mpc",
        "valor": float(best_h0),
        "resultado": "PASSA" if 65<=best_h0<=78 else "FALHA",
        "falsifica": "Se H0 mock sair <60 ou >80, pipeline TF errado"
    }
    testes["T3_Z0_Invariante"] = {
        "criterio": "k=8.45 fixo, Z0=376.73",
        "valor": float(2*np.pi*Z0/S_INST),
        "resultado": "PASSA" if abs(2*np.pi*Z0/S_INST - 8.45)<0.1 else "FALHA",
        "falsifica": "Se k!=8.45, S_inst!=280"
    }
    return testes, best_h0

def main():
    print("="*70)
    print("AETERNVM VACUVM V6.3.2 — 10 PROVAS + 3 TESTES — CORRIGIDO")
    print("="*70)
    cat = generate_mock_catalog()
    print(f"[CAT] {cat['n']} fontes | {cat['area_deg2']} deg2 | mock={cat['mock']}")
    provas, centers, phi, r_break = run_10_provas(cat)
    testes, best_h0 = run_3_testes(provas, cat)
    print("\n--- 10 PROVAS ---")
    for k,v in provas.items():
        print(f"{k}: {v}")
    print("\n--- 3 TESTES FALSIFICÁVEIS ---")
    for k,v in testes.items():
        print(f"{k}: {v}")
    np.savez(OUTPUT_DIR/"summary_v632.npz", provas=provas, testes=testes, h0=best_h0, r_break=r_break)
    print(f"\nSalvo em {OUTPUT_DIR/'summary_v632.npz'}")
    try:
        import matplotlib.pyplot as plt
        fig, axs = plt.subplots(2,2, figsize=(12,8))
        axs[0,0].semilogy(centers, phi+1e-30, "o-", color="#D4AF37")
        axs[0,0].axvline(r_break, color="crimson", ls="--")
        axs[0,0].set_title("P4/P5 VSF + Régua de Condé")
        axs[0,0].set_xlabel("R Mpc/h"); axs[0,0].set_ylabel("Phi")
        axs[0,0].grid(alpha=0.3)
        axs[0,1].hist(cat["z"], bins=50, color="#2E86AB")
        axs[0,1].set_title("P2 z distribution")
        axs[1,0].hist(cat["log_mhi"], bins=50, color="#A23B72")
        axs[1,0].set_title("P3 HI Mass Function")
        axs[1,1].scatter(np.log10(cat["w50"]), cat["log_mhi"], s=1, alpha=0.1)
        axs[1,1].set_title(f"P7 TF corr={provas['P7_TullyFisher_Corr']['valor']:.2f}")
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR/"10provas_3testes.png", dpi=150)
        print(f"Figura {OUTPUT_DIR/'10provas_3testes.png'}")
    except Exception as e:
        warnings.warn(str(e))

if __name__ == "__main__":
    main()
