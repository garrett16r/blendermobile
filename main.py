from picozero import pico_led
from machine import Pin, PWM
import rp2
import sys
import aioble
import bluetooth
import uasyncio as asyncio
import time

pico_led.on()

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


while True:
    if rp2.bootsel_button() == 1:
        sys.exit()        
    stop()
    