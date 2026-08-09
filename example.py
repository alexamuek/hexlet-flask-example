from flask import Flask, request, render_template

# Это callable WSGI-приложение
app = Flask(__name__)

#users = [{"id": 1, "name": "Alex"}, {"id": 2, "name": "Miron"}]

users = [
    {"id": 1, "name": "mike"},
    {"id": 2, "name": "mishel"},
    {"id": 3, "name": "adel"},
    {"id": 4, "name": "keks"},
    {"id": 5, "name": "kamila"},
]

'''@app.route("/users/<nick>")
def user(nick):
    return render_template(
        "users/xss.html",
        name = nick
    )'''

@app.route("/users")
def get_users():
    value = request.args.get("query", default=None, type=None)
    if value is not None:
        result = list([item for item in users if value in item["name"]])
    else:
        result = users
    #return param 
    return render_template(
        "users/index2.html",
        data = result,
        query = value
    )

'''@app.route("/users")
def users():
    param=request.args.get("param", default=None, type=None)
    #return param 
    return render_template(
        "users/xss.html",
        name = param
    )'''


'''render_template(
        "users/xss.html",
        name = param
    )'''

'''@app.route("/users")
def users_show():
    return render_template(
        "users/index.html",
        users = users
    )'''


'''@app.route("/users/<id>")
def users_show(id):
    return render_template(
        "users/show.html",
        id = id,
        name = f"user-{id}"
    )'''

'''@app.route("/courses/<id>")
def courses_show(id):
    return f"Course id: {id}"'''

'''@app.post('/users')
def users():
    return 'Users', 302'''

# uv run flask --app example run --port 8000  - запуск development сервера