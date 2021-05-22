#!/bin/bash

echo "--------------BOT SETUP--------------------------"
echo "Do you want to generate keys? (y/n)"
read choice
if [[ $choice=="y" ]]; then
    echo "Enter AUTH_HANDLER_KEY"
    read AUTH_HANDLER_KEY

    echo "Enter AUTH_HANDLER_PRIVATE_KEY"
    read AUTH_HANDLER_PRIVATE_KEY

    echo "Enter ACCESS_TOKEN"
    read ACCESS_TOKEN

    echo "Enter ACCESS_TOKEN_PRIVATE"
    read ACCESS_TOKEN_PRIVATE

    echo -e "#Bot Secret\n\nAUTH_HANDLER_KEY = \"$AUTH_HANDLER_KEY\"\nAUTH_HANDLER_PRIVATE_KEY = \"$AUTH_HANDLER_PRIVATE_KEY\"\nACCESS_TOKEN = \"$ACCESS_TOKEN\"\nACCESS_TOKEN_PRIVATE = \"$ACCESS_TOKEN_PRIVATE\"\n" > Secret.py
    echo "Keys generated!!"
fi

echo "Do you want to download pip and venv? (y/n)"
read choice
if [[ $choice=="y" ]]; then
    sudo apt install -y python3-pip python3-venv
    echo "Installed PIP and VENV!!"
fi

echo "Do you want to generate Virtual environment? (y/n)"
read choice
if [[ $choice=="y" ]]; then
    
fi

echo "Bot Config Done!"

