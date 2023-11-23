from flask import Flask, render_template
import json
import requests
from getpass import getpass


app = Flask(__name__)

@app.route('/')
def index():
    api_url = "https://suap.ifrn.edu.br/api/"
    user = "20201181110005"
    password = "32542395rR@"
    ano_letivo = "2022"
    periodo_letivo = "1"

    user_data = {"username": user, "password": password}

    # gerar token
    response = requests.post(api_url+"v2/autenticacao/token/", json=user_data)

    token = response.json()["access"]

    headers = {
            "Authorization": f'Bearer {token}'
    }

    response = requests.get(f"{api_url}v2/minhas-informacoes/boletim/{ano_letivo}/{periodo_letivo}/", json=user_data, headers=headers)
    print(response.json())

    boletim = response.json()
    return render_template('index.html', boletim=boletim)