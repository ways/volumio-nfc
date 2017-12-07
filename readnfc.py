#!/usr/bin/env python3

# https://github.com/HubCityLabs/py532lib
# sudo apt install libnfc5 libnfc-bin libnfc-examples python3
# /etc/nfc/libnfc.conf must contain:
# device.name = "PN532 over I2C"
# device.connstring = "pn532_i2c:/dev/i2c-1"
# mo/sda/tx -> raspi pyhsical 3
# nss/sclk/rx -> raspi physical 5

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import subprocess
import time

pn532 = Pn532_i2c()
pn532.SAMconfigure()
verbose = True

known_cards = {
  # examples
  # 'spop,spotify:track:2Wf0uMfCpwLO1B2Up3NbXH': b'K\x01\x01\x04D \x07\x04TX:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)',
  # 'webradio,http://nrk-mms-live.telenorcdn.net:80/nrk_radio_super_aac_h': b'K\x01\x01\x04D \x07\x04Tn:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)',
  # 'spop,spotify:user:larsfp:playlist:230fLEiOPRXfmGTEQ4GHu3': b'K\x01\x01\x04D \x07\x04TX:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)',

  'webradio,http://nrk-mms-live.telenorcdn.net:80/nrk_radio_super_aac_h': b'K\x01\x01\x04D \x07\x04Tn:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)',
  'spop,spotify:user:larsfp:playlist:230fLEiOPRXfmGTEQ4GHu3': b'K\x01\x01\x04D \x07\x04TX:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)',
  'webradio,http://ice1.somafm.com/secretagent-128-aac': b'K\x01\x01\x04D \x07\x04Tl:T*\x80\x0cu3\x81\x02\xc1\x051 \x0f\x84)'
  }

while True:
    card_data = pn532.read_mifare().get_data()
    if verbose: print(card_data)
    
    for name, nfcid in known_cards.items():
        if card_data == nfcid:
            type, url = name.split(',')
            print(type + ' ' + url)
            subprocess.call(['volumio', 'clear'])
            subprocess.call(['node', '/volumio/app/plugins/system_controller/volumio_command_line_client/commands/addplay.js', type, url])
    time.sleep(2)

