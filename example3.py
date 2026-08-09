from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import json
import repository

# Это callable WSGI-приложение
app = Flask(__name__)
app.secret_key = "Alex_secret_key"
file = 'data.json'
app.logger.setLevel("INFO")
repo = repository.Repository()


@app.get("/users")
def users_index():
    #users = session.get("users_list", [])
    users = repo.get_content()
    app.logger.info(f"here!! {users}")
    return render_template(
            "users/index3.html",
            users=users
        )

@app.get("/users/<int:id>")
def users_show(id):
    user=repo.find(id)
    #users = session.get("users_list", None)
    #user = next(item for item in users if item["id"] == id)
    return render_template(
            "users/show1.html",
            user=user
        )


@app.route("/users/new")
def users_new():
    user = {
        "name": "",
        "email": ""
    }
    errors = {}

    return render_template("users/new.html", user=user, errors=errors)

@app.post("/users")
def users_post():
    # извлекаем данные из формы
    user = request.form.to_dict()
    app.logger.info(user)
    # валидируем данные
    errors = validate(user)
    if errors:
        flash("Bad data!!", "error")
        return render_template(
            "users/new.html",
            user=user,
            errors=errors,
        ), 422
    # сохраняем нового пользователя
    #session.setdefault("users_list", [])
    #next_id = max([item["id"] for item in  session["users_list"]], default=0) + 1
    #session["users_list"].append({**user,**{"id": next_id}})
    repo.save(user)
    flash("User was added!", "success")
    # делаем редирект на список пользователей
    return redirect(url_for('users_index'), code=302)

@app.route("/users/<int:id>/delete", methods=["POST"])
def users_delete(id):
    repo.delete(id)
    #users = session.get("users_list", None)
    #new_list = list(user for user in users if user["id"] != int(id))
    #app.logger.info(f"after delete={new_list}")
    #session["users_list"] = new_list
    flash("User has been deleted", "success")
    return redirect(url_for("users_index"))

@app.route("/users/<int:id>/edit")
def users_edit(id):
    #users = session.get("users_list", [])
    #user = next(item for item in users if item["id"] == int(id))
    user = repo.find(id)
    errors = []
    return render_template(
        "users/edit.html",
        user=user,
        errors=errors,
    )

@app.route("/users/<int:id>/patch", methods=["POST"])
def users_patch(id):
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            "users/edit.html",
            user=data,
            errors=errors,
        ), 422
    repo.save({**data, **{"id": int(id)}})
    #users = session.get("users_list", [])
    #new_users = []
    #for user in users:
    #    if user["id"] == int(id):
    #        new_users.append({**data, **{"id": int(id)}})
    #    else:
    #        new_users.append(user)
    #session["users_list"] = new_users
    flash("User has been updated", "success")
    return redirect(url_for("users_index"))

def validate(data):
    errors = {}
    if len(data["name"]) < 3:
        errors["name"] = "Bad name!"
    if len(data["email"]) < 10:
        errors["email"] = "Bad email format!"
    return errors

################################################################################
'''






def save(data):
    with open(file, 'a') as f:
        existing = get_data()
        new_id = max([item["id"] for item in existing], default=0) + 1
        before_json = {"id": new_id, "name": data["name"], "email": data["email"]}
        json_data = json.dumps(before_json)
        f.write(json_data+'\n')

def get_data():
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
        lines = data.split('\n')
        result = [json.loads(line) for line in lines if line.strip()]
    return result



def update(user, user_id):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
    lines = data.split('\n')
    new_lines = []
    for item in lines:
        if not item.strip():           # если пустая
            continue 
        if json.loads(item)["id"] == user_id:
            new_lines.append(json.dumps({"id": user_id, "name": user["name"], "email": user["email"]}))
        else:
            new_lines.append(item)
    data_to_save = "\n".join(new_lines)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(data_to_save)

def find_user(id):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
        lines = data.split('\n')
        result = next(json.loads(line) for line in lines if json.loads(line)["id"] == id)
    return result
'''

# uv run flask --app example run --port 8000  - запуск development сервера