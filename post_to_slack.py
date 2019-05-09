import os
import random
import argparse
import requests
import base64

from dotenv import load_dotenv


API_URL = "https://slack.com/api/chat.postMessage"


def get_api_token():
    token = os.getenv("PEPUBOT_SLACK_API_TOKEN")
    if token:
        return token
    b64_token = os.getenv("PEPUBOT_SLACK_API_TOKEN_B64")
    # GitLab masked variables don't suppoer == so we don't have padding...
    b64_token = b64_token + "=" * (-len(b64_token) % 4)
    token = base64.b64decode(b64_token).decode("utf-8").strip()
    return token


def send_message(channel, message, retries=3):
    data = {
        "token": get_api_token(),
        "channel": channel,
        "text": message,
        "as_user": True,
    }
    response = requests.post(API_URL, data=data)


def get_valid_reddit_posts():
    response_data = requests.get(
        "https://www.reddit.com/r/ProgrammerHumor/top/.json?t=week&sort=top",
        headers={
            "User-Agent": "Pepubot v1.0"
        }
    ).json()
    posts = response_data["data"]["children"]
    posts = list(filter(lambda x: x["kind"] == "t3", posts))
    return posts


def get_reddit_meme():
    posts = get_valid_reddit_posts()
    image_url = random.choice(posts)["data"]["url"]
    return image_url


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
    parser.add_argument("--mode", type=str, choices=ModeChoices.options())
    parser.add_argument("--channel", type=str, default="@riskimies")
    parser.add_argument("--message", type=str, default="")
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()
    channel = os.getenv("PEPUBOT_CHANNEL", args.channel)
    mode = os.getenv("PEPUBOT_MODE", args.mode)
    message = os.getenv("PEPUBOT_MESSAGE", args.message)

    if not (channel and mode):
        print("Missing channel or mode, please see the help menu")
        return

    if mode == "reddit":
        send_message(channel, get_reddit_meme())
    if mode == "message":
        if not message:
            print("Missing message, please see the help menu")
            return
        send_message(channel, message)


if __name__ == "__main__":
    main()
