from flask import Flask
import random as rd

from flask import request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

all_quotes = [{"id": 0,"quote": "нулевая цитата"}, {"id": 1,"quote": "первая цитата"}, {"id": 2,"quote": "вторая цитата"}, {"id": 3,"quote": "третья цитата"}]


about_me = {
    "name": "Евгений",
    "surname": "Курских",
    "email": "epersic@mail.ru"
}

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/about")
def about():
    return about_me

@app.route("/quotes") 
def get_all_quotes():
    return all_quotes

@app.route("/quotes/<int:id>") ## Задание 1 и 2 из Практика - часть 1
def get_quotes(id):
    if id >=0 and id <= len(all_quotes)-1:
        return all_quotes[id]
    else:
        return f'404, цитаты c id {id} нет('

@app.route("/quotes/count") ## Задание 3 из Практика - часть 1
def get_quotes_count():
    return {"count": str(len(all_quotes))}

@app.route("/quotes/random") ## Задание 4 из Практика - часть 1
def get_random_quote():
    return all_quotes[rd.randint(0, len(all_quotes)-1)]

@app.route("/quotes", methods=['POST']) # для Практики части 2 
def create_quote():
   data = request.json
   print("data = ", data)
   all_quotes.append({"id": len(all_quotes), "quote":data["text"]}) 
   return data, 201

if __name__ == "__main__":
    app.run(debug=True)
