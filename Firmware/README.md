
# micropython_compiler

cd ./micropython_compiler/ports/esp32
source ../../../esp-idf/export.sh
make BOARD=LILYGO_TTGO_LORA32


esptool.py --chip esp32s2 --port /dev/ttyACM0 erase_flash
esptool.py --chip esp32s2 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x1000 esp32_s2.bin
