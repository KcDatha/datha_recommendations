import streamlit as st
import pickle
import requests
import random

# Load the data
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies_list = movies["title"].values

# TMDB API key
API_KEY = "30c33629725f632ec3ee2e1d59030dab"

# Function to fetch movie posters and details
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster_url = "https://via.placeholder.com/500x750?text=No+Image"
        return {
            "poster": poster_url,
            "overview": data.get("overview", "No overview available."),
            "rating": data.get("vote_average", "N/A"),
            "release_date": data.get("release_date", "Unknown"),
            "genres": ", ".join([genre['name'] for genre in data.get('genres', [])])
        }
    except Exception:
        return {
            "poster": "https://via.placeholder.com/500x750?text=Error",
            "overview": "No overview available.",
            "rating": "N/A",
            "release_date": "Unknown",
            "genres": "Unknown"
        }

# Function to fetch random movies for the homepage
def get_random_movies(num_movies=5):
    random_indices = random.sample(range(len(movies)), num_movies)
    random_movies = []
    for idx in random_indices:
        movie_id = movies.iloc[idx].id
        details = fetch_movie_details(movie_id)
        random_movies.append({
            "title": movies.iloc[idx].title,
            "poster": details["poster"],
            "overview": details["overview"],
            "rating": details["rating"],
            "release_date": details["release_date"],
            "genres": details["genres"]
        })
    return random_movies

# Function to recommend movies
def recommend(movie):
    try:
        if movie not in movies['title'].values:
            return []
            
        movie_index = movies[movies['title'] == movie].index[0]
        movie_id = movies.iloc[movie_index].id
        
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        
        if response.status_code != 200:
            return []
            
        data = response.json()
        
        if not data.get('results'):
            return []
        
        recommended_movies = []
        for movie in data['results'][:5]:
            details = fetch_movie_details(movie['id'])
            details['title'] = movie.get('title', 'Unknown Title')
            recommended_movies.append(details)
        
        return recommended_movies
        
    except Exception as e:
        return []

# Streamlit layout settings
st.set_page_config(page_title="🎥 Movie Recommender", layout="wide")

