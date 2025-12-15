import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import time

# SECURE: Get API endpoints from Streamlit secrets ONLY
# These will NEVER be visible in the code or to users
try:
    ANI_LIST_API_URL = st.secrets["ANI_LIST_API_URL"]
    GOGO_ANIME_BASE_URL = st.secrets["GOGO_ANIME_BASE_URL"]
except Exception as e:
    st.error("⚠️ Configuration error. Please contact the administrator.")
    st.stop()

st.set_page_config(
    page_title="Lucifero - Anime Streamer",
    page_icon="👹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'anime_data' not in st.session_state:
    st.session_state.anime_data = None
if 'selected_anime' not in st.session_state:
    st.session_state.selected_anime = None
if 'streaming_url' not in st.session_state:
    st.session_state.streaming_url = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'trending'
if 'trending_anime' not in st.session_state:
    st.session_state.trending_anime = []

themes = {
    'dark': {
        'bg': '#0a0a0a',
        'secondary_bg': '#1a1a1a',
        'card_bg': '#2a2a2a',
        'text': '#ffffff',
        'accent': '#ff4444',
        'border': '#444444'
    },
    'light': {
        'bg': '#f5f5f5',
        'secondary_bg': '#ffffff',
        'card_bg': '#ffffff',
        'text': '#1a1a1a',
        'accent': '#cc0000',
        'border': '#e0e0e0'
    }
}

current_theme = themes[st.session_state.theme]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
    
    * {{
        box-sizing: border-box;
    }}
    
    .stApp {{
        background: {current_theme['bg']};
        color: {current_theme['text']};
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {current_theme['secondary_bg']};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {current_theme['accent']};
        border-radius: 5px;
    }}
    
    .ascii-art {{
        font-family: 'Courier New', monospace;
        text-align: center;
        color: {current_theme['accent']};
        font-size: clamp(6px, 2vw, 10px);
        line-height: 1.2;
        margin: 15px 0;
        animation: glow 2s ease-in-out infinite alternate;
        white-space: pre;
        overflow-x: auto;
    }}
    
    @keyframes glow {{
        from {{ text-shadow: 0 0 5px {current_theme['accent']}, 0 0 10px {current_theme['accent']}; }}
        to {{ text-shadow: 0 0 10px {current_theme['accent']}, 0 0 20px {current_theme['accent']}, 0 0 30px {current_theme['accent']}; }}
    }}
    
    .main-title {{
        font-family: 'Cinzel', serif;
        font-size: clamp(32px, 8vw, 72px);
        font-weight: 900;
        text-align: center;
        color: {current_theme['accent']};
        text-transform: uppercase;
        letter-spacing: clamp(2px, 1vw, 8px);
        margin: 15px 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        animation: titlePulse 3s ease-in-out infinite;
    }}
    
    @keyframes titlePulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
    }}
    
    .subtitle {{
        font-family: 'Libre Baskerville', serif;
        font-style: italic;
        text-align: center;
        color: {current_theme['text']};
        font-size: clamp(14px, 3vw, 18px);
        margin-bottom: 20px;
        opacity: 0.8;
    }}
    
    .anime-card {{
        background: {current_theme['card_bg']};
        border: 2px solid {current_theme['border']};
        border-radius: 12px;
        overflow: hidden;
        margin: 10px 0;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
    }}
    
    .anime-card:hover {{
        transform: translateY(-5px);
        border-color: {current_theme['accent']};
        box-shadow: 0 8px 25px rgba(255, 68, 68, 0.3);
    }}
    
    .anime-card-img {{
        width: 100%;
        height: 0;
        padding-bottom: 140%;
        position: relative;
        overflow: hidden;
        background: {current_theme['secondary_bg']};
    }}
    
    .anime-card-img img {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
    }}
    
    .anime-info {{
        padding: 12px;
    }}
    
    .anime-title {{
        font-family: 'Libre Baskerville', serif;
        font-size: clamp(12px, 2vw, 16px);
        font-weight: 700;
        color: {current_theme['text']};
        margin-bottom: 8px;
        line-height: 1.3;
        height: 42px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }}
    
    .anime-meta {{
        font-size: clamp(10px, 1.5vw, 12px);
        color: {current_theme['text']};
        opacity: 0.6;
        font-family: 'Courier New', monospace;
        line-height: 1.5;
    }}
    
    .score-badge {{
        display: inline-block;
        background: {current_theme['accent']};
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: clamp(10px, 1.5vw, 12px);
        margin-top: 5px;
    }}
    
    .section-header {{
        font-family: 'Cinzel', serif;
        font-size: clamp(20px, 4vw, 28px);
        color: {current_theme['accent']};
        text-align: center;
        margin: 30px 0 20px 0;
        text-transform: uppercase;
        letter-spacing: clamp(1px, 0.5vw, 3px);
    }}
    
    .video-container {{
        position: relative;
        width: 100%;
        height: 0;
        padding-bottom: 56.25%;
        margin: 20px auto;
        background: #000;
        border-radius: 12px;
        overflow: hidden;
        max-width: 100%;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }}
    
    .video-container iframe {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }}
    
    .stButton button {{
        background: {current_theme['accent']};
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-family: 'Libre Baskerville', serif;
        font-weight: bold;
        transition: all 0.3s ease;
        font-size: clamp(12px, 2vw, 14px);
        width: 100%;
    }}
    
    .stButton button:hover {{
        background: {current_theme['text']};
        color: {current_theme['bg']};
        transform: scale(1.05);
    }}
    
    .stTextInput input {{
        background: {current_theme['secondary_bg']};
        color: {current_theme['text']};
        border: 2px solid {current_theme['border']};
        border-radius: 8px;
        padding: 12px;
        font-family: 'Libre Baskerville', serif;
        font-size: clamp(12px, 2vw, 14px);
    }}
    
    .stTextInput input:focus {{
        border-color: {current_theme['accent']};
    }}
    
    .error-box {{
        background: rgba(255, 68, 68, 0.1);
        border: 2px solid {current_theme['accent']};
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }}
    
    @media (max-width: 768px) {{
        .anime-card {{
            margin: 8px 0;
        }}
        
        .anime-info {{
            padding: 10px;
        }}
        
        .section-header {{
            margin: 20px 0 15px 0;
        }}
        
        .video-container {{
            border-radius: 8px;
        }}
        
        .stButton button {{
            padding: 8px 16px;
        }}
    }}
    
    @media (max-width: 480px) {{
        .anime-card-img {{
            padding-bottom: 150%;
        }}
        
        .anime-title {{
            height: 38px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

ascii_art = """
    ⟨⟨ 𝕷𝖀𝕮𝕴𝕱𝕰𝕽𝕺 ⟩⟩
    
    ▓▓▓▒▒▒▒ ANIME STREAMER ▒▒▒▒▓▓▓
"""

st.markdown(f'<div class="ascii-art">{ascii_art}</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">LUCIFERO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Il Diavolo dell\'Anime</div>', unsafe_allow_html=True)

col_toggle1, col_toggle2, col_toggle3 = st.columns([4, 1, 4])
with col_toggle2:
    if st.button("🌓 THEME", key="theme_toggle"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

nav_cols = st.columns(3)
with nav_cols[0]:
    if st.button("🔥 TRENDING", key="nav_trending", use_container_width=True):
        st.session_state.current_page = 'trending'
        st.rerun()
with nav_cols[1]:
    if st.button("🔍 SEARCH", key="nav_search", use_container_width=True):
        st.session_state.current_page = 'search'
        st.rerun()
with nav_cols[2]:
    if st.button("▶️ PLAYER", key="nav_player", use_container_width=True):
        st.session_state.current_page = 'player'
        st.rerun()

st.markdown("---")

def get_anilist_trending():
    """Fetch trending anime from AniList API"""
    anilist_query = '''
    query {
        Page(page: 1, perPage: 24) {
            media(sort: TRENDING_DESC, type: ANIME, status: RELEASING) {
                id
                title {
                    romaji
                    english
                }
                coverImage {
                    large
                    extraLarge
                }
                averageScore
                episodes
                status
            }
        }
    }
    '''
    
    try:
        response = requests.post(
            ANI_LIST_API_URL, 
            json={'query': anilist_query}, 
            timeout=15,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        data = response.json().get('data', {}).get('Page', {}).get('media', [])
        
        trending = []
        for anime in data:
            title = anime['title']['english'] or anime['title']['romaji']
            trending.append({
                'title': title,
                'image': anime['coverImage']['extraLarge'] or anime['coverImage']['large'],
                'score': anime.get('averageScore', 'N/A'),
                'episodes': anime.get('episodes', 'N/A'),
                'status': anime.get('status', 'N/A'),
                'anilist_id': anime['id']
            })
        
        return trending
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return []
    except requests.exceptions.RequestException as e:
        st.error("❌ Network error. Please check your connection.")
        return []
    except Exception as e:
        st.error("❌ Error loading trending anime. Please try again later.")
        return []

def search_gogoanime(title):
    """Search for anime on streaming server"""
    try:
        search_title = re.sub(r'[^\w\s]', '', title).strip()
        search_url = f"{GOGO_ANIME_BASE_URL}/search?keyword={search_title.replace(' ', '+')}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": GOGO_ANIME_BASE_URL
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='film-poster')
        
        if results:
            first_result = results[0].find('a', class_='film-poster-ahref')
            if first_result and first_result.get('href'):
                anime_url = first_result['href']
                if anime_url.startswith('/'):
                    anime_url = GOGO_ANIME_BASE_URL + anime_url
                
                anime_id_match = re.search(r'/([^/]+-\d+)$', anime_url)
                if anime_id_match:
                    return anime_id_match.group(1)
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Search timed out. Please try again.")
        return None
    except Exception as e:
        st.error("❌ Search failed. Please try again later.")
        return None

def get_episodes_from_api(anime_id):
    """Fetch episode list for an anime"""
    api_url = f"{GOGO_ANIME_BASE_URL}/get_episodes?id={anime_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"{GOGO_ANIME_BASE_URL}/anime/{anime_id}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        if not data.get('success', False) or not data.get('episodes'):
            return []
        return data['episodes']
    except Exception as e:
        st.error("❌ Failed to load episodes.")
        return []

def search_anime(anime_name):
    """Search anime by name"""
    search_url = f"{GOGO_ANIME_BASE_URL}/search?keyword={anime_name.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": GOGO_ANIME_BASE_URL
    }
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        st.error("❌ Search failed. Please try again.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='film-poster')
    search_results = []
    
    for result in results[:24]:
        first_result = result.find('a', class_='film-poster-ahref')
        if first_result and first_result.get('href'):
            anime_url = first_result['href']
            if anime_url.startswith('/'):
                anime_url = GOGO_ANIME_BASE_URL + anime_url
            
            anime_id_match = re.search(r'/([^/]+-\d+)$', anime_url)
            if anime_id_match:
                anime_id = anime_id_match.group(1)
                title_elem = result.find('img')
                title = title_elem.get('alt', 'Unknown Title') if title_elem else 'Unknown Title'
                image = title_elem.get('src', '') if title_elem else ''
                
                result_data = {
                    'title': title,
                    'anime_id': anime_id,
                    'anime_url': anime_url,
                    'image': image
                }
                
                if not any(existing['anime_id'] == anime_id for existing in search_results):
                    search_results.append(result_data)
    
    return search_results

def get_streaming_url(anime_id, episode_id):
    """Generate streaming URL for an episode"""
    return f"{GOGO_ANIME_BASE_URL}/streaming.php?id={anime_id}&ep={episode_id}&server=hd-1&type=sub"

# TRENDING PAGE
if st.session_state.current_page == 'trending':
    st.markdown('<div class="section-header">TRENDING ANIME</div>', unsafe_allow_html=True)
    
    if not st.session_state.trending_anime:
        with st.spinner("🔄 Loading trending anime..."):
            st.session_state.trending_anime = get_anilist_trending()
    
    if st.session_state.trending_anime:
        cols_per_row = 4
        for i in range(0, len(st.session_state.trending_anime), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(st.session_state.trending_anime):
                    anime = st.session_state.trending_anime[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="anime-card">
                            <div class="anime-card-img">
                                <img src="{anime['image']}" alt="{anime['title']}">
                            </div>
                            <div class="anime-info">
                                <div class="anime-title">{anime['title']}</div>
                                <div class="anime-meta">
                                    <span class="score-badge">⭐ {anime.get('score', 'N/A')}</span><br>
                                    Episodes: {anime.get('episodes', 'N/A')}<br>
                                    Status: {anime.get('status', 'N/A')}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("▶️ STREAM", key=f"trending_{i}_{j}"):
                            with st.spinner("🔄 Connecting to server..."):
                                anime_id = search_gogoanime(anime['title'])
                                if anime_id:
                                    st.session_state.selected_anime = {
                                        'title': anime['title'],
                                        'anime_id': anime_id,
                                        'image': anime['image']
                                    }
                                    st.session_state.anime_data = get_episodes_from_api(anime_id)
                                    st.session_state.current_page = 'player'
                                    st.rerun()
                                else:
                                    st.error("❌ Anime not found on streaming server")
    else:
        st.markdown("""
        <div class="error-box">
            <h3>⚠️ Unable to load trending anime</h3>
            <p>Please check your internet connection and try refreshing the page.</p>
        </div>
        """, unsafe_allow_html=True)

# SEARCH PAGE
elif st.session_state.current_page == 'search':
    st.markdown('<div class="section-header">SEARCH ANIME</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("", placeholder="Enter anime name...", label_visibility="collapsed")
    with col2:
        search_btn = st.button("🔍 SEARCH", use_container_width=True)
    
    if search_btn and search_term:
        with st.spinner("🔄 Searching..."):
            results = search_anime(search_term)
            st.session_state.search_results = results
    
    if st.session_state.search_results:
        st.markdown(f'<div class="section-header">📊 {len(st.session_state.search_results)} RESULTS FOUND</div>', unsafe_allow_html=True)
        
        cols_per_row = 4
        for i in range(0, len(st.session_state.search_results), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(st.session_state.search_results):
                    result = st.session_state.search_results[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="anime-card">
                            <div class="anime-card-img">
                                <img src="{result['image']}" alt="{result['title']}">
                            </div>
                            <div class="anime-info">
                                <div class="anime-title">{result['title']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("✅ SELECT", key=f"select_{i}_{j}"):
                            st.session_state.selected_anime = result
                            st.session_state.anime_data = get_episodes_from_api(result['anime_id'])
                            st.session_state.current_page = 'player'
                            st.rerun()

# PLAYER PAGE
elif st.session_state.current_page == 'player':
    if st.session_state.streaming_url:
        st.markdown('<div class="section-header">NOW STREAMING</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="video-container">
            <iframe src="{st.session_state.streaming_url}" allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("❌ CLOSE PLAYER"):
            st.session_state.streaming_url = None
            st.rerun()
        st.markdown("---")
    
    if st.session_state.selected_anime:
        st.markdown(f'<div class="section-header">{st.session_state.selected_anime["title"]}</div>', unsafe_allow_html=True)
        
        if st.session_state.anime_data:
            st.markdown(f'<div class="anime-meta" style="text-align: center; margin: 20px 0; font-size: clamp(14px, 2vw, 16px);">📺 AVAILABLE EPISODES: {len(st.session_state.anime_data)}</div>', unsafe_allow_html=True)
            
            eps_per_row = 6
            for i in range(0, len(st.session_state.anime_data), eps_per_row):
                cols = st.columns(eps_per_row)
                for j in range(eps_per_row):
                    if i + j < len(st.session_state.anime_data):
                        episode = st.session_state.anime_data[i + j]
                        with cols[j]:
                            if st.button(f"EP {episode['chapter_number']}", key=f"ep_{episode['s_id']}", use_container_width=True):
                                anime_id = st.session_state.selected_anime['anime_id']
                                st.session_state.streaming_url = get_streaming_url(anime_id, episode['s_id'])
                                st.rerun()
        else:
            st.markdown("""
            <div class="error-box">
                <h3>⚠️ No episodes available</h3>
                <p>This anime may not be available for streaming yet.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👈 Select an anime from Trending or Search to start watching")

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; font-family: 'Libre Baskerville', serif; opacity: 0.6; margin: 30px 0; font-size: clamp(12px, 2vw, 14px);">
    LUCIFERO © 2024 | Made with ❤️ for Anime Fans
</div>
""", unsafe_allow_html=True)