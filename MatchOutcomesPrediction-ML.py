
# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
# from scipy.stats import zscore

# Loading the dataset
data = pd.read_csv("/content/all_matches.csv")
print(data.head())

#checking if our dataset has any null values

null_values = data.isnull().sum()
print(null_values)

# Adding some null values

data.loc[data.sample(frac=0.1).index, ['home_score', 'away_score']] = np.nan

print("Null values:")
print(data.isnull().sum())

# Dropping the 'date' column as it is not necessary for our project
data = data.drop(columns=['date'])

# Impute missing values with mean
imputer = SimpleImputer(strategy='mean')
data[['home_score', 'away_score']] = imputer.fit_transform(data[['home_score', 'away_score']])

# Check for remaining null values
print("Remaining null values:")
print(data.isnull().sum())

# Apply one-hot encoding for the categorical columns
categorical_columns = ['home_team', 'away_team', 'tournament', 'country']
encoder = OneHotEncoder(sparse_output=False)
# encoder = OneHotEncoder(sparse_output=False, drop='first')

encoded_data = encoder.fit_transform(data[categorical_columns])
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))

# Combine with numerical data
data = pd.concat([data.drop(columns=categorical_columns), encoded_df], axis=1)
# print(data.head())

# # Calculate Z-scores for numerical columns
# data[['home_score', 'away_score']] = data[['home_score', 'away_score']].apply(zscore)

# Select only a subset of numerical columns for the correlation matrix because my dataset is huge and colab is not able to load it
subset = data[['home_score', 'away_score', 'neutral']]
corr_matrix = subset.corr()

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap (Subset)')
plt.show()

# Feature scaling
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)
data = pd.DataFrame(data_scaled, columns=data.columns)

# Split data
X = data.drop(columns=['home_score'])  # Target is 'home_score'
y = (data['home_score'] > 0).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# KNN Classifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

# Metrics for KNN
precision_knn = precision_score(y_test, y_pred_knn)
recall_knn = recall_score(y_test, y_pred_knn)
f1_knn = f1_score(y_test, y_pred_knn)

print(f"KNN Classification:\n{classification_report(y_test, y_pred_knn)}")

# Decision Tree Classifier
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)

# Metrics for Decision Tree
precision_dt = precision_score(y_test, y_pred_dt)
recall_dt = recall_score(y_test, y_pred_dt)
f1_dt = f1_score(y_test, y_pred_dt)

print(f"Decision Tree Classification:\n{classification_report(y_test, y_pred_dt)}")

# Logistic Regression
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

# Metrics for Logistic Regression
precision_lr = precision_score(y_test, y_pred_lr)
recall_lr = recall_score(y_test, y_pred_lr)
f1_lr = f1_score(y_test, y_pred_lr)

print(f"Logistic Regression Classification:\n{classification_report(y_test, y_pred_lr)}")

results = {}
results['KNN'] = {'Precision': precision_knn, 'Recall': recall_knn, 'F1 Score': f1_knn}
results['Decision Tree'] = {'Precision': precision_dt, 'Recall': recall_dt, 'F1 Score': f1_dt}
results['Logistic Regression'] = {'Precision': precision_lr, 'Recall': recall_lr, 'F1 Score': f1_lr}

# Plot Precision Comparison
plt.figure(figsize=(8, 5))
precision_values = [results[model]['Precision'] for model in results]
plt.bar(results.keys(), precision_values, color='blue')
plt.title('Precision Comparison')
plt.ylabel('Precision')
plt.show()

# Plot Recall Comparison
plt.figure(figsize=(8, 5))
recall_values = [results[model]['Recall'] for model in results]
plt.bar(results.keys(), recall_values, color='green')
plt.title('Recall Comparison')
plt.ylabel('Recall')
plt.show()

# Plot F1 Score Comparison
plt.figure(figsize=(8, 5))
f1_values = [results[model]['F1 Score'] for model in results]
plt.bar(results.keys(), f1_values, color='red')
plt.title('F1 Score Comparison')
plt.ylabel('F1 Score')
plt.show()