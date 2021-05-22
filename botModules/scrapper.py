import tweepy
import pandas as pd


consumer_key = "v2praQAeajPMy3BrmfH06jZGg"
consumer_secret = "GFRa26obYLCYhR3WqhLlzdROlKNFaw8pM42cXygr47quthfb5u"
acces_token = "3425123352-1mwXLuxtqm7q32MOpH2BfS0E1sBAmR5DkThClAO"
acces_secret = "h7WN2z5nYtw0Kofra0N6URARH6aCmBT3D45AR9YOuU2Ey"  

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acces_token, acces_secret)
api =tweepy.API(auth)

user_name = input('Enter the username : ')
number_of_tweets = int(input('\nEnter the number of tweets you want to get : '))
tweets = []
likes= []
time =[]

for i in tweepy.Cursor(api.user_timeline, id = user_name, tweet_mode="extended").items(number_of_tweets):
    tweets.append(i.full_text)
    likes.append(i.favorite_count)
    time.append(i.created_at)
    
df = pd.DataFrame({'tweets': tweets, 'likes': likes, 'time': time})
print(df)

