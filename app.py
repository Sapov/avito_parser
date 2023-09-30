import os
# from dotenv import load_dotenv
# load_dotenv()
from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from main import AvitoParser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://sasha:123123@localhost:5432/base_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)
menu = [
    {'name': "Главная", 'url': 'main'},
    {'name': "Поиск", 'url': 'search'},
]


class Base:
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.Text())
    link = db.Column(db.String())
    price = db.Column(db.String())
    created_at = db.Column(db.String())
    city = db.Column(db.String())

    def __init__(self, id, name, description, link, price, created_at, city):
        self.city = city
        self.created_at = created_at
        self.price = price
        self.link = link
        self.description = description
        self.name = name
        self.id = id


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/search', methods=['POST', 'GET'])
def search():
    # ua = request.headers.get('User-Agent')
    if request.method == 'POST':
        print(request.form)
        url_avito = f"https://www.avito.ru/voronezh?localPriority=0&q={request.form['url'].replace(' ', '+')}"

        AvitoParser(url=url_avito, items=request.form['keywords'].split(',')).run()
    else:
        return render_template('search.html', menu=menu)
    return render_template('search.html', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
