# IMDbWikiSearch

This Python script allows you to search for movies using the IMDb API and fetch their Wikipedia summaries asynchronously.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/Syslogine/IMDbWikiSearch.git
   ```

2. Install the required dependencies:

   ```bash
   pip install imdbpy aiohttp bleach
   ```

3. Run the script:

   ```bash
   python main.py
   ```

4. Enter a movie title when prompted.

5. The script will fetch movie details, including IMDb ID, year, and Wikipedia summary. Results are saved to a JSON file.

## Requirements

- Python 3.7 or higher
- IMDbPY library
- aiohttp library
- bleach library

## Script Overview

### IMDbWikipediaSearch Class

- `__init__(self, output_file="imdb_wikipedia_results.json", log_file="error_log.txt")`: Initializes the IMDbWikipediaSearch object with output and log file names.

- `get_wikipedia_summary_async(self, session, page_title)`: Asynchronously fetches Wikipedia summary for a given page title using aiohttp.

- `fetch_movie_details(self, ia, movie)`: Asynchronously fetches IMDb and Wikipedia details for a given movie.

- `search_imdb_async(self, query)`: Searches for movies on IMDb based on the given query and fetches details for each movie asynchronously.

### Main Section

- Accepts user input for a movie title.

- Creates an instance of IMDbWikipediaSearch.

- Runs the search and saves results to a JSON file.

## Contributing

If you'd like to contribute to this project, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).