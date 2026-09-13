#!/usr/bin/env python3
"""
AETERNVM VACUVM V6.3.1 — Pipeline FAST / FASHI DR2

Autor: Gustavo Alves Condé
DOI base: 10.5281/zenodo.22735900 (V3) e 10.5281/zenodo.22700008 (Paper 2)
Uso:
 1. Coloque o arquivo FASHI_DR2.fits (ou.csv) no mesmo diretório, ou
 2. Deixe USE_MOCK = True para gerar catálogo sintético com semente 37673.
Dependências mínimas:
 pip install numpy scipy astropy matplotlib
Etapas:
 1. Carregar (ou gerar) catálogo HI
 2. Régua de Condé (ISE-Void) — Void Size Function
 3. Triângulo de Condé — P(k,n)
 4. Estimativa H0 via Tully-Fisher (mock)
 5. Gerar figuras e resumo numérico
"""
from __future__ import annotations
import numpy as np
from pathlib import Path
import warnings

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
USE_MOCK = True # False → tenta ler FASHI_DR2.fits /.csv
SEED = 37673 # referência a Z0 = 376.73 Ω
N_SOURCES = 156_411
AREA_DEG2 = 19_500.0
R_MIN, R_MAX = 5.0, 80.0 # Mpc/h
N_BINS = 25
OUTPUT_DIR = Path("output_v631")
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Catálogo
# ---------------------------------------------------------------------------
def generate_mock_catalog(n: int = N_SOURCES, seed: int = SEED) -> dict:
    """Gera catálogo sintético com propriedades estatísticas plausíveis."""
    rng = np.random.default_rng(seed)
    ra = rng.uniform(0, 360, n)
    dec = np.degrees(np.arcsin(rng.uniform(-1, 1, n)))
    z = rng.exponential(0.05, n).clip(0.01, 0.25)
    log_mhi = rng.normal(9.4, 0.7, n)
    w50 = rng.lognormal(np.log(150), 0.4, n)
    return {
        "ra": ra, "dec": dec, "z": z,
        "log_mhi": log_mhi, "w50": w50,
        "n": n, "area_deg2": AREA_DEG2, "mock": True
    }

def load_real_catalog(path: str | Path = "FASHI_DR2.fits") -> dict:
    path = Path(path)
    if path.suffix.lower() in {".fits", ".fit"}:
        from astropy.table import Table
        t = Table.read(path)
        return {
            "ra": np.array(t["RA"]),
            "dec": np.array(t["DEC"]),
            "z": np.array(t["z_HI"]),
            "log_mhi": np.log10(np.array(t["M_HI"])),
            "w50": np.array(t["W50"]),
            "n": len(t),
            "area_deg2": AREA_DEG2,
            "mock": False
        }
    elif path.suffix.lower() == ".csv":
        import pandas as pd
        df = pd.read_csv(path)
        return {
            "ra": df["RA"].values,
            "dec": df["DEC"].values,
            "z": df["z_HI"].values,
            "log_mhi": np.log10(df["M_HI"].values),
            "w50": df["W50"].values,
            "n": len(df),
            "area_deg2": AREA_DEG2,
            "mock": False
        }
    raise FileNotFoundError(f"Arquivo não encontrado: {path}")

