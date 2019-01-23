#!/bin/bash

clear

echo "Eliverse Infrastructure Server - OPZ Mark I"
echo "-------------------------------------------"
echo "Checking available Wi-Fi APN's in range...."

# Check available Wi-Fi APNS
nmcli -p -f SSID,MODE,CHAN,RATE,SIGNAL,SECURITY dev wifi list

echo ""

while true; do
    read -p "Would you like to connect to Wi-Fi? [Y/n]" yn
    case $yn in
        [Yy]* ) nmtui; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
