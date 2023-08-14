# Adafruit Itsybitsy nRF52840

![](<../../.gitbook/assets/image (3).png>)

Either use the drag and drop UF2 method or more steps involved - Arduino uploading method.\
\
For the UF2 method

* Download the UF2 file for the itsybitsy _board in the current release_
* Double click that reset button. You will then get a USB drive on your computer. Drag and drop the UF2 file to the root of that drive.
* It SHOULD disconnect from your pC if successful – but as I say the loghts should change colour to Green
* More details see the steps [here](https://learn.adafruit.com/adafruit-metro-m0-express/uf2-bootloader-details#entering-bootloader-mode-2929745)

Or the Arduino uploading method.

* Check the setup of your [Arduino IDE](https://learn.adafruit.com/bluefruit-nrf52-feather-learning-guide/arduino-bsp-setup) (remember we're using the nRF52840 board!)
* Upload the [sketch](../../../../arduino/arduino\_nRF52840/arduino\_nRF52840.ino) to your feather.
* Run the server side code
* Done!
