#MicroPython TCA9554 8-Bit I2C I/O Expander with Interrupt
#By Dobodu
#Free Usage
#
# exemple
#
#TFT_TE = tca9554.TCA9554(i2c, pin=0, io=1)
#   TFT_TE is an INPUT reading TCA9554 Pin 0
#
#TFT_TE.value(1) will set TCA9554 pin 0 to HIGH

#TFT_CDE = tca9554.TCA9554(i2c, pin=1, io=0)
#   TFT_CDE is an OUTPUT writing TCA9554 Pin 1
#
#TFT_TE.value() will reas TCA9554 Pin 1 value
#
#IRQ not handled for now...


LIBNAME = "TCA9554"

from  machine  import I2C

#TCA9554 REGITER

TCA9554_ADDR = (0x20, 0x27) #In real Adress can be 0x20 to 0x27 depending A2-A1-A0 voltage
TCA9554_IN  = const(0x00) #Input register
TCA9554_OUT = const(0x01) #Output register
TCA9554_POL = const(0x02) #Polarity inversion register (1=data inverted)
TCA9554_CONF = const(0x03) #Config register (0=output, 1=input)

class TCA9554:
  
    def __init__(self, i2c, pin, address=None, io=0, pol=0, debug=False):
        
        if (pin < 0) and (pin >7) :
            raise OSError('Wrong pin number (0..7)')
        
        self._i2c = i2c
        self._pin = pin
        self._io = io
        self._pol = pol
        self._buff = bytearray(1)
        self._debug = debug
        
        #Test for IRQ sim
        self.IRQ_FALLING = 2
        self.IRQ_RISING = 1
        
        if address == None :
            devices = set(self._i2c.scan())
            mpus = devices.intersection(set(TCA9554_ADDR))
            nb_of_mpus = len(mpus)
            
            if nb_of_mpus == 0:
                self._ready = False
                self._dbg("No device detected")
                return   
            elif nb_of_mpus == 1:
                self._address = mpus.pop()
                self._dbg("Device found at",hex(self._address))
            else:
                raise ValueError("Two devices detected: must specify a device address")
        else :   
            self._address = address   

        #Set input or output
        self.set_io(self._io)
        #Set pin polarity
        self.set_pol(self._pol)
   
   
    #SET PIN AS INPUT(1) or OUTPUT(0)
    def set_io(self, io_val):
        _conf = self._i2c.readfrom_mem(self._address , TCA9554_CONF, 1)[0]
        if io_val : #if input
            _conf |= (1<<self._pin)
        else :
            _conf &= ~(1<<self._pin)
        self._buff[0] = _conf
        self._i2c.writeto_mem(self._address, TCA9554_CONF , self._buff)
    
    #SET PIN POLARITY 
    def set_pol(self, io_inv_pol):
        _pola = self._i2c.readfrom_mem(self._address , TCA9554_POL, 1)[0]
        if io_inv_pol : #if inverted polarity
            _pola |= (1<<self._pin)
        else :
            _pola &= ~(1<<self._pin)
        self._buff[0] = _pola
        self._i2c.writeto_mem(self._address, TCA9554_POL , self._buff)   
    
    #SET PIN VALUE
    def set(self, value):
        _regvalue = self._i2c.readfrom_mem(self._address, TCA9554_OUT, 1)[0]
        if value == 1 :
            _regvalue |= (1<<self._pin)
        elif value == 0 :
            _regvalue &= ~(1<<self._pin)
        self._buff[0] = _regvalue
        self._i2c.writeto_mem(self._address, TCA9554_OUT, self._buff)

    #READ PIN VALUE
    def get(self):
        _regvalue = self._i2c.readfrom_mem(self._address, TCA9554_IN, 1)[0]
        _regvalue = (_regvalue >> self._pin) & 1
        self._dbg("Pin", self._pin, "Value",_regvalue)
        return (_regvalue)
    
    #Value to act as a normal GPIO PIN
    def value(self, value=None):
        if value==None :
            return(self.get())
        else :
            self.set(value)
            
    #Irq to act like a normal irq handler
    def irq(self, trigger, handler):
        self._dbg("IRQ not handled for now")
    
    #DEBUG
    def _dbg(self, *args, **kwargs):
        if self._debug:
            print("DBG:\t",LIBNAME,":\t", *args, **kwargs)
