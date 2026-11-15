# Lo que le falta al proyecto antes de entregar

Entrega: **domingo 15 nov, antes de las 18:00 (hora de México)**. Cierre oficial 23:59 AoE.

Paper editable: https://claude.ai/artifact/GJ6QQBS8jAwyvHwXRfMnLQ · PDF y Word actuales en `paper/`.

## Ya resuelto (no hace falta tocarlo)
- [x] Recogida de las 230 respuestas, con capturas, huellas y commits.
- [x] Clasificación ciega por dos personas y consenso de los 38 desacuerdos.
- [x] Análisis reproducible (`python datos/analisis.py`), 3 figuras en inglés y tablas.
- [x] Paper en inglés con la estructura de la plantilla, apéndice de ética y uso dual, y declaración de uso de LLMs.
- [x] Referencias verificadas abriendo cada fuente (34 + 1).
- [x] H3 reformulada (puertas de entrada gratuitas, no gratis frente a pago).
- [x] Fiabilidad reportada con acuerdo simple (89–91 %) además de la kappa (0.42).
- [x] Tabla de la matriz movida al apéndice para ahorrar espacio.
- [x] Repositorio público, README en inglés, licencia, `requirements.txt` y clave de códigos publicada.

## Pendiente: lo tiene que hacer el equipo

### 1. Texto del paper (prioridad alta)
- [ ] **Leer el paper entero y reescribirlo con sus palabras.** La plantilla pide que el equipo escriba principalmente la entrega, y la declaración de uso de LLMs dice que lo hicieron.
- [ ] **Recortar el cuerpo a unas 5–6 páginas.** Ahora ocupa unas 7–8; el máximo es 8 y la guía recomienda unas 4. Candidatos para acortar:
  - el segundo párrafo de *Related Work*;
  - *Hiding depth (H1)*;
  - el párrafo *Both sides of the guardian angel* de la discusión.
- [ ] **Autores y afiliaciones** en el bloque de autores (ahora dice `[Author Name 1], [Affiliation]`).
- [ ] **Author Contributions:** quién diseñó, clasificó, adjudicó, escribió e hizo el video.
- [ ] **Revisar la declaración de uso de LLMs** y ajustarla si algo no refleja lo que hicieron.
- [ ] **Revisión de literatura:** leer al menos PaSBench (arXiv 2505.17455) y las fuentes de la tabla del apéndice B. Pueden quitar o cambiar las que no les convenzan.
- [ ] (Opcional) Que alguien del área de salud revise la clave de P0, P2, P5 y P8.

### 2. Formato de entrega
- [ ] Copiar el texto final a la **plantilla oficial de Google Docs**: https://docs.google.com/document/d/17b3JWki-ZkaqdmqGI5d0gof-HwlGuWU9Mc1_klNZXKs/copy?usp=sharing. Pegar desde `paper/which_door_you_walk_through.docx`; las figuras están en `resultados/fig1_mapa_aviso.png`, `fig2_apps.png` y `fig3_paneles.png`.
- [ ] Borrar el texto de instrucciones de la plantilla y exportar a PDF (máximo 25 MB).
- [ ] Si cambian alguna cifra o figura, avisar para comprobar que coincide con los datos.

### 3. Repositorio
- [ ] Si cambian el nombre del repo, actualizar el enlace en el paper (sección *Code and Data*) y en este README.
- [ ] Poner los nombres del equipo en el README (sección *Team*).

### 4. App y video
- [x] App con diseño profesional: `app/web/which-door.html` (un solo archivo) y publicada en https://claude.ai/artifact/SiFCkWeoDoss3MdD6M8JUq (privada: compartirla desde Share si se quiere enlace público).
- [ ] Pulir la página (`datos/web_plantilla.html` → `python datos/construir_web.py`): aspecto más limpio y menos amontonado (más aire entre secciones, menos elementos por pantalla, la sección "The bench" más simple) y animaciones sutiles al hacer scroll y al cambiar de tirada. Idealmente con la skill frontend-design si ya está instalada.
- [ ] Video de 3 a 5 minutos (opcional, pero suma): el problema, un caso real con las capturas de `datos/capturas/`, un recorrido por la app y los resultados.

### 5. Entrega
- [ ] Subir el PDF en la página del sprint ("Submit your project"), con título, resumen, enlace al repositorio y video.
- [ ] Revisión final: título, autores, resumen de 150 a 250 palabras y apéndice de limitaciones y ética.

### 6. Opcional, si sobra tiempo
- [ ] Prueba de la app de Gemini con sesión iniciada (P0, P1, P3 y P8, 5 tiradas cada uno) para aislar el efecto del modelo.
- [ ] Mandar los casos a Google (divulgación responsable) y mencionarlo en el paper.
