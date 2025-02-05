from flask import Flask
import random as rd

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

all_quotes = ["цитата с id 0", "цитата с id 1", "цитата с id 2", "цитата с id 3", "цитата с id 4", "цитата с id 5"]

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

@app.route("/quotes/<int:id>") ## Задание 1 и 2 из Практика - часть 1
def get_quotes(id):
    if id >=0 and id <= len(all_quotes)-1:
        return all_quotes[id]
    else:
        return f'404, цитаты c id {id} нет('

@app.route("/quotes/count") ## Задание 3 из Практика - часть 1
def get_quotes_count():
    return {"count": str(len(all_quotes))}

@app.route("/quotes/rnd") ## Задание 4 из Практика - часть 1
def get_random_quote():
    return all_quotes[rd.randint(0, len(all_quotes)-1)]

if __name__ == "__main__":
    app.run(debug=True)
