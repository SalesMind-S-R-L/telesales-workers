#!/bin/bash
cd /Users/simocors/Desktop/telesales || exit 1
L=/Users/simocors/Desktop/telesales/tue_run
nohup /usr/bin/caffeinate -i /usr/bin/python3 "$L/culligan_09jun_scheduler.py" >> "$L/run_tue.out" 2>&1 &
echo "scheduler PID $! $(date)" >> "$L/run_tue.out"
nohup /usr/bin/caffeinate -i /usr/bin/python3 "$L/culligan_recall_daemon.py" >> "$L/recall_tue.out" 2>&1 &
echo "recall PID $! $(date)" >> "$L/recall_tue.out"
echo "CAMPAGNA MARTEDI AVVIATA $(date)"
