#!/bin/sh

# Reference: https://weworkweplay.com/play/rebooting-the-raspberry-pi-when-it-loses-wireless-connection-wifi/
ping -c4 google.com > /dev/null
 
if [ $? != 0 ] 
then
  sudo /sbin/shutdown -r now
fi