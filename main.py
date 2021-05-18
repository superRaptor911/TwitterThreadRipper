import bot

def main():
    api = bot.authenticate()
    bot.startBot(api)


if __name__ == '__main__':
    main()
