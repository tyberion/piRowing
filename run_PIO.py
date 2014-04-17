from PIO import *

def main():
    bus = smbus.SMBus(BUSNUM)

    config_pins(bus, ADDRESS, 'A', [0], False)

    set_pins(bus, ADDRESS, 'A', [0], True)
    #output_bank = get_pins(bus, ADDRESS, 'A')
    #get_pin_values(output_bank,2)[0]

    import time
    import pickle
    from datetime import date

    now = date.today()
    nowString = '%d%02d%02d' % (now.year, now.month, now.day)

    a_prev = 0
    N = 0
    dT = []
    t0 = time.time()
    while True:
        output_bank = get_pins(bus, ADDRESS, 'A')
        a = get_pin_values(output_bank,7)[0]
        da = a-a_prev
        a_prev = a
        #print a[7]

        if da == 1:
            t = time.time()
            dt = t-t0
            t0 = t
            dT.append(dt)
            N+=1
            if N % 100 == 0:
                #print((N,T[N]))
                pickle.dump(dT, open('%s-times.pcl' % nowString, 'wb'))
                print('dumped')
        #time.sleep(0.001)

if __name__ == '__main__':
    main()
