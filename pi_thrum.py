from modes import thrum_live
from modes import thrum_step

if __name__ == "__main__":
    print("Welcome to pi-thrum! An interactive 12-step sequencer for"
          " drum samples!\nTo stop program press CTRL+C\n")
    
    step = thrum_step.StepPlay(verbose=True)
    
    try:
        step.run()
    except KeyboardInterrupt:
        print("\nThanks for Playing!")
        step.cleanup()
        exit()
