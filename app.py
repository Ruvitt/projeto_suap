from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
from config import client_id, client_secret

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

oauth.register(
    name='suap',
    client_id= client_id,
    client_secret= client_secret,
    api_base_url='https://suap.ifrn.edu.br/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://suap.ifrn.edu.br/o/token/',
    authorize_url='https://suap.ifrn.edu.br/o/authorize/',
    fetch_token=lambda: session.get('suap_token')
)

def obter_anos_letivos():
    periodo_data = oauth.suap.get('/api/v2/minhas-informacoes/meus-periodos-letivos/')
    anos_letivos = [periodo['ano_letivo'] for periodo in periodo_data.json()]	
    anos_letivos = list(dict.fromkeys(anos_letivos))

    return anos_letivos

def obter_boletim(ano_letivo):
    if 'suap_token' in session:
        periodo_letivo = 1 

        boletim_response = oauth.suap.get(f'/api/v2/minhas-informacoes/boletim/{ano_letivo}/{periodo_letivo}/')
        return boletim_response.json()

    return None

@app.route('/')
@app.route('/<ano_letivo>/')
def index(ano_letivo = '2023'):
    if 'suap_token' in session:
        anos_letivos = obter_anos_letivos()
        ano_letivo_selecionado = ano_letivo

        user_data = oauth.suap.get('v2/minhas-informacoes/meus-dados')
        boletim_data = obter_boletim(ano_letivo_selecionado)
        return render_template('userdata.html', user_data=user_data.json(), boletim_data=boletim_data, anos_letivos=anos_letivos, ano_letivo_selecionado=ano_letivo_selecionado)
    else:
        return render_template('index.html')
    
@app.route('/boletim', methods=['POST'])
def atualizar_boletim():
    ano_letivo = request.form.get('ano_letivo')
    return redirect(url_for('index', ano_letivo=ano_letivo))
    
@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    print(redirect_uri)
    return oauth.suap.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('suap_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def auth():
    token = oauth.suap.authorize_access_token()
    session['suap_token'] = token
    return redirect(url_for('index'))