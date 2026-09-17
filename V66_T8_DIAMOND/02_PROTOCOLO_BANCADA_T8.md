# Teste de Bancada V6.6 T8 - Protocolo Experimental

Segue DOI 10.5281/zenodo.22649556 (Bancada) e DOI 10.5281/zenodo.22672602 (Engenharia).

## Materiais
- Membrana diamante policristalino CVD, 5 μm, 1cm x 1cm, edge-exfoliation (HKU method)
- 100nm Au sputtered ambos lados (Fig.S3 Jing et al. 2026)
- PET flexível + insulating tape (teste inicial fora UHV)
- Para UHV: substrato Ti-6Al-4V + Mu-metal shielding (como A8.0)

## Passo 1 - Caracterização fora UHV (reproduz Science Advances)
1. Montar device como Fig.2A: uma ponta fixa, outra deformada por força controlada
2. Medir d33 com piezometer (Fig.2B): esperado 4 pC/N @5um
3. Medir V vs strain 0.35%, 0.70%, 1.05% (Fig.2D): esperado ~20, ~40, ~60mV
4. Teste ciclico 7000 ciclos @0.35% strain (Fig.2G): estabilidade <5% drift

## Passo 2 - Dentro da Câmara UHV Toroidal
1. Instalar membrana na parede interna do toroide, área de maior strain acústico
2. Conexão Guanella 8.45Ω → 50Ω (bancada RF existente 915MHz)
3. Bombeio até ≤1e-9 mbar, monitorar S11, Q, S21 vs pressão
4. Excitar modo breathing com PZT externo calibrado e medir resposta diamante

## Passo 3 - Balanço Fechado
1. Medir P_RF, P_HV, P_vac, P_control com wattímetro independente
2. Medir P_out_diamond = V² / 50Ω
3. Calcular P_res = P_out_el + P_out_th - (P_RF+P_HV+P_vac+P_control+P_aux)
4. Análise cega Conde-Ruler: conde_ruler.measure(time_series) sobre 1M shots de V(t)
   - Se z-score εR >3.903 (q99) → FALHA
   - Se z-score <2.64 (q95) → APROVADO

## Passo 4 - Integração com Gerador
1. Stack 10 membranas 1cm² em série (0.7V total @1.4%)
2. Rectenna Toroidal para retificar AC → DC
3. Calorimetria independente para P_out_th

## Critérios de Falseabilidade
- Se P_res / F_res / T_res não sobreviver a balanço fechado + calorimetria + controle simétrico + polarização invertida + análise cega → hipótese enfraquecida
- Resultado positivo em um sistema não implica positivo em outros

## Saída
- rvm_params_diamond_15bins.csv
- fig_T8_diamond_UHV_V66.png
- fig_diamond_S11_Q_vs_pressao.png
