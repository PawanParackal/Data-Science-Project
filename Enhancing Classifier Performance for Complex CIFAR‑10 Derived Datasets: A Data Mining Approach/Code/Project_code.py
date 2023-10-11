import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score



data = pd.read_csv('./train.csv')

imputer = SimpleImputer(strategy="mean")  # Use mean imputation
data = imputer.fit_transform(data)

scaler = StandardScaler()
data[:, :100] = scaler.fit_transform(data[:, :100])

X = data[:, :-1]  # Features (all columns except the last one)
y = data[:, -1]   # Labels (last column)

decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()
k_neighbors = KNeighborsClassifier()
naive_bayes = GaussianNB()

decision_tree.fit(X, y)
random_forest.fit(X, y)
k_neighbors.fit(X, y)
naive_bayes.fit(X, y)

decision_tree_scores = cross_val_score(decision_tree, X, y, cv=5, scoring='f1_macro')
random_forest_scores = cross_val_score(random_forest, X, y, cv=5, scoring='f1_macro')
k_neighbors_scores = cross_val_score(k_neighbors, X, y, cv=5, scoring='f1_macro')
naive_bayes_scores = cross_val_score(naive_bayes, X, y, cv=5, scoring='f1_macro')

# Choose the model with the best cross-validated F1 score
best_model = max([
    ("Decision Tree", np.mean(decision_tree_scores)),
    ("Random Forest", np.mean(random_forest_scores)),
    ("K-Nearest Neighbors", np.mean(k_neighbors_scores)),
    ("Naive Bayes", np.mean(naive_bayes_scores))
], key=lambda x: x[1])

print(f"The best model is {best_model[0]} with F1 score: {best_model[1]:.2f}")


print(data.head())


"$PWD/html":/var/www/html