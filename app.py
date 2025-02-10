from flask import Flask, jsonify, g, abort
import random as rd
from pathlib import Path
from flask import request
import sqlite3

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.exc import InvalidRequestError
from flask_migrate import Migrate

class Base(DeclarativeBase):
    pass

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.json.ensure_ascii = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)
mirgate = Migrate(app, db)

class QuoteModel(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=1)

    def __init__(self, author, text, rating=1):
        self.author = author
        self.text  = text
        self.rating = rating
    def to_dict(self):
        dict1 = {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "rating": self.rating
        }
        return dict1
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(path_to_db)
#     return db

@app.route("/quotes") 
def get_all_quotes():
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()
    quotes = []
    for quote in quotes_db:
        quotes.append(quote.to_dict())
    return jsonify(quotes), 200

@app.route("/quotes/<int:quote_id>")
def get_quote(quote_id):
    quote = db.session.get(QuoteModel, quote_id)
    
    if quote:
        return jsonify(quote.to_dict()), 200
    return jsonify({"error": f"Цитата {quote_id} не найдена"}), 404

@app.route("/quotes/count")
def get_quotes_count():
    count = db.session.query(QuoteModel).count()
    if count is not None:
        return jsonify(count=count), 200

    abort(503)

@app.route("/quotes/random")

def get_random_quote():
    quotes = db.session.scalars(db.select(QuoteModel)).all()
    
    if quotes:
        random_quote = rd.choice(quotes)
        return jsonify(random_quote.to_dict()), 200
    return jsonify({"error": "Нет цитат в базе данных"}), 404

@app.route("/quotes", methods=['POST'])
def create_quote():

    new_quote_data = request.json
    
    if not all(key in new_quote_data for key in ["author", "text"]):
        return jsonify({"error": "Отсутствуют необходимые поля: author или text"}), 400

    new_quote = QuoteModel(
        author=new_quote_data['author'],
        text=new_quote_data['text'],
        rating=new_quote_data['rating']
    )
    
    db.session.add(new_quote)
    db.session.commit()
    
    return jsonify(new_quote.to_dict()), 201

@app.route("/quotes/<int:quote_id>", methods=["PUT"])
def update_quote(quote_id):

    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Нет данных для обновления"}), 400
    
    quote = db.session.get(QuoteModel, quote_id)
    
    if not quote:
        return jsonify({"error": f"Цитата с id {quote_id} не найдена"}), 404
    
    new_author = data.get("author", quote.author)
    new_text = data.get("text", quote.text)
    new_rating = data.get("rating", quote.rating) 
    
    quote.author = new_author
    quote.text = new_text
    quote.rating = new_rating
    
    db.session.commit()

    return jsonify({
        "id": quote.id,
        "author": quote.author,
        "text": quote.text,
        "rating": quote.rating  
    }), 200


@app.route("/quotes/<int:quote_id>", methods=["DELETE"])
def delete_quote(quote_id):
    quote = db.session.get(QuoteModel, quote_id)
    if not quote:
        return jsonify({"error": f"Цитата с id {quote_id} не найдена"}), 404
    
    db.session.delete(quote)
    db.session.commit()
    
    return jsonify({"message": f"Цитата {quote_id} удалена"}), 200

# @app.route("/quotes/filter")
# def filter_quotes():
#     try:
#         quotes = db.session.scalars(QuoteModel).filter_by(**request.args).all()
#     except InvalidRequestError:
#         return (
#             (
#                 "Invalid data. Possible values: author, data, rating"
#                 f"Recieved: {", ".join(request.args.keys())}"
#             ),
#             400,
#         )
#     return jsonify([quote.to_dict() for quote in quotes], 200)

if __name__ == "__main__":
    app.run(debug=True)
