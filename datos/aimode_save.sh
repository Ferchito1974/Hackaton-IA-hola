#!/bin/bash
# usage: save.sh P n sha shot_path
set -e
SP=/c/Users/fereu/AppData/Local/Temp/claude/2d01f8be25d11e6a/a649febc-c3b2-445e-813c-62f81cd28a0a/scratchpad
P=$1; N=$2; SHA=$3; SHOT=$4
cd $SP
out=$(python prep.py aimode_${P}_t${N} $SHA $P)
echo "$out"
echo "$out" | grep -q "hash_ok True" || { echo "HASH MISMATCH - not saved"; exit 1; }
URL=$(cat $SP/aimode_${P}_t${N}.url)
cd /c/Users/fereu/Desktop/Universidad/vision/hackathon_epistemics/datos
python guardar.py aimode "AI Mode (sin etiqueta)" $P $N "$URL" < $SP/aimode_${P}_t${N}.txt
python guardar_captura.py "$SHOT" aimode_${P}_t${N}
