This library handle TCA9554 GPIO extender with Micropython

You need to setup first the I2C bus and then declare 

TFT_TE = tca9554.TCA9554(i2c, pin=0, io=1)
   TFT_TE is an INPUT reading TCA9554 Pin 0
TFT_TE.value(1) will set TCA9554 pin 0 to HIGH

TFT_CDE = tca9554.TCA9554(i2c, pin=1, io=0)
   TFT_CDE is an OUTPUT writing TCA9554 Pin 1
#TFT_TE.value() will reas TCA9554 Pin 1 value

IRQ not handled for now...
