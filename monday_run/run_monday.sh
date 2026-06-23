#!/bin/bash
cd /Users/simocors/Desktop/telesales || exit 1
LOGDIR=/Users/simocors/Desktop/telesales/monday_run
# scheduler 4 fasce
nohup /usr/bin/caffeinate -i /usr/bin/python3 "$LOGDIR/culligan_08jun_scheduler.py" >> "$LOGDIR/run_monday.out" 2>&1 &
echo "scheduler PID $! $(date)" >> "$LOGDIR/run_monday.out"
# recall daemon live
nohup /usr/bin/caffeinate -i /usr/bin/python3 "$LOGDIR/culligan_recall_daemon.py" >> "$LOGDIR/recall_monday.out" 2>&1 &
echo "recall PID $! $(date)" >> "$LOGDIR/recall_monday.out"
echo "CAMPAGNA LUNEDI AVVIATA $(date)"
