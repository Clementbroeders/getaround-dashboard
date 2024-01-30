## LIBRAIRIES ##
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib


## FONCTIONS ##
def load_data():
    csv_path = 'src/get_around_pricing_project.csv'
    pricing = pd.read_csv(csv_path).iloc[:, 1:]
    X = pricing.drop("rental_price_per_day", axis=1)
    y = pricing["rental_price_per_day"]
    bool_columns = ['private_parking_available', 'has_gps', 'has_air_conditioning', 'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires']
    for col in bool_columns:
        X[col] = X[col].astype(int)
    return X, y


def preprocess_data(X):
    numeric_features = ["mileage", "engine_power"]
    categorical_features = X.drop(columns=numeric_features).columns.tolist()
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), categorical_features)
        ])
    X_processed = preprocessor.fit_transform(X)
    return X_processed, preprocessor


def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model


def save_model_and_preprocessor(model, preprocessor):
    joblib.dump(model, 'src/model.pkl')
    joblib.dump(preprocessor, 'src/preprocessor.pkl')
    joblib.dump(model, 'fastapi/src/model.pkl')
    joblib.dump(preprocessor, 'fastapi/src/preprocessor.pkl')


def evaluate_model(model, X, y):
    print('Score R2 final :', model.score(X, y))
    y_pred = model.predict(X)
    mse_regressor = mean_squared_error(y, y_pred)
    print('MSE finale :', mse_regressor)
    print('RMSE finale :', np.sqrt(mse_regressor))
    
    
def evaluate_model_test(model, X_train, y_train, X_test, y_test):
    print('Score R2 training set :', model.score(X_train, y_train))   
    print('Score R2 test set :', model.score(X_test, y_test))
    y_pred_test = model.predict(X_test)
    mse_test = mean_squared_error(y_test, y_pred_test)
    print('MSE test set :', mse_test)
    print('RMSE test set :', np.sqrt(mse_test))


## LANCER LE SCRIPT AVEC UN TRAIN / TEST SPLIT ##
print('Lancement du script pour le modèle de test')
X, y = load_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
X_train_processed, preprocessor = preprocess_data(X_train)
X_test_processed = preprocessor.transform(X_test)
model = train_model(X_train_processed, y_train)
save_model_and_preprocessor(model, preprocessor)
evaluate_model_test(model, X_train_processed, y_train, X_test_processed, y_test)
print('--------------------------------------')


## LANCER LE SCRIPT ##
print('Lancement du script pour le modèle final')
X, y = load_data()
X_processed, preprocessor = preprocess_data(X)
model = train_model(X_processed, y)
save_model_and_preprocessor(model, preprocessor)
evaluate_model(model, X_processed, y)
print('--------------------------------------')