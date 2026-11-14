cd /c/Users/fereu/Desktop/Universidad/vision/hackathon_epistemics/datos || exit 1
S=/c/Users/fereu/AppData/Local/Temp/claude/2d01f8be25d11e6a/a649febc-c3b2-445e-813c-62f81cd28a0a/scratchpad
python $S/save2.py $S/$1_t$2.json "Sonnet 5.5 Medio" $1 $2 $3 $4 && python guardar_captura.py "C:\Users\fereu\.claude\projects\C--Users-fereu-Desktop-Universidad-vision\a649febc-c3b2-445e-813c-62f81cd28a0a\tool-results\mcp-Claude_Browser-blob-$5.jpg" claude_$1_t$2; tail -1 respuestas.csv
