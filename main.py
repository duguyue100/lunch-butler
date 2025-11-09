# main.py
import os
import requests

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_menu_data() -> list[dict]:
    # Minimum example — replace with scraping or LLM later
    return [
        {
            "name": "Toni-Areal",
            "type": "url",
            "content": "https://www.zfv.ch/de/essen-gehen/gastronomie-im-toni-areal#menu",
        },
        {
            "name": "technopark",
            "type": "url",
            "content": "https://www.zfv.ch/de/essen-gehen/gastronomie-im-technopark-zuerich",
        },
        {
            "name": "Jao Praya (Thai Restaurant)",
            "type": "text",
            "content": "Pad Thai, Green Curry, Tom Yum Soup",
        },
        {
            "name": "LianHua (Chinese Restaurant)",
            "type": "text",
            "content": "Kung Pao Chicken, Sweet and Sour Pork, Fried Rice",
        },
        {
            "name": "Lunch 5",
            "type": "url",
            "content": "http://www.lunch-5.ch/uploads/menuplan.pdf",
        },
        {
            "name": "Food Trucks",
            "type": "text",
            "content": "Tacos Truck, Vegan Burger Truck, Sushi Truck",
        },
    ]


def generate_lunch_message():
    menu = get_menu_data()
    items = "\n".join(f"- {item}" for item in menu)

    return f"""🥡 *Today's Lunch Ideas*

Here are some options for today:
{items}

Bon appetit! 😋
"""


def post_to_slack(text: str):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"channel": SLACK_CHANNEL_ID, "text": text}
    r = requests.post(url, json=payload, headers=headers)
    print("Slack response:", r.text)


if __name__ == "__main__":
    msg = generate_lunch_message()
    post_to_slack(msg)
