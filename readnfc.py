#!/usr/bin/env python3

# https://github.com/HubCityLabs/py532lib
# sudo apt install libnfc5 libnfc-bin libnfc-examples python3
# /etc/nfc/libnfc.conf must contain:
# device.name = "PN532 over I2C"
# device.connstring = "pn532_i2c:/dev/i2c-1"
# mo/sda/tx -> raspi pyhsical 3
# nss/sclk/rx -> raspi physical 5
# test nfc reader with sudo i2detect -y 1
# Logs at sudo journalctl -u readnfc

tagfile='readnfc.list'

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from subprocess import call
import time
import logging

pn532 = Pn532_i2c()
pn532.SAMconfigure()

# Read tag list
with open(tagfile, "rb") as f:
  tags = f.read()

known_cards = {
  # Webradio, nrk radio super
  'webradio,http://nrk-mms-live.telenorcdn.net:80/nrk_radio_super_aac_h': b'K\x01\x01\x04D \x07\x04Tn:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)',
  # Spotify, playlist Edvard 2017
  'spop,spotify:user:larsfp:playlist:230fLEiOPRXfmGTEQ4GHu3': b'K\x01\x01\x04D \x07\x04TX:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)',
  # Imagine dragons, popular
  'spop,spotify:artist:53XhwfbYqKCa1cC15pYq2q': b'K\x01\x01\x04D \x07\x04Tl:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)',
  # Spotify, playlist rolig
  'webradio,http://nrk-mms-live.telenorcdn.net:80/nrk_radio_alltid_nyheter_aac_h': b'K\x01\x01\x00D\x00\x07\x04!T\xcao?\x81',
  # Spotify, playlist Oskar 2017
  'spop,spotify:track:5HOpkTTVcmZHnthgyxrIL8': b'K\x01\x01\x00D\x00\x07\x04\xc6\xbcB\xa6L\x80',
  # Webradio, somafm secret agent (blx)
  'webradio,http://ice1.somafm.com/secretagent-128-aac': b'K\x01\x01\x00\x04\x08\x04\x8b\x8bD\x9d',
  # Spotify, playlist drums (ruter)
  'spop,spotify:user:larsfp:playlist:0PRJtN7p3FUMb3aNKsyrRL': b'K\x01\x01\x03D \x07\x04)\x15\n\xc0.\x80\x06uw\x81\x02\x80'
  }

logging.info(str(len(known_cards)) + "tags in store. Ready to read.")
while True:
    card_data = pn532.read_mifare().get_data()
    print('Card data: %s' % str(card_data))
    
    logging.info('Stop any music currently playing')
    call(['/usr/local/bin/volumio', 'clear', '>&', '/dev/null'])
    call(['/usr/bin/mpc', '-q', 'stop']) # This shouldn't be necessary, but...

    # Loop list of tags in search for the one scanned
    for name, nfcid in known_cards.items():
        if card_data == nfcid: # Found!
            # Play audio feedback (file needs to be in local music archive
            call(['/usr/local/bin/node', '/volumio/app/plugins/system_controller/volumio_command_line_client/commands/addplay.js', 'mpd', 'mnt/INTERNAL/thankyouk.mp3'])
            time.sleep(0.5)

            type, url = name.split(',')
            logging.info(type + ' ' + url)

            # Play selected source
            call(['/usr/local/bin/node', '/volumio/app/plugins/system_controller/volumio_command_line_client/commands/addplay.js', type, url])
            break # Stop searching
    time.sleep(5) # Keep same card from being read again

