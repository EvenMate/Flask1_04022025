from flask import Flask, jsonify, g, abort
import random as rd
from pathlib import Path
from flask import request
import sqlite3
app = Flask(__name__)
app.json.ensure_ascii = False

BASE_DIR = Path(__file__).parent
path_to_db = BASE_DIR / "store.db"  

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(path_to_db)
    return db

# quotes = [
#     {
#         "id": 1,
#         "author": "Rick Cook",
#         "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
#     },
#     {
#         "id": 2,
#         "author": "Waldi Ravens",
#         "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
#     },
#     {
#         "id": 3,
#         "author": "Mosher’s Law of Software Engineering",
#         "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
#     },
#     {
#         "id": 4,
#         "author": "Yoggi Berra",
#         "text": "В теории, теория и практика неразделимы. На практике это не так."
#     }
# ]

@app.route("/quotes") 
def get_all_quotes():
    quotes = []
    select_quotes = "SELECT * from quotes"
    cursor = get_db().cursor()
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchall() # имеет тип данных список кортежей, list[tuple]
    keys = ("id","author","text")
    #выполняем преобразование типа список кортежей на список словарей
    for quote_db in quotes_db:
        quote = dict(zip(keys, quote_db))
        quotes.append(quote)
    return jsonify(quotes), 200

@app.route("/quotes/<int:quote_id>") ## Задание 1 и 2 из Практика - часть 1
def get_quotes(quote_id):
    select_quote = "SELECT * FROM quotes WHERE id = ?"
    cursor = get_db().cursor()
    cursor.execute(select_quote, (quote_id, ))
    quote_db = cursor.fetchone()
    if quote_db:
        keys = ("id","author","text")
        quote = dict(zip(keys, quote_db))
        return quote
    return {"404": f"Цитата {quote_id} не найдена"}    

@app.route("/quotes/count") ## Задание 3 из Практика - часть 1
def get_quotes_count():
    select_quote = "SELECT count(*) as count FROM quotes"
    cursor = get_db().cursor()
    cursor.execute(select_quote)
    count = cursor.fetchone()
    if count:
        return jsonify(count=count[0])
    abort(503)
@app.route("/quotes/random") ## Задание 4 из Практика - часть 1


@app.route("/quotes/random")
def get_random_quote():
    select_all_quotes = "SELECT * FROM quotes"
    cursor = get_db().cursor()
    cursor.execute(select_all_quotes)
    quotes_db = cursor.fetchall()
    
    if quotes_db:
        keys = ("id", "author", "text")
        random_quote_db = rd.choice(quotes_db) 
        quote = dict(zip(keys, random_quote_db))
        return quote
    
    return {"404": "Цитаты не найдены"}

def generate_new_id():  # пока не используется, тк вместо него cursor.lastrowid
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM quotes")  
    max_id = cursor.fetchone()[0]  
    
    return (max_id + 1) if max_id is not None else 1 # выбираем максимальное значение из всех id-шников и делаем +1

@app.route("/quotes", methods=[ 'POST'])
def create_quote():
    new_quote = request.json
    insert_quote = "INSERT INTO quotes (author, text) VALUES (?, ?)"
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(insert_quote, (new_quote['author'], new_quote['text']))
    answer = cursor.lastrowid
    connection.commit()
    new_quote['id'] = answer
    return jsonify(new_quote), 201

@app.route("/quotes/<int:quote_id>", methods=["PUT"])
def update_quote(quote_id):

    data = request.get_json()
    if not data:
        return {"error": "Нет данных для обновления"}, 400

    select_quote = "SELECT * FROM quotes WHERE id = ?"
    cursor = get_db().cursor()
    cursor.execute(select_quote, (quote_id,))
    quote_db = cursor.fetchone()
    
    if not quote_db:
        return {"error": f"Цитата с id {quote_id} не найдена"}, 404

    new_author = data.get("author", quote_db[1]) 
    new_text = data.get("text", quote_db[2]) 

    update_query = "UPDATE quotes SET author = ?, text = ? WHERE id = ?"
    cursor.execute(update_query, (new_author, new_text, quote_id))
    get_db().commit()

    return {"message": "Цитата обновлена", "id": quote_id, "author": new_author, "text": new_text}

    

@app.route("/quotes/<int:quote_id>", methods=["DELETE"])  ## Удаление цитаты по id
def delete_quote(quote_id):
    delete_query = "DELETE FROM quotes WHERE id = ?"
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(delete_query, (quote_id,))
    conn.commit()
    
    if cursor.rowcount:
        return {"message": f"Цитата {quote_id} удалена"}
    return {"404": f"Цитата {quote_id} не найдена"}

if __name__ == "__main__":
    app.run(debug=True)
