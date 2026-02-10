from picozero import pico_led
from machine import Pin, PWM
import rp2
import sys
import aioble
import bluetooth
import uasyncio as asyncio
import time

UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
UART_RX_UUID      = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
UART_TX_UUID      = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

uart_service = aioble.Service(UART_SERVICE_UUID)
uart_rx = aioble.Characteristic(
    uart_service,
    UART_RX_UUID,
    write=True,
    write_no_response=True,
)
uart_tx = aioble.Characteristic(
    uart_service,
    UART_TX_UUID,
    notify=True,
)

aioble.register_services(uart_service)


motor_enable = PWM(Pin(4))
motor_enable.freq(1000)

motor_dir1 = Pin(2, Pin.OUT)
motor_dir2 = Pin(3, Pin.OUT)

def forward(speed=40000):
    motor_dir1.on()
    motor_dir2.off()
    motor_enable.duty_u16(speed)
    
def reverse(speed=40000):
    motor_dir1.off()
    motor_dir2.on()
    motor_enable.duty_u16(speed)
    
def stop():
    motor_enable.duty_u16(0)


async def handle_uart():
    print("Waiting for BLE connection...")

    async with await aioble.advertise(
        interval_us=250_000,
        name="Blendermobile",
        services=[UART_SERVICE_UUID],
    ) as connection:
        print("Connected:", connection.device)

        while connection.is_connected():
            packet = await uart_rx.written()
            #msg = data.decode()
            #print("RX:", msg)
            print("RAW:", packet)

async def main():
    while True:
        try:
            await handle_uart()
        except Exception as e:
            print("BLE error:", e)

asyncio.run(main())


#while True:
#    if rp2.bootsel_button() == 1:
#        sys.exit()        
#    stop()
    
