import smbus

BUSNUM = 1
ADDRESS = 0x20


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
