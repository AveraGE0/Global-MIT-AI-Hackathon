"""Module to merge generated videos with sound."""
from moviepy import (  #pylint: disable=import-error
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip
)
from src.logging import get_logger


logger = get_logger(__name__)


def add_voiceover_to_video(
    video_path: str,
    audio_path: str,
    output_path: str,
    audio_start_time: float = 0, 
    original_audio_factor: float = 0.3
) -> str:
    """
    Add a voiceover audio track to an existing video.
    
    Args:
        video_path (str): Path to the input video file
        audio_path (str): Path to the voiceover audio file
        output_path (str): Path where the output video will be saved
        audio_start_time (float): Time in seconds when the voiceover should start. Default is 0.
        original_audio_factor (float): Volume factor for the original video audio.
            0 = mute original audio, 1 = keep original volume. Default is 0.3.
            
    Returns:
        str: Path to the output video file
    """
    try:
        logger.info("Merging video: %s, with audio %s", video_path, audio_path)
        video_clip = VideoFileClip(video_path)
        video_clip.with_start('00:00:00.00')
        voice_over = AudioFileClip(audio_path)\
            .with_start('00:00:00.00')\
            .with_duration(video_clip.duration)
        original_audio = video_clip.audio

        if original_audio is not None and original_audio_factor > 0:
            # Reduce the volume of the original audio
            original_audio = original_audio.volumex(original_audio_factor)

            # Create a composite audio clip with both audio tracks
            new_audio = CompositeAudioClip([
                original_audio,
                voice_over.set_start(audio_start_time)
            ])
        else:
            # Use only the voiceover
            new_audio = voice_over

        # Set the new audio to the video
        final_clip = video_clip.with_audio(new_audio)

        # Write the result to a file
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )

        # Close the clips to free up resources
        video_clip.close()
        if original_audio is not None:
            original_audio.close()
        voice_over.close()

        return output_path

    except Exception as e:
        print(f"Error adding voiceover to video: {str(e)}")
        raise


if __name__ == "__main__":
    add_voiceover_to_video(
        "data/brainrot1.mp4",
        "data/tts/brainrot.mp3",
        output_path="data/starbucks_italian_brainrot.mp4"
    )
