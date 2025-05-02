import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import Timeout, ConnectionError, RequestException


def get_tiktok_trends_from_creative_center():
    """Scrape trending hashtags from TikTok Creative Center."""
    url = (
        "https://www.tiktok.com/business/en/creativecenter/inspiration/popular/hashtag"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "\
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=(5, 15))
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find the script tag containing the trend data
        script_tags = soup.find_all("script")
        trend_data = None

        for script in script_tags:
            if script.string and "window.INIT_DATA" in script.string:
                # Extract the JSON data
                json_str = (
                    script.string.split("window.INIT_DATA = ")[1].split("};")[0] + "}"
                )
                trend_data = json.loads(json_str)
                break

        if not trend_data:
            return []

        # Extract trending hashtags from the data
        trending_hashtags = []
        for item in trend_data.get("inspirationData", {}).get("data", []):
            trending_hashtags.append(
                {
                    "hashtag": item.get("title"),
                    "views": item.get("value"),
                    "growth_rate": item.get("growthRate"),
                    "rank": item.get("rank"),
                }
            )

        return trending_hashtags

    except Timeout:
        print("Request to TikTok timed out - they might be rate limiting")
        # Return cached or mock data
    except ConnectionError:
        print("Connection error when accessing TikTok")
        # Return cached or mock data
    except RequestException as e:
        print(f"Error accessing TikTok: {str(e)}")
        # Return cached or mock data
