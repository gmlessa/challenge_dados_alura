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
def predict(id: int):
    cliente = pd.read_json(pega_cliente(id))
    random_forest_prediction = random_forest.predict(cliente)
    return {"indice": id, "previsao" : random_forest_prediction[0]}

@app.get("/predict_custom")
def predict_custom_client(idade_pessoa: int, salario_pessoa: float, situacao_propriedade_pessoa: str, tempo_trabalhado_pessoa: int,
                      motivo_emprestimo: str, pontuacao_emprestimo: str, valor_emprestimo: int, taxa_juros_emprestimo: float,
                      foi_inadimplente_cb: str, tempo_primeira_solicitacao_credito_cb: float):

    dados_cliente = pd.DataFrame({
        'situacao_propriedade_pessoa_Aluguel': 0,
        'situacao_propriedade_pessoa_Hipoteca': 0,
        'situacao_propriedade_pessoa_Outro': 0,
        'situacao_propriedade_pessoa_Própria': 0,
        'motivo_emprestimo_Educativo': 0,
        'motivo_emprestimo_Empreendimento': 0,
        'motivo_emprestimo_Melhora do lar': 0,
        'motivo_emprestimo_Médico': 0,
        'motivo_emprestimo_Pagamento de débitos': 0,
        'motivo_emprestimo_Personal': 0,
        "idade_pessoa" : idade_pessoa,
        "salario_pessoa" : salario_pessoa,
        "situacao_propriedade_pessoa": situacao_propriedade_pessoa,
        "tempo_trabalhado_pessoa": tempo_trabalhado_pessoa,
        "motivo_emprestimo": motivo_emprestimo,
        "pontuacao_emprestimo": pontuacao_emprestimo,
        "valor_emprestimo": valor_emprestimo,
        "taxa_juros_emprestimo": taxa_juros_emprestimo,
        "porcentagem_salario_emprestimo": valor_emprestimo/salario_pessoa,
        "foi_inadimplente_cb": foi_inadimplente_cb,
        "tempo_primeira_solicitacao_credito_cb": tempo_primeira_solicitacao_credito_cb
    }, index = [0])

    dados_ml = pd.read_csv("https://raw.githubusercontent.com/gmlessa/challenge_dados_alura/main/Semana%202/dados_tratados_para_ml.csv")
    dados_ml.drop(columns = "Unnamed: 0", inplace = True)
    dados_cliente["idade_pessoa"] = (dados_cliente["idade_pessoa"] - dados_ml["idade_pessoa"].min())/(dados_ml["idade_pessoa"].max() - dados_ml["idade_pessoa"].min())
    dados_cliente["salario_pessoa"] = (dados_cliente["salario_pessoa"] - dados_ml["salario_pessoa"].mean())/dados_ml["salario_pessoa"].std()
    dados_cliente["tempo_trabalhado_pessoa"] = (dados_cliente["tempo_trabalhado_pessoa"] - dados_ml["tempo_trabalhado_pessoa"].min())/(dados_ml["tempo_trabalhado_pessoa"].max() - dados_ml["idade_pessoa"].min())
    troca = {
        "A" : 7,
        "B" : 6,
        "C" : 5,
        "D" : 4,
        "E" : 3,
        "F" : 2,
        "G" : 1
    }
    dados_cliente["pontuacao_emprestimo"] = dados_cliente["pontuacao_emprestimo"].map(troca)
    dados_cliente["valor_emprestimo"] = (dados_cliente["valor_emprestimo"] - dados_ml["valor_emprestimo"].mean())/dados_ml["valor_emprestimo"].std()
    dados_cliente["taxa_juros_emprestimo"] = (dados_cliente["taxa_juros_emprestimo"] - dados_ml["taxa_juros_emprestimo"].min())/(dados_ml["taxa_juros_emprestimo"].max() - dados_ml["idade_pessoa"].min())
    troca2 = {
        "N" : 0,
        "S" : 1
    }
    dados_cliente["foi_inadimplente_cb"] = dados_cliente["foi_inadimplente_cb"].map(troca2)
    dados_cliente["tempo_primeira_solicitacao_credito_cb"] = (dados_cliente["tempo_primeira_solicitacao_credito_cb"] - dados_ml["tempo_primeira_solicitacao_credito_cb"].min())/(dados_ml["tempo_primeira_solicitacao_credito_cb"].max() - dados_ml["idade_pessoa"].min())

    if dados_cliente["situacao_propriedade_pessoa"].values[0] == "Aluguel":
        dados_cliente["situacao_propriedade_pessoa_Aluguel"] = 1
    elif dados_cliente["situacao_propriedade_pessoa"].values[0] == "Hipoteca":
        dados_cliente["situacao_propriedade_pessoa_Hipoteca"] = 1
    elif dados_cliente["situacao_propriedade_pessoa"].values[0] == "Outro":
        dados_cliente["situacao_propriedade_pessoa_Outro"] = 1
    elif dados_cliente["situacao_propriedade_pessoa"].values[0] == "Própria":
        dados_cliente["situacao_propriedade_pessoa_Própria"] = 1
    elif dados_cliente["motivo_emprestimo"].values[0] == "Educativo":
        dados_cliente["motivo_emprestimo_Educativo"] = 1
    elif dados_cliente["motivo_emprestimo"].values[0] == "Empreendimento":
        dados_cliente["motivo_emprestimo_Empreendimento"] = 1
    elif dados_cliente["motivo_emprestimo"].values[0] == "Melhora do lar":
        dados_cliente["motivo_emprestimo_Melhora do lar"] = 1
    elif dados_cliente["motivo_emprestimo"].values[0] == "Médico":
        dados_cliente["motivo_emprestimo_Médico"] = 1
    elif dados_cliente["motivo_emprestimo"].values[0] == "Pagamento de débitos":
        dados_cliente["motivo_emprestimo_Pagamento de débitos"] = 1
    elif dados_cliente["motivo_emprestimo"].values[0] == "Personal":
        dados_cliente["motivo_emprestimo_Personal"] = 1

    dados_cliente.drop(columns=["situacao_propriedade_pessoa", "motivo_emprestimo"], inplace = True)
    print(dados_cliente.head())
    previsao_cliente = random_forest.predict(dados_cliente)

    return {"idade_pessoa" : idade_pessoa, "salario_pessoa": salario_pessoa, "situacao_propriedade_pessoa": situacao_propriedade_pessoa, "tempo_trabalhado_pessoa": tempo_trabalhado_pessoa,
                      "motivo_emprestimo": motivo_emprestimo, "pontuacao_emprestimo": pontuacao_emprestimo, "valor_emprestimo": valor_emprestimo, "taxa_juros_emprestimo": taxa_juros_emprestimo,
                      "foi_inadimplente_cb": foi_inadimplente_cb, "tempo_primeira_solicitacao_credito_cb": tempo_primeira_solicitacao_credito_cb,"previsao" : previsao_cliente[0], "chance_0": random_forest.predict_proba(dados_cliente).tolist()[0][0], "chance_1": random_forest.predict_proba(dados_cliente).tolist()[0][1]}