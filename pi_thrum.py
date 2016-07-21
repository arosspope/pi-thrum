from modes import step

if __name__ == "__main__":
    print("Welcome to pi-thrum! An interactive 12-step sequencer for"
          " drum samples!\nTo stop program press CTRL+C\n")
    
    program = step.StepPlay(verbose=True)
    
    try:
        program.run()
    except KeyboardInterrupt:
        print("\nThanks for Playing!")
        program.cleanup()
        exit()
