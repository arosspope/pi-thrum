from modes import thrum_live

if __name__ == "__main__":
    live = thrum_live.LivePlay(verbose=True)
    live.runLiveMode()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nThanks for Playing!")
        live.stopLiveMode()
        exit()