# Inject custom CSS for advanced UI
def add_custom_css():
    st.markdown("""
        <style>
            /* Modern clean background */
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #ffffff, #f0f0f0);
                color: #000000;
            }
            
            /* Enhanced header with light skyblue gradient */
            .header {
                text-align: center;
                padding: 2.5rem;
                background: linear-gradient(120deg, #87CEEB, #B0E0E6);
                border-radius: 16px;
                margin: 1.5rem 0;
                box-shadow: 0 4px 15px rgba(135, 206, 235, 0.2);
            }
            
            .header h1 {
                color: #000000;
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }
            
            .header p {
                color: #1a1a1a;
                font-size: 1.2rem;
                font-weight: 500;
                margin-top: 0.5rem;
            }
            
            /* Movie details section */
            .movie-details {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 16px;
                padding: 2rem;
                color: #000000;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            
            .movie-details h1 {
                color: #000000;
                font-weight: 600;
            }
            
            /* Tags styling */
            .tag {
                background: rgba(240, 240, 240, 0.9);
                border: 1px solid rgba(0, 0, 0, 0.1);
                color: #000000;
                padding: 0.4rem 1rem;
                border-radius: 20px;
                display: inline-block;
                margin: 0.2rem;
                font-weight: 500;
            }
            
            /* Overview section */
            .overview {
                color: #000000;
                line-height: 1.6;
                margin-top: 1rem;
                background: rgba(248, 249, 250, 0.9);
                padding: 1rem;
                border-radius: 10px;
            }
            
            /* Section headers */
            .section-header {
                text-align: center;
                padding: 1.5rem;
                margin-bottom: 2rem;
                background: linear-gradient(to right, #3b82f6, #60a5fa);
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .section-header h2 {
                color: white;
                font-size: 2rem;
                font-weight: bold;
                margin: 0;
                margin-bottom: 0.5rem;
            }
            
            .section-header p {
                color: rgba(255, 255, 255, 0.9);
                font-size: 1.1rem;
                margin: 0;
            }
            
            /* Movie ratings and genres text */
            .stMarkdown {
                color: #000000 !important;
            }
            
            /* Button styling */
            .stButton > button {
                background: #ffffff;
                color: #000000;
                border: 1px solid rgba(0, 0, 0, 0.1);
                font-weight: 500;
            }
            
            /* Top search section */
            .top-search {
                margin: 2rem 0;
                text-align: center;
            }
            
            .movie-list {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                padding: 1rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .movie-list .stButton button {
                width: 100%;
                text-align: left;
                background: transparent;
                border: none;
                padding: 0.5rem 1rem;
                margin: 0.2rem 0;
                color: #000000;
                font-size: 1rem;
                transition: background-color 0.3s;
            }
            
            .movie-list .stButton button:hover {
                background-color: rgba(135, 206, 235, 0.2);
                border-radius: 5px;
            }
            
            /* Quick recommendations styling */
            .quick-recommendations {
                display: none;
            }
            
            .stButton button {
                background: none;
                border: none;
                color: #000000;
                padding: 0.5rem;
                font-size: 0.95rem;
                text-decoration: none;
                margin: 0.2rem 0;
                cursor: pointer;
                width: 100%;
                text-align: center;
                border-radius: 4px;
                transition: all 0.2s;
            }
            
            .stButton button:hover {
                background: rgba(135, 206, 235, 0.2);
                color: #3b82f6;
            }
            
            .movie-names {
                padding: 0.5rem 1rem;
                line-height: 1.5;
            }
            
            .movie-names .stButton button {
                background: none;
                border: none;
                color: #000000;
                padding: 0;
                font-size: 0.95rem;
                text-decoration: none;
                margin: 0;
                cursor: pointer;
                display: inline;
            }
            
            .movie-names .stButton button:hover {
                color: #3b82f6;
                text-decoration: underline;
            }
            
            .separator {
                color: #000000;
                margin: 0 0.2rem;
            }
            
            /* Recommendations styling */
            .recommendations-header {
                margin: 2rem 0 1rem 0;
                padding: 1rem;
                background: rgba(135, 206, 235, 0.1);
                border-radius: 8px;
                text-align: center;
            }
            
            .recommendations-header h2 {
                color: #000000;
                font-size: 1.5rem;
                margin: 0;
            }
            
            .recommendations-grid {
                margin: 1rem 0;
                padding: 1rem;
            }
            
            .movie-card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 0.8rem;
                margin-top: 0.5rem;
                transition: transform 0.2s;
            }
            
            .movie-card:hover {
                transform: translateY(-5px);
            }
            
            .movie-title {
                font-size: 1rem;
                font-weight: bold;
                color: #000000;
                margin-bottom: 0.5rem;
            }
            
            .movie-info {
                display: flex;
                flex-direction: column;
                gap: 0.3rem;
            }
            
            .rating, .genres {
                font-size: 0.9rem;
                color: #000000;
            }
            
            img {
                pointer-events: none;
                max-width: 100%;
                height: auto;
            }
            
            .stImage {
                pointer-events: none;
            }
            
            /* Disable image click and expand */
            img {
                pointer-events: none !important;
            }
            
            button[title="View fullscreen"] {
                display: none !important;
            }
            
            .stImage > div > div {
                pointer-events: none !important;
            }
            
            /* Remove image overlay on hover */
            .stImage:hover::before {
                display: none !important;
            }
            
            .stImage > img {
                pointer-events: none !important;
            }
            
            .quick-recommendations .movie-poster {
                margin-bottom: 0.5rem;
            }
            
            .quick-recommendations .movie-card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 0.8rem;
                margin-bottom: 1rem;
            }
            
            .quick-recommendations .movie-title {
                font-size: 1rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            
            .quick-recommendations .movie-info {
                display: flex;
                flex-direction: column;
                gap: 0.3rem;
            }
            
            .quick-recommendations button {
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                background: transparent;
                border: none;
                cursor: pointer;
                z-index: 1;
            }
            
            .quick-recommendations .stButton {
                position: relative;
                margin: 0;
                padding: 0;
            }
            
            .quick-recommendations .movie-card {
                position: relative;
                transition: transform 0.2s;
            }
            
            .quick-recommendations .stButton:hover .movie-card {
                transform: translateY(-5px);
            }
            
            /* Search Results Styling */
            .search-results-header {
                background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
                color: white;
                padding: 1rem 2rem;
                border-radius: 10px;
                margin: 2rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .search-results-header h2 {
                margin: 0;
                font-size: 1.5rem;
            }
            
            .search-movie-card {
                background: white;
                border-radius: 12px;
                padding: 1rem;
                margin: 0.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s, box-shadow 0.2s;
                position: relative;
            }
            
            .search-movie-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
            }
            
            .search-movie-card .movie-poster {
                border-radius: 8px;
                overflow: hidden;
                margin-bottom: 1rem;
            }
            
            .search-movie-card .movie-details {
                padding: 0.5rem;
            }
            
            .search-movie-card .movie-title {
                font-size: 1rem;
                font-weight: bold;
                color: #1f2937;
                margin-bottom: 0.5rem;
            }
            
            .search-movie-card .movie-info {
                display: flex;
                flex-direction: column;
                gap: 0.3rem;
            }
            
            .search-movie-card .rating,
            .search-movie-card .genres {
                font-size: 0.9rem;
                color: #4b5563;
            }
            
            /* Make entire card clickable */
            .search-movie-card button {
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                background: transparent;
                border: none;
                cursor: pointer;
                z-index: 1;
            }
            
            .movie-poster {
                position: relative;
                overflow: hidden;
                border-radius: 8px;
            }
            
            .movie-poster img {
                width: 100%;
                height: auto;
                display: block;
            }
            
            /* Hide fullscreen button and disable interactions */
            .movie-poster button,
            .movie-poster [data-testid="stImage"] > div > div:last-child {
                display: none !important;
            }
            
            /* Search Bar Styling */
            .stTextInput > div > div > input {
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 12px 16px;
                background-color: white;
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .stTextInput > div > div > input:focus {
                border-color: rgb(59, 130, 246);
                box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
                outline: none;
            }
            
            .stTextInput > div > div > input:hover {
                border-color: rgb(147, 197, 253);
            }
            
            /* Search icon and placeholder styling */
            .stTextInput > div > div > input::placeholder {
                color: rgb(107, 114, 128);
                font-weight: bold;
                opacity: 0.8;
            }
            
            /* Label styling */
            .stTextInput label {
                font-weight: bold !important;
                color: rgb(31, 41, 55) !important;
            }
        </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Initialize session state at the beginning of the file
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

# Header Section
st.markdown("""
    <div class="header">
        <h1>🎬 Movie Magic</h1>
        <p>Discover Your Next Favorite Movie</p>
    </div>
""", unsafe_allow_html=True)

# Search input with custom styling
movie_search = st.text_input("", placeholder="🔍 Search for movies...", key="movie_search")

# Show search results if there's a search query
if movie_search:
    with st.spinner('Searching for movies...'):
        matching_movies = []
        search_term = movie_search.lower()
        
        for title in movies_list:
            if search_term in title.lower():
                movie_index = movies[movies['title'] == title].index[0]
                movie_id = movies.iloc[movie_index].id
                details = fetch_movie_details(movie_id)
                details['title'] = title
                details['id'] = movie_id
                matching_movies.append(details)
        
        if matching_movies:
            st.markdown("""
                <div class="search-results-header">
                    <h2>🔍 Search Results</h2>
                </div>
            """, unsafe_allow_html=True)
            
            cols = st.columns(5)
            for idx, movie in enumerate(matching_movies[:5]):
                with cols[idx]:
                    # Make the entire card clickable
                    if st.button("", key=f"search_{idx}_{hash(movie['title'])}"):
                        st.session_state.selected_movie = movie
                        st.rerun()
                    
                    st.markdown(f'<div class="search-movie-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="movie-poster">', unsafe_allow_html=True)
                    st.image(movie['poster'], use_container_width=True, output_format='JPEG')
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="movie-details">
                            <div class="movie-title">{movie['title']}</div>
                            <div class="movie-info">
                                <span class="rating">⭐ {movie['rating']}</span>
                                <span class="genres">🎭 {movie['genres']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("🔍 No movies found matching your search.")

# Only show popular movies if no movie is selected and no search is active
elif not st.session_state.selected_movie:
    st.markdown("""
        <div class="section-header">
            <h2>🎬 Popular Movies</h2>
            <p>Discover trending movies that everyone's watching</p>
        </div>
    """, unsafe_allow_html=True)

    sample_movies = random.sample(list(movies_list), 12)
    cols = st.columns(4)

    for idx, movie_title in enumerate(sample_movies):
        with cols[idx % 4]:
            movie_index = movies[movies['title'] == movie_title].index[0]
            movie_id = movies.iloc[movie_index].id
            details = fetch_movie_details(movie_id)
            
            # Make the entire card clickable
            if st.button("", key=f"popular_{hash(movie_title)}", help="Click to see details"):
                details['title'] = movie_title
                details['id'] = movie_id
                st.session_state.selected_movie = details
                st.rerun()
            
            # Display movie poster and details
            st.markdown(f'<div class="movie-poster">', unsafe_allow_html=True)
            st.image(details['poster'], use_container_width=True, output_format='JPEG')
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-title">{movie_title}</div>
                    <div class="movie-info">
                        <span class="rating">⭐ {details['rating']}</span>
                        <span class="genres">🎭 {details['genres']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Show detailed view when a movie is selected
if st.session_state.selected_movie:
    movie = st.session_state.selected_movie
    
    if st.button("← Back"):
        st.session_state.selected_movie = None
        st.rerun()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f'<div class="movie-poster">', unsafe_allow_html=True)
        st.image(movie['poster'], use_container_width=True, output_format='JPEG')
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.title(movie['title'])
        st.markdown(f'<span class="tag">⭐ {movie["rating"]}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="tag">📅 {movie["release_date"]}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="tag">🎭 {movie["genres"]}</span>', unsafe_allow_html=True)
        st.markdown('<div class="overview">', unsafe_allow_html=True)
        st.markdown("**Overview:**")
        st.write(movie['overview'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show recommendations
    st.markdown("""
        <div class="recommendations-header">
            <h2>Similar Movies You Might Like</h2>
        </div>
    """, unsafe_allow_html=True)
    
    recommended_movies = recommend(movie['title'])
    
    if recommended_movies:
        st.markdown('<div class="recommendations-grid">', unsafe_allow_html=True)
        cols = st.columns(5)
        for idx, rec_movie in enumerate(recommended_movies):
            with cols[idx]:
                st.markdown(f'<div class="movie-poster">', unsafe_allow_html=True)
                st.image(rec_movie['poster'], use_container_width=True, output_format='JPEG')
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="movie-card">
                        <div class="movie-title">{rec_movie['title']}</div>
                        <div class="movie-info">
                            <span class="rating">⭐ {rec_movie['rating']}</span>
                            <span class="genres">🎭 {rec_movie['genres']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("More Info", key=f"rec_{idx}_{hash(rec_movie['title'])}"):
                    st.session_state.selected_movie = rec_movie
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
