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
    # Map the GPIO pins to each button
    # Note:
    #	* Buttons 0 - 5, play sound AND are used as part of the step seq
    #	* Buttons 6 - 11, are for the step seq only
    __soundBNTs     = [ 4, 18, 17, 27, 22, 23 ]
    __stepBNTs 	    = [ 24, 25, 5, 6, 12, 13 ]
    __stepChannels  = [ 4, 18, 17, 27, 22, 23, 24, 25, 5, 6, 12, 13 ]
    __playBNT	= 19 
    __recBNT 	= 16
    __LED		= 26
    
    
    def __init__(self, verbose=False, bpm=120000.0):
        """
        Initialise class variables, GPIO, and sound
        
        @param verbose - True for verbose print statements
        @param bpm - Beats per minute
        """
        # Initialise class variables
        self.__verbose = verbose
        self.__playSteps = False
        self.__recording = False
        self.__bpm = bpm
        self.__stepTime = 15000.0 / bpm
        self.__stepPatterns = []
        self.__samples 	= []
        self.__currSamp = None
        
        # Initialise pattern for each step (i.e. what sounds will play)
        for i in range(12):
            self.__stepPatterns.append([None])
            
        # Initialise GPIO and sound samples
        self.__GPIOInit()
        self.__soundInit()
    
    def run(self):
        """
        Runs the main program (step-sequencer) when invoked
        """
        # Initialise callbacks - which will start multi-threading
        self.__initCBs()
        
        step = -1
        next_time = time.time()
        
        # Begin main loop - will halt when user supplies CTRL+C
        while True:
            if self.__playSteps:
                if time.time() >= next_time:
                    step = (step + 1) % 12
                    self.__playPattern(self.__stepPatterns[step])
                    next_time += self.__stepTime
        
    def cleanup(self):
        """
        Cleanup method which should be invoked before program exit
        """
        # Destroy pygame objects and de-init GPIO pins
        pygame.quit()
        GPIO.output(self.__LED, GPIO.LOW)
        GPIO.cleanup()    
    
    def __playPattern(self, pattern):
        """
        Plays a collection of sounds called a 'pattern'
        
        @param pattern - The collection of sounds
        """
        for sound in pattern:
            if sound != None: sound.play()

    def __GPIOInit(self):
        """
        Initialises the GPIO pins for the pi
        (tested on the Pi3 Model B+)
        """
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
        """
        Initialises the pygame module and loads the sound samples
        """
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
        """
        Initialises the Callback functions for each Input IO pin
        """
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
        """
        Callback for sound button (a sound button also doubles as a step
        button)
        
        @param channel - The GPIO PIN that the signal was sent on
        @param sound - The sound to play
        """
        step = self.__stepChannels.index(channel)
        self.__prtVerb("Sound bnt IO-{0}, Step={1}".format(channel, step))
        
        if self.__recording:
            self.__toggleStepSample(step, self.__currSamp)
        else:
            sound.play()
            self.__currSamp = sound
            
    def __stepCB(self, channel):
        """
        Callback for step button
        
        @param channel - The GPIO PIN that the signal was sent on
        """
        step  = self.__stepChannels.index(channel)
        self.__prtVerb("Step bnt IO-{0}, Step={1}".format(channel, step))
        
        if self.__recording:
            self.__toggleStepSample(step, self.__currSamp)
                
    def __playCB(self, channel):
        """
        Callback for play button
        
        @param channel - The GPIO PIN that the signal was sent on
        """
        self.__prtVerb("Play bnt IO-{0}".format(channel))
        self.__playSteps = not self.__playSteps # Toggle playing
        
    def __recCB(self, channel):
        """
        Callback for record button
        
        @param channel - The GPIO PIN that the signal was sent on
        """
        self.__prtVerb("Record bnt IO-{0}".format(channel))
        GPIO.output(self.__LED, not GPIO.input(self.__LED)) # Toggle LED
        self.__recording = not self.__recording # Toggle recording
       
    def __toggleStepSample(self, step, sample):
        """
        Will either add or remove a sound sample to/from a step 'pattern'
        
        @param step   - The step to check
        @param sample - The sample to add or remove
        """
        # Determine if the currently selected sample is 'on' the step
        # if so - remove it, if not - add it
        if sample in self.__stepPatterns[step]:
            self.__stepPatterns[step].remove(sample)
        else:
            self.__stepPatterns[step].append(sample)
    
    def __prtVerb(self, mesg):
        """
        Verbose message print method
        
        @param mesg - The message to print
        """
        if self.__verbose:
            print(mesg)
