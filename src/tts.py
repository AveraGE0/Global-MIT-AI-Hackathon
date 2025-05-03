"""Module to make tts."""
import pyttsx3  # pylint: disable=import-error

from src.logging import get_logger


logger = get_logger(__name__)

# Initialize the TTS engine
engine = pyttsx3.init(driverName='nsss')


def text_to_speech(text: str, rate: int = 150, volume: float = 0.9) -> str:
    """Function for performing TTS.

    Args:
        text (str): Text that is being transcribed to speech
        rate (int): Speech rate in words per minute. Default is 150.
            Lower values slow down speech, higher values speed it up.
            Typical range is 100-250.
        volume (float): Volume level for the speech output, ranging from 0.0 to 1.0.
            0.0 is silent, 1.0 is maximum volume. Default is 0.9.

    Returns:
        str: The path where the speech was saved.
    """
    # Set properties (optional)
    engine.setProperty('rate', rate)    # Speed of speech
    engine.setProperty('volume', volume)  # Volume (0.0 to 1.0)

    # Get available voices
    voices = engine.getProperty('voices')

    # Try to find an Italian-sounding voice (or any voice you prefer)
    for voice in voices:
        if "ita" in voice.id.lower() or "luca" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    # Save to file
    out_file = "/Users/mfr/Projects/Global-MIT-AI-Hackathon/data/tts/output.mp3"
    engine.save_to_file(text, out_file)
    # Run the engine and wait
    engine.runAndWait()
    logger.info("Saved tts output to %s", out_file)

    return out_file
