import os
import shutil
import gzip
import pandas as pd


def copy_and_transform(source_path, destination_path):
    """
    Copy and transform a .gz file to a .txt file.

    Parameters:
    source_path (str): The path to the source .gz file.
    destination_path (str): The path to the destination .txt file.
    """
    try:
        with gzip.open(source_path, 'rb') as f_in:
            with open(destination_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        print(f"An error occurred while processing '{source_path}': {e}")


def main():
    """
    Main function to read data files, merge them, and process .gz files.
    """
    # File paths
    filtered_ratings_file = 'C:\\Users\\koens\\Bureaublad\\Thesis 2.0\\goodreads\\ratings.tsv'
    source_folder = 'C:\\Users\\koens\\Bureaublad\\Thesis 2.0\\raw_data\\DBNL-20230214\\output\\text'
    destination_folder = 'C:\\Users\\koens\\Bureaublad\\Thesis 2.0\\raw_book_data\\text'

    # Read the filtered ratings and metadata files
    ratings_df = pd.read_csv(filtered_ratings_file,
                             sep='\t',
                             header=None,
                             names=['DBNLti_id', 'Title', 'Rating'])

    # Iterate over rows to process .gz files
    for index, row in ratings_df.iterrows():
        title = row['Title']
        dbnl_id = row['DBNLti_id']
        if pd.notna(dbnl_id):
            gz_file = os.path.join(source_folder, dbnl_id + '_01.txt.gz')
            if os.path.exists(gz_file):
                txt_file = os.path.join(destination_folder, dbnl_id + '.txt')
                copy_and_transform(gz_file, txt_file)
                print(f"Transformed '{gz_file}' to '{txt_file}' and moved to special folder.")
            else:
                print(f"Could not find .gz file for title: '{title}'")
        else:
            print(f"Could not find DBNLti_id for title: '{title}'")


if __name__ == "__main__":
    main()
