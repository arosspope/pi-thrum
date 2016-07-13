from modes import thrum_live

if __name__ == "__main__":
    live = thrum_live.LivePlay()
    live.runLiveMode()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Thanks for Playing!")
        live.stopLiveMode()
        exit()
