# AETERNVM VACUVM V6.3.3 — FAST FASHI DR2 — 10 PROVAS + 3 TESTES CORRIGIDO

DOI Zenodo: 10.5281/zenodo.22735900 (V3 - será V4 após release V6.3.3)
Autor: Gustavo Alves Condé — ORCID 0009-0003-9173-363X — Baixo Guandu/ES
Base: Papel 2 Log-Uniforme 10.5281/zenodo.22700008

## O que foi corrigido
Saímos de pipeline com 3 funções para 10 provas convergentes independentes + 3 testes falsificáveis.

**10 Provas:** P1 Densidade 8.02 src/deg2, P2 Mediana z, P3 Mass Function, P4 Régua slope, P5 ISE logp, P6 Triângulo N/S, P7 TF corr, P8 Z0 k=8.45, P9 N_inst=22, P10 Fluxo R_K/k=3053.6

**3 Testes:** T1 logp>1 em DR2 real, T2 H0 65-78, T3 k invariante

## Como rodar
pip install numpy scipy astropy matplotlib
python pipeline_v631_moda.py
