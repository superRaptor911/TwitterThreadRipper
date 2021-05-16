import tweepy
import requests
import json
import Secret
import time

# SERVER = "http://twitterthreadripper.ml/server"
SERVER = "http://twitterbot.com/server"
BOT_NAME = "SuperRaptorBot"

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


def extractTextFromTweet(tweet):
    text = ""
    if 'retweeted_status' in dir(tweet):
        text=tweet.retweeted_status.full_text
    else:
        text=tweet.full_text
    return text


def getCompactTweet(tweet):
    return {
            "id": tweet.id_str,
            "text": extractTextFromTweet(tweet),
            "name": tweet.user.name,
            "username": tweet.user.screen_name,
            "time": str(tweet.user.created_at),
            "image": tweet.user.profile_image_url,
            "image_https": tweet.user.profile_image_url_https,
            "likes": tweet.favorite_count,
            "retweets": tweet.retweet_count,
    }


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
    for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=99999, tweet_mode="extended").items(1000):
        if hasattr(tweet, 'in_reply_to_status_id'):
            if tweet.in_reply_to_status_id == tweetID:
                # print("Got sub tweet : " + tweet.text)
                replies.append(getReplies(api, tweet))
    return {"tweet": getCompactTweet(parentTweet), "replies": replies}



def getThreadTree(api, root):
    print("Geting Thread tree for " + root.id_str)
    # print("Tweet: " + root.text)
    threadTree = getReplies(api, root)
    return threadTree


def checkMentions(api, keywords, since_id):
    print("Checking for mentions ...")
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        setLastProcessedTheadID(new_since_id)
        if any(keyword in tweet.text.lower() for keyword in keywords):
            print(f"Evaluating user:{tweet.user.name}")
            root = getRootTweet(api, tweet)
            if root is None:
                print("error: none root")
            else:
                threadID = tweet.id_str
                username = tweet.user.screen_name
                uploadThreadToServer(username, threadID, getThreadTree(api, root))
            print("\n")
    return new_since_id

#################################################################

def uploadThreadToServer(username, threadID, thread):
    print("Uploading thread for user:" + username)
    serverResponse = requests.post(f"{SERVER}/threads.php", json = {"type" :"addThread",
        "name": username, "threadID": threadID, "thread": json.dumps(thread)})

    if serverResponse.status_code != 200:
        print('Error: Request to server failed')
        return

    print(serverResponse.text)
    result = json.loads(serverResponse.text)
    if result["result"] == True:
        print(f"Uploaded thread for user: {username} id : {threadID}")
    else:
        print(f"Error: Failed to Upload thread for user: {username} id : {threadID}")
    return


def getLastProcessedThreadID():
    print("Getting Last processed thread id")
    serverResponse = requests.post(f"{SERVER}/bot.php", json = {"type" :"getThreadID", "botName": BOT_NAME})
    if serverResponse.status_code != 200:
        print('Error: Request to server failed')
        quit(1)

    result = json.loads(serverResponse.text)
    if result["result"] == True:
        threadID = int(result["threadID"])
        print(f"Got Last Thread id : {threadID}")
        return threadID
    else:
        print('Error: Did not get last Thread ID Using 1')
    return 1


def setLastProcessedTheadID(threadID):
    print(f"Setting Last processed thread id to : {threadID}")
    serverResponse = requests.post(f"{SERVER}/bot.php", json = {"type" :"setThreadID", "botName": BOT_NAME, "threadID": threadID})
    if serverResponse.status_code != 200:
        print('Error: Request to server failed')
        quit(1)

    print(serverResponse.text)
    result = json.loads(serverResponse.text)
    if result["result"] == True:
        print(f"Set Last Thread id to : {threadID}")
        return threadID
    else:
        print('Error: failed to set last Thread ID ')


def main():
    api = authenticate()
    while True:
        fromID = getLastProcessedThreadID()
        checkMentions(api, ["save"], fromID)
        print("Waiting 60 seconds.....")
        time.sleep(60)


if __name__ == '__main__':
    main()
