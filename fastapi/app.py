### LIBRAIRIES ###
from fastapi import FastAPI
import uvicorn
import pandas as pd 
from pydantic import BaseModel
import joblib


### APP ###
app = FastAPI()


### LOAD FILES & MODEL ###
pricing = pd.read_csv('src/get_around_pricing_project.csv').iloc[:,1:]
preprocessor = joblib.load('src/preprocessor.pkl')
model = joblib.load('src/model.pkl')


### FONCTIONS ###
class RentalPrediction(BaseModel):
    filters_list: list


### GET ###
@app.get("/")
async def index():
    message = "Bienvenue sur l'API de GetAround Dashboard. Ce '/' est l'endpoint le plus simple et celui par défaut. Si vous voulez en savoir plus, consultez la documentation de l'api à '/docs'"
    return message


### POST ###
@app.post("/predict")
async def predict_rental_price(data: RentalPrediction):
    """
    <h2>Endpoint pour prédire le prix de location.</h2>

    <h3>Paramètres :</h3>
    <p><b>dict :</b> Un dictionnaire "filters_list", contenant une liste avec les paramètres suivants :</p>
    <ul>
        <li><b>model_key (str):</b> Nom du modèle,</li>
        <li><b>mileage (float):</b> Kilométrage du véhicule,</li>
        <li><b>engine_power (float):</b> Puissance du moteur,</li>
        <li><b>fuel (str):</b> Type de carburant,</li>
        <li><b>paint_color (str):</b> Couleur de la peinture,</li>
        <li><b>car_type (str):</b> Type de voiture,</li>
        <li><b>private_parking_available (int):</b> Disponibilité d'un parking privé (0 ou 1),</li>
        <li><b>has_gps (int):</b> Présence du GPS (0 ou 1),</li>
        <li><b>has_air_conditioning (int):</b> Présence de la climatisation (0 ou 1),</li>
        <li><b>automatic_car (int):</b> Voiture automatique (0 ou 1),</li>
        <li><b>has_getaround_connect (int):</b> Présence de Getaround Connect (0 ou 1),</li>
        <li><b>has_speed_regulator (int):</b> Régulateur de vitesse (0 ou 1),</li>
        <li><b>winter_tires (int):</b> Pneus d'hiver (0 ou 1),</li>
    </ul>

    <h3>Returns :</h3>
    <p><b>dict :</b> Un dictionnaire contenant la prédiction (float).</p>
    
    <h3>Exemple :</h3>
    <p>{"filters_list": ["Alfa Romeo", 0, 66, "diesel", "beige", "convertible", 1, 1, 1, 1, 1, 1, 1]}</p>
    """
    global pricing, preprocessor, model
    input_data = pd.DataFrame([data.filters_list], columns=pricing.drop("rental_price_per_day", axis=1).columns)
    input_data = preprocessor.transform(input_data)
    prediction = model.predict(input_data)
    return {"prediction": prediction[0]}


### RUN APP ###
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)