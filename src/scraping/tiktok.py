"""Module to get TikTok trend data"""
from enum import StrEnum
from typing import Dict, List, Optional, Union

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, RequestException, Timeout
import vcr

from src.logging import get_logger


logger = get_logger(__name__)


class TikTokTrends(StrEnum):
    HASHTAGS = "hashtags"
    SONGS = "songs"


def extract_tiktok_hashtags(
    soup: BeautifulSoup,
) -> List[Dict[str, Optional[Union[str, int]]]]:
    """
    Extract hashtag information from TikTok's Creative Center HTML with robust selectors.

    Args:
        soup: BeautifulSoup object containing parsed HTML from the TikTok Creative Center page

    Returns:
        List of dictionaries with hashtag information including:
        - hashtag: The hashtag text (including # symbol)
        - post_count: Number of posts using this hashtag
        - trend_direction: Direction of trend ('up', 'down', or 'stable')
        - rank: Rank of the hashtag
    """
    trending_hashtags: List[Dict[str, Optional[Union[str, int]]]] = []
    cards = soup.find_all("a", id="hashtagItemContainer")
    for card in cards:
        hashtag = card.find("span", class_="CardPc_titleText__RYOWo").text.strip()
        rank = int(card.find(
            "span", class_="RankingStatus_rankingIndex__ZMDrH"
        ).text.strip())
        post_count = card.find("span", class_="CardPc_itemValue__XGDmG").text.strip()

        # Determine trend direction
        trend_direction: str = "stable"
        if (
            card.select_one(".i-icon-arrow-up")
            or card.select_one('[class*="rising"]')
            or card.select_one('svg path[stroke="#5CA537"]')
        ):
            trend_direction = "up"
        elif (
            card.select_one(".i-icon-arrow-down")
            or card.select_one('[class*="falling"]')
            or card.select_one('svg path[stroke="#FF0000"]')
        ):
            trend_direction = "down"

        trending_hashtags.append(
            {
                "hashtag": hashtag.replace("#", "").lstrip(),
                "rank": rank,
                "post_count": post_count or "N/A",
                "trend_direction": trend_direction,
            }
        )

    return trending_hashtags


def extract_tiktok_songs(
    soup: BeautifulSoup,
) -> List[Dict[str, Optional[Union[str, int]]]]:
    """
    Extract song information from TikTok's Creative Center HTML with robust selectors.

    Args:
        soup: BeautifulSoup object containing parsed HTML from the TikTok Creative Center page

    Returns:
        List of dictionaries with hashtag information including:
        - name: The hashtag text (including # symbol)
        - trend_direction: Direction of trend ('up', 'down', or 'stable')
        - rank: Rank of the hashtag
    """
    trending_songs: List[Dict[str, Optional[Union[str, int]]]] = []
    cards = soup.find_all("a", class_="ItemCard_soundItemContainer__GUmFb")
    for card in cards:
        name = card.find("span", class_="CardPc_titleText__RYOWo").text.strip()
        rank = int(card.find(
            "span", class_="RankingStatus_rankingIndex__ZMDrH"
        ).text.strip())

        # Determine trend direction
        trend_direction: str = "stable"
        if (
            card.select_one(".i-icon-arrow-up")
            or card.select_one('[class*="rising"]')
            or card.select_one('svg path[stroke="#5CA537"]')
        ):
            trend_direction = "up"
        elif (
            card.select_one(".i-icon-arrow-down")
            or card.select_one('[class*="falling"]')
            or card.select_one('svg path[stroke="#FF0000"]')
        ):
            trend_direction = "down"

        trending_songs.append(
            {
                "name": name,
                "rank": rank,
                "trend_direction": trend_direction,
            }
        )

    return trending_songs


@vcr.use_cassette(
    "data/fixtures/tiktok_trends_cassette_hashtags.yaml",
    record_mode="once",
    match_on=["uri", "method"],
)
def get_tiktok_hashtag_trends(url, limit=1):
    """Get trending hashtags from TikTok Creative Center."""
    return _get_tiktok_trends_from_creative_center(url, TikTokTrends.HASHTAGS)[:limit]


@vcr.use_cassette(
    "data/fixtures/tiktok_trends_cassette_songs.yaml",
    record_mode="once",
    match_on=["uri", "method"],
)
def get_tiktok_song_trends(url, limit=6):
    """Get trending songs from TikTok Creative Center."""
    return _get_tiktok_trends_from_creative_center(url, TikTokTrends.SONGS)[:limit]


def _get_tiktok_trends_from_creative_center(
    url: str,
    trend_type: TikTokTrends
) -> List[Dict[str, Optional[Union[str, int]]]]:
    """
    Scrape trending hashtags from TikTok Creative Center.

    Returns:
        List of dictionaries containing hashtag information
    """

    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,"
        "*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
    }

    try:
        response = requests.get(url, headers=headers, timeout=(5, 15))
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Use the robust extraction function
        if trend_type == TikTokTrends.HASHTAGS:
            trending = extract_tiktok_hashtags(soup)
        elif trend_type == TikTokTrends.SONGS:
            trending = extract_tiktok_songs(soup)
        else:
            raise ValueError(
                f"Error wrong trend type given, should be {TikTokTrends.__members__.values()}"
            )

        return trending

    except Timeout:
        print("Request to TikTok timed out - they might be rate limiting")
        return []
    except ConnectionError:
        print("Connection error when accessing TikTok")
        return []
    except RequestException as e:
        print(f"Error accessing TikTok: {str(e)}")
        return []
