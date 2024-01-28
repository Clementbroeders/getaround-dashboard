### LIBRAIRIES ###
import uvicorn
import pandas as pd 
from fastapi import FastAPI


### APP ###
app = FastAPI()


### LOAD FILES ###



### FONCTIONS ###
# class Machinelearning():
#     prediction : list


### GET ###
@app.get("/")
async def index():

    message = "Bienvenue sur notre API. Ce '/' est l'endpoint le plus simple et celui par défaut. Si vous voulez en savoir plus, consultez la documentation de l'api à '/docs'"

    return message


### RUN APP ###
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)