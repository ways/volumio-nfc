# Control Volumio.org using NFC

This is a collection of scripts to control a volumio based music player using a PN532 NFC reader. Idea from http://blog.zenona.com/ and http://tilman.de/projekte/audiosphere/.

## Idea

* Use NFC stickers or cards.
* When scanned, the id of the sticker is matched with a list. If contained in list, queue is cleared and selected music starts playing.
* Additional buttons are required for i.e. play/pause, next, volume up.
* Any music source can be used.
* Format of music list: see readnfc.list

## Hardware setup

* Install Volumio on a Pi. Tested with version 2.323-2.344.
* Connect and configure NFC reader as advised, this script assumes i2c.
* Change /etc/nfc/libnfc.conf to contain:

  device.name = "PN532 over I2C"
  device.connstring = "pn532_i2c:/dev/i2c-1"

* Test with sudo i2detect -y 1 and # nfc-list to make sure NFC reader is connected.
* Fetch https://github.com/HubCityLabs/py532lib
* sudo apt install libnfc5 libnfc-bin libnfc-examples python3
* Download this repo and run readnfc.py manually to test.
* To make it autostart, copy systemd service file readnfc.service to /etc/systemd/system/readnfc.service and enable.
* Systemd timer to restart service soon after boot is needed for unknown reason. Also included.

Optional:

* Set up GPIO script to connect buttons.
* Thank me.

## Todo

* It would be very nice if all this could be turned into a proper volumio plugin.
* An easy way to store new tags?
* LED to notify when volumio is ready.
* Better voice feedback.
* Debug some volumio problems like https://volumio.org/forum/play-stop-being-toggled-next-t8327.html

