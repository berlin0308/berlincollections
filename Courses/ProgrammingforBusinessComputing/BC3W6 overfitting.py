import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

bike = pd.read_csv("C:\\Users\\BERLIN CHEN\\Desktop\\BC- Python\\BC3W6 overfitting.csv")

X = bike.drop(["lent"], axis = 1) 
y = bike["lent"]                  

train_X, valid_X, train_y, valid_y = train_test_split(X, y, test_size = 0.3)

lm = LinearRegression()
lm.fit(train_X, train_y) 
print("R Square:    ", lm.score(train_X, train_y)) 

predicted_y = lm.predict(valid_X) 
rss = ((predicted_y - valid_y) ** 2).mean()
tss = ((valid_y.mean() - valid_y) ** 2).mean()
print(1 - rss / tss) 