# ---------------------------------------------------------------------------
# 2. Régua de Condé (ISE-Void simplificada)
# ---------------------------------------------------------------------------
def void_size_function(cat: dict, r_bins: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    from astropy.cosmology import FlatLambdaCDM
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    d = cosmo.comoving_distance(cat["z"]).value
    ra_rad = np.radians(cat["ra"])
    dec_rad = np.radians(cat["dec"])
    x = d * np.cos(dec_rad) * np.cos(ra_rad)
    y = d * np.cos(dec_rad) * np.sin(ra_rad)
    zc = d * np.sin(dec_rad)
    coords = np.vstack([x, y, zc]).T
    n_rand = 5_000
    rng = np.random.default_rng(SEED + 1)
    r_max_survey = np.percentile(d, 95)
    rand = rng.uniform(-r_max_survey, r_max_survey, size=(n_rand, 3))
    from scipy.spatial import cKDTree
    tree = cKDTree(coords)
    dist, _ = tree.query(rand, k=1)
    hist, edges = np.histogram(dist, bins=r_bins)
    centers = 0.5 * (edges[:-1] + edges[1:])
    vol = (4/3)*np.pi*(edges[1:]**3 - edges[:-1]**3)
    phi = hist / (vol * n_rand + 1e-30)
    return centers, phi

def isv_void_logp(centers: np.ndarray, phi: np.ndarray) -> tuple[float, float, float]:
    log_r = np.log(centers + 1e-6)
    mask = phi > 0
    if mask.sum() < 5:
        return 0.0, np.nan, np.nan
    coef = np.polyfit(log_r[mask], np.log(phi[mask] + 1e-30), 1)
    model = np.exp(np.polyval(coef, log_r))
    resid = (phi - model) / (model + 1e-30)
    idx = np.nanargmax(resid)
    sigma = np.nanstd(resid)
    logp = resid[idx] / (sigma + 1e-6) if sigma > 0 else 0.0
    return float(logp), float(centers[idx]), float(resid[idx])

# ---------------------------------------------------------------------------
# 3. Triângulo de Condé
# ---------------------------------------------------------------------------
def triangle_conde(k: int, n: int) -> float:
    from math import comb
    return comb(n, k) / (2 ** n)

# ---------------------------------------------------------------------------
# 4. H0 via Tully-Fisher (mock)
# ---------------------------------------------------------------------------
def estimate_h0_tf(cat: dict) -> tuple[float, float]:
    v = cat["w50"] / 2.0
    from astropy.cosmology import FlatLambdaCDM
    h0_grid = np.linspace(60, 80, 41)
    chi2 = []
    for h0 in h0_grid:
        cosmo = FlatLambdaCDM(H0=h0, Om0=0.3)
        d_l = cosmo.luminosity_distance(cat["z"]).value
        pred = 2.5 * np.log10(v) + 5 * np.log10(d_l)
        obs = cat["log_mhi"] * 2.5
        chi2.append(np.nanmean((obs - pred)**2))
    best = h0_grid[np.argmin(chi2)]
    sigma = 2.5
    return float(best), float(sigma)

# ---------------------------------------------------------------------------
# 5. Execução principal
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("AETERNVM VACUVM V6.3.1 — Pipeline FAST / FASHI DR2")
    print("=" * 60)
    if USE_MOCK:
        print(f"[1] Gerando catálogo mock (semente = {SEED})...")
        cat = generate_mock_catalog()
    else:
        print("[1] Carregando catálogo real...")
        cat = load_real_catalog()
    print(f" Fontes: {cat['n']:,} | Área: {cat['area_deg2']:,.0f} deg² | Mock: {cat['mock']}")

    print("[2] Calculando Void Size Function + Régua de Condé...")
    r_bins = np.linspace(R_MIN, R_MAX, N_BINS + 1)
    centers, phi = void_size_function(cat, r_bins)
    logp, r_break, resid = isv_void_logp(centers, phi)
    print(f" log(p) máximo ≈ {logp:.2f} em R ≈ {r_break:.1f} Mpc/h")

    print("[3] Triângulo de Condé (exemplo k=72, n=100)...")
    p_tri = triangle_conde(72, 100)
    print(f" P(72,100) = {p_tri:.3e}")

    print("[4] Estimativa H0 (Tully-Fisher proxy)...")
    h0, h0_err = estimate_h0_tf(cat)
    print(f" H0 ≈ {h0:.1f} ± {h0_err:.1f} km/s/Mpc (mock)")

    summary = {
        "n_sources": cat["n"],
        "area_deg2": cat["area_deg2"],
        "mock": cat["mock"],
        "logp_ise": logp,
        "r_break_mpc_h": r_break,
        "h0_proxy": h0,
        "h0_err": h0_err,
        "p_triangle_example": p_tri,
    }
    np.savez(OUTPUT_DIR / "summary_v631.npz", **summary)
    print(f"\n[5] Resumo salvo em {OUTPUT_DIR / 'summary_v631.npz'}")

    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.semilogy(centers, phi + 1e-30, "o-", color="#D4AF37", label="VSF proxy")
        ax.axvline(r_break, color="crimson", ls="--", label=f"quebra candidata R={r_break:.1f}")
        ax.set_xlabel("R [Mpc/h]")
        ax.set_ylabel(r"$\Phi(R)$ (proxy)")
        ax.set_title("Void Size Function — mock FASHI / Régua de Condé")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / "vsf_regua.png", dpi=150)
        print(f" Figura salva: {OUTPUT_DIR / 'vsf_regua.png'}")
    except Exception as e:
        warnings.warn(f"Matplotlib não disponível ou erro: {e}")

    print("\nConcluído. Substitua USE_MOCK=False e forneça FASHI_DR2.fits para dados reais.")
    print("Lembrete: resultados de mock NÃO constituem confirmação observacional.")

if __name__ == "__main__":
    main()
