# Pi-Thrum
Pi-Thrum is a program for the Raspberry Pi that uses the on-board GPIO pins 
to create a basic 12-step sequencer with retro 8-bit drum samples.
A small demo of the program running can be found here:

[![pi-thrum-demo](http://img.youtube.com/vi/QzZMy-4yDzU/0.jpg)](http://www.youtube.com/watch?v=QzZMy-4yDzU)

## Hardware Requirements
+ Breadboard
+ 14 x Tactile Push buttons
+ 330 Ohm resistor
+ Red LED
+ Circuit Leads

Using the above components, construct the circuit as displayed in the [schematic](pi-thrum-schem.jpg). 
Please note, that the program/circuit has only been tested on the Pi 3 Model B - although, 
I'm sure it will still work on older versions of the pi with similar GPIO pin layouts.

## Software Requirements
Using python 3, the following extra libraries are required:
+ Pygame 1.9.2
+ RPi.GPIO 0.6.2

## Running the program
```
user@raspberrypi:[pi-thrum]$ python3 pi_thrum.py
Welcome to pi-thrum! An interactive 12-step sequencer for drum samples!
To stop program press CTRL+C

^C
Thanks for Playing!
user@raspberrypi:[pi-thrum]$
```
After the user enters the initial command, control is transferred to the various buttons 
within the circuit to manipulate the step sequencer and samples.

When record mode is inactive (as indicated by the LED), buttons 0 - 5 will play the various 
drum samples assigned to them.
When record mode is active, pressing any of the buttons 0 - 11 will assign the mostly recently
played sound to the corresponding step. Running and stopping the sequence is controlled via the 
play button. 

To halt the entire program, the user must supply the keyboard interrupt CTRL+C.
