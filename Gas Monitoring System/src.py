import time
import RPi.GPIO as GPIO
from smbus import SMBus
from blynkapi import Blynk
from time import sleep

BLYNK_AUTH = 'code-of-blynk-account-which-is-used'
BLYNK_HOST = 'blynk.cloud'
BLYNK_PORT = 8080
blynk = Blynk(BLYNK_AUTH, server=BLYNK_HOST, port=BLYNK_PORT)

SENSOR_PIN = 34
BUZZER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

i2c_bus = SMBus(1)
LCD_ADDR = 0x27

def lcd_init():
    i2c_bus.write_byte_data(LCD_ADDR, 0x00, 0x38)
    i2c_bus.write_byte_data(LCD_ADDR, 0x00, 0x39)
    i2c_bus.write_byte_data(LCD_ADDR, 0x00, 0x14)
    i2c_bus.write_byte_data(LCD_ADDR, 0x00, 0x73)
    i2c_bus.write_byte_data(LCD_ADDR, 0x00, 0x56)
    i2c_bus.write_byte_data(LCD_ADDR, 0x00, 0x6C)

def lcd_display(line, msg):
    i2c_bus.write_byte_data(LCD_ADDR, 0x00, 0x80 | line)
    for i in range(len(msg)):
        i2c_bus.write_byte_data(LCD_ADDR, 0x40, ord(msg[i]))

def check_gas_level():
    value = GPIO.input(SENSOR_PIN)

    value = (value * 100)

    if value >= 50:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        lcd_display(0x01, "Warning!")
        blynk.virtual_write(1, 255)
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        lcd_display(0x01, "Normal")
        blynk.virtual_write(1, 0)

# Send the value to Blynk app
    blynk.virtual_write(0, value)
    lcd_display(0x40, f"GAS Level: {value}%")
    print(f"GAS Level: {value}")

# Main loop
def main():
    lcd_init()
    lcd_display(0x01, "System Loading")
    time.sleep(2)

    for _ in range(15):
        lcd_display(0x01, ".")
        time.sleep(0.2)

    lcd_display(0x01, "Ready")

    while True:
        check_gas_level()
        blynk.run()
        time.sleep(0.2)

if __name__ == "__main__":
    main()
