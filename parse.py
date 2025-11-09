import requests

from markdownify import markdownify as md


def parse_url(url: str) -> str:
    response = requests.get(url)
    html_content = response.text
    markdown_content = md(html_content)

    return markdown_content


if __name__ == "__main__":
    test_url = "https://app.food2050.ch/de/v2/zfv/zhdk,toni-areal/mensa-molki/mittagsverpflegung/menu/weekly"
    markdown = parse_url(test_url)
    print(markdown)
