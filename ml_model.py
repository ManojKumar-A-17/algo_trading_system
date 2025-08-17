# Decision Tree Classifier.
# ml_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import ta

def prepare_ml_data(df):
    # Calculate MACD
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    
    # Target: 1 if next day's close is higher than today, else 0
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    
    # Drop last row (no target available)
    df = df.dropna()
    
    features = ['RSI', 'MACD', 'Volume', 'MA20', 'MA50']
    X = df[features]
    y = df['Target']
    
    return X, y

def train_and_evaluate(df):
    X, y = prepare_ml_data(df)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Model: Decision Tree
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    return model, accuracy

