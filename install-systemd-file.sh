#!/usr/bin/env bash
sudo cp pi-fan-tuner.service /lib/systemd/system/pi-fan-tuner.service
sudo systemctl daemon-reload
sudo systemctl enable pi-fan-tuner
sudo systemctl start pi-fan-tuner