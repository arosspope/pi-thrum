"""
Circuit setup (For Raspberry Pi3 Model B+):
    GPIO4  ___/ ___ GND      - Button 0
    GPIO17 ___/ ___ GND      - Button 1
    GPIO18 ___/ ___ GND      - Button 2
    GPIO22 ___/ ___ GND      - Button 3
    GPIO23 ___/ ___ GND      - Button 4
    GPIO24 ___/ ___ GND      - Button 5
"""
import RPi.GPIO as GPIO
import pygame

class LivePlay:
    """Defines functionality for 'live' push button sound playing"""
    # Map the GPIO pins to each button
    __buttons = [ 4, 17, 18, 22, 23, 24 ]

    # Samples for Live play
    __samples = []

    # Callbacks for each button
    __buttonCBs = []
    
    def __GPIOInit(self):
        GPIO.setmode(GPIO.BCM)

        # Setup GPIO for each button
        for button in self.__buttons:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __soundInit(self):
        # Initialise pygame module
        pygame.mixer.pre_init(44100, -16, 12, 512)
        pygame.init()
        
        self.__samples.append(pygame.mixer.Sound('samples/606SNAR.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/CR8KBASS.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/CR8KCLAP.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/CR8KHITM.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/CR8KSNAR.WAV'))
        self.__samples.append(pygame.mixer.Sound('samples/snare.wav'))

        for sample in self.__samples:
            sample.set_volume(.95)

    def __init__(self):
        self.__GPIOInit()
        self.__soundInit()

    def runLiveMode(self):
        i = 0

        #TODO: Investigate why simple for loop to initilise wont work
        GPIO.add_event_detect(4, GPIO.RISING, callback=lambda x: buttonCallBack(4, self.__samples[0]),
                              bouncetime=200)

        GPIO.add_event_detect(17, GPIO.RISING, callback=lambda x: buttonCallBack(17, self.__samples[1]),
                              bouncetime=200)

        GPIO.add_event_detect(18, GPIO.RISING, callback=lambda x: buttonCallBack(18, self.__samples[2]),
                              bouncetime=200)

        GPIO.add_event_detect(22, GPIO.RISING, callback=lambda x: buttonCallBack(22, self.__samples[3]),
                              bouncetime=200)

        GPIO.add_event_detect(23, GPIO.RISING, callback=lambda x: buttonCallBack(23, self.__samples[4]),
                              bouncetime=200)

        GPIO.add_event_detect(24, GPIO.RISING, callback=lambda x: buttonCallBack(24, self.__samples[5]),
                              bouncetime=200)

        """
        for button in self.__buttons:
            GPIO.add_event_detect(button, GPIO.RISING,
                                  callback=lambda x: buttonCallBack(button, self.__samples[i]),
                                  bouncetime=200)
            print(button)
            i += 1
        """
        
    def stopLiveMode(self):
        pygame.quit()

        for button in self.__buttons:
            GPIO.remove_event_detect(button)

def buttonCallBack(channel, sound):
        sound.play()
        
"""
def b1Callback(channel):
    global clap, snare
    clap.play()
    #snare.play()
    print("Falling-edge detected. Button 1 pressed")
    
def b2Callback(channel):
    global snare
    snare.play()
    print("Rising-edge detected. Button 2 pressed")


if __name__ == "__main__":
    GPIOInit()
    soundInit()
    GPIO.add_event_detect(B2_GPIX, GPIO.RISING, callback=b2Callback,
                          bouncetime=200)
    GPIO.add_event_detect(B1_GPIX, GPIO.FALLING, callback=b1Callback,
                          bouncetime=200)

    # GPIO.remove_event_detect(port_num)
    while True:
        pass
"""
