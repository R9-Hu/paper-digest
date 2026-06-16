# Scheduling (systemd user timer)

The daily 08:00 run is driven by a **systemd user timer** (not cron) so it
**catches up missed runs** after the machine was asleep/off (`Persistent=true`).

## Install

```bash
mkdir -p ~/.config/systemd/user
cp systemd/paper-digest.service systemd/paper-digest.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now paper-digest.timer
loginctl enable-linger "$USER"      # run even when logged out
```

## Operate

```bash
systemctl --user list-timers paper-digest.timer   # next/last fire times
systemctl --user start paper-digest.service       # run now (full pipeline)
journalctl --user -u paper-digest.service -n 50    # logs from the last run
systemctl --user disable --now paper-digest.timer # stop scheduling
```

`Persistent=true` means: if the scheduled 08:00 trigger was missed (laptop off),
the job runs once on the next boot/login, then resumes the normal schedule. Unlike
cron, a missed slot is not silently dropped. A single catch-up run still collects
everything new since the last successful run (fetch is incremental + deduped).
