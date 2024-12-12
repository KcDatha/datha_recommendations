import streamlit as st
import pickle
import requests
import random

# This MUST be the first Streamlit command
st.set_page_config(page_title="🎥 Movie Recommender", layout="wide")

# Now you can have other Streamlit commands
try:
    movies = pickle.load(open("movies_list.pkl", "rb"))
    movies_list = movies["title"].values
except Exception as e:
    st.error(f"Error loading movies data: {e}")

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

# Function to fetch cast information
def fetch_movie_cast(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
        response = requests.get(url).json()
        cast = response.get('cast', [])
        # Get top 5 cast members
        main_cast = [actor['name'] for actor in cast[:5]]
        return main_cast
    except Exception:
        return ["Cast information not available"]

# Function to fetch random movies for the homepage
def get_random_movies(num_movies=20):
    random_indices = random.sample(range(len(movies)), num_movies)
    random_movies = []
    for idx in random_indices:
        movie_id = movies.iloc[idx].id
        details = fetch_movie_details(movie_id)
        cast = fetch_movie_cast(movie_id)
        random_movies.append({
            "title": movies.iloc[idx].title,
            "poster": details["poster"],
            "overview": details["overview"],
            "rating": details["rating"],
            "release_date": details["release_date"],
            "genres": details["genres"],
            "cast": cast,
            "id": movie_id
        })
    return random_movies

# Function to recommend movies
def recommend(movie):
    try:
        # Add debug print to check if movie exists in DataFrame
        if movie not in movies['title'].values:
            st.warning(f"Movie '{movie}' not found in database")
            return []
            
        # Get movie ID
        movie_index = movies[movies['title'] == movie].index[0]
        movie_id = movies.iloc[movie_index].id
        
        # Add debug print for API call
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        
        # Check API response status
        if response.status_code != 200:
            st.warning(f"TMDB API error: {response.status_code}")
            return []
            
        data = response.json()
        
        # Check if we got any recommendations
        if not data.get('results'):
            st.info("No recommendations found for this movie")
            return []
        
        recommended_movies = []
        for movie in data['results'][:5]:  # Get top 5 recommendations
            details = fetch_movie_details(movie['id'])
            details['title'] = movie.get('title', 'Unknown Title')  # Add title to details
            recommended_movies.append(details)
        
        return recommended_movies
        
    except Exception as e:
        st.error(f"Recommendation error: {str(e)}")
        return []

# Function to fetch movies by actor
def fetch_movies_by_actor(actor_name):
    try:
        # First, get the actor's ID
        search_url = f"https://api.themoviedb.org/3/search/person?api_key={API_KEY}&query={actor_name}"
        search_response = requests.get(search_url).json()
        
        if not search_response.get('results'):
            return []
            
        actor_id = search_response['results'][0]['id']
        
        # Then, get their complete movie credits
        credits_url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={API_KEY}"
        credits_response = requests.get(credits_url).json()
        
        # Get movies where they were part of the cast (not crew)
        movies = credits_response.get('cast', [])
        
        # Sort by popularity and get top 15 movies
        movies.sort(key=lambda x: x.get('popularity', 0), reverse=True)
        movies = movies[:15]
        
        # Format the results
        formatted_movies = []
        for movie in movies:
            if movie.get('title') and movie.get('id'):
                poster = fetch_movie_details(movie['id'])['poster']
                formatted_movies.append((movie['title'], poster))
                
        return formatted_movies
        
    except Exception as e:
        st.error(f"Error fetching actor movies: {str(e)}")
        return []

# Inject custom CSS for advanced UI
def add_custom_css():
    st.markdown("""
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1f1c2c, #928dab);
                color: white;
            }

            /* Header styles */
            .header {
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                color: white;
                border-radius: 8px;
                margin-bottom: 30px;
            }

            /* Movie cards in a row */
            .movie-row {
                display: flex;
                overflow-x: auto;
                gap: 20px;
                padding: 10px 0;
                margin-bottom: 30px;
            }

            .movie-card {
                flex: 0 0 auto;
                background: #2c2c54;
                border-radius: 12px;
                padding: 10px;
                width: 200px;
                text-align: center;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .movie-card:hover {
                transform: scale(1.1);
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.4);
            }

            .movie-card img {
                border-radius: 8px;
                width: 100%;
                height: auto;
            }

            .movie-card h4 {
                margin: 10px 0;
                font-size: 1rem;
                color: #ffcc00;
            }

            .movie-card p {
                font-size: 0.85rem;
                color: #d9d9d9;
            }
        </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

# Silently load data without any print or write statements
@st.cache_data  # Cache the data loading
def load_data():
    movies = pickle.load(open("movies_list.pkl", "rb"))
    movies_list = movies["title"].values
    return movies, movies_list

# Load data silently
movies, movies_list = load_data()

# Remove any automatic writes or debug messages
if 'write' in st.session_state:
    del st.session_state.write

# Custom CSS for better UI
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        color: white;
    }

    .header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        color: white;
        border-radius: 8px;
        margin-bottom: 30px;
    }

    .big-button {
        background-color: #1E1E1E;
        color: white;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 24px;
        margin: 10px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .big-button:hover {
        background-color: #4CAF50;
        color: white;
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        gap: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header">
    <h1>🎥 Welcome to the Movie Recommender System</h1>
    <p>Get personalized recommendations or explore random movies below!</p>
</div>
""", unsafe_allow_html=True)

# Navigation buttons with search bars
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="button-container">
            <button class="big-button" onclick="document.getElementById('movie-search').click()">
                🎥 Movie Search
            </button>
        </div>
    """, unsafe_allow_html=True)
    movie_search = st.text_input("Search for a movie", key="movie_search_input")
    if movie_search:
        # Filter movies that match the search query (case-insensitive)
        matching_movies = []
        search_term = movie_search.lower()
        
        # Search for all partial matches
        for title in movies_list:
            if search_term in title.lower():  # Changed from exact match to partial match
                movie_index = movies[movies['title'] == title].index[0]
                movie_id = movies.iloc[movie_index].id
                details = fetch_movie_details(movie_id)
                details['title'] = title
                details['id'] = movie_id
                matching_movies.append(details)
        
        if matching_movies:
            st.subheader(f"Found {len(matching_movies)} matches:")
            # Display all matches in grid
            for i in range(0, len(matching_movies), 5):
                cols = st.columns(5)
                batch = matching_movies[i:i+5]
                for col, movie in zip(cols, batch):
                    with col:
                        st.image(movie['poster'], caption=movie['title'], use_container_width=True)
                        st.markdown(f"<div class='rating-badge'>⭐ {movie['rating']}</div>", unsafe_allow_html=True)
                        st.write(f"**{movie['genres']}**")
                        if st.button(f"🎬 Similar Movies", key=f"view_{movie.get('id', movie['title'])}"):
                            st.session_state.selected_movie = movie
                            st.rerun()
        else:
            st.error("🔍 No movies found matching your search.")
        
with col2:
    st.markdown("""
        <div class="button-container">
            <button class="big-button" onclick="document.getElementById('actor-search').click()">
                🎭 Actor Search
            </button>
        </div>
    """, unsafe_allow_html=True)
    actor_name = st.text_input("Search for an actor", key="actor_search_input")
    if actor_name:
        actor_movies = fetch_movies_by_actor(actor_name)
        if actor_movies:
            st.subheader(f"Movies featuring {actor_name}")
            for i in range(0, len(actor_movies), 5):
                cols = st.columns(5)
                batch = actor_movies[i:i+5]
                for col, (movie_title, movie_poster) in zip(cols, batch):
                    with col:
                        st.image(movie_poster, caption=movie_title, use_container_width=True)
        else:
            st.warning("No movies found for this actor.")

# Display random movies section
st.header("🎲 Explore Random Movies")
random_movies = get_random_movies(20)

if st.session_state.selected_movie is None:
    for i in range(0, len(random_movies), 5):
        row_movies = random_movies[i:i+5]
        cols = st.columns(5)
        
        for col, movie in zip(cols, row_movies):
            with col:
                st.image(movie['poster'], caption=movie['title'], use_container_width=True)
                st.write(f"Rating: {movie['rating']}")
                st.write(f"Genres: {movie['genres']}")

else:
    movie = st.session_state.selected_movie
    if st.button("← Back to Movies"):
        st.session_state.selected_movie = None
        st.rerun()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(movie['poster'], use_container_width=True)
    with col2:
        st.title(movie['title'])
        st.write(f"**Rating:** {movie['rating']}")
        st.write(f"**Release Date:** {movie['release_date']}")
        st.write(f"**Genres:** {movie['genres']}")
        st.write("**Overview:**")
        st.write(movie['overview'])
        st.write("**Main Cast:**")
        if 'cast' in movie:
            for actor in movie['cast']:
                st.write(f"• {actor}")
    
    # Similar Movies Section
    st.header("Similar Movies You Might Like")
    
    try:
        recommended_movies = recommend(movie['title'])
        
        if recommended_movies:
            similar_movies_cols = st.columns(5)
            for idx, rec_movie in enumerate(recommended_movies):
                with similar_movies_cols[idx]:
                    st.image(rec_movie['poster'], caption=rec_movie['title'], use_container_width=True)
                    st.write(f"**Rating:** {rec_movie['rating']}")
                    st.write(f"**Genres:** {rec_movie['genres']}")
        else:
            st.info("No similar movies found at this time.")
                    
    except Exception as e:
        st.error("Unable to fetch similar movies at this time.")

