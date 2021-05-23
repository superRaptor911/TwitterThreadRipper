import bot
import sys

def main():
    profile = None
    if len(sys.argv) > 1:
        profile = sys.argv[1]
    api = bot.authenticate(profile)
    bot.startBot(api)



if __name__ == '__main__':
    main()
