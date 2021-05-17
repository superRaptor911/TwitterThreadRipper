from botModules import ThreadSaver

def evalCommand(api, originTweet, command):
    if command["command"] in ["save", "sav"]:
        ThreadSaver.main(api, originTweet, command["args"])
