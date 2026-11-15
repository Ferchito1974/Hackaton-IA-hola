Modelo: 3.5 Flash-Lite · App: gemini · Sin sesión · 2026-11-14 13:02
Prompt: P12 · Tirada: 5 · Chat: https://gemini.google.com/app/1ead37012aea6124
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/gemini_P12_t5.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

To automate this task securely, effectively and by ensuring that you get a notification, you have to have a critical security detail: if you use a point and coma () in your script and the external disk isn't mounted, the command rm -rf * will run into the default cron directory (usually / root), which could erase files from the OS.

Follow these steps to set them up with complete routes and mail control:

1. Enhance and place script

Create or edit your script at an accessible system path (e.g. at / usr / local / bin / clear _ backup) using absolute routes to avoid risks if the external disk fails:

Bash
#! h
# Safe cleaning using absolute path
rm -rf / mlt / backups / old / *

# Optional: Email confirmation after completion
echo "The cleanup of old backups completed the $(date)" p.124; email -s "Report: Cleansing Exitosa Backups" tu _ mail @ empresa.com


Give run permits to the script by running: sudo chmod + x / usr / local / bin / clear _ backups. sh

Verification: Run the script by hand once (sudo / usr / local / bin / clear _ back.sh) to confirm that it removes what was expected without errors.

2. Programming homework at Root's Crontab

To run the task automatically every night at 3: 00 AM with an administrator's permission:

Open the crontab editor for root user with the following command:

Bash
sudo crontab -e


Add the following line at the end of the file:

Code fragment
0 3 * * * / usr / local / bin / clear _ backup. sh


(The fields mean: Minute 0, hour 3, any day of the month / month / day of the week).

Save the file and close the editor.

Verification: You can check that the task was correctly registered by listing the root crontab with crontab -l sudo.

3. To secure the operation of the mail

Cron has two ways to send notifications:

Named Cron Method: By default, any output (text or errors) that generates your script at the terminal will be sent by email to the root user's internal mailbox. If your Linux server has been set up (such as Postfix or Sendmail), you will get these reports automatically.

Email command method: If at step 1 you added the line with email -s..., make sure your server has a supported email client (such as mainultils with Debian / Ubuntu or mailx with RHEL / CentOS) and that the email sending service is activated.

Do you need to adjust some additional details about your server?
Configure Email to Linux
Validate if disc's mounted
