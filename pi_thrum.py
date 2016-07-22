"""
Entry to the 'pi-thrum' program.

@author Andrew Pope
"""
import step

if __name__ == "__main__":
    print("Welcome to pi-thrum! An interactive 12-step sequencer for"
          " drum samples!\nTo stop program press CTRL+C\n")
    
    program = step.Step()
    
    try:
        program.run()
    except KeyboardInterrupt:
        print("\nThanks for Playing!")
        program.cleanup()
        exit()
