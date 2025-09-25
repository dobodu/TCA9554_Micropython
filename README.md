# This library handle TCA9554 GPIO extender with Micropython
## You need to setup first the I2C 

Configuring TFT_TE as an INPUT reading TCA9554 Pin 0

> TFT_TE = tca9554.TCA9554(i2c, pin=0, io=1)
> 
> TFT_TE.value(1) will set TCA9554 pin 0 to HIGH

Configuring TFT_CDE as an OUTPUT writing TCA9554 Pin 1

> TFT_CDE = tca9554.TCA9554(i2c, pin=1, io=0)
>
> TFT_TE.value() will read TCA9554 Pin 1 value

IRQ not handled for now...
