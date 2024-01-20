import random
from datetime import datetime
import logging

# Konfiguracja loggera
logging.basicConfig(filename='LibraryArchive.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')


class Library:
    total_views = 0

    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_movies(self):
        return sorted([item for item in self.items if isinstance(item, Movie)],
                      key=lambda x: x.format_title())

    def get_series(self):
        return sorted([item for item in self.items if isinstance(item, Series)],
                      key=lambda x: x.format_title())

    def search(self, title):
        return [item for item in self.items if title.lower() in item.title.lower()]

    def play(self, item, views_to_add=1):
        item.views += views_to_add
        Library.total_views += views_to_add
        logging.info(f"Played {item.format_title()}. Total views: {Library.total_views}")

    def generate_views(self):
        if not self.items:
            print("Biblioteka jest pusta. Dodaj filmy i seriale przed uruchomieniem symulacji.")
            return

        item = random.choice(self.items)
        views = random.randint(1, 100)
        self.play(item, views_to_add=views)
        print(f"Wygenerowano {views} wyświetleń {item.format_title()}. Suma: {Library.total_views}")
        logging.info(f"Wygenerowano {views} wyświetleń {item.format_title()}. Suma: {Library.total_views}")

    def run_simulation(self, num_iterations):
        for i in range(num_iterations):
            self.generate_views()
        logging.info(f"Wyświetlenia po symulacji: {Library.total_views}")

    def top_titles(self, num_titles, content_type=None):
        if content_type == "movies":
            items = self.get_movies()
        elif content_type == "series":
            items = self.get_series()
        else:
            items = self.items

        sorted_items = sorted(items, key=lambda x: x.views, reverse=True)
        return sorted_items[:num_titles]


class Movie:

    def __init__(self, title, release_year, genre, views=0):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.views = views

    def format_title(self):
        return f"{self.title} ({self.release_year})"

    def __str__(self):
        return f"{self.format_title()} - {self.views} views"


class Series(Movie):

    def __init__(self, title, release_year, genre, season_number, episode_number, views=0):
        super().__init__(title, release_year, genre, views)
        self.season_number = season_number
        self.episode_number = episode_number

    def format_title(self):
        return f"{self.title} S{self.season_number:02d}E{self.episode_number:02d}"

    def __str__(self):
        return f"{self.format_title()} - {self.views} views"


if __name__ == "__main__":
    library = Library()

    # Dodawanie filmów i seriali do biblioteki
    library.add_item(Movie("Pulp Fiction", 1994, "Crime"))
    library.add_item(Series("The Simpsons", 1989, "Animation", 2, 7))
    library.add_item(Series("Two and a Half Men", 2003, "Comedy", 3, 5))
    library.add_item(Movie("The Shawshank Redemption", 1994, "Drama"))
    library.add_item(Series("Breaking Bad", 2008, "Drama", 5, 2))
    library.add_item(Series("The Punisher", 2014, "Action", 2, 4))
    library.add_item(Movie("The Dark Knight", 2008, "Action"))
    library.add_item(Movie("The Godfather", 1972, "Crime"))
    library.add_item(Series("Peaky Blinders", 2013, "Crime", 4, 4))
    library.add_item(Movie("Blade Runner", 1982, "Science Fiction"))

    print("Biblioteka filmów:")
    for item in library.items:
        print(item)

    logging.info(f"Suma wyświetleń przed symulacją: {Library.total_views}")

    library.run_simulation(10)

    current_date = datetime.now().strftime("%d.%m.%Y")
    print(f"\nNajpopularniejsze filmy i seriale dnia {current_date}:")
    top_titles = library.top_titles(3)
    for i, title in enumerate(top_titles, 1):
        print(f"{i}. {title}")
        logging.info(f"{i}. {title}")

    logging.info(f"Suma wyświetleń po symulacji: {Library.total_views}")
