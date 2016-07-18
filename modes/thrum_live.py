"""
Circuit setup (Tested on Raspberry Pi3 Model B+):
    GPIO4  ___/ ___ GND      - Button 0
    GPIO18 ___/ ___ GND      - Button 1
    GPIO17 ___/ ___ GND      - Button 2
    GPIO27 ___/ ___ GND      - Button 3
    GPIO22 ___/ ___ GND      - Button 4
    GPIO23 ___/ ___ GND      - Button 5
"""
import threading
import RPi.GPIO as GPIO
import pygame

class LivePlay:
    """Defines functionality for 'live' push button sound playing"""
    # Map the GPIO pins to each button
    __buttons = [ 4, 18, 17, 27, 22, 23 ]

    # Samples for Live play
    __samples = []

    # Callbacks for each button
    __buttonCBs = []
    
    def __prtVerb(self, mesg):
        if self.__verbose:
            print(mesg)
    
    def __GPIOInit(self):
        # Set mode PIN numbering to BCM, and define GPIO pin functions
        GPIO.setmode(GPIO.BCM)

        for button in self.__buttons:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __soundInit(self):
        # Initialise pygame module
        pygame.mixer.pre_init(44100, -16, 12, 512) # TODO: Tweak values?
        pygame.init()
        
        # Load sounds from samples folder
        self.__samples.append(pygame.mixer.Sound('samples/606SNAR.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/CR8KBASS.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/CR8KCLAP.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/CR8KHITM.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/CR8KSNAR.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/snare.wav'))

        for sample in self.__samples:
            sample.set_volume(.95)

    def __init__(self, verbose=False):
        self.__GPIOInit()
        self.__soundInit()
        self.__verbose = verbose

    def __buttonCallBack(self, channel, sound):
            self.__prtVerb("Channel {0} pressed".format(channel))
            sound.play()

    def runLiveMode(self):
        # This method simply defines the functionality upon button press
        # (defining the callbacks upon event detection)
        for i in range(6):
            button = self.__buttons[i]
            sample = self.__samples[i]
            
            GPIO.add_event_detect(button, GPIO.RISING, callback=lambda x, 
                                  y=sample: self.__buttonCallBack(x, y),
								  bouncetime=200)
        
    def stopLiveMode(self):
        # Cleanup function: Destroys pygame objects and removes button 
        # callbacks
        pygame.quit()
        for button in self.__buttons:
            GPIO.remove_event_detect(button)
