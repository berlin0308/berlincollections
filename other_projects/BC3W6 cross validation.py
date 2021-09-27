import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

bike = pd.read_csv("C:\\Users\\BERLIN CHEN\\Desktop\\BC- Python\\BC3W6 underfitting.csv") 

X = bike.drop(["lent"], axis = 1)
y = bike["lent"]

lm = LinearRegression()
print(cross_val_score(lm, X, y, cv = 4).mean()) 