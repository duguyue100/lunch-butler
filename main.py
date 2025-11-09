# main.py
import os
import requests
from datetime import datetime

from parse import parse_url

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

SYSTEM_PROMPT = """You are the official Lunch Butler of LatticeFlow and responsible for providing daily lunch suggestions to the team.

Today is {DATE}.

Below is a list of available lunch options from various cafeterias, restaurants, and food trucks in the area.
{MENU_DATA}

Your task is to generate a friendly and engaging Slack message that lists today's lunch options in a clear and appealing manner.
"""


def get_menu_data() -> list[dict]:
    # Minimum example — replace with scraping or LLM later
    return [
        {
            "name": "Toni-Areal",
            "type": "url",
            "content": "https://app.food2050.ch/de/v2/zfv/zhdk,toni-areal/mensa-molki/mittagsverpflegung/menu/weeklyh",
        },
        {
            "name": "technopark",
            "type": "url",
            "content": "https://app.food2050.ch/de/v2/zfv/technopark-zurich/technopark/mittagsverpflegung/menu/weekly",
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
            "additional_info": "The dishes in the rows 'immer gut' and below available every day.",
        },
        {
            "name": "Food Trucks",
            "type": "text",
            "content": "Tacos Truck, Vegan Burger Truck, Sushi Truck",
        },
    ]


def prepare_menu_item(item: dict) -> str:
    if item["type"] == "url":
        parsed_content = parse_url(item["content"])
        return f"{item['name']}:\n{parsed_content}"
    elif item["type"] == "text":
        return f"{item['name']}: {item['content']}"
    else:
        return f"{item['name']}: (No details available)"


def prepare_menu(menu: list[dict]) -> str:
    pass


def generate_lunch_message() -> str:
    menu = get_menu_data()
    items = "\n".join(f"- {item}" for item in menu)

    date_str = datetime.now().strftime("%B %d, %Y")

    system_prompt_filled = SYSTEM_PROMPT.format(DATE=date_str, MENU_DATA=items)

    return system_prompt_filled


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
