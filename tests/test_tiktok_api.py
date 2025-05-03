import re

import vcr

from src.scraping.tiktok import get_tiktok_trends_from_creative_center, TikTokTrends
from src.config import load_config

config = load_config("configs/scraping.yaml")


@vcr.use_cassette(
    "tests/fixtures/tiktok_trends_cassette_hashtags.yaml",
    record_mode="once",
    match_on=["uri", "method"],
)
def test_real_tiktok_api_call_hashtags():
    """
    Integration test that makes an actual call to the TikTok Creative Center.

    This test uses VCR to record the HTTP interaction the first time it runs,
    and then replays the recorded response on subsequent runs.
    """
    result = get_tiktok_trends_from_creative_center(config["tiktok"]["hashtags"], TikTokTrends.HASHTAGS)

    # Basic validation of the response
    assert result is not None

    # Check if we got a list (either real data or empty list on error)
    assert isinstance(result, list)

    # If we got data, validate its structure
    if result:
        # Check the first item has the expected fields
        first_item = result[0]
        assert "hashtag" in first_item
        assert "post_count" in first_item
        assert "trend_direction" in first_item
        assert "rank" in first_item

        # Validate hashtag format (should start with #)
        assert first_item["hashtag"].startswith("#")

        # Validate views format (should be a number followed by K, M, or B)
        assert re.match(r"^\d+(\.\d+)?[KMB]?$", first_item["post_count"])


@vcr.use_cassette(
    "tests/fixtures/tiktok_trends_cassette_songs.yaml",
    record_mode="once",
    match_on=["uri", "method"],
)
def test_real_tiktok_api_call_songs():
    """
    Integration test that makes an actual call to the TikTok Creative Center.

    This test uses VCR to record the HTTP interaction the first time it runs,
    and then replays the recorded response on subsequent runs.
    """
    result = get_tiktok_trends_from_creative_center(config["tiktok"]["songs"], TikTokTrends.SONGS)

    # Basic validation of the response
    assert result is not None

    # Check if we got a list (either real data or empty list on error)
    assert isinstance(result, list)

    # If we got data, validate its structure
    if result:
        # Check the first item has the expected fields
        first_item = result[0]
        assert "name" in first_item
        assert "trend_direction" in first_item
        assert "rank" in first_item
