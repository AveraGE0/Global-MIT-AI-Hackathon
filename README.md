# 🌐 A2_TEAM: Global MIT AI Hackathon (Trend-Aware Brand Video Generator)

## 🏆 About the Hackathon

The Global MIT AI Hackathon brings together talented students from prestigious institutions worldwide, including MIT, Harvard, ETH Zurich, TUM, Oxford, and IIT Bombay. This 24-hour sprint focuses on accelerating learning and experimentation in cutting-edge AI methods, while building bridges between academic institutions, industry pioneers, and international organizations.

The hackathon features four distinct tracks:
- Agentic AI & Data Engineering
- Model Fine-Tuning & Adaptation
- **Rapid Prototyping & App Building** (chosen track)
- Small Model Deployment

## The Challenge: Trend-Aware Brand Video Generator (Task 15)

The Trend-Aware Brand Video Generator is an innovative AI-powered tool that helps brands create engaging, trend-aligned video content for social media platforms. This application automates the process of identifying current social media trends and generating branded promotional videos that leverage these trends to maximize engagement and reach.
### Key Features

- **Multi-Platform Trend Discovery**: Automatically identifies trending content from TikTok, LinkedIn, and Instagram
Displays trending hashtags with engagement metrics and visual previews
Provides platform-specific trend details (audio tracks, effects, hashtags)
TikTok Music Integration
- For TikTok videos, allows selection of trending songs to enhance content relevance
- Displays song previews, artist information, and usage statistics Integrates selected music into the final video production
- Brand Customization
- Collects essential brand information including name, product description, and logo 
- Offers **customizable video preferences** (length, tone, format)
- Supports multiple video formats: vertical, square, landscape, and carousel
- **Agentic, AI-Powered** Content Generation
- **Analyzes selected trends** using advanced AI agents
- Generates **tailored video prompts** based on brand and trend context
- Creates **platform-optimized captions** and hashtag recommendations
- Produces visually appealing videos that blend **brand identity** with **trending elements**
- Performance **Analytics**
- Provides engagement predictions and trend alignment metrics
- Offers strategic posting recommendations (timing, audience targeting)

## 🛠️ Installation & Setup

- Python version: 3.12
- Install dependencies with `pip install -r requirements.txt`
- Run the app via Streamlit: `python -m streamlit run src/ui/video_generation_app.py`

## Workflow

The application guides users through a streamlined four-step process:

- **Trend Selection**: Browse and select from current trending content across platforms
- **Song Selection**: For TikTok videos, choose a trending song that complements the selected trend
- **Video Configuration**: Customize video settings and brand elements
- **Video Generation**: AI-powered creation of trend-aligned branded video with caption and hashtags

## Technical Implementation

The application leverages several advanced technologies:

- **Streamlit** for the interactive user interface
- Custom **web scraping** modules for real-time trend data collection (e.g. TikTok)
- **Watson AI** for natural language processing and content generation
    - React framework, Langchain, Tool: google-search hosted on IBM-cloud
    - **Agentic web search** to accurately capture the meaning of trends for generation
- **Video generation capabilities** for producing the final content (WAN or via API-service providers)

## Why It Matters

Attention is the most expensive currency in marketing. This solution helps brands:

- Capitalize on social media momentum in real-time
- Radically increase engagement, visibility, and reach with minimal input
- Lower content creation costs by eliminating the need for agencies or human creators


Whether used to promote a local business, a global brand, or even this hackathon itself, this tool turns any brand into a viral storyteller overnight.