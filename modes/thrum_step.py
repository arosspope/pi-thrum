"""
Circuit setup (Tested on Raspberry Pi3 Model B+):
    GPIO4  ___/ ___ GND		- Button 0
    GPIO18 ___/ ___ GND     - Button 1
    GPIO17 ___/ ___ GND     - Button 2
    GPIO27 ___/ ___ GND     - Button 3
    
    GPIO22 ___/ ___ GND     - Button 4
    GPIO23 ___/ ___ GND     - Button 5
    GPIO24 ___/ ___ GND     - Button 6
    GPIO25 ___/ ___ GND     - Button 7
    
    GPIO5  ___/ ___ GND     - Button 8
    GPIO6  ___/ ___ GND     - Button 9
    GPIO12 ___/ ___ GND     - Button 10
    GPIO13 ___/ ___ GND     - Button 11
    
    GPIO19 ___/ ___ GND		- Play (Button)
    GPIO16 ___/ ___ GND		- REC (Button)
    
    GPIO26 -->|-[330R]- GND - LED
"""
import RPi.GPIO as GPIO
import pygame

class StepPlay:
    """Defines functionality for the step sequencer"""
    # Map the GPIO pins to each button
    # Note:
    #	* Buttons 0 - 5, play sound AND are used as part of the step seq
    #	* Buttons 6 - 11, are for the step seq only
    __soundBNTs = [ 4, 18, 17, 27, 22, 23 ]
    __stepBNTs 	= [ 24, 25, 5, 6, 12, 13 ]
    __playBNT	= 19
    __recBNT 	= 16
    __LED		= 26

    # Samples for Live play
    __samples 	= []

    # Callbacks for each button
    __soundCBs	= []
    __stepCBS	= []
    
    def __prtVerb(self, mesg):
        if self.__verbose:
            print(mesg)
    
    def __GPIOInit(self):
        # Set mode PIN numbering to BCM, and define GPIO pin functions
        GPIO.setmode(GPIO.BCM)
		
		# Func for sound buttons
        for button in self.__soundBNTs:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Func for step buttons
        for button in self.__stepBNTs:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
        # Func for play & rec buttons
        GPIO.setup(self.__playBNT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__recBNT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		# Func for LED output
        GPIO.setup(self.__LED, GPIO.OUT)
		
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

    def __soundCB(self, channel, sound):
        self.__prtVerb("Channel {0} pressed".format(channel))
        sound.play()
        # TODO: implement
            
    def __stepCB(self, channel):
        self.__prtVerb("Channel {0} pressed".format(channel))
		# TODO: implement
    
    def __playCB(self, channel):
        self.__prtVerb("Channel {0} pressed".format(channel))
		# TODO: implement
        
    def __recCB(self, channel):
        self.__prtVerb("Channel {0} pressed".format(channel))
        
        if GPIO.input(self.__LED):
            GPIO.output(self.__LED, GPIO.LOW)
        else:
            GPIO.output(self.__LED, GPIO.HIGH)

    def runStepMode(self):
        # This method simply defines the functionality upon button press
        # (defining the callbacks upon event detection)
        for i in range(6):
            button = self.__soundBNTs[i]
            sample = self.__samples[i]
            
            GPIO.add_event_detect(button, GPIO.RISING, callback=lambda x, 
                                  y=sample: self.__soundCB(x, y),
								  bouncetime=200)
                                  
        for button in self.__stepBNTs:
            GPIO.add_event_detect(button, GPIO.RISING, callback=lambda x:
                                  self.__stepCB(x), bouncetime=200)
                                  
        GPIO.add_event_detect(self.__playBNT, GPIO.RISING,
                              callback=lambda x:self.__playCB(x), 
                              bouncetime=200)
                              
        GPIO.add_event_detect(self.__recBNT, GPIO.RISING,
                              callback=lambda x:self.__recCB(x),
                              bouncetime=200)					 
        
        
    def stopStepMode(self):
        # Cleanup function: Destroys pygame objects and removes button 
        # callbacks
        pygame.quit()
        #for button in self.__buttons:
        #    GPIO.remove_event_detect(button)
