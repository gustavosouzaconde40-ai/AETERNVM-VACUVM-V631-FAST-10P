[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22739495.svg)](https://doi.org/10.5281/zenodo.22739495)
[![DOI Conceito](https://zenodo.org/badge/DOI/10.5281/zenodo.22735900.svg)](https://doi.org/10.5281/zenodo.22735900)

# AETERNVM VACUVM V6.3.7 — FAST + MEERKAT + GW150914 + SPARC — 11 PROVAS + 4 TESTES

DOI Zenodo:
- Conceito: 10.5281/zenodo.22735900
- V6.3.3 BASE: 10.5281/zenodo.22735900 (10 Provas + 3 Testes) v3
- V6.3.6 MEERKAT: 10.5281/zenodo.22739495 (V631.1) v4
- V6.3.7 GW+SPARC: A SER GERADO (V631.2) v5

Autor: Gustavo Alves Condé — ORCID 0009-0003-8264-7907 — Baixo Guandu/ES
Base: Papel 2 Log-Uniforme 10.5281/zenodo.22700008
Cadeia 11 DOIs - Pai: 10.5281/zenodo.21856036

## O que foi corrigido
Saímos de pipeline com 3 funções para 11 provas convergentes independentes + 4 testes falsificáveis.

**11 Provas:** P1 Densidade 8.02 src/deg2, P2 Mediana z, P3 Mass Function, P4 Régua slope, P5 ISE logp=1.84, P6 Triângulo N/S, P7 TF corr, P8 Z0 k=8.45, P9 N_inst=22, P10 Fluxo R_K/k=3053.6, P11 Vibração GW150914 h=1e-21 ΔL=4e-18m

**4 Testes:** T1 logp>1 em DR2 real, T2 H0 65-78, T3 k invariante, T4 γ_trad=4.333 vs γ_AET=3.967 Δγ=-0.367 Γ=0.12 NANOGrav/SKA

## Como rodar
pip install numpy scipy astropy matplotlib
python pipeline_v631_moda.py
python emulacao_meerkat_Pk.py
python emulacao_GW150914_T4.py
python emulacao_SPARC_RAR.py

## CAMADA SPARC - PAPER 2 - 3 TESTES

Antes só no Zenodo 10.5281/zenodo.22735900, agora integrado no GitHub:

Teste I Régua - Não Evolução a_eff(z)=const:
a_local=1.20e-10 m/s², a_eff(REBELS-25 z=7.31)=1.22e-10 razão 1.0167 dif 1.7% média imutável 1.00041294 q95=2.64 => APROVADO

Teste II Triângulo - Centroide 1/ln2:
fb(x)=1/(x ln b) xi_b∈(1,2) 1M amostras centroide teórico 1.442695 empírico 1.443012 razão 1.000219 erro 0.02% dispersão 0.11 dex => APROVADO

Teste III Zbites - RAR SPARC 153 galáxias sem a0 universal:
g_obs = g_bar + sqrt(g_bar * g_vac) g_vac=g†*xi_b/<xi_b> resíduo log10=0.033 dex <0.11 dex boost 4.14x => APROVADO

Equação V6.3: dH/dt = -2ν∫ω·(∇×ω)dV + ∫v·(∇×F_fogo)dV - Γ(m_eff²)H
Γ(m_eff²)=Γ0·δ²/(m_eff⁴+δ²)
E_entra = E_sai + E_perdas + E_depletada
S_inst=280 Z0=376.73Ω≡1 k=8.45Ω=2π*Z0/S_inst N_inst=22 R_K/k=3053.6

Arquivos SPARC: emulacao_SPARC_RAR.py, fig_SPARC_RAR_153.png

## ATUALIZAÇÃO V631.1 - MEERKAT (13/09/2026)

MARCO HISTÓRICO COMPLEMENTAR AO FAST:
Detecção DIRETA do espectro de potência HI pelo MeerKAT em z=0.32 e z=0.44 sem correlação óptica cruzada.
Paper: Paul et al. 2025, ApJL DOI 10.3847/2041-8213/ae808f - 96h 3 a >9 sigma
FAST = HI individual z=1.29 (21cm->48cm) 156.411 fontes - MeerKAT = HI difuso z=0.32/0.44 (21cm->27.7cm/30.2cm)
Fechamento: P7 Teia, P8 Matéria Escura Z_geometrica, P10 Paradigma
Arquivo: SINTESE-MEERKAT-FAST-COMPLEMENTAR-V631.1.md - Figura: fig_meerkat_Pk_comparacao.png

## ATUALIZAÇÃO V631.2 - 11 ANOS GW150914 (14/09/2026)

Evento: m1=36 Msun m2=29 Msun E_rad=3.0 Msun d_L=410 Mpc h=1e-21 Abbott et al. 2016 PRL 116,061102
Balanço: E_GW=5.36e47 J E_depletada Γ=0.12=6.43e46 J
T4: γ_trad=4.333 vs γ_AET=3.967 Δγ=-0.367 falsificável NANOGrav 15yr SKA LISA ET
Limite GW170817 |c_GW-c|/c<1e-15 δZ<7.53e-13Ω OK
Arquivo: SINTESE-GW150914-V631.2.md - Figura: fig_GW150914_T4_fundo.png

## REPOS RAIZ IMUTÁVEIS

- Régua: 10.5281/zenodo.22071438 / 10.5281/zenodo.22096687
- Triângulo: 10.5281/zenodo.22165685 / 10.5281/zenodo.22164502
- Zbites VIEC: 10.5281/zenodo.22166470
- Bancada Z0: 10.5281/zenodo.22649556 - RF 915MHz 8.45→50Ω Guanella UHV Toroidal Rectenna
- Engenharia: 10.5281/zenodo.22672602 - P_res F_res T_res Propulsor A8.0
- 6 Provas histórico: 10.5281/zenodo.22307797
- Paper2 Log-Uniforme + V6.3: 10.5281/zenodo.22700008 e 10.5281/zenodo.22735900
