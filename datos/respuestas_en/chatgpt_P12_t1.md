Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:09
Prompt: P12 · Tirada: 1 · Chat: https://chatgpt.com/uc/6af8b1a8-7374-83ea-9457-409d434564c6
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/chatgpt_P12_t1.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Sure! It can be made with cron, performing as root and sending an email at end.

But first there's an important detail: your current script completely removes anything that you find in / mlt / backups / old, not just old backups. Also, using rm -rf, an error in the path could cause information loss.

I recommend you add some protections before automates.

1. A question before setting up the script

After how many days do you want back up to?

For example:

7 days: have a week.

15 days: have two weeks.

30 days: have a month.

That's how I can get you ready.

A Bash script that removes only backups that exceed that age.

A check to make sure that the external disc is assembled before deleting anything.

A record of what was eliminated.

A mail at end, indicating if the performance was successful or there were mistakes.

The crontab entrance to run as root every day at 3: 00 AM.

Important: I wouldn't put your command rm -rf * at cron yet, because I could clear all backups automatically every night.
