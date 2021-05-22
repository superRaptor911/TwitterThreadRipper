def printTweet(tweet):
    try:
        media = tweet.extended_entities['media']
        for i in media:
            print(i["media_url_https"])
    except AttributeError:
        print("no media")
    except KeyError:
        print("key error")


def main(api, originTweet, commands):
    printTweet(originTweet)
