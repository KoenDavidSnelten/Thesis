# Github Thesis repository
## The Sentiment of Literature: Predicting Quality Using Sentimentanlysis and Stylistic Features
### Koen David Snelten (S4568966) of RUG

## How to use
### Make sure you have the correct paths!
1. Run goodreads/main.py;  You need a metadata file with ID and title and a folder containing the .gz; This returns a file with ID, title and rating of the files with enough lines.
2. Run raw_book_data/gz_to_text.py; This transforms all .gz to .txt files from the previous step.
3. Run raw_book_data/get_n_lines.py; This gets all first 100 and last 100 lines.
4. Run zelfscan/zelfscan.py; This will return all stylistic features in a folder.
5. Run zelfscan/get_data.py; To combine all data in one file.
6. Run sentiment/main.py; This will return all sentiment features in a folder. You should run this on a strong computer cluster.
7. Run sentiment/combine_output.py; To combine all data in one file.
8. Run machine/linear_model.py; This returns the linear regression model results.
9. Run machine/bayes_model.py; This returns the BayesRidge regression model results.
