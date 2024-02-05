#!/bin/bash

# no arguments, Vasily
if [ $# != 0 ]; then
    echo "usage: ${0##*/}"
    exit 1
fi

# clone systemd timer entrie
cp ./ticket_sales_to_spreadsheet.* ~/.config/systemd/user

# force reload of timers, immediately start and enable
systemctl --user daemon-reload
systemctl start --user ticket_sales_to_spreadsheet.timer
systemctl enable --user ticket_sales_to_spreadsheet.timer
