#!/usr/bin/env python
import binascii
import time
import mraa

class OPT3001(object):
    i2C = None
    def __init__(self):
        self.i2C = mraa.I2c(1);
        self.i2C.address(0x47);
        self.i2C.write(bytearray(b'\x01\xc4\x10')); #write config
        #0x01 - config adr
        #0xc4 - full scale, 100ms conv. time, contiue mesuring
        #0x10 - latch

    def getLux(self):
        self.i2C.write(bytearray(b'\x00')); #read light value 16bit
        d = self.i2C.read(2);
        if not d: return 0 #Failed reading - happens sometimes
        lraw = int(binascii.hexlify(d),16);
        res = lraw & 0x0FFF; #extracted fractional result mantissa 11:0
        exp = (lraw>>12) & 0x000F; #extracted exponent 3:0
        return 0.01*(2**(int(exp)))*int(res); #lux

def main():
    opt3001 = OPT3001()
    for x in xrange(10):
        print "Lux reading: %s" % (opt3001.getLux(), )
        time.sleep(3)

if __name__ == "__main__":
    main()