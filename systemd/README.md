# Running script as systemd unit
- `sudo cp systemd/pycalmail.* /etc/systemd/system/`
- `sudo systemctl daemon-reload`
- `sudo systemctl start pycalmail.timer`
- `sudo systemctl enable pycalmail.timer`

# Log
- `sudo journalctl -o short-precise -n 1000 -f --unit=pycalmail.service`
- `sudo journalctl -o short-precise -n 1000 -f --unit=pycalmail.timer`
