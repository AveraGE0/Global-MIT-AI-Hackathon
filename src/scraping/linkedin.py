"""Module for getting linkedin trend data."""
import json
import os
from typing import List, Dict, Union


from src.logging import get_logger


logger = get_logger(__name__)


def load_linkedin_hashtag_data(file_path: str) -> List[Dict[str, str]]:
    """
    Load linkedin hashtag data from a JSON file.

    Args:
        file_path: Path to the JSON file containing hashtag data

    Returns:
        List of dictionaries containing hashtag information with keys:
        - hashtag: The hashtag name (without # symbol)
        - posts: The number of posts for this hashtag (e.g., "1.835B")

    Raises:
        FileNotFoundError: If the specified file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        KeyError: If the hashtag data is missing required keys
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error("File not found: %s", file_path)
            raise FileNotFoundError(f"The file {file_path} does not exist")

        # Open and read the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Validate data structure
        if not isinstance(data, list):
            logger.error("Invalid data format: Expected a list, got %s", type(data).__name__)
            raise ValueError("The JSON file should contain a list of hashtag objects")

        # Validate each hashtag entry
        validated_data = []
        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                logger.warning("Skipping invalid entry at index %d: Not a dictionary", i)
                continue

            if "hashtag" not in entry or "followers" not in entry:
                logger.warning("Skipping invalid entry at index %d: Missing required keys", i)
                continue

            validated_data.append(
                {"hashtag": entry["hashtag"], "followers": entry["followers"]}
            )

        logger.info(
            "Successfully loaded %d hashtags from %s", 
            len(validated_data),
            {file_path}
        )
        return validated_data

    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in file %s: %s", file_path, str(e))
        raise
    except Exception as e:
        logger.error("Error loading hashtag data: %s", str(e))
        raise


def get_linkedin_trending_hashtags(
    file_path: str,
    limit: int = 1
) -> List[Dict[str, Union[str, int]]]:
    """
    Get trending Linkedin hashtags from a JSON file with optional filtering.

    Args:
        file_path: Path to the JSON file containing hashtag data
        limit: Maximum number of hashtags to return (default: 10)
        min_posts: Minimum number of posts required (default: None)

    Returns:
        List of dictionaries containing hashtag information with keys:
        - hashtag: The hashtag name (without # symbol)
        - follower: The original post count string (e.g., "1.835B")
    """
    hashtag_data = load_linkedin_hashtag_data(file_path)
    hashtag_data.sort(key=lambda x: x["followers"], reverse=True)
    return hashtag_data[:limit]
