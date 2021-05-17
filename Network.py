import requests
import json

SERVER = "http://twitterthreadripper.ml/server"
# SERVER = "http://twitterbot.com/server"

def uploadThreadToServer(username, threadID, thread):
    print("Uploading thread for user:" + username)
    serverResponse = requests.post(f"{SERVER}/threads.php", json = {"type" :"addThread",
        "name": username, "threadID": threadID, "thread": json.dumps(thread)})

    if serverResponse.status_code != 200:
        print('Error: Request to server failed')
        return

    print(serverResponse.text)
    result = json.loads(serverResponse.text)
    if result["result"] == True:
        print(f"Uploaded thread for user: {username} id : {threadID}")
    else:
        print(f"Error: Failed to Upload thread for user: {username} id : {threadID}")
    return


def getLastProcessedThreadID():
    print("Getting Last processed thread id")
    serverResponse = requests.post(f"{SERVER}/bot.php", json = {"type" :"getThreadID"})
    if serverResponse.status_code != 200:
        print('Error: Request to server failed')
        quit(1)

    result = json.loads(serverResponse.text)
    if result["result"] == True:
        threadID = int(result["threadID"])
        print(f"Got Last Thread id : {threadID}")
        return threadID
    else:
        print('Error: Did not get last Thread ID Using 1')
    return 1


def lockThreadID(threadID) -> bool:
    print(f"Locking thread id : {threadID}")
    serverResponse = requests.post(f"{SERVER}/bot.php", json = {"type" :"lockThread", "threadID": threadID})
    if serverResponse.status_code != 200:
        print('Error: Request to server failed. exiting')
        quit(1)

    print(serverResponse.text)
    result = json.loads(serverResponse.text)
    if result["result"] == True:
        print(f"Locked Thread : {threadID}")
        return True

    print(f'Warning: failed to lock Thread ID : {threadID}')
    return False


def unlockThreadID(threadID):
    print(f"unlocking thread id : {threadID}")
    serverResponse = requests.post(f"{SERVER}/bot.php", json = {"type" :"unlockThread", "threadID": threadID})
    if serverResponse.status_code != 200:
        print('Error: Request to server failed. exiting')
        quit(1)

    print(serverResponse.text)
    result = json.loads(serverResponse.text)
    if result["result"] == True:
        print(f"Unlocked Thread : {threadID}")
    else:
        print(f'Error: failed to unlock Thread ID : {threadID}')
