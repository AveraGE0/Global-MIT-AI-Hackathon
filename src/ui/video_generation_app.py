import io
import json
import logging
import time
from typing import Dict, List, Optional, Tuple, Union
from langchain.prompts import PromptTemplate

import pandas as pd
import requests
import streamlit as st
from PIL import Image
from src.logging import get_logger
from src.llm.agent import agent_call

from src.llm.prompt_template import video_creating_prompt, create_hashtags,predict_viral, create_caption

from src.llm.generator_llm import setup_watsonx_llm_video, setup_watsonx_llm


logger = get_logger(__name__)

# Constants
PLATFORMS = ["TikTok", "LinkedIn", "Instagram"]
TONE_OPTIONS = ["Very Serious", "Professional", "Neutral", "Fun", "Humorous"]
VIDEO_FORMATS = ["Short-form vertical", "Square", "Landscape", "Carousel"]


def configure_page_settings():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Trend-Aware Video Generator",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for a more professional look
    st.markdown(
        """
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .trend-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }
    .trend-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def fetch_trending_content(platform: str) -> List[Dict]:
    """
    Fetch trending content from the specified platform.

    Args:
        platform: The social media platform to fetch trends from

    Returns:
        A list of trending content items with metadata
    """
    logger.info("Fetching trends from %s", platform)

    # In a real implementation, this would call your trend detection API
    # Mock data for demonstration
    mock_trends = {
        "TikTok": [
            {
                "id": "tt1",
                "title": "Dance Challenge",
                "description": "#DanceChallenge trending with over 2M videos this week",
                "engagement": "2.3M videos",
                "image_url": "https://placehold.co/300x500/FF5151/FFF?text=Dance+Challenge",
                "audio": "Oh No - Kreepa",
            },
            {
                "id": "tt2",
                "title": "Productivity Hack",
                "description": "Quick productivity tips in 15-second format",
                "engagement": "1.7M videos",
                "image_url": "https://placehold.co/300x500/51A3FF/FFF?text=Productivity+Hack",
                "audio": "Monkeys Spinning Monkeys - Kevin MacLeod",
            },
            {
                "id": "tt3",
                "title": "Day in the Life",
                "description": "Creators showing their daily routine with fast cuts",
                "engagement": "4.2M videos",
                "image_url": "https://placehold.co/300x500/51FF8D/000?text=Day+in+Life",
                "audio": "Steven Universe - L.Dre",
            },
        ],
        "LinkedIn": [
            {
                "id": "li1",
                "title": "Career Growth Framework",
                "description": "Professionals sharing career development matrices",
                "engagement": "12K shares",
                "image_url": "https://placehold.co/600x400/0077B5/FFF?text=Career+Growth",
                "hashtags": "#CareerAdvice #ProfessionalDevelopment",
            },
            {
                "id": "li2",
                "title": "AI Implementation Stories",
                "description": "Case studies of AI deployment in enterprises",
                "engagement": "8.5K shares",
                "image_url": "https://placehold.co/600x400/0077B5/FFF?text=AI+Stories",
                "hashtags": "#ArtificialIntelligence #TechTrends",
            },
            {
                "id": "li3",
                "title": "Work-Life Balance Confessions",
                "description": "Authentic stories about balancing career and personal life",
                "engagement": "15K shares",
                "image_url": "https://placehold.co/600x400/0077B5/FFF?text=Work-Life",
                "hashtags": "#WorkLifeBalance #WellnessAtWork",
            },
        ],
        "Instagram": [
            {
                "id": "ig1",
                "title": "Transition Reels",
                "description": "Quick outfit/location changes with smooth transitions",
                "engagement": "5.7M posts",
                "image_url": "https://placehold.co/500x500/E1306C/FFF?text=Transitions",
                "effect": "Glitch Effect",
            },
            {
                "id": "ig2",
                "title": "Product Unboxing",
                "description": "Aesthetic unboxing videos with ASMR elements",
                "engagement": "3.2M posts",
                "image_url": "https://placehold.co/500x500/E1306C/FFF?text=Unboxing",
                "effect": "Soft Zoom",
            },
            {
                "id": "ig3",
                "title": "Behind The Scenes",
                "description": "Showing the process behind products or services",
                "engagement": "2.8M posts",
                "image_url": "https://placehold.co/500x500/E1306C/FFF?text=BTS",
                "effect": "VHS Filter",
            },
        ],
    }

    # Simulate API call delay
    time.sleep(1)

    return mock_trends.get(platform, [])


def display_trend_card(trend: Dict, index: int, platform: str) -> None:
    """
    Display a single trend card with selection button.

    Args:
        trend: Dictionary containing trend information
        index: Unique index for the trend
        platform: The platform this trend is from
    """
    with st.container():
        st.markdown(f"<div class='trend-card'>", unsafe_allow_html=True)

        # Title and engagement
        st.subheader(f"🔥 {trend['title']}")
        st.caption(f"Engagement: {trend['engagement']}")

        # Image
        st.image(trend["image_url"], use_container_width=True)

        # Description
        st.markdown(f"**{trend['description']}**")

        # Platform-specific details
        if platform == "TikTok":
            st.text(f"🎵 Audio: {trend['audio']}")
        elif platform == "LinkedIn":
            st.text(f"Hashtags: {trend['hashtags']}")
        elif platform == "Instagram":
            st.text(f"✨ Effect: {trend['effect']}")

        # Select button
        if st.button("Select This Trend", key=f"trend_{platform}_{index}"):
            st.session_state.selected_trend = trend
            st.session_state.selected_platform = platform
            logger.info(f"Selected trend: {trend['title']} from {platform}")

        st.markdown("</div>", unsafe_allow_html=True)


def display_trends_for_platform(platform: str) -> None:
    """
    Display all trending content for a specific platform.

    Args:
        platform: The platform to display trends for
    """
    if st.button(f"Fetch {platform} Trends", key=f"fetch_{platform}"):
        with st.spinner(f"Analyzing latest {platform} trends..."):
            trends = fetch_trending_content(platform)

            if not trends:
                st.warning(f"No trends found for {platform}")
                return

            # Store trends in session state
            st.session_state[f"{platform.lower()}_trends"] = trends

    # Display trends if they exist in session state
    if f"{platform.lower()}_trends" in st.session_state:
        trends = st.session_state[f"{platform.lower()}_trends"]

        # Create columns for layout
        if len(trends) >= 3:
            cols = st.columns(3)
            for i, trend in enumerate(trends):
                with cols[i % 3]:
                    display_trend_card(trend, i, platform)
        else:
            for i, trend in enumerate(trends):
                display_trend_card(trend, i, platform)


def collect_brand_information() -> None:
    """Collect and store brand information in the sidebar."""
    with st.sidebar:
        st.header("Brand Information")

        # Basic brand info
        st.session_state.brand_name = st.text_input(
            "Brand Name", value=st.session_state.get("brand_name", "")
        )

        st.session_state.brand_slogan = st.text_area(
            "Slogan or Tagline",
            value=st.session_state.get("brand_slogan", ""),
            max_chars=100,
        )

        # Brand logo
        st.session_state.brand_logo = st.file_uploader(
            "Upload Brand Logo", type=["png", "jpg", "jpeg"]
        )

        # Brand colors
        st.session_state.brand_color = st.color_picker(
            "Brand Primary Color", value=st.session_state.get("brand_color", "#FF4B4B")
        )

        st.session_state.brand_secondary_color = st.color_picker(
            "Brand Secondary Color",
            value=st.session_state.get("brand_secondary_color", "#4B4BFF"),
        )

        st.markdown("---")

        # Style preferences
        st.header("Video Preferences")

        st.session_state.video_length = st.slider(
            "Video Length (seconds)",
            min_value=5,
            max_value=30,
            value=st.session_state.get("video_length", 15),
        )

        st.session_state.tone = st.select_slider(
            "Tone", options=TONE_OPTIONS, value=st.session_state.get("tone", "Neutral")
        )

        st.session_state.video_format = st.selectbox(
            "Video Format",
            options=VIDEO_FORMATS,
            index=VIDEO_FORMATS.index(
                st.session_state.get("video_format", "Short-form vertical")
            ),
        )


def generate_video() -> bool:
    """
    Generate a video based on selected trend and brand information.

    Returns:
        Boolean indicating if video generation was successful
    """
    # Check if we have the necessary information
    if not hasattr(st.session_state, "selected_trend"):
        st.warning("Please select a trend first")
        return False

    if not st.session_state.brand_name:
        st.warning("Please enter your brand name")
        return False

    # In a real implementation, this would call your video generation API
    logger.info("Generating video with the following parameters:")
    logger.info(f"Brand: {st.session_state.brand_name}")
    logger.info(f"Trend: {st.session_state.selected_trend['title']}")
    logger.info(f"Platform: {st.session_state.selected_platform}")
    
    # TODO call prompt maker here

    trend_search = f"What is {st.session_state.selected_trend['title']}"
    payload = {"messages": [{"content": trend_search, "role": "user"}]}
    trend_explanation = agent_call(payload)

    llm_text_to_video = setup_watsonx_llm_video()
    llm_caption_hashtags = setup_watsonx_llm()

    prompt_video_creation = video_creating_prompt()

    prompt_video = prompt_video_creation.format(
        brand_name=st.session_state.brand_name,
        product=st.session_state.brand_product,
        tone=st.session_state.tone,
        trend_description=trend_explanation
    )

    final_video_prompt = llm_text_to_video.invoke(prompt_video)

    prompt_caption_creation = create_caption()

    prompt_caption = prompt_caption_creation.format(
        brand_name=st.session_state.brand_name,
        product=st.session_state.brand_product,
        tone=st.session_state.tone)

    final_caption = llm_caption_hashtags.invoke(prompt_caption)

    prompt_hashtag_creation = create_hashtags()

    prompt_hashtags = prompt_hashtag_creation.format(
        brand_name=st.session_state.brand_name,
        product=st.session_state.brand_product,
        hashtags=st.session_state.selected_trend['title'],
        tone=st.session_state.tone)

    final_hashtags = llm_caption_hashtags.invoke(prompt_hashtag_creation)

    # Simulate video generation delay
    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        "Analyzing brand assets...",
        "Adapting trend format...",
        "Generating video frames...",
        "Adding brand elements...",
        "Applying effects and transitions...",
        "Adding audio...",
        "Finalizing video...",
    ]

    for i, step in enumerate(steps):
        # Update progress bar and status
        progress = (i + 1) / len(steps)
        progress_bar.progress(progress)
        status_text.text(step)
        time.sleep(0.5)

    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()

    # Store generated video in session state (mock data)
    st.session_state.generated_video = {
        "url": "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_2mb.mp4",
        "thumbnail": "https://placehold.co/800x450/333/FFF?text=Generated+Video+Thumbnail",
        "hashtags": [
            f"#{st.session_state.brand_name.replace(' ', '')}",
            f"#{st.session_state.selected_trend['title'].replace(' ', '')}",
            "#trending",
            "#viralmarketing",
        ],
    }

    return True


def display_generated_video() -> None:
    """Display the generated video and related information."""
    if not hasattr(st.session_state, "generated_video"):
        return

    video_data = st.session_state.generated_video

    st.subheader("🎉 Your Generated Video")

    # Video player
    st.video(video_data["url"])

    # Results in columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Suggested Hashtags")
        hashtags = " ".join(video_data["hashtags"])
        st.code(hashtags)

        if st.button("Copy Hashtags"):
            st.toast("Hashtags copied to clipboard!")

    with col2:
        st.subheader("Video Details")
        st.markdown(f"**Brand:** {st.session_state.brand_name}")
        st.markdown(f"**Trend:** {st.session_state.selected_trend['title']}")
        st.markdown(f"**Platform:** {st.session_state.selected_platform}")
        st.markdown(f"**Duration:** {st.session_state.video_length} seconds")

    # Download button
    st.download_button(
        label="Download Video",
        data=b"sample video data",  # Would be actual video data in production
        file_name=f"{st.session_state.brand_name.replace(' ', '_')}_trend_video.mp4",
        mime="video/mp4",
        key="download_video",
    )

    # Share options
    share_col1, share_col2, share_col3 = st.columns(3)

    with share_col1:
        if st.button("Share to Instagram"):
            st.toast("Opening Instagram share...")

    with share_col2:
        if st.button("Share to TikTok"):
            st.toast("Opening TikTok share...")

    with share_col3:
        if st.button("Share to LinkedIn"):
            st.toast("Opening LinkedIn share...")


def main():
    """Main application function."""
    # Initialize session state if needed
    if "page" not in st.session_state:
        st.session_state.page = "trends"

    # Configure page settings
    configure_page_settings()

    # App header
    st.title("🚀 Trend-Aware Brand Video Generator")
    st.subheader("Auto-Capture What's Viral, Auto-Create What Sells")

    # Collect brand information in sidebar
    collect_brand_information()

    # Main content area
    if st.session_state.page == "trends":
        display_trends_page()
    elif st.session_state.page == "generation":
        display_generation_page()
    elif st.session_state.page == "results":
        display_results_page()

    # Footer
    st.markdown("---")
    st.caption("© 2023 Trend-Aware Brand Video Generator | MIT AI Hackathon")


def display_trends_page():
    """Display the trends selection page with tabs for each platform."""
    st.markdown("## Select a Trending Format")
    st.markdown(
        "Browse trending content formats from different platforms and select one "
        "that aligns with your brand."
    )

    # Create tabs for different platforms
    tabs = st.tabs(PLATFORMS)

    # Display trends for each platform in its tab
    for i, platform in enumerate(PLATFORMS):
        with tabs[i]:
            display_trends_for_platform(platform)

    # Navigation
    st.markdown("---")
    if hasattr(st.session_state, "selected_trend"):
        trend_info = (
            f"Selected: **{st.session_state.selected_trend['title']}** "
            f"from **{st.session_state.selected_platform}**"
        )
        st.success(trend_info)

        if st.button("Continue to Video Generation", type="primary"):
            st.session_state.page = "generation"
            st.rerun()
    else:
        st.info("👆 Please select a trend from one of the platforms above to continue")


def display_generation_page():
    """Display the video generation configuration page."""
    st.markdown("## Configure Your Brand Video")

    # Show selected trend information
    if hasattr(st.session_state, "selected_trend"):
        trend = st.session_state.selected_trend
        platform = st.session_state.selected_platform

        st.info(f"Creating video based on: **{trend['title']}** from **{platform}**")

        # Display trend preview
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                trend["image_url"],
                caption=f"Trend: {trend['title']}",
                use_container_width=True,
            )

        with col2:
            st.subheader("Trend Details")
            st.markdown(f"**Description:** {trend['description']}")
            st.markdown(f"**Engagement:** {trend['engagement']}")

            # Platform-specific details
            if platform == "TikTok":
                st.markdown(f"**Audio:** {trend['audio']}")
            elif platform == "LinkedIn":
                st.markdown(f"**Hashtags:** {trend['hashtags']}")
            elif platform == "Instagram":
                st.markdown(f"**Effect:** {trend['effect']}")

    # Advanced configuration options
    st.markdown("### Advanced Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.include_captions = st.checkbox(
            "Include Auto-Generated Captions",
            value=st.session_state.get("include_captions", True),
        )

        st.session_state.include_logo = st.checkbox(
            "Include Brand Logo", value=st.session_state.get("include_logo", True)
        )

    with col2:
        st.session_state.include_cta = st.checkbox(
            "Include Call-to-Action", value=st.session_state.get("include_cta", True)
        )

        if st.session_state.include_cta:
            st.session_state.cta_text = st.text_input(
                "Call-to-Action Text",
                value=st.session_state.get("cta_text", "Learn More"),
            )

    # Generate video button
    st.markdown("### Ready to Create Your Video?")

    generate_col1, generate_col2 = st.columns([3, 1])

    with generate_col1:
        if st.button("Generate Brand Video", type="primary", key="generate_video_btn"):
            with st.spinner("Creating your trend-aligned video..."):
                success = generate_video()
                if success:
                    st.session_state.page = "results"
                    st.rerun()

    with generate_col2:
        if st.button("← Back to Trends", key="back_to_trends_btn"):
            st.session_state.page = "trends"
            st.rerun()


def display_results_page():
    """Display the results page with the generated video."""
    st.markdown("## Your Trend-Aligned Brand Video")

    # Display the generated video and related information
    display_generated_video()

    # Analytics and insights
    st.markdown("### Predicted Performance")

    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

    with metrics_col1:
        st.metric(label="Est. Engagement Rate", value="4.8%", delta="2.1%")

    with metrics_col2:
        st.metric(label="Trend Alignment", value="92%", delta="High")

    with metrics_col3:
        st.metric(label="Brand Visibility", value="85%", delta="Good")

    with metrics_col4:
        st.metric(label="Viral Potential", value="76%", delta="Above Avg")

    # Recommendations
    st.markdown("### Recommendations")

    st.info(
        "🔍 **Posting Strategy:** Based on this trend, we recommend posting "
        f"this video on {st.session_state.selected_platform} between 6-8 PM "
        "when engagement for similar content is highest."
    )

    st.info(
        "🎯 **Audience Targeting:** This content is likely to resonate most with "
        "18-34 year old users interested in technology and innovation."
    )

    # Navigation buttons
    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 2])

    with nav_col1:
        if st.button("← Back to Generation", key="back_to_generation_btn"):
            st.session_state.page = "generation"
            st.rerun()

    with nav_col2:
        if st.button("Start Over", key="start_over_btn"):
            # Reset selected trend
            if hasattr(st.session_state, "selected_trend"):
                del st.session_state.selected_trend
            if hasattr(st.session_state, "selected_platform"):
                del st.session_state.selected_platform
            if hasattr(st.session_state, "generated_video"):
                del st.session_state.generated_video

            st.session_state.page = "trends"
            st.rerun()

    with nav_col3:
        if st.button(
            "Generate Another Video with Same Brand",
            key="another_video_btn",
            type="primary",
        ):
            if hasattr(st.session_state, "selected_trend"):
                del st.session_state.selected_trend
            if hasattr(st.session_state, "selected_platform"):
                del st.session_state.selected_platform
            if hasattr(st.session_state, "generated_video"):
                del st.session_state.generated_video

            st.session_state.page = "trends"
            st.rerun()


def initialize_session_state():
    """Initialize default values in session state."""
    defaults = {
        "brand_name": "",
        "brand_slogan": "",
        "brand_color": "#FF4B4B",
        "brand_secondary_color": "#4B4BFF",
        "video_length": 15,
        "tone": "Neutral",
        "video_format": "Short-form vertical",
        "include_captions": True,
        "include_logo": True,
        "include_cta": True,
        "cta_text": "Learn More",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


if __name__ == "__main__":
    try:
        # Initialize session state with defaults
        initialize_session_state()

        # Run the main application
        main()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}", exc_info=True)
