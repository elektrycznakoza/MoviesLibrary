import random
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(
    handlers=[TimedRotatingFileHandler(filename='LibraryArchive.log', when='midnight', interval=1, backupCount=7)],
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)


class Library:
    total_views = 0

    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_movies(self):
        return sorted([item for item in self.items if isinstance(item, Movie)],
                      key=lambda x: x.title)

    def get_series(self):
        return sorted([item for item in self.items if isinstance(item, Series)],
                      key=lambda x: x.title)

    def search(self, title):
        return [item for item in self.items if title.lower() in item.title.lower()]

    def generate_views(self):
        if not self.items:
            print("Biblioteka jest pusta. Dodaj filmy i seriale przed uruchomieniem symulacji.")
            return

        item = random.choice(self.items)
        views = random.randint(1, 100)
        for _ in range(views):
            item.play()
        print(
            f"Wygenerowano {views} wyświetleń {item}. Suma: {Library.total_views}"
        )
        logging.info(
            f"Wygenerowano {views} wyświetleń {item}. Suma: {Library.total_views}"
        )

    def run_simulation(self, num_iterations):
        if not self.items:
            print("Biblioteka jest pusta. Dodaj filmy i seriale przed uruchomieniem symulacji.")
            return

        for i in range(num_iterations):
            self.generate_views()
        logging.info(f"Wyświetlenia po symulacji: {Library.total_views}")

    def top_titles(self, num_titles, content_type=None):
        if not self.items:
            return []

        if content_type == "movies":
            items = self.get_movies()
        elif content_type == "series":
            items = self.get_series()
        else:
            items = self.items

        sorted_items = sorted(items, key=lambda x: x.views, reverse=True)
        return sorted_items[:min(num_titles, len(sorted_items))]


class Movie:
    def __init__(self, title, release_year, genre):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.views = 0

    def play(self):
        self.views += 1
        Library.total_views += 1
        logging.info(f"Played {self.title}. Total views: {Library.total_views}")

    def __str__(self):
        return f"{self.title} ({self.release_year}) - {self.views} views"


class Series:
    def __init__(self, title, genre, total_episodes=15):
        self.title = title
        self.genre = genre
        self.season_number = 1
        self.episode_number = 1
        self.views = 0
        self.total_episodes = total_episodes

    def play(self):
        self.views += 1
        Library.total_views += 1
        logging.info(f"Played {self} - {self.views} views")

    def generate_random_episode(self):
        self.season_number = random.randint(1, 5)  # Losowy sezon od 1 do 5
        self.episode_number = random.randint(1, min(self.total_episodes, 15))  # Losowy odcinek od 1 do min(total_episodes, 15)

    def __str__(self):
        return f"{self.title} S{self.season_number:02d}E{self.episode_number:02d} - {self.views} views"

    def summary_str(self):
        return f"{self.title} S{self.season_number:02d}E{self.episode_number:02d} - {self.views} views"


if __name__ == "__main__":
    library = Library()

    library.add_item(Movie("Pulp Fiction", 1994, "Crime"))
    library.add_item(Series("The Simpsons", "Animation"))
    library.add_item(Series("Two and a Half Men", "Comedy"))
    library.add_item(Movie("The Shawshank Redemption", 1994, "Drama"))
    library.add_item(Series("Breaking Bad", "Drama"))
    library.add_item(Series("The Punisher", "Action"))
    library.add_item(Movie("The Dark Knight", 2008, "Action"))
    library.add_item(Movie("The Godfather", 1972, "Crime"))
    library.add_item(Series("Peaky Blinders", "Crime"))
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
        if isinstance(title, Series):
            title.generate_random_episode()
            print(f"{i}. {title.summary_str()}")
        else:
            print(f"{i}. {title}")

        logging.info(f"{i}. {title.summary_str() if isinstance(title, Series) else str(title)}")

    logging.info(f"Suma wyświetleń po symulacji: {Library.total_views}")
