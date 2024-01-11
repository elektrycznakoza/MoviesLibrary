import random
from datetime import datetime
import logging

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
                      key=lambda x: x.title)

    def get_series(self):
        return sorted([item for item in self.items if isinstance(item, Series)],
                      key=lambda x: x.title)

    def search(self, title):
        return [item for item in self.items if title.lower() in item.title.lower()]

    def generate_views(self):
        item = random.choice(self.items)
        views = random.randint(1, 100)
        for _ in range(views):
            item.play()
        print(
            f"Wygenerowano {views} wyświetleń {item.title}. Suma: {Library.total_views}"
        )
        logging.info(
            f"Wygenerowano {views} wyświetleń {item.title}. Suma: {Library.total_views}"
        )

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

    def play(self):
        self.views += 1
        Library.total_views += 1
        logging.info(f"Played {self.title}. Total views: {Library.total_views}")

    def __str__(self):
        return f"{self.title} ({self.release_year}) - {self.views} views"


class Series(Movie):
    def __init__(self, title, release_year, genre, season_number, episode_number, views=0):
        super().__init__(title, release_year, genre, views)
        self.season_number = season_number
        self.episode_number = episode_number
        self.original_format = f"{self.title} S{self.season_number:02d}E{self.episode_number:02d}"

    def play(self):
        super().play()
        self.episode_number += 1

    def generate_random_episode(self):
        return random.randint(1, 100)

    def __str__(self):
        if self.episode_number:
            return f"{self.title} ({self.release_year}) S{self.season_number:02d}E{self.episode_number:02d} - {self.views} views"
        else:
            return f"{self.title} ({self.release_year}) - {self.views} views"

    def summary_str(self):
        return f"{self.title} ({self.release_year})"

if __name__ == "__main__":
    library = Library()

    library.add_item(Movie("Pulp Fiction", 1994, "Crime"))
    library.add_item(Series("The Simpsons", 1989, "Animation", 1, 1))
    library.add_item(Series("Two and a Half Men", 2003, "Comedy", 1, 1))
    library.add_item(Movie("The Shawshank Redemption", 1994, "Drama"))
    library.add_item(Series("Breaking Bad", 2008, "Drama", 1, 1))
    library.add_item(Series("The Punisher", 2014, "Action", 1, 1))
    library.add_item(Movie("The Dark Knight", 2008, "Action"))
    library.add_item(Movie("The Godfather", 1972, "Crime"))
    library.add_item(Series("Peaky Blinders", 2013, "Crime", 1, 1))
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
            print(f"{i}. {title.summary_str()} - {title.views} views")
        else:
            print(f"{i}. {title}")

        logging.info(f"{i}. {title}")

    logging.info(f"Suma wyświetleń po symulacji: {Library.total_views}")
