import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

# Load the data
data = pd.read_csv("C:/Users/koens/Bureaublad/Thesis 2.0/machine/data/combined_sent_data.tsv",
                   sep="\t")
data_rating = pd.read_csv("C:\\Users\\koens\\Bureaublad\\Thesis 2.0\\goodreads\\ratings.tsv",
                          sep="\t")
data_stylistic = pd.read_csv("C:/Users/koens/Bureaublad/Thesis 2.0/machine/data/output.tsv",
                             sep="\t")

merged_data = pd.merge(data, data_rating, on='DBNLti_id', how='inner')
final_data = pd.merge(merged_data, data_stylistic, on='DBNLti_id', how='inner')


# Split the data into features and target variable
X = final_data.drop(columns=["DBNLti_id", "Rating", "Title"])
y = final_data["Rating"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)

# Initialize the linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Compute Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# Compute R-squared (R2)
r2 = r2_score(y_test, y_pred)
print("R-squared:", r2)

# Compute Root Mean Squared Error (RMSE)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print("Root Mean Squared Error:", rmse)

# Create a DataFrame for real and predicted ratings
results = pd.DataFrame({'Real': y_test, 'Predicted': y_pred})

# Plot the distribution of the real and predicted average rating values
plt.figure(figsize=(10, 6))
sns.histplot(results['Real'], bins=20, kde=True, color='blue',
             label='Real', stat="density")
sns.histplot(results['Predicted'], bins=20, kde=True, color='red',
             label='Predicted', stat="density")
plt.title('Real vs Predicted Average Rating Values Linear Regression')
plt.xlabel('Real Rating')
plt.ylabel('Predicted Rating')
plt.legend()
plt.grid(True)
plt.savefig('real_vs_predicted_distribution_linear.png')
plt.show()
