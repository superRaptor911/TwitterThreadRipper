import tweepy
import uuid
import Network
import Secret
import time
import Network
import Utility
from botModules import Controller

Current_reccursion_level = 0
Tweets_processed_in_reccursion = 0
BOT_ID = str(uuid.uuid1())

# Authentication
def authenticate():
    auth = tweepy.OAuthHandler(Secret.AUTH_HANDLER_KEY, Secret.AUTH_HANDLER_PRIVATE_KEY)
    auth.set_access_token(Secret.ACCESS_TOKEN, Secret.ACCESS_TOKEN_PRIVATE)

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
    while True:
        fromID = Network.getLastProcessedThreadID()
        try:
            checkMentions(api,fromID)
        except tweepy.TweepError as e:
            print(e.reason)
            print("Fatal Error: connection failed\nWaitng 120 secs")
            time.sleep(120)
        print("Waiting 60 seconds.....")
        time.sleep(60)
