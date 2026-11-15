# Lo que falta para entregar

Entrega: **domingo 15 nov, antes de las 18:00 (hora de México)**. Cierre oficial 23:59 AoE. Se entrega en la página del sprint con el botón **"Submit your project"**.

Todo lo técnico está terminado y en el repositorio:
- datos (230 respuestas, capturas, huellas, traducciones);
- clasificación y consenso;
- análisis y figuras;
- paper en inglés (`paper/`);
- página de demostración (`app/web/which-door.html`);
- traducciones de los prompts (`piloto/prompts_en.md`);
- guion del video ([VIDEO_GUION.md](VIDEO_GUION.md)).

## Lo que solo puede hacer el equipo

### 1. Paper (prioridad alta)
- [ ] **Leer el paper entero y reescribirlo con sus palabras.** La plantilla pide que la entrega final la escriba el equipo, y la declaración de uso de LLMs dice que lo hicieron. Paper editable: https://claude.ai/artifact/GJ6QQBS8jAwyvHwXRfMnLQ
- [ ] **Recortar el cuerpo a unas 5–6 páginas.** Ahora ocupa unas 8, que es el máximo. Candidatos:
  - el segundo párrafo de *Related Work*;
  - *Hiding depth (H1)*;
  - *Both sides of the guardian angel*.
- [ ] **Autores y afiliaciones** (ahora dice `[Author Name 1], [Affiliation]`).
- [ ] **Author Contributions**: quién hizo qué.
- [ ] **Revisión de literatura**: leer al menos PaSBench (arXiv 2505.17455) y revisar las fuentes del apéndice B.
- [ ] **Pasar el texto a la plantilla oficial de Google Docs** (https://docs.google.com/document/d/17b3JWki-ZkaqdmqGI5d0gof-HwlGuWU9Mc1_klNZXKs/copy?usp=sharing), pegando desde `paper/which_door_you_walk_through.docx`, y borrar el texto de instrucciones. Las figuras son `resultados/fig1_mapa_aviso.png`, `fig2_apps.png` y `fig3_paneles.png`.
- [ ] Exportar a PDF (máximo 25 MB). Si cambian alguna cifra, avisar a Claude para comprobar que coincide con los datos.

### 2. Video (opcional, pero suma)
- [ ] Grabar siguiendo [VIDEO_GUION.md](VIDEO_GUION.md) (unos 3:30), con la página de demostración.
- [ ] Subirlo a YouTube (oculto) o a Drive y copiar el enlace.

### 3. Repositorio
- [ ] Nombres del equipo en el README (sección *Team*).
- [ ] Si cambian el nombre del repo, actualizar el enlace en el paper (*Code and Data*), en el README y en la página.
- [ ] Compartir la página publicada desde **Share** si se quiere un enlace público (https://claude.ai/artifact/SiFCkWeoDoss3MdD6M8JUq). Si no, basta con el archivo del repo.

### 4. Entrega
- [ ] En "Submit your project": título, resumen (150–250 palabras), PDF, enlace al repositorio y enlace al video.
- [ ] Revisión final: autores, resumen, apéndice de limitaciones y ética, y declaración de uso de LLMs.

## Opcional (no hace falta para entregar)
- Prueba de mitigación en Gemini: 9 de 20 respuestas recogidas (`geminimit_*`). Está **incompleta** y **no se usa** en el paper.
- Prueba de la app de Gemini con sesión iniciada, para aislar el efecto del modelo.
- Enviar los casos a Google (divulgación responsable).
