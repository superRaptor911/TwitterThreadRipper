import Network
import Utility

def getParentTweet(api , tweet):
    if tweet == None:
        print("fatal error: Tweet null")
        return tweet

    if tweet.in_reply_to_status_id == None:
        print("Waring: Parent Tweet not found")
        return tweet

    parent = api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended")
    if parent == None:
        print("fatal error: Failed to get parent tweet")
        return tweet
    return parent


def tweetToThreadTree(tweet):
    return {"tweet": tweet, "replies": []}


def saveVideo(api, originTweet):
    threadID = originTweet.id_str
    username = originTweet.user.screen_name

    if Network.lockThreadID(threadID):
        print("\nGoing to rip video from tweet 😁")
        parentTweet = getParentTweet(api, originTweet)
        videoUrls = Utility.extractVideosFromTweet(parentTweet)

        replyText = f"@{username} "
        if len(videoUrls) == 0:
            replyText = replyText + "Sorry 😩 Failed to get videos"
        else:
            thread = tweetToThreadTree(Utility.getCompactTweet(parentTweet))
            Network.uploadThreadToServer(username, threadID, thread)
            replyText = replyText + "Here's you video download link.\n"

        for videos in videoUrls:
            if len(videos) > 0:
                link = videos[0]["link"]
                replyText = replyText + f"Video Link: {link}\n"

        print(replyText)
        try:
            if not originTweet.user.following:
                print("Following : " + username)
                originTweet.user.follow()

            api.update_status(
                status = replyText,
                in_reply_to_status_id = originTweet.id,
            )
        except:
            print("Failed to Send Message")
        Network.unlockThreadID(threadID)


def main(api, originTweet, args):
    if 'video' in args:
        saveVideo(api, originTweet)

