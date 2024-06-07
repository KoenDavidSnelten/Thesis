import pandas as pd
import matplotlib.pyplot as plt

# Read the .tsv file into a pandas DataFrame
file_path = 'ratings.tsv'  # Replace with your actual file path
df = pd.read_csv(file_path, sep='\t')

# Plot the distribution of the ratings
plt.figure(figsize=(10, 6))
plt.hist(df['Rating'], bins=10, edgecolor='black')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.grid(True)

# Save the plot as a .png file
output_file = 'rating_distribution.png'
plt.savefig(output_file)
plt.show()

print(f"The plot has been saved as {output_file}")
