
def printTweet(tweet):
    try:
        print(tweet.entities['media'][0]["media_url_https"])
    except AttributeError:
        print("no media")
    except KeyError:
        print("key error")


def main(api, originTweet, commands):
    printTweet(originTweet)
