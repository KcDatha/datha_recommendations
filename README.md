# Movie Recommendation System

Welcome to the **Movie Recommendation System**, a dynamic and personalized platform that simplifies movie discovery using machine learning. This project provides tailored recommendations, enabling users to explore movies based on their preferences and metadata such as genres, keywords, and cast details.

---

## Features

- **Search Functionality**: Instantly search for movies by title and view real-time results.
- **Dynamic Recommendations**: Get personalized movie suggestions based on your selections.
- **Detailed Movie Information**: View genres, release dates, IMDb ratings, and cast details for selected movies.
- **Responsive UI**: Access the platform seamlessly across desktops, tablets, and mobile devices.
- **Random Movie Suggestions**: Discover movies with dynamic random recommendations.

---

## Technologies Used

- **Python**: Core language for development.
- **Streamlit**: Framework for building an interactive user interface.
- **TMDB API**: To fetch dynamic movie data like posters, genres, and ratings.
- **Pandas**: For data preprocessing and manipulation.
- **Scikit-learn**: For implementing content-based recommendation using cosine similarity.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KcDatha/datha_recommendations.git
   ```
2. Navigate to the project directory:
   ```bash
   cd movie-recommendation-system
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run jagratha.py
   ```

---

## How It Works

1. **Data Preprocessing**:
   - Merges movie and credit datasets.
   - Creates a "tags" column by combining genres, keywords, and cast.
   - Applies stemming and stopword removal for better content-based filtering.

2. **Recommendation Engine**:
   - Uses cosine similarity to rank movies based on their relevance to user input.
   - Dynamically fetches movie details and recommendations via the TMDB API.

3. **User Interaction**:
   - Users can search for movies, view details, and explore recommendations dynamically.
   - The system also provides random movie suggestions on the homepage.

---


## Future Enhancements

- **User Profiles**: Save preferences and track viewing history.
- **Watchlists and Trailers**: Add advanced features to enhance user engagement.
- **Improved Search**: Implement fuzzy search to handle typos and similar queries.
- **Scalability**: Optimize for handling larger datasets and increased traffic.


---

## Acknowledgements

- The Movie Database (TMDB) API for providing dynamic movie data.
- Open-source libraries and frameworks used in the development.

---

Thank you for visiting the repository. Happy movie discovery!
