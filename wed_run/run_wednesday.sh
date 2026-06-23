#!/bin/bash
cd /Users/simocors/Desktop/telesales || exit 1
L=/Users/simocors/Desktop/telesales/wed_run
nohup /usr/bin/caffeinate -i /usr/bin/python3 "$L/culligan_10jun_scheduler.py" >> "$L/run_wed.out" 2>&1 &
echo "scheduler PID $! $(date)" >> "$L/run_wed.out"
nohup /usr/bin/caffeinate -i /usr/bin/python3 "$L/culligan_recall_daemon.py" >> "$L/recall_wed.out" 2>&1 &
echo "recall PID $! $(date)" >> "$L/recall_wed.out"
echo "CAMPAGNA MERCOLEDI AVVIATA $(date)"
