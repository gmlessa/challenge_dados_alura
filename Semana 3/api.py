import pandas as pd
from fastapi import FastAPI
import joblib

app = FastAPI()
random_forest = joblib.load("forest.pkl")

@app.get("/cliente")
def pega_cliente(id: int):
    dados = pd.read_csv("https://raw.githubusercontent.com/gmlessa/challenge_dados_alura/main/Semana%202/dados_tratados_para_ml.csv")
    cliente = pd.DataFrame(dados.iloc[id]).T
    cliente.drop(columns=["Unnamed: 0", "status_emprestimo"], inplace=True)
    cliente_json = cliente.to_json()
    return cliente_json

@app.get("/ids")
def ids():
    dados = pd.read_csv("https://raw.githubusercontent.com/gmlessa/challenge_dados_alura/main/Semana%202/dados_tratados_para_ml.csv")
    ids = dados["Unnamed: 0"].astype("string")
    return {"ids": ids}

@app.get("/predict/")
def predict():
    cliente = pd.read_json(pega_cliente(id))
    random_forest_prediction = random_forest.predict(cliente)
    return {"indice": id, "previsao" : random_forest_prediction[0]}