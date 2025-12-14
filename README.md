# Lucifero - Anime Streamer

A Streamlit web application for streaming anime content with a dark theme interface.

## Features
- Trending anime from AniList API
- Search functionality for finding specific anime
- Embedded video player for streaming episodes
- Dark/Light theme toggle
- Responsive design for all devices

## Dependencies
All required packages are listed in `requirements.txt`.

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Environment Variables

This application uses environment variables for API endpoints. Copy the `.env.example` file to `.env` and update the values with your own endpoints.

## Running the Application

To run the Streamlit app locally:
```
streamlit run main.py
```

## Deployment

This app can be deployed to various platforms including:
- Streamlit Cloud
- Heroku
- AWS
- Google Cloud Platform

For Streamlit Cloud deployment:
1. Push this repository to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Select `main.py` as the entry point
5. Add the required environment variables in the Secrets section
6. Deploy the app