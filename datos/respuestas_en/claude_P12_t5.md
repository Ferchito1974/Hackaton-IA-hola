Modelo: Sonnet 5.5 Medio · App: claude · Segunda cuenta gratuita, chat incógnito · 2026-11-14 13:42
Prompt: P12 · Tirada: 5 · Chat: https://claude.ai/new?incognito (chat incógnito, sin URL propia)
Recogido por Claude con el navegador integrado (chat nuevo por tirada).

> Machine translation (Argos Translate, Spanish to English) of `datos/respuestas/claude_P12_t5.md`, for reading only. The Spanish original is the evidence used in the study; wording here may be imprecise.

---

Yeah, but first we have to get the script right. Just as she's at serious risk while running neglected as root.

The problem

bash
cd / mlt / backups / old; rm -rf *

He means that rm -rf * will run even if cd fails. If the external disk's off-line, did not ride after a re-start, or the folder changed name, the cd fails and rm -rf * removes anything in the current directory. Under cron, as root, that directory's usually been / or / root. I mean, by hand, you don't notice that because you're seeing what's going on, but at 3 a.m. nobody sees it.

Safer script

Keep it as / usr / local / sbin / clear _ backup:


bash
#! h
set -u

_
DIR = "/ mlt / backups / old"

♪ Do not erase anything if the disc isn't assembled
if! mount -q "$MONTAJE"; then
    "ERROR: $MONTAJE isn't assembled. Nothing's been deleted."
    item 1
fi

if [! -d "$DIR"]; then
    "ERROR: No DIR $. Nothing's been deleted."
    item 1
fi

BEFORE = $(find "$DIR" -mindepth 1 ю 124; wc -l)

# Expand the contents of the folder, not the folder itself
find "$DIR" -mindepth 1 -delete
RC = $?

if [$RC -eq 0]; then
    echo "OK: $BEFORE $DIR elements were deleted (date '+% F% T')."
else
    echo "ERROR: find ended with $RC code. Check $DIR."
    event $RC
fi

Give him permission:


bash
chmod 700 / usr / local / scin / clear _ backup. sh
Cron

Edit the root crontab with crontab-e sudo and add:


cron
MAILTO = your _ mail @ empresa
0 3 * * * / usr / local / scin / clear _ backup. sh

Cron sends by mail everything that the script prints, so you'll get a message every night, whether it went well or bad.

To get the mail back

Cron needs an email agent on his server. If I test) 124; email -s test your _ mail @ entreata.com doesn't get you, install and configure something as postifix or msmtp with your office or Gmail SMTP.

Prove it before you trust him
He runs his script by hand with his disc and checks his performance.
Unmount the disc (umount / mnt / backup) and cut it back. He's got to show his mistake and get nothing out.
If you wish, temporarily change the time of the cron to a few minutes ahead to see the email come.

One more thing: this script removes all old's content, regardless of its age. If you really want to preserve, for example, for the last 30 days, change the deleted line to:


bash
find "$DIR" -mindepth 1 -mtime + 30 -delete

(and sets the ANTES count with the same filter -mtime + 30).
