from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configuração do Flask e banco de dados
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'  # Necessário para sessões, mas não precisa ser usado para login
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de banco de dados para armazenar os resultados
class Sentiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)

# Função para análise de sentimentos
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    if sentiment_score['compound'] >= 0.05:
        return 'Positivo'
    elif sentiment_score['compound'] <= -0.05:
        return 'Negativo'
    else:
        return 'Neutro'

# Rota para a página inicial (formulário de análise de sentimentos)
@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment_result = None
    if request.method == 'POST':
        text = request.form['text']
        sentiment_result = analyze_sentiment(text)

        # Armazenar a análise no banco de dados
        sentiment_entry = Sentiment(text=text, sentiment=sentiment_result)
        db.session.add(sentiment_entry)
        db.session.commit()

    # Apenas os 5 mais recentes para exibir na página inicial
    sentiment_history = Sentiment.query.order_by(Sentiment.id.desc()).limit(5).all()

    return render_template('index.html', sentiment_result=sentiment_result, sentiment_history=sentiment_history)

# Rota para a página de histórico
@app.route('/history', methods=['GET'])
def history():
    # Busca todo o histórico no banco de dados
    sentiment_history = Sentiment.query.order_by(Sentiment.id.desc()).all()
    return render_template('history.html', sentiment_history=sentiment_history)

if __name__ == '__main__':
    # Garantir que a criação do banco de dados ocorra dentro do contexto da aplicação
    with app.app_context():
        db.create_all()  # Cria as tabelas do banco de dados
    app.run(debug=True)
