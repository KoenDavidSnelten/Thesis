import pandas as pd
import os


def get_data(folder_path):
    # Initialize an empty list to store DataFrame objects
    data_frames = []

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a .txt file
        if file_name.endswith('.txt'):
            # Extract DBNLti_id from the file name
            dbnlti_id = os.path.splitext(file_name)[0]

            # Read the .txt file as a pandas DataFrame
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, sep='\t')

            # Add a column for DBNLti_id
            df['DBNLti_id'] = dbnlti_id

            # Append the DataFrame to the list
            data_frames.append(df)

    # Concatenate all DataFrames into a single DataFrame
    result = pd.concat(data_frames, ignore_index=True)
    return result


def combine_dataframes(goodread_data, sentiment_data, stylometric_data):
    # Merge goodread_data with sentiment_data on 'DBNLti_id'
    merged_data = pd.merge(goodread_data, sentiment_data, on='DBNLti_id')

    # Merge the result with stylometric_data on 'DBNLti_id'
    merged_data = pd.merge(merged_data, stylometric_data, on='DBNLti_id')

    # Reorder columns as desired
    merged_data = merged_data[['DBNLti_id',
                               'Title',
                               'Rating',
                               'average_sent_first',
                               'average_sent_last',
                               'average_sent',
                               'difference_sent',
                               'HLR',
                               'TTR',
                               'Stopwoord_verhouding',
                               'Gemiddeld_aantal_woorden_per_zin',
                               'Gemiddeld_aantal_letters_per_woord']]

    return merged_data


def main():
    sentiment_folder_path = "C:/Users/koens/Bureaublad/Thesis/sentiment/output_data"
    stylometric_folder_path = "C:/Users/koens/Bureaublad/Thesis/tscan/output_data"
    goodread_data = pd.read_csv("C:/Users/koens/Bureaublad/Thesis/raw_book_data/merged_data.tsv",
                                sep='\t')
    sentiment_data = get_data(sentiment_folder_path)
    stylometric_data = get_data(stylometric_folder_path)

    # Call the function to combine the DataFrames
    combined_data = combine_dataframes(goodread_data,
                                       sentiment_data,
                                       stylometric_data)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Specify the folder path to save the .tsv file
    output_folder = 'C:/Users/koens/Bureaublad/Thesis/machine/data'

    # Define the output file path
    output_file_path = os.path.join(output_folder, 'combined_data.tsv')

    # Save the combined data as a .tsv file
    combined_data.to_csv(output_file_path, sep='\t', index=False)

    print(f"Combined data saved to: {output_file_path}")


if __name__ == '__main__':
    main()
