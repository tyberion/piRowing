import smbus

BUSNUM = 1
ADDRESS = 0x20

bus = smbus.SMBus(BUSNUM)

def write_pins(bus, address, bank, pins, value=False):
    value_int = value * 2 - 1

    output_bank = bus.read_byte_data(address, bank)

    if not (type(pins) == list):
        pins = [pins]

    if value:
        set_outputs = 0
    else:
        set_outputs = 0xff

    for pin in pins:
        set_outputs += (2**pin) * value_int

    if value:
        output_bank |= set_outputs
    else:
        output_bank &= set_outputs

    bus.write_byte_data(address, bank, output_bank)

def config_pins(bus, address, bank, pins, output=False):
    CONFB1A = 0x00
    CONFB2A = 0x01

    if bank == 'A':
        write_pins(bus, address, CONFB1A, pins, value=output)
    else:
        write_pins(bus, address, CONFB2A, pins, value=output)

def set_pins(bus, address, bank, pins, value):
    B1A = 0x12
    B2A = 0x13

    if not (type(pins) == list):
        pins = [pins]

    if bank == 'A':
        write_pins(bus, address, B1A, pins, value=value)
    else:
        write_pins(bus, address, B2A, pins, value=value)

def get_pins(bus, address, bank):
    B1A = 0x12
    B2A = 0x13

    if bank == 'A':
        return bus.read_byte_data(address, B1A)
    else:
        return bus.read_byte_data(address, B2A)

def get_pin_values(value, pins):
    if not (type(pins) == list):
        pins = [pins]
    return [(value >> pin) % 2 for pin in pins]

config_pins(bus, ADDRESS, 'A', [0], False)

set_pins(bus, ADDRESS, 'A', [0], True)
output_bank = get_pins(bus, ADDRESS, 'A')
get_pin_values(output_bank,2)[0]

import time
import pickle

a_prev = 0
t0 = time.time()
N = 0
T = []
while True:
    output_bank = get_pins(bus, ADDRESS, 'A')
    a = get_pin_values(output_bank,[0,1,2,3,4,5,6,7])
    #print a[7]

    if a[7]-a_prev == 1:
        t = time.time()
        T.append(t-t0)
        t0 = t
        print((N,T[N]))
        N+=1
        if N % 500 == 0:
            pickle.dump(T, open('times-%d.pcl' % N, 'wb'))
            print('dumped')
    a_prev = a[7]
    time.sleep(0.002)
