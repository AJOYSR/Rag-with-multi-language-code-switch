#!/bin/zsh
# One night of test runs: starts the Ollama server if needed, keeps the Mac awake, and stops
# cleanly after HOURS (default 8). Re-run each night; it resumes where it stopped.
# Usage: scripts/night_run.sh [HOURS]
cd "$(dirname "$0")/.." || exit 1
HOURS=${1:-8}
LOG=05_experiments/runs/logs; mkdir -p $LOG
if ! curl -s -m 2 localhost:11434/api/version >/dev/null; then
  nohup /opt/homebrew/opt/ollama/bin/ollama serve >> $LOG/ollama_serve.log 2>&1 &
  for i in {1..30}; do curl -s -m 2 localhost:11434/api/version >/dev/null && break; sleep 1; done
fi
export RUN_DEADLINE=$(( $(date +%s) + HOURS * 3600 ))
STAMP=$(date +%Y%m%d_%H%M)
echo "test runs started $(date), stop by $(date -r $RUN_DEADLINE)" | tee -a $LOG/night_$STAMP.log
nohup caffeinate -i make -s test-run >> $LOG/night_$STAMP.log 2>&1 &
echo "running in background; progress: tail -f $LOG/night_$STAMP.log"
