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

This application requires certain environment variables to function properly. To set them up:

1. Copy the `.env.example` file to create a new file named `.env`:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file and replace the placeholder values with your actual API endpoints:
   ```
   ANI_LIST_API_URL=your_anilist_api_endpoint_here
   GOGO_ANIME_BASE_URL=your_gogoanime_base_url_here
   ```

**Important:** The `.env` file is included in `.gitignore` and will not be committed to the repository, keeping your credentials secure.

## Running the Application

To run the Streamlit app locally:
```
streamlit run main.py
```

## Deployment

### Streamlit Cloud Deployment (Recommended):

1. Push this repository to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Select `main.py` as the entry point
5. Add the required environment variables in the Secrets section:
   - `ANI_LIST_API_URL` = `your_anilist_api_endpoint_here`
   - `GOGO_ANIME_BASE_URL` = `your_gogoanime_base_url_here`
6. Deploy the app

### Heroku Deployment:

1. Install the Heroku CLI and log in
2. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```
3. Set the environment variables:
   ```
   heroku config:set ANI_LIST_API_URL=your_anilist_api_endpoint_here
   heroku config:set GOGO_ANIME_BASE_URL=your_gogoanime_base_url_here
   ```
4. Deploy the app:
   ```
   git push heroku main
   ```

### Troubleshooting Deployment Issues:

If you encounter "installer returned a non-zero exit code" error:

1. Ensure all environment variables are properly set
2. Check that your `requirements.txt` file is correctly formatted
3. Verify that your `Procfile` contains:
   ```
   web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
   ```
4. Make sure your application can run without interactive input