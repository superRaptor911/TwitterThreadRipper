import bot
import sys

def main():
    configFile = None
    if len(sys.argv) > 1:
        configFile = sys.argv[1]
    api = bot.authenticate(profile)
    bot.startBot(api)



if __name__ == '__main__':
    main()
