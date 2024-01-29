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
    message = "Bienvenue sur notre API. Ce '/' est l'endpoint le plus simple et celui par défaut. Si vous voulez en savoir plus, consultez la documentation de l'api à '/docs'"
    return message


### POST ###
@app.post("/predict")
async def predict_rental_price(data: RentalPrediction):
    global pricing, preprocessor, model
    input_data = pd.DataFrame([data.filters_list], columns=pricing.drop("rental_price_per_day", axis=1).columns)
    input_data = preprocessor.transform(input_data)
    prediction = model.predict(input_data)
    return {"prediction": prediction[0]}


### RUN APP ###
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)