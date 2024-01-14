import imdb
import json
import logging
import asyncio
import aiohttp
import bleach

class IMDbWikipediaSearch:
    def __init__(self, output_file="imdb_wikipedia_results.json", log_file="error_log.txt"):
        self.output_file = output_file
        self.log_file = log_file

        # Set up logging
        logging.basicConfig(filename=self.log_file, level=logging.ERROR)

    async def get_wikipedia_summary_async(self, session, page_title):
        url = f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=true&titles={page_title}'

        async with session.get(url, headers={'User-Agent': 'YourUserAgent/1.0'}) as response:
            data = await response.json()

        page_id = next(iter(data['query']['pages']))
        page = data['query']['pages'][page_id]

        if 'extract' in page:
            # Use bleach to remove HTML tags
            summary = bleach.clean(page['extract'], tags=[], strip=True)

            # Remove newline characters
            summary = summary.replace('\n', ' ')

            return summary
        else:
            return f"No Wikipedia page found for '{page_title}'."

    async def fetch_movie_details(self, ia, movie):
        # Fetch Wikipedia summary for the movie
        async with aiohttp.ClientSession() as session:
            wikipedia_summary = await self.get_wikipedia_summary_async(session, movie['title'])

        # Basic information
        movie_info = {
            "Title": movie['title'],
            "IMDb ID": movie.getID(),
            "Year": movie.get('year', None),
            "Wikipedia Summary": wikipedia_summary,
        }

        return movie_info

    async def search_imdb_async(self, query):
        ia = imdb.IMDb()

        # Search for movies
        results = ia.search_movie(query, results=None)

        if not results:
            print(f"No results found for '{query}'. Please try a different search term.")
            return

        print(f"Found {len(results)} results for '{query}'. Fetching details...")

        data = []

        # Fetch details for each movie
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_movie_details(ia, movie) for movie in results]
            movie_details = await asyncio.gather(*tasks)

        # Sort the data list based on the "Year" field
        movie_details.sort(key=lambda x: (x.get("Year", float('inf')) or float('inf')))

        # Save the data to a JSON file
        try:
            with open(self.output_file, "w", encoding="utf-8") as json_file:
                json.dump(movie_details, json_file, indent=4, ensure_ascii=False)
            print(f"Results successfully saved to {self.output_file}")
        except Exception as e:
            logging.error(f"Error: Unable to save results to {self.output_file}. {e}")
            print(f"An error occurred while saving the results. Please check the log file ({self.log_file}) for details.")

if __name__ == "__main__":
    # Get user input for the search term
    search_term = input("Enter a movie title: ")

    # Perform the search and save results to JSON file
    imdb_wikipedia_search = IMDbWikipediaSearch()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(imdb_wikipedia_search.search_imdb_async(search_term))
