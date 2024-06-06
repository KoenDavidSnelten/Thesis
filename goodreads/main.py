import random
import time
import requests
import os
import pickle
import gzip
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import pandas as pd


def search_books_on_goodreads(book_title):
    """
    Search for books on Goodreads based on the provided title.

    Args:
        book_title (str): The title of the book to search for.

    Returns:
        list: A list of tuples containing book title, URL, and average rating.
              Each tuple represents a search result.
    """
    time.sleep(random.uniform(0.5, 1))
    try:
        encoded_title = quote_plus(book_title)
        search_url = f"https://www.goodreads.com/search?utf8=%E2%9C%93&q={encoded_title}&search_type=books&search%5Bfield%5D=on"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all book titles, URLs, and average ratings
        books = soup.find_all(class_='bookTitle')
        results = []
        for book in books:
            title = book.text.strip()
            url = 'https://www.goodreads.com' + book['href']

            # Find the average rating
            rating_tag = book.find_next(class_='minirating')
            average_rating = rating_tag.text.strip().split()[0] if rating_tag else "N/A"

            results.append((title, url, average_rating))

        return results
    except Exception as e:
        print("An error occurred:", e)
        return None


def read_titles_from_tsv(file_path):
    """
    Read titles from a TSV file and filter them based on specific criteria.

    Args:
        file_path (str): The path to the TSV file.

    Returns:
        list: A list of tuples containing DBNLti_id and title for eligible titles.
    """
    titles = []
    df = pd.read_csv(file_path, sep='\t')

    for index, row in df.iterrows():
        DBNLti_id = row['DBNLti_id']
        title = row['Title']
        gz_file_path = os.path.join('C:\\Users\\koens\\Bureaublad\\Thesis 2.0\\raw_data\\DBNL-20230214\\output\\text',
                                    f'{DBNLti_id}_01.txt.gz')
        if os.path.isfile(gz_file_path):
            with gzip.open(gz_file_path, 'rt', encoding='utf-8') as file:
                line_count = sum(1 for line in file)
                if line_count > 200:
                    titles.append((DBNLti_id, title))

    return titles


def main():
    tsv_file_path = 'C:\\Users\\koens\\Bureaublad\\Thesis 2.0\\raw_data\\DBNL-20230214\\output\\metadata.tsv'

    pickle_file_path = 'C:\\Users\\koens\\Bureaublad\\Thesis 2.0\\goodreads\\titles.pkl'

    if os.path.isfile(pickle_file_path):
        with open(pickle_file_path, 'rb') as file:
            title_list = pickle.load(file)
        print(f"Data loaded from {pickle_file_path}")
    else:
        title_list = read_titles_from_tsv(tsv_file_path)
        with open(pickle_file_path, 'wb') as file:
            pickle.dump(title_list, file)
        print(f"Data saved to {pickle_file_path}")

    rating_list = []

    for item in title_list:
        DBNLti_id, book_title = item
        search_result = search_books_on_goodreads(book_title)
        if search_result:
            first_book = search_result[0]
            try:
                rating = float(first_book[2])
            except ValueError:
                print(first_book[2])
                print("Is not a numerical:", book_title)
                continue

            if rating == 0.0:
                print(rating)
                print("No ratings:", book_title)
                continue

            rating_list.append((DBNLti_id, book_title, rating))
            print(book_title, "found!")
        else:
            print("No results found.")

    # Create a DataFrame from rating_list
    df = pd.DataFrame(rating_list, columns=['DBNLti_id', 'Title', 'Rating'])

    # Save DataFrame to a .tsv file
    output_tsv_file_path = 'ratings.tsv'
    df.to_csv(output_tsv_file_path, sep='\t', index=False)

    print("Rating list saved as ratings.tsv")


if __name__ == '__main__':
    main()
