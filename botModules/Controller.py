from botModules import ThreadSaver
from botModules import Debug
from botModules import MediaSaver

def evalCommand(api, originTweet, command):
    if command["command"] in ["save", "sav"]:
        ThreadSaver.main(api, originTweet, command["args"])
    elif command["command"] in ["debugvideo", "adhkh"]:
        Debug.main(api, originTweet, command["args"])
    elif command["command"] in ["get", "download"]:
        MediaSaver.main(api, originTweet, command["args"])
