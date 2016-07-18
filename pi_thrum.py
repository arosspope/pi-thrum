from modes import thrum_live
from modes import thrum_step

if __name__ == "__main__":
    #live = thrum_live.LivePlay(verbose=True)
    #live.runLiveMode()
    
    step = thrum_step.StepPlay(verbose=True)
    step.runStepMode()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nThanks for Playing!")
        #live.stopLiveMode()
        exit()
