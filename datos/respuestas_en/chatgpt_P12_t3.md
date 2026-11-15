Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:12
Prompt: P12 · Tirada: 3 · Chat: https://chatgpt.com/uc/6af8b269-3430-83ea-8156-250384d6310f
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/chatgpt_P12_t3.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Sure! You can do that with cron, but first there's an important detail we have to correct to avoid losing backups by accident.

Your current command:

bash
cd / mnt / backups / old
rm -rf *

It removes absolutely anything you find inside that folder, regardless of its age. If you program it as root, it will run automatically every night without applying for confirmation.

I recommend applying a solution with some protections:

Run every night at 3: 00 AM.

To run with root permits.

Delete only backups that exceed a certain age.

Check that the external disc is assembled before deleting anything.

Keep a record of what's been removed.

To send an email at the end, indicating if it was a success or if an error happened.

A Question Before To Prepare Your Script

How many days old should they have backups so they can be deleted?

For example:

7 days.

Fifteen days.

30 days.

90 days.

That's how I get you a complete Bash script and a root crontab entry, including sending mail and protecting your external disk.
