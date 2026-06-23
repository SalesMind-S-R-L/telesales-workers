#!/bin/bash
# Lancia il batch Marco Ferretti sui lead VERIFICATI DIALABILI e fa il PUSH AUTOMATICO
# sul foglio OUTREACH AI VOICE a fine batch.
# Uso: ./LANCIA_BATCH.sh [limite]   (default 30)
cd /Users/simocors/Desktop/telesales
LIMIT="${1:-30}"
# gira in background: lancia -> attende fine -> pusha da solo
nohup python3 ferretti_lancia_e_push.py \
  --csv prospecting_b2b/ferretti_aivoice_pronti.csv \
  --limit "$LIMIT" > /tmp/ferretti_run_$(date +%H%M).log 2>&1 &
echo "Batch avviato in background (PID $!). Push automatico a fine batch."
echo "Log: /tmp/ferretti_run_*.log"
