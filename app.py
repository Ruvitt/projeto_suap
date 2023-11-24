from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

oauth.register(
    name='suap',
    client_id= 'TngAXh7VYGOGINrdVEU0kuK89EfwpI1s3su0JEDV',
    client_secret= '2vOrYRMkJpQPB1rPcAh4TnPMG2QSAwHkIFI9LpDXGPFJKrRatWHluc4h2LFcoiKwClkx9TulGNSntDqYDU389h1TBOT4ABY8GxH3ldW4FMmaQJpcgSrNhmbZPzl8m1N1',
    api_base_url='https://suap.ifrn.edu.br/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://suap.ifrn.edu.br/o/token/',
    authorize_url='https://suap.ifrn.edu.br/o/authorize/',
    fetch_token=lambda: session.get('suap_token')
)

@app.route('/')
def index():
    if 'suap_token' in session:
        ano_letivo = session['ano_letivo']
        periodo_letivo = 1
        user_data = oauth.suap.get('v2/minhas-informacoes/meus-dados')
        boletim_data = oauth.suap.get(f'/api/v2/minhas-informacoes/boletim/{ano_letivo}/{periodo_letivo}/')
        print(user_data.json())
        print(boletim_data.json()) 
        return render_template('userdata.html', user_data=user_data.json(), boletim_data=boletim_data.json())
    else:
        return render_template('index.html')
    
@app.route('/login', methods=['POST'])
def login():
    session['ano_letivo'] = request.form['ano_letivo']
    redirect_uri = url_for('auth', _external=True)
    print(redirect_uri)
    return oauth.suap.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('suap_token', None)
    session.pop('ano_letivo', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def auth():
    token = oauth.suap.authorize_access_token()
    session['suap_token'] = token
    return redirect(url_for('index'))