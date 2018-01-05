#!/usr/bin/env python3

# Inspired by https://volumio.org/forum/turn-led-when-volumio-ready-t5746.html

import subprocess, sys
from time import sleep
from gpiozero import PWMLED

pingserver = 'web.larsfp.clh.no'
led = PWMLED(18)

def log(message=''):
    print (message)
    sys.stdout.flush()

def setup():
    led.blink() # Notify startup

def checkStatus():
    p = subprocess.Popen(
        '/usr/local/bin/volumio status',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    out, err = p.communicate()

    #print (status)
    #print(err)

    if 0 != p.returncode:
        led.blink()
        log("Status: error " + err.decode())
    elif 'play' in out.decode():
        #log("Status: playing")
        led.on()
    else:
        led.pulse()

    sleep(2)

def checkNetwork():
    #'sudo /bin/ping -c2 -W 5 ' + pingserver
    p = subprocess.Popen(
        '/usr/bin/curl --silent ' + pingserver + ' > /dev/null '
    )

    if 0 != p.returncode:
        led.blink()
        log("Status: network error.")
        sleep(10)
    else:
        log("Status: network OK.")

def destroy():
    led.off()


if __name__ == '__main__':       ## Program start from here
    setup()

    try:
        count=0
        while True:
            checkStatus()
            count+=1
            if count%60:
              checkNetwork()

    except KeyboardInterrupt:      ## When 'CTRL+C' is pressed.
        destroy()
