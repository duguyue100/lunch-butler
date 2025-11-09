# main.py
import os
import requests
from datetime import datetime

from parse import parse_url
from openai import OpenAI


SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """You are the official Lunch Butler of LatticeFlow and responsible for providing daily lunch suggestions to the team.

Today is {DATE}.

Below is a list of available lunch options from various cafeterias, restaurants, and food trucks in the area.
Each option is a section started by "# Location:" followed by the name of the place, and then the menu items or a URL to the menu.

{MENU_DATA}

Your task is to generate a friendly and engaging Slack message that lists TODAY's lunch options in a clear and appealing manner. Your response MUST meet the following criteria:
- Some menu items are written in Swiss German. Translate them to English in the response.
- Pay special attention to any additional information provided for each menu.
- Use emoji to colorfully highlight different food options (e.g., 🍔 for burgers, 🍣 for sushi, 🌮 for tacos, etc.).
- Your response should include a top choice for the day, based on variety and appeal.
- For completeness, make a summary of all available options at the end of the message. And format them in a list.
"""


def get_menu_data() -> list[dict]:
    # Minimum example — replace with scraping or LLM later
    return [
        {
            "name": "Toni-Areal",
            "type": "url",
            "content": "https://app.food2050.ch/de/v2/zfv/zhdk,toni-areal/mensa-molki/mittagsverpflegung/menu/weekly",
        },
        {
            "name": "Technopark",
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
    print("Parsing menu item:", item["name"])
    menu_str = f"# Location: {item['name']}\n"
    if "additional_info" in item:
        menu_str += f"**Note:** {item['additional_info']}\n\n"
    if item["type"] == "url":
        parsed_content = parse_url(item["content"])

        menu_str += parsed_content
    elif item["type"] == "text":
        menu_str += item["content"]

    return menu_str


def prepare_menu(menu: list[dict]) -> str:
    menu_str = ""
    for item in menu:
        menu_str += prepare_menu_item(item) + "\n\n"  # Extra newline for spacing

    return menu_str.strip()


def generate_lunch_message() -> str:
    menu = prepare_menu(get_menu_data())

    date_str = datetime.now().strftime("%B %d, %Y")

    system_prompt_filled = SYSTEM_PROMPT.format(DATE=date_str, MENU_DATA=menu)

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": system_prompt_filled},
        ],
    )

    return str(response.choices[0].message.content)


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
    print(msg)
    post_to_slack(msg)
