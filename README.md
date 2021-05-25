![BFH Banner](https://trello-attachments.s3.amazonaws.com/542e9c6316504d5797afbfb9/542e9c6316504d5797afbfc1/39dee8d993841943b5723510ce663233/Frame_19.png)
# ThreadRipperBot

Site: [TwitterThreadRipper](https://twitterthreadripper.ga)

Thread Ripper Bot is a twitter bot which is a part of ThreadRipperBot Net. Thread Ripper bot's task
is to rip threads from Twitter and submit them to BotNet Server .

Server Repo: [repo](https://github.com/superRaptor911/super-raptor-bot-website)

### Thread Ripper bot can:

* Save Twitter threads
* Save Videos from Twitter
* Reply to user when ripping gets completed
* Can save threads up to 7 days old.
* Work with other bots in the network

### Commands

Reply any Tweet with any of these commands to save them in your dashboard. 

* **@threadRipperBot save** -- Save a thread (You will get reply from our bot when your request is completed).

* **@threadRipperBot save full** -- Save entire thread including replies and sub replies by other people.
(Warnig: it's a very slow process and will take lot of time, Max tweets saved : 25) (You will get
reply from our bot when your request is completed)

* **@threadRipperBot save video** -- To save videos in a tweet (Yo will get reply from our bot with video download links)


## Team members

1. [Aditya Aravind](https://github.com/superRaptor911 "RAPTOR")
2. [Vyshnav KS](https://github.com/Vyshnav-KS "KS")
3. [Aswin CHandra](https://github.com/28aswin2001 "aswin")

## Team Id

`BFH/recJlC5PthruZaYYj/2021`

## Link to product walkthrough

https://user-images.githubusercontent.com/58220198/119441370-a6925b00-bd43-11eb-83a7-edb32f5b3524.mp4

[Project Walkthrough](https://twitterthreadripper.ga/server/bfg.mp4)

## How it Works ?

* This bot searches for "@threadRipperBot" using Twitter Search API and checks for valid commands.
* When valid command is found, The bot takes permission from
  [server](https://github.com/superRaptor911/super-raptor-bot-website) to process the Tweet.
* Permission to process this Tweet is given if no other bot is working on this Tweet.

### @threadRipperBot save

* Get Parent Tweet and append into an array
* Repeat above step until root tweet is found
* When root is found upload the array to the server
* reply the user about completion of their request

### @threadRipperBot save full

* Get Parent Tweet 
* Repeat above step until root tweet is found
* When root is found get root tweet ID and add this tweet into a tree (can be achieved with python's dict)
* Search for Tweets which are reply to tweet ID using Twitter Search API and add those tweets into
  the tree.
* Similarly continue above step for replies to get sub-replies and also add them into the tree.
* reply the user about completion of their request

### @threadRipperBot save video

* Get Parent Tweet 
* Search for videos in parent tweet
* If found reply the user with video download link and upload the thread to server
* Else reply failed to get video

## Libraries used

* tweepy==3.10.0

## How to configure

**Note: Tested only on Debian based distos and python 3.8+ is recommended**

If your running this for the first time run `./setup.sh`. Enter your API Keys for Twitter and
Virtual env will be generated for you.

## How to Run

1. Enable Virtual env: `source env/bin/activate` (if you are using fish shell use activate.fish) 
1. Run `python3 main.py` to run the bot

