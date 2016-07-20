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
import time

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
    
    def __init__(self, verbose=False):
        self.__GPIOInit()
        self.__soundInit()
        self.__verbose = verbose
        self.__playSteps = False
    
    def runStepMode(self):
        # Initialise callbacks - which will start multi-threading
        self.__initCBs()
        self.play() 
    
    def play(self):
        p1 = [ False, True, False, False, False, False ]
        p2 = [ False, False, False, False, False, False ]
        grid = [ p1, p2, p1, p1, p2, p2, p1, p2, p1, p2, p1, p2 ]
        
        step_time = 0.1 #5000.0 / 120 #( / bpm)
        step = -1
        next_time = time.time()
        
        
        while True:
            if self.__playSteps:
                if time.time() >= next_time:
                    step = (step + 1) % 12
                    self.playpattern(grid, step)
                    next_time += step_time
        
    def playpattern(self, grid, step):
        pattern = grid[step]
        
        for i in range(6):
            if pattern[i]:
                self.__samples[i].play()
        
    def stopStepMode(self):
        # Cleanup function: Destroys pygame objects and de-init GPIO pins
        pygame.quit()
        GPIO.output(self.__LED, GPIO.LOW)
        GPIO.cleanup()
    
    def __GPIOInit(self):
        # Set mode PIN numbering to BCM, and define GPIO pin functions
        GPIO.setmode(GPIO.BCM)
        
        # Setup Function for input Pins
        inputBNTs = (self.__soundBNTs + self.__stepBNTs)
        inputBNTs.append(self.__playBNT)
        inputBNTs.append(self.__recBNT)
		
        for b in inputBNTs:
            GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		# Func for ouput Pins
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

    def __initCBs(self):
        # Initialise the Callback functions for each Input IO pin
        # Sound Button Callbacks:
        for i in range(6):
            bnt = self.__soundBNTs[i]
            smp = self.__samples[i]
            GPIO.add_event_detect(bnt, GPIO.RISING, callback=lambda x,y=smp:
                                  self.__soundCB(x, y), bouncetime=200)
                                  
        # Step Button Callbacks:
        for bnt in self.__stepBNTs:
            GPIO.add_event_detect(bnt, GPIO.RISING, callback=lambda x:
                                  self.__stepCB(x), bouncetime=200)
                                  
        # Play Button Callback:
        GPIO.add_event_detect(self.__playBNT, GPIO.RISING, callback=lambda x:
                              self.__playCB(x), bouncetime=200)
                              
        # Record Button Callback:
        GPIO.add_event_detect(self.__recBNT, GPIO.RISING, callback=lambda x:
                              self.__recCB(x), bouncetime=200)
    
    def __soundCB(self, channel, sound):
        self.__prtVerb("Sound bnt IO-{0}".format(channel))
        sound.play()
        # TODO: implement
            
    def __stepCB(self, channel):
        self.__prtVerb("Step bnt IO-{0}".format(channel))
		# TODO: implement
    
    def __playCB(self, channel):
        self.__prtVerb("Play bnt IO-{0}".format(channel))
        self.__playSteps = not self.__playSteps # Toggle playing
		# TODO: implement
        
    def __recCB(self, channel):
        self.__prtVerb("Record bnt IO-{0}".format(channel))
        GPIO.output(self.__LED, not GPIO.input(self.__LED)) # Toggle LED
       
    def __prtVerb(self, mesg):
        if self.__verbose:
            print(mesg)
