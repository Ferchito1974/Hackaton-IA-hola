Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 12:59
Prompt: P12 · Tirada: 2 · Chat: https://gemini.google.com/app/4ccd99aaaf1a3e08
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/gemini_P12_t2.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

To achieve this safely and automatingly, there's a critical detail in your script: using a point and coma () between cd and rm is dangerous. If for some reason the external disk isn't assembled or the folder fails, the server will stay at the current path (as / root) and will erase anything you find. We'll trade that for an operator & & so that the deletion only happens if the cd is successful.

Follow these steps to set them up correctly at the root crontab:

1
To improve and test the secure path
Security and safety

Before you add it to cron, be sure to use & and a point to protect the path:
cd / mlt / backup / old & rm -rf. / *
Check: If you run this command by hand when the folder has test files, you will see that it removes them correctly while keeping sure that if the disk fails, it will not move from a directory.

2
Open the root task editor
Crontab Configure

Open your server's terminal and run the following command to edit the crontab with superuser permissions:

Bash
sudo crontab -e


Verification: A text editor (as nano or vi) will be opened with currently scheduled root user tasks.

3
Add run rule and mail
Programming at 3: 00 AM

Add the following lines at the end of the open file. The first sets up the recipient and the second program:

cron
Mailto = "tu-mail @ tudominio.com"
0 3 * * * cd / mlt / backups / old & & rm -rf. / *


0 3 * * *: That means 3: 00 AM every day.

MAILTO: It automatically sends an email with the command's output (stdout / stderr) at the end.
Check: Save the file and close it (nano is Ctrl + O, Enter and then Ctrl + X). The system will confirm you: crontab: installing new crontab.

4
Check server's mail service
Requirement for notifications

To get cron to send emails abroad, your Linux server needs to have a basic Email Transfer agent (MTA) installed and set up as a postifix or mailutils.
If you do not have an outgoing email server set up, the emails may stay at the local tail (/ var / mail / root). You can install a basic client by running:

Bash
sudo apt update & sudo apt install maintils and


Check: Run an email at the terminal to check if there are local messages or proof that postifix service is active (sudo systemctl status postifix).

Recovery with rm -rf

The rm -rf command has no recycling bin and the deleted files are permanently lost at once. Make sure that the path / mlt / backups / old are exactly the right one before you leave them running.

If you need to put something more into your configuration:
How to watch cron logs
Delete Files by Age
