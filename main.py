import tweepy
import Secret

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
        return False

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


def main():
    authenticate()

if __name__ == '__main__':
    main()
