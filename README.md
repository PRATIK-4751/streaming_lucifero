# Lucifero - Anime Streamer

A Streamlit-based anime streaming application that fetches trending anime data and provides streaming links.

## Environment Variables Setup

This application requires two environment variables to function properly:

1. `ANI_LIST_API_URL` - GraphQL endpoint for anime data (default: https://graphql.anilist.co)
2. `GOGO_ANIME_BASE_URL` - Base URL for anime streaming (default: https://gogoanime.com.by)

### For Local Development

Copy the `.env.example` file to `.env` and populate with your own values:

```bash
cp .env.example .env
```

Edit the `.env` file and replace the placeholder values with the actual API endpoints.

**Important:** The `.env` file is included in `.gitignore` and will not be committed to the repository, keeping your configuration secure.

### For Streamlit Cloud Deployment

Streamlit Cloud does not use `.env` files. You must set environment variables in the Streamlit Cloud dashboard:

1. Go to your Streamlit app settings in the Streamlit Cloud dashboard
2. Navigate to the "Secrets" section
3. Add the following environment variables:

```
ANI_LIST_API_URL = "https://graphql.anilist.co"
GOGO_ANIME_BASE_URL = "https://gogoanime.com.by"
```

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (as described above)

3. Run the application:
   ```bash
   streamlit run main.py
   ```

## Dependencies

- Streamlit 1.31.0
- Requests 2.31.0
- Beautiful Soup 4.12.2
- Python Dotenv 1.0.0

## Security Note

Never commit `.env` files to version control. The `.env` file is already added to `.gitignore` to prevent accidental commits of sensitive information.