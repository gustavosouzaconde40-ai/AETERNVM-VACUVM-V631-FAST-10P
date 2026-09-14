---
title: 'AETERNVM VACUVM V6.3.3: FAST FASHI DR2 10 Proofs + 3 Tests Corrigido - Intensity Mapping Validation with MeerKAT'
tags:
    - cosmology
    - radio astronomy
    - neutral hydrogen
    - 21cm line
    - intensity mapping
    - active vacuum
    - FAST
    - MeerKAT
authors:
    - name: Gustavo Alves Conde
    orcid: 0009-0003-9173-363X
    affiliation: 1
affiliations:
    - name: Independent Researcher, Baixo Guandu/ES, Brazil
    index: 1
date: 13 September 2026
bibliography: paper.bib
---

# Summary

The `AETERNVM VACUVM V6.3.3` pipeline provides 10 convergent independent tests + 3 falsifiable tests for the FAST FASHI DR2 neutral hydrogen (HI) catalog (156,411 sources). This release V631.1 incorporates the complementary direct detection of the HI power spectrum by MeerKAT at z=0.32 and z=0.44 [@paul2025] (DOI: 10.3847/2041-8213/ae808f, 96h archival data, 3-9 sigma) without optical cross-correlation.

While FAST proves individual distant HI (z=1.29, 21cm -> 48cm), MeerKAT proves diffuse statistical HI (z=0.32/0.44, 21cm -> 27.7cm/30.2cm) via Hydrogen Intensity Mapping. Together they validate the Active Vacuum model in two regimes.

The pipeline evolves from 3 functions to 10 independent convergent tests: P1 Density 8.02 src/deg2, P2 Median z, P3 Mass Function, P4 Declivity Ruler, P5 ISE logp, P6 N/S Triangle, P7 TF corr, P8 Z0 k=8.45, P9 N_inst=22, P10 Flux R_K/k=3053.6, plus T1 logp>1 in real DR2, T2 H0 65-78, T3 k invariant.

# Statement of Need

Current HI cosmology relies on either individual galaxy detection (FAST) or cross-correlated Intensity Mapping. The direct auto-power spectrum detection by MeerKAT demonstrates that diffuse HI mapping is feasible without optical tracers, a key prediction of active vacuum frameworks. This software provides the first falsifiable pipeline to test vacuum activity signatures in large-scale HI distribution, bridging FAST, MeerKAT, SKA-Mid and BINGO (Brazil).

# Key Features

- 10 Proofs + 3 Tests fully reproducible: `pip install numpy scipy astropy matplotlib && python pipeline_v631_moda.py`
- Direct validation against Paul et al. 2025 MeerKAT data
- Log-Uniform baseline: 10.5281/zenodo.22700008

# Acknowledgements

Based on Zenodo records 10.5281/zenodo.22739495 and 10.5281/zenodo.22735900.

# References
