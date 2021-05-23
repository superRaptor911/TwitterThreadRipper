import Network
import tweepy
import Utility
import time

Current_reccursion_level = 0
Tweets_processed_in_reccursion = 0
Max_Tweets = 25

def getTweetsTillRoot(api, fromTweet):
    arr = []
    parent = fromTweet
    arr.append(Utility.getCompactTweet(parent, False))

    while parent and parent.in_reply_to_status_id != None:
        parent = api.get_status(parent.in_reply_to_status_id, tweet_mode="extended")
        spaces = '  ' * Current_reccursion_level
        print(spaces + "Got sub tweet for : " + parent.user.screen_name)
        arr.append(Utility.getCompactTweet(parent))
    return arr

def arrayToThreadTree(arr):
    parentTweet = arr[0]
    replies = []
    arr = arr[1:len(arr)]
    if len(arr) > 0:
        replies.append(arrayToThreadTree(arr))
    return {"tweet": parentTweet, "replies": replies}


def getRootTweet(api, tweet):
    if tweet == None:
        print("fatal erroe: Tweet null")
        return tweet
    if tweet.in_reply_to_status_id == None:
        print("Got root!")
        return tweet
    parent = api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended")
    return getRootTweet(api, parent)



def getReplies(api, parentTweet):
    tweetID = parentTweet.id
    name = parentTweet.user.screen_name
    replies=[]
    global Current_reccursion_level
    global Tweets_processed_in_reccursion

    Current_reccursion_level += 1
    retryCount = 0
    while retryCount < 5:
        try:
            # Tweet limiter
            if Tweets_processed_in_reccursion < Max_Tweets:
                for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=90, tweet_mode="extended").items(50):
                    if hasattr(tweet, 'in_reply_to_status_id'):
                        if tweet.in_reply_to_status_id == tweetID:
                            spaces = '  ' * Current_reccursion_level
                            Tweets_processed_in_reccursion += 1
                            print(spaces + "Got sub tweet for : " + tweet.user.screen_name)
                            print("Tweets_processed_in_reccursion = " + str(Tweets_processed_in_reccursion))
                            replies.append(getReplies(api, tweet))
            break
        except tweepy.TweepError as e:
            print(e.reason)
            print(f"Fatal Error: connection failed\nWaitng {60 * retryCount} secs")
            retryCount += 1
            time.sleep(60 * retryCount)

    Current_reccursion_level -= 1
    return {"tweet": Utility.getCompactTweet(parentTweet), "replies": replies}



def getThreadTree(api, root):
    global Current_reccursion_level
    global Tweets_processed_in_reccursion

    Current_reccursion_level = 0
    Tweets_processed_in_reccursion = 0
    print("Geting Thread tree for " + root.id_str)
    # print("Tweet: " + root.text)
    threadTree = getReplies(api, root)
    return threadTree

def sendThreadSavedMessage(api, originTweet):
    threadID = originTweet.id_str
    username = originTweet.user.screen_name
    text = f"""@{username} I saved your Twitter thread.
View ur saved thread: https://twitterthreadripper.ga/thread/{threadID}

Login to keep track of ur saved threads: https://twitterthreadripper.ga
"""
    try:
        if not originTweet.user.following:
            print("Following : " + username)
            originTweet.user.follow()

        api.update_status(
            status = text,
            in_reply_to_status_id = originTweet.id,
        )
    except:
        print("Failed to Send Message")


def saveFullThread(api, originTweet):
    threadID = originTweet.id_str
    username = originTweet.user.screen_name

    if Network.lockThreadID(threadID):
        print(f"Evaluating user:{originTweet.user.name}")
        root = getRootTweet(api, originTweet)

        if root is None:
            print("error: none root")
        else:
            Network.uploadThreadToServer(username, threadID, getThreadTree(api, root))
            sendThreadSavedMessage(api, originTweet)
        Network.unlockThreadID(threadID)
        print("\n")


def saveThread(api, originTweet):
    threadID = originTweet.id_str
    username = originTweet.user.screen_name

    if Network.lockThreadID(threadID):
        print(f"Evaluating user:{originTweet.user.name}")
        thread = getTweetsTillRoot(api, originTweet)
        thread = thread[::-1]

        if len(thread) == 0:
            print("Empty Thread : for Thread id: " + threadID)
        else:
            Network.uploadThreadToServer(username, threadID, arrayToThreadTree(thread))
            sendThreadSavedMessage(api, originTweet)
        Network.unlockThreadID(threadID)
        print("\n")


def main(api, originTweet, args):
    if 'full' in args:
        saveFullThread(api, originTweet)
    else:
        saveThread(api, originTweet)

