#!/bin/bash
# PatchCore Reproduction & Validation Scripts for Pill and Metal_nut

# 1. Pill - Sampling Ratio Study (1%, 10%, 25%, 99%)
for pct in 0.01 0.1 0.25 0.99
do
    PYTHONPATH=src python bin/run_patchcore.py \
    --gpu 0 --seed 0 results/pill_ratio_$pct \
    patch_core -b wideresnet50 -le layer2 -le layer3 --anomaly_scorer_num_nn 1 --patchsize 3 \
    sampler -p $pct approx_greedy_coreset \
    dataset --resize 256 --imagesize 224 -d pill mvtec $1
done

# 2. Metal_nut - Resolution & Layer Study
# Res 324
PYTHONPATH=src python bin/run_patchcore.py \
--gpu 0 --seed 0 results/metal_nut_res324 \
patch_core -b wideresnet50 -le layer2 -le layer3 \
sampler -p 0.1 approx_greedy_coreset \
dataset --resize 356 --imagesize 324 -d metal_nut mvtec $1

# Layer 1+2+3
PYTHONPATH=src python bin/run_patchcore.py \
--gpu 0 --seed 0 results/metal_nut_layer123 \
patch_core -b wideresnet50 -le layer1 -le layer2 -le layer3 \
sampler -p 0.1 approx_greedy_coreset \
dataset --resize 256 --imagesize 224 -d metal_nut mvtec $1
