
def getCommandFromTweetText(tweetText):
    strings = tweetText.split(" ")
    filteredStrings = [x for x in strings if not x.lower().startswith('@')]

    if len(filteredStrings) == 0:
        return False
    return {
            "command": filteredStrings[0],
            "args": filteredStrings[1:len(filteredStrings)]
    }


def extractTextFromTweet(tweet, isExtended = True):
    text = ""
    if isExtended:
        if 'retweeted_status' in dir(tweet):
            text=tweet.retweeted_status.full_text
        else:
            text=tweet.full_text
    else:
        text = tweet.text
    return text

def extractVideosFromTweet(tweet):
    videoUrls = []
    try:
        media = tweet.extended_entities['media'][0]
        if media["type"] == "video":
            files = []
            for i in media["video_info"]["variants"]:
                files.append(i["url"])
            videoUrls.append(files)
    except AttributeError:
        print("no media")
    except KeyError:
        print("no media")
    return videoUrls


def extractImagesFromTweet(tweet):
    images = []
    try:
        for media in tweet.extended_entities['media']:
            images.append(media["media_url_https"])
    except AttributeError:
        print("no media")
    except KeyError:
        print("no media")
    return images



def getCompactTweet(tweet, isExtended = True):
    return {
            "id": tweet.id_str,
            "text": extractTextFromTweet(tweet, isExtended),
            "name": tweet.user.name,
            "username": tweet.user.screen_name,
            "time": str(tweet.user.created_at),
            "image": tweet.user.profile_image_url,
            "image_https": tweet.user.profile_image_url_https,
            "likes": tweet.favorite_count,
            "retweets": tweet.retweet_count,
            "images": extractImagesFromTweet(tweet),
            "videos": extractVideosFromTweet(tweet)
    }


def truncText(text : str, size) -> str:
    strLen = len(text)
    if strLen <= size:
        return text
    if size > 3:
        return text[0: size - 3] + "..."
    return text[0:size]
