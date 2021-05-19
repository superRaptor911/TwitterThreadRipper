import Network
import tweepy
import Utility

Current_reccursion_level = 0
Tweets_processed_in_reccursion = 0

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
    Current_reccursion_level += 1
    for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=90, tweet_mode="extended").items(50):
        if hasattr(tweet, 'in_reply_to_status_id'):
            if tweet.in_reply_to_status_id == tweetID:
                spaces = '  ' * Current_reccursion_level
                print(spaces + "Got sub tweet for : " + tweet.user.screen_name)
                replies.append(getReplies(api, tweet))

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
            Network.unlockThreadID(threadID)
        print("\n")


def main(api, originTweet, args):
    if 'full' in args:
        saveFullThread(api, originTweet)
    else:
        saveThread(api, originTweet)

