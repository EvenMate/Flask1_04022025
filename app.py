from flask import Flask
import random as rd

from flask import request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

all_quotes = [{"id": 0, "author": "evgeny", "quote": "нулевая цитата"}, {"id": 1, "author": "evgeny", "quote": "первая цитата"}, {"id": 2, "author": "evgeny", "quote": "вторая цитата"}, {"id": 3, "author": "evgeny", "quote": "третья цитата"}]


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
        return {"404": f'цитаты c id {id} нет('}

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
   all_quotes.append({"id": len(all_quotes), "author":data["author"], "quote":data["text"]}) 
   return data, 201

@app.route("/quotes/<int:id>", methods=['PUT']) ## работает если в PUT application/json поля также называются
def edit_quote(id):
    if id >=0 and id <= len(all_quotes)-1:
        new_data = request.json
        all_quotes[id].update(new_data)
        return all_quotes[id], 200
    else:
        return {"404": "нет такой цитаты"}, 404
    
@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id):
    global all_quotes
    item_to_delete = next((item for item in all_quotes if item.get("id") == id), None)

    if item_to_delete is None:
        return {"error": f"Цитата с ID {id} не найдена"}, 404

    all_quotes = [item for item in all_quotes if item.get("id") != id]
    return {"200": f"удалена цитата {id}"}, 200

if __name__ == "__main__":
    app.run(debug=True)
