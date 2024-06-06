import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import spacy
import pandas as pd

# Ensure required resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy Dutch model
nlp = spacy.load('nl_core_news_sm')


def calculate_complexity(text):
    # Tokenize the text into sentences
    zinnen = sent_tokenize(text)

    # Tokenize each sentence into words
    woorden_per_zin = [word_tokenize(zin) for zin in zinnen]

    # Flatten the list of words
    alle_woorden = [woord for zin in woorden_per_zin for woord in zin]

    # Filter words to remove stopwords and punctuation, and lower the letters
    stopwoorden = set(stopwords.words("dutch"))
    gefilterde_woorden = [woord.lower() for woord in alle_woorden
                          if woord.isalnum() and woord.lower() not in stopwoorden]

    # Calculate total number of sentences
    aantal_zinnen = len(zinnen)

    # Calculate total number of words
    totaal_aantal_woorden = len(gefilterde_woorden)

    # Calculate total number of letters
    totaal_aantal_letters = sum(len(woord) for woord in gefilterde_woorden)

    # Calculate the number of stopwords
    aantal_stopwoorden = len([woord for woord in alle_woorden if woord.lower() in stopwoorden])

    # Calculate stopword ratio
    if (totaal_aantal_woorden - aantal_stopwoorden) != 0:
        stopwoord_verhouding = aantal_stopwoorden / (totaal_aantal_woorden - aantal_stopwoorden)
    else:
        stopwoord_verhouding = 0

    # Calculate the average number of words per sentence
    gemiddeld_aantal_woorden_per_zin = totaal_aantal_woorden / aantal_zinnen

    # Calculate the average number of letters per word
    gemiddeld_aantal_letters_per_woord = totaal_aantal_letters / totaal_aantal_woorden

    # Calculate the number of unique words
    aantal_unieke_woorden = len(set(gefilterde_woorden))

    # Calculate the number of hapax legomena (words that occur only once)
    hapax_legomena = [woord for woord in gefilterde_woorden
                      if gefilterde_woorden.count(woord) == 1]

    # Calculate the Type-Token Ratio (TTR)
    ttr = aantal_unieke_woorden / totaal_aantal_woorden

    # Calculate the Hapax Legomena Ratio (HLR)
    hlr = len(hapax_legomena) / totaal_aantal_woorden

    # Use spaCy for POS tagging
    doc = nlp(' '.join(alle_woorden))

    # Count frequency of different parts of speech
    pos_counts = Counter(token.pos_ for token in doc)

    # Calculate frequency for each requested part of speech
    totaal_aantal_tokens = len(doc)
    frequentie_werkwoorden = pos_counts['VERB'] / totaal_aantal_tokens
    frequentie_zelfstandige_naamwoorden = pos_counts['NOUN'] / totaal_aantal_tokens
    frequentie_voornaamwoorden = pos_counts['PRON'] / totaal_aantal_tokens
    frequentie_bijwoorden = pos_counts['ADV'] / totaal_aantal_tokens

    # Count punctuation frequency
    punctuations = [token.text for token in doc if token.is_punct]
    frequentie_leestekens = len(punctuations) / totaal_aantal_tokens

    return (hlr,
            ttr,
            stopwoord_verhouding,
            gemiddeld_aantal_woorden_per_zin,
            gemiddeld_aantal_letters_per_woord,
            frequentie_werkwoorden,
            frequentie_zelfstandige_naamwoorden,
            frequentie_voornaamwoorden,
            frequentie_bijwoorden,
            frequentie_leestekens)


def main():
    input_folder = "C:\\Users\\koens\\Bureaublad\\Thesis 2.0\\raw_book_data\\first100"
    output_folder = "output_data"

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Check if the file already exists in the output folder
        if os.path.exists(output_path):
            print(f"Skipping {filename} as it already exists in the output folder.")
            continue

        # Read text from input file
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Calculate complexity
        complexity_data = calculate_complexity(text)

        # Create DataFrame
        data = {
            'HLR': [complexity_data[0]],
            'TTR': [complexity_data[1]],
            'Stopwoord verhouding': [complexity_data[2]],
            'Gemiddeld aantal woorden per zin': [complexity_data[3]],
            'Gemiddeld aantal letters per woord': [complexity_data[4]],
            'Frequentie van werkwoorden': [complexity_data[5]],
            'Frequentie van zelfstandige naamwoorden': [complexity_data[6]],
            'Frequentie van voornaamwoorden': [complexity_data[7]],
            'Frequentie van bijwoorden': [complexity_data[8]],
            'Frequentie van leestekens': [complexity_data[9]]
        }
        df = pd.DataFrame(data)

        # Write to TSV
        df.to_csv(output_path, sep='\t', index=False)
        print(f"Processed {filename} and saved results to {output_path}.")


if __name__ == '__main__':
    main()
