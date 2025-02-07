from flask import Flask
import random as rd

from flask import request

app = Flask(__name__)
app.json.ensure_ascii = False

quotes = [
    {
        "id": 1,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
    },
    {
        "id": 2,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 3,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 4,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так."
    }
]

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
    return quotes

@app.route("/quotes/<int:id>") ## Задание 1 и 2 из Практика - часть 1
def get_quotes(id):
    for quote in quotes:
        if quote["id"] == id:
            return quote
    return {"404": f"Цитата {id} не найдена"}    

@app.route("/quotes/count") ## Задание 3 из Практика - часть 1
def get_quotes_count():
    return {"count": str(len(quotes))}

@app.route("/quotes/random") ## Задание 4 из Практика - часть 1
def get_random_quote():
    return rd.choice(quotes)

# @app.route("/quotes", methods=['POST']) # решение с урока
# def create_quote():
#    new_quote = request.json
#    last_quote = quotes[-1]  
#    new_id = last_quote["id"] + 1
#    new_quote["id"] = new_id
#    quotes.append(new_quote) 
#    return new_quote, 201

def generate_new_id(): # генерация id
    return max(quote["id"] for quote in quotes) + 1 # выбираем максимальное значение из всех id-шников и делаем +1

@app.route("/quotes", methods=['POST']) 
def create_quote():
   new_quote = request.json
   new_quote["id"] = generate_new_id()
   quotes.append(new_quote) 
   return new_quote, 201

@app.route("/quotes/<int:id>", methods=['PUT']) 
def edit_quote(id):
    new_data = request.json
    for quote in quotes:
        if quote["id"] == id:
            if "author" in new_data:
                quote["author"] = new_data["author"]
            if "text" in new_data:
                quote["text"] = new_data["text"]
            return quote, 201
    return {"404": f"Цитата {id} не найдена"}   
    
@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id):
    for quote in quotes:
        if quote["id"] == id:
            quotes.remove(quote)
            return quote, 200
    return {"404": f"Цитата {id} не найдена"} 

if __name__ == "__main__":
    app.run(debug=True)
