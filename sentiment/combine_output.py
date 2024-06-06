import os
import pandas as pd


def combine_txt_to_tsv(input_directory, output_file):
    """
    Combine multiple .txt files in a directory into a single .tsv file.

    Args:
        input_directory (str): Path to the directory containing .txt files.
        output_file (str): Path to the output .tsv file.

    Returns:
        None
    """
    # List to hold all data frames
    data_frames = []

    # Iterate over all files in the directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_directory, file_name)
            dbnlti_id = os.path.splitext(file_name)[0]

            # Read the content of the file into a DataFrame
            df = pd.read_csv(file_path, sep='\t')

            # Add a new column for the file name (id)
            df.insert(0, 'DBNLti_id', dbnlti_id)

            # Append the DataFrame to the list
            data_frames.append(df)

    # Combine all DataFrames into one
    combined_df = pd.concat(data_frames, ignore_index=True)

    # Save the combined DataFrame to a .tsv file
    combined_df.to_csv(output_file, sep='\t', index=False)


def main():
    input_directory = 'output_data'
    output_file = 'combined_sent_data.tsv'
    combine_txt_to_tsv(input_directory, output_file)


if __name__ == "__main__":
    main()
