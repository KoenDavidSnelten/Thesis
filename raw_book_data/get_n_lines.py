import os


def copy_lines(source_path, destination_path, num_lines, from_start=True):
    """
    Copy the first or last num_lines from a text file.

    Parameters:
    source_path (str): The path to the source text file.
    destination_path (str): The path to the destination text file.
    num_lines (int): The number of lines to copy.
    from_start (bool): If True, copy from the start of the file.
    If False, copy from the end.
    """
    try:
        with open(source_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            selected_lines = lines[:num_lines] if from_start else lines[-num_lines:]

        with open(destination_path, 'w', encoding='utf-8') as file:
            file.writelines(selected_lines)
    except Exception as e:
        print(f"An error occurred while copying lines from '{source_path}': {e}")


def process_files(source_folder,
                  first100_folder,
                  last100_folder,
                  num_lines=100):
    """
    Process all text files in the source folder,
    copying the first and last num_lines
    lines to separate folders.

    Parameters:
    source_folder (str): The folder containing the source text files.
    first100_folder (str): The folder to store the first num_lines of each file.
    last100_folder (str): The folder to store the last num_lines of each file.
    num_lines (int): The number of lines to copy from the start and end of each file.
    """
    os.makedirs(first100_folder, exist_ok=True)
    os.makedirs(last100_folder, exist_ok=True)

    for filename in os.listdir(source_folder):
        if filename.endswith('.txt'):
            source_path = os.path.join(source_folder, filename)
            first100_path = os.path.join(first100_folder, filename)
            last100_path = os.path.join(last100_folder, filename)

            copy_lines(source_path, first100_path, num_lines, from_start=True)
            copy_lines(source_path, last100_path, num_lines, from_start=False)

            print(f"Processed '{source_path}':")
            print(f"  Copied first {num_lines} lines to '{first100_path}'")
            print(f"  Copied last {num_lines} lines to '{last100_path}'")


def main():
    # Specify the source and destination folders
    source_folder = 'text'
    first100_folder = 'first100'
    last100_folder = 'last100'

    # Process the files
    process_files(source_folder, first100_folder, last100_folder)


if __name__ == "__main__":
    main()
