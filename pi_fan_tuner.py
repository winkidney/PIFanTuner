#!/usr/bin/python2.7
# coding:utf-8
import logging
from time import sleep

from RPi import GPIO

from cmdtree import INT
from cmdtree import command
from cmdtree import entry
from cmdtree import group
from cmdtree import option


GPIO_CONTROL_PORT = 12
FAN_ON_TEMPERATURE = 45


def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", 'r') as f:
        temp = float(f.read()) / 1000
    return temp


def init():
    GPIO.setmode(GPIO.BOARD)


def set_debug():
    logging.basicConfig(level=logging.DEBUG)


@group(name="port", help="Turn a pin port to `IN` or `OUT`")
def port_manage():
    pass


@option("port", help="Port on GPIO Physical Port", type=INT, default=GPIO_CONTROL_PORT)
@port_manage.command("turn-out", help="Turn a port into `OUT` mode")
def turn_port_out(port):
    GPIO.setup(port, GPIO.OUT)
    GPIO.output(port, 1)
    return True


@option("port", help="Port number of GPIO Physical Port", type=INT, default=GPIO_CONTROL_PORT)
@port_manage.command("turn-in", help="Turn a port into `IN` mode")
def turn_port_in(port):
    GPIO.setup(port, GPIO.IN)
    return False


@option("loop", help="loop until user interrupting execution.", is_flag=True)
@command("cpu-show")
def show_cpu_temperature(loop):

    def show_temperature():
        print("Cpu Temperature is: {0}".format(get_cpu_temp()))

    if loop:
        while True:
            show_temperature()
            sleep(1)
    else:
        show_temperature()


@option(
    "on-t",
    help="Temperature which triggers the fan on.",
    type=INT,
    default=FAN_ON_TEMPERATURE,
)
@option(
    "port",
    help="Port number of GPIO Physical Port",
    type=INT,
    default=GPIO_CONTROL_PORT,
)
@group(name="fan", help="Auto tune the cpu fan in `simple` or `auto` mode.")
def auto_fan():
    pass


@auto_fan.command("on", help="Turn one the fan.")
def on_fan(port, **kwargs):
    turn_port_out(port)


@auto_fan.command("off", help="Turn off the fan.")
def off_fan(port, **kwargs):
    turn_port_in(port)


@option("debug", is_flag=True, default=False)
@auto_fan.command("simple", help="Simply turn on or off the fan in given temperature range.")
def simple_on_of(debug, port, on_t):
    if debug:
        set_debug()

    fan_on = turn_port_in(port)

    try:
        while True:
            temperature = get_cpu_temp()
            if temperature >= on_t:
                if not fan_on:
                    logging.debug("Temperature {0} CPU fan on.".format(temperature))
                    fan_on = turn_port_out(port)
            else:
                if fan_on:
                    logging.debug("Temperature {0} CPU fan off.".format(temperature))
                    fan_on = turn_port_in(port)
            sleep(10)
    except Exception:
        logging.exception("Error occurs while tune fan status:")
        GPIO.cleanup()


def main():
    init()
    entry()


if __name__ == '__main__':
    main()
