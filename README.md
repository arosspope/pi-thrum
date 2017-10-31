# pi-thrum :notes:

Using a raspberry pi and breadboard, pi-thrum is a simple 12-step sequencer with retro 8-bit drum samples.

## Setup
### Required software packages
The project has been tested and written for python 3 on a debian based system. In addition to python 3,
two extra python packages are required for the game to run: [pygame](https://pypi.python.org/pypi/Pygame) (v1.9.2)
and [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) (v0.6.2). Assuming you have pip, you could install the required packages like so:
```bash
$ pip install Pygame==1.9.2     //For playing sound bytes on the pi
$ pip install RPi.GPIO==0.6.2   //For interacting with the GPIO pins on the pi
```
### Hardware

In addition to installing software, this project will require you to construct a simple circuit. Please note, that this project has only been tested on the Pi 3 Model B. However, I am sure it will still work on older versions of the pi with similar GPIO pin layouts (you may have to change some of the source code).
Using the following parts list:

+ Breadboard
+ Tactile push buttons (x14)
+ 330 Ohm resistor
+ Colour LED
+ Jumper leads

Construct the circuit on the breadboard as per the rudimentary schematic ...

![schematic](https://i.imgur.com/aAv4dUF.png)

## Operation
```
$ python3 pi_thrum.py
Welcome to pi-thrum! An interactive 12-step sequencer for drum samples!
To stop program press CTRL+C
...
```
After the user enters the initial command, control is transferred to the various buttons
within the circuit to manipulate the step sequencer and samples.

When record mode is inactive (as indicated by the LED), buttons 0 - 5 will play the various
drum samples assigned to them.
When record mode is active, pressing any of the buttons 0 - 11 will assign the mostly recently
played sound to the corresponding step. Running and stopping the sequence is controlled via the
play button. To halt the entire program, the user must supply the keyboard interrupt CTRL+C.

An simple demo of the project can be found here:

[![pi-thrum-demo](http://img.youtube.com/vi/QzZMy-4yDzU/0.jpg)](http://www.youtube.com/watch?v=QzZMy-4yDzU)
> Check out my "sick beats"
