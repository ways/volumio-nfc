# Control Volumio.org using NFC

This is a collection of scripts to control a volumio based music player using a PN532 NFC reader. Idea from http://blog.zenona.com/ and http://tilman.de/projekte/audiosphere/.

## Idea

* Use NFC stickers or cards.
* When scanned, the id of the sticker is matched with a list. If contained in list, queue is cleared and selected music starts playing.
* Additional buttons are required for i.e. play/pause, next, volume up.
* Any music source can be used.
* Format of music list: 'source,uri': 'nfc-sticker-id'.
** Example: 'webradio,http://ice1.somafm.com/secretagent-128-aac': b'K\x01...'
** Example: 'spop,spotify:track:2Wf0uMfCpwLO1B2Up3NbXH': b'K\x01\x01...'

## Hardware setup

* Connect and configure NFC reader as advised, this script assumes i2c.
* Change /etc/nfc/libnfc.conf to contain:

  device.name = "PN532 over I2C"
  device.connstring = "pn532_i2c:/dev/i2c-1"

* Test with sudo i2detect -y 1 and # nfc-list to make sure NFC reader is connected.
* Fetch https://github.com/HubCityLabs/py532lib
* sudo apt install libnfc5 libnfc-bin libnfc-examples python3
* Copy readnfc.py
* Test by running script manually
* To make it autostart, copy systemd service file readnfc.service to /etc/systemd/system/readnfc.service and enable.

Optional:

* Set up GPIO script to connect buttons.
* Thank me.

## Todo

* Move tag list to separate file.
* It would be very nice if all this could be turned into a proper volumio plugin.

