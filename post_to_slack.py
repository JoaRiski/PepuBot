import os
import argparse
import requests

from dotenv import load_dotenv


API_URL = "https://slack.com/api/chat.postMessage"


def send_message(channel, message, retries=3):
    data = {
        "token": os.getenv("SLACK_API_TOKEN"),
        "channel": channel,
        "text": message,
        "as_user": True,
    }
    response = requests.post(API_URL, data=data)
    print(response.content)


def get_reddit_meme():
    return "Big meme here"


class OptionList:
    @classmethod
    def options(cls):
        return [
            value
            for key, value in vars(cls).items()
            if not key.startswith("_")
        ]


class ModeChoices(OptionList):
    reddit = "reddit"
    message = "message"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, choices=ModeChoices.options(), required=True)
    parser.add_argument("--channel", type=str, default="@riskimies")
    parser.add_argument("--message", type=str, default="")
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()
    message = ""
    if args.mode == "reddit":
        message = get_reddit_meme()
    if args.mode == "message":
        message = args.message

    channel = args.channel
    if channel and message:
        send_message(channel, message)


if __name__ == "__main__":
    main()
