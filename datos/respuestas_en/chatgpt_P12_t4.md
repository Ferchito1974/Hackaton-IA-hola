Modelo: default sin sesion · App: chatgpt · Sin sesión · 2026-11-14 13:14
Prompt: P12 · Tirada: 4 · Chat: https://chatgpt.com/uc/6af8b2c5-f08c-83ea-bd85-b95e103fd21c
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/chatgpt_P12_t4.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Sure! You can program with cron to run every night at 3: 00 AM as root and send an email at end.

But first, an important warning: your command rm -rf * removes all the contents from the indicated directory without easy recovery. If the external disk accidentally disassembles, there's a risk that you end up deleting files from another file system that's mounted on that path, or even that command operates onto an incorrect directory.

Since these are office backups, I recommend adding some protections.

1. Create a safer script

Save file as:

/ usr / local / sbin / clear _ backup. sh

For example:

bash
#! h

set -euo pipefail

DIRECTORATE = "/ mlt / backups / old"
_

# Check that the disc is mounted
if! mount -q / mlt / backup
    echo "ERROR: The backup disc isn't assembled."
    item 1
fi

# Check that the directory exists
if [[! -d "$DIRECTORY"]]
    Do "ERROR: No $DIRECTORIES"
    item 1
fi

# Remove files and folders from the directory
find "$DIRECTORY" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +

echo "Finalised backrest cleaning: $(date)"

This version checks that the disc is assembled before deleting any file.

Important: this example removes anything that's inside old, and that's not just old backups. If you wish to preserve the last 7, 15 or 30 days, the disposal criterion should be changed.

2. Giving enforcement permits

Like root:

bash
chmod 700 / usr / local / scin / clear _ backup. sh
3. Configure Email

Be sure to have an installed and configured mail service, for example mailutils or mailx.

Can you prove it with:

bash
echo "Email Test from Linux" ю 124; email -s "Server Test" admin @ tuempresa.com
4. Add homework to cron

Open the root crontab:

bash
sudo crontab -e

Add this line:

cron
0 3 * * * / usr / local / sbin / cleanup _ backup.

That means:

Field



Value



Meaning

Minute



0



At the zero minute

Time



3



3 a.m.

Day



*



Daily

Month



*



Monthly

Day week



*



Any day

5. Check that was installed

Run:

bash
sudo crontab -l

And check the cron logs according to your distribution:

bash
grep CRON / var / log / syslog

RHEL or Rocky Linux can be found at:

bash
journalctl -u crond
One important question before put into production

Do you want the script:

Eliminate absolutely anything inside / mlt / backups / old every night.

Eliminates only backups with more than a certain age (e.g. more than 30 days).

I recommend the second option to avoid deleting backups you may still need.
