
# micropython_compiler

cd ./micropython_compiler/ports/esp32
source ../../../esp-idf/export.sh
make BOARD=LILYGO_TTGO_LORA32


instruction:
- create/modify boot.py and main.py
    Cyberpot_MPY/micropython_compiler/ports/esp32/modules/_boot.py
- add new mpy lib
    Cyberpot_MPY/micropython_compiler/ports/esp32/boards/POT_V1.3/modules


log:
[1066/1306] cd /home/devpc/junk/Cyberpot_MPY/micropython_compiler/por...rpot_MPY/micropython_compiler/ports/esp32/boards/POT_V1.3/manifest.py
MPY apa106.py
MPY flashbdev.py
MPY _boot.py
MPY espnow.py
MPY inisetup.py
MPY uasyncio/__init__.py
MPY uasyncio/core.py
MPY uasyncio/event.py
MPY uasyncio/funcs.py
MPY uasyncio/lock.py
MPY uasyncio/stream.py
MPY urequests.py
MPY mip/__init__.py
MPY ntptime.py
MPY webrepl.py
MPY webrepl_setup.py
MPY dht.py
MPY onewire.py
MPY ds18x20.py
MPY neopixel.py
MPY umqtt/robust.py
MPY umqtt/simple.py
MPY upysh.py
MPY wifismart.py
MPY s2mini.py
MPY sht3x.py

