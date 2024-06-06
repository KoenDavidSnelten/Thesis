import os
import sys
import torch
from transformers import RobertaTokenizer as rt
from transformers import RobertaForSequenceClassification as rc
from torch.nn import functional as F
import pandas as pd

# Initialize tokenizer and model
tokenizer = rt.from_pretrained("pdelobelle/robbert-v2-dutch-base")
model = rc.from_pretrained("pdelobelle/robbert-v2-dutch-base")


def calc_sent(input_text):
    """
    Calculate the sentiment score for the given input text.

    Args:
        input_text (str): Text for which sentiment is to be calculated.

    Returns:
        float: Average sentiment probability for the text.
    """
    # Split the text into individual sentences based on periods
    sentences = [sentence.strip() for sentence in input_text.split(".")
                 if sentence.strip()]

    sentiment_probs_total = [0, 0]

    for sentence in sentences:
        # Skip empty sentences
        if len(sentence.strip()) == 0:
            continue

        # Tokenize input text and truncate if necessary
        inputs = tokenizer(sentence.strip(),
                           return_tensors="pt",
                           max_length=512,
                           truncation=True)

        # Perform inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        probs = F.softmax(logits, dim=1).squeeze().numpy()

        # Add sentiment probabilities to the total
        sentiment_probs_total += probs

    # Calculate average sentiment probabilities
    average_sentiment_probs = sentiment_probs_total / len(sentences)

    return average_sentiment_probs[0]


# Define input paths
input_path_first = "/home3/s4568966/Scriptie/input_data/first100"
input_path_last = "/home3/s4568966/Scriptie/input_data/last100"
input_path = "/home3/s4568966/Scriptie/output_data"


def calc_sent_values(filename):
    """
    Calculate sentiment values for the first and last 100 sentences of a file.

    Args:
        filename (str): Name of the file to process.

    Returns:
        tuple: Sentiment probabilities for the first 100 sentences,
        last 100 sentences,
        average sentiment,
        and the difference in sentiment.
    """
    file_path_first = os.path.join(input_path_first, filename)
    file_path_last = os.path.join(input_path_last, filename)

    with open(file_path_first, 'r') as file:
        first100 = file.read()
    with open(file_path_last, 'r') as file:
        last100 = file.read()

    average_sent_first = calc_sent(first100)
    average_sent_last = calc_sent(last100)
    average_sent = (average_sent_first + average_sent_last) / 2
    difference_sent = abs(average_sent_first - average_sent_last)

    return average_sent_first, average_sent_last, average_sent, difference_sent


def main(split):
    """
    Main function to process files and calculate sentiment values.

    Args:
        split (int): The starting index for processing files.
    """
    for filename in os.listdir(input_path_first)[split::100]:
        output_file_path = os.path.join(input_path, filename)
        if os.path.exists(output_file_path):
            continue
        print(filename)
        output_data = calc_sent_values(filename)

        data = {
            "average_sent_first": output_data[0],
            "average_sent_last": output_data[1],
            "average_sent": output_data[2],
            "difference_sent": output_data[3]
        }
        index = [filename]
        df = pd.DataFrame(data, index=index)
        df.to_csv(output_file_path, sep='\t', index=False)


if __name__ == "__main__":
    split = int(sys.argv[1])
    main(split)
