# ¿Te avisa la IA de lo que no le preguntaste?

Proyecto para el **AI x Epistemics Research Sprint** (Apart Research, 13–15 nov 2026).

Medimos si los chatbots que usa la gente avisan **por iniciativa propia** de un riesgo que va escondido dentro de una petición normal (un plan de desayunos con un medicamento que interactúa con la toronja, una fiesta infantil con alimentos que causan asfixia, un script que puede borrar el disco…). Es decir, si actúan como "ángel guardián" (Forethought, *Angels-on-the-Shoulder*).

## Diseño
- **14 prompts** (P0–P12 y el control C1) en salud, ingeniería e informática, con riesgos de tres niveles de dificultad. Textos y clave de riesgos en [`piloto/bateria_prompts.md`](piloto/bateria_prompts.md).
- **Apps:** Gemini (sin sesión), ChatGPT (sin sesión) y Claude (cuenta gratuita, chat incógnito); 5 tiradas por prompt, cada una en un chat nuevo. Exploratorio: AI Mode del buscador de Google (P0, P1, P3, P8).
- **Clasificación a ciegas** por dos evaluadores (¿avisa?, ¿el plan final es seguro?, ¿falsa seguridad?) y acuerdo con kappa de Cohen.

## Estructura
| Carpeta | Contenido |
|---|---|
| `piloto/` | Pruebas manuales del 13 nov y batería de prompts |
| `datos/respuestas/` | Cada respuesta completa, tal cual, con modelo, fecha y hora |
| `datos/capturas/` | Captura de pantalla de cada tirada (desde que se activó) |
| `datos/respuestas.csv` | Una fila por respuesta |
| `datos/HUELLAS.sha256` | Huella SHA-256 de cada archivo, para comprobar que nada cambió |
| `datos/*.py` | Scripts de guardado, huellas, clasificación a ciegas y análisis |
| `clasificacion/` | Textos sin nombre de app y hojas de cada evaluador ([instrucciones](clasificacion/INSTRUCCIONES.md)) |

## Reglas mientras se clasifica
- **Evaluadores:** trabajen solo en `clasificacion/` y suban solo su hoja. **No abran `datos/respuestas/` ni `datos/capturas/`** hasta terminar: los nombres de archivo dicen la app.
- La tabla código → app (`CLAVE_NO_ABRIR.csv`) no está en el repositorio; se publica al terminar la clasificación.

## Reproducir el análisis
```bash
pip install scipy matplotlib
python datos/analisis.py
```

Todo el material se creó durante el sprint (13–15 nov 2026). La recogida de respuestas la hizo Claude con el navegador integrado de Claude Code, copiando el texto de cada respuesta sin modificarlo; la clasificación la hacen personas del equipo.
