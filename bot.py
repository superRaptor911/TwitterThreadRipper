import tweepy
import uuid
import Network
import Secret
import time
import Network
import Utility
import json
from botModules import Controller

BOT_ID = str(uuid.uuid1())

AUTH_HANDLER_KEY = Secret.AUTH_HANDLER_KEY
AUTH_HANDLER_PRIVATE_KEY = Secret.AUTH_HANDLER_PRIVATE_KEY

ACCESS_TOKEN = Secret.ACCESS_TOKEN
ACCESS_TOKEN_PRIVATE = Secret.ACCESS_TOKEN_PRIVATE

# Load profile
def setupProfileKeys(profile):
    if profile:
        file = open("secret.json", 'r')
        if file:
            data = json.load(file)
            if profile in data:
                p = data[profile]
                global AUTH_HANDLER_KEY
                global AUTH_HANDLER_PRIVATE_KEY
                global ACCESS_TOKEN
                global ACCESS_TOKEN_PRIVATE

                AUTH_HANDLER_KEY = p[0]
                AUTH_HANDLER_PRIVATE_KEY = p[1]
                ACCESS_TOKEN = p[2]
                ACCESS_TOKEN_PRIVATE = p[3]
                print("Using profile " + profile)
            else:
                print("Error: Profile not found")
                exit(1)

# Authentication
def authenticate(profile):
    setupProfileKeys(profile)


    auth = tweepy.OAuthHandler(AUTH_HANDLER_KEY, AUTH_HANDLER_PRIVATE_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_PRIVATE)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication successful")
    except:
        print("Error:Authentication failed")
        exit(1)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api




def checkMentions(api, since_id):
    print("Checking for mentions ...")
    searchQuery = '@threadRipperBot'
    retweet_filter='-filter:retweets'

    for tweet in tweepy.Cursor(api.search,q=searchQuery+retweet_filter, since_id=since_id, timeout=90).items(50):
        command = Utility.getCommandFromTweetText(tweet.text.lower())
        if command:
            Controller.evalCommand(api, tweet, command)
        Network.pingServer(BOT_ID)
    Network.pingServer(BOT_ID)



def startBot(api):
    retryCount = 0
    while True:
        fromID = Network.getLastProcessedThreadID()
        try:
            checkMentions(api,fromID)
            retryCount = max(0, retryCount - 1)
        except tweepy.TweepError as e:
            print(e.reason)
            retryCount += 1
            print(f"Fatal Error: connection failed\nWaitng {120 * retryCount} secs")
            time.sleep(120 * retryCount)
            retryCount = min(retryCount, 10)
        print("Waiting 60 seconds.....")
        time.sleep(60)